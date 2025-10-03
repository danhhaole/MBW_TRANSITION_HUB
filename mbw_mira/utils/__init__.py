import frappe
import hmac
import hashlib
import json
from rapidfuzz import fuzz
from frappe.utils import now_datetime
from mbw_mira.mbw_mira.doctype.mira_interaction.mira_interaction import create_mira_interaction
from urllib.parse import unquote

import csv


def send_email_job(talentprofile_id, action_id, step_id):
    from mbw_mira.utils.email import send_email
    """
    Gửi email cho ứng viên, hỗ trợ cả message raw hoặc template.
    """

    # Lấy thông tin candidate
    talentprofiles = frappe.get_cached_doc("Mira Prospect", talentprofile_id)
    action = frappe.get_doc("Action", action_id)
    step = frappe.get_cached_doc("CampaignStep", step_id)

    logger = frappe.logger("campaign")
    if not talentprofiles.email:
        frappe.throw("Candidate does not have an email.")
    # Nếu ứng viên đã unsubcrible
    if talentprofiles.email_opt_out:
        logger.error("Candidate unsubcrible")
        return

    context = (talentprofiles, action, step)
    message = render_template(step.template, context)

    config_step = {}
    if step and hasattr(step, "config"):
        config_step = json.loads(step.config)
    subject = "Thông báo"
    if config_step and hasattr(config_step, "subject"):
        subject = render_template(config_step.get("subject"), context)
    talent_email = talentprofiles.email
    template = None
    template_args = None
    if not talent_email:
        logger.error("[EMAIL ERROR] Missing candidate_email")
        return

    if not subject:
        logger.error(f"[EMAIL ERROR] Missing subject for {talent_email}")
        return

    if not message:
        logger.error(
            f"[EMAIL ERROR] Neither message nor template provided for {talent_email}"
        )
        return

    action.executed_at = now_datetime()
    try:
        result = send_email(
            recipients=[talent_email],
            subject=subject,
            content=message if not template else None,
            template=template,
            template_args=template_args,
        )
        create_mira_interaction(
            {
                "talent_id": talentprofile_id,
                "interaction_type": "EMAIL_SENT",
                "source_action": action.name,
            }
        )
        if result:
            action.status = "EXECUTED"
            action.result = {
                "status": "Success",
                "message": f"[EMAIL] Sent to {talentprofile_id} — step: {step} — candidate: {talentprofile_id}",
            }
        else:
            action.status = "FAILED"
            action.result = {
                "error": f"[EMAIL] Error Sent to {talent_email} — step: {step} — candidate: {talentprofile_id}",
                "traceback": frappe.get_traceback(),
            }
        action.save(ignore_permissions=True)
        frappe.db.commit()
    except Exception as e:
        frappe.log_error(frappe.get_traceback(), "[EMAIL ERROR] send_email_job")
        action.status = "FAILED"
        action.result = {"error": str(e), "traceback": frappe.get_traceback()}
        action.save(ignore_permissions=True)
        frappe.db.commit()
        raise


def send_sms_job(talentprofile_id, action_id, step_id):
    try:
        talentprofiles = frappe.get_cached_doc("Mira Prospect", talentprofile_id)
        action = frappe.get_doc("Action", action_id)
        step = frappe.get_cached_doc("CampaignStep", step_id)
        # Gửi thật nếu có provider
        phone = talentprofiles.phone
        message = None
        talent_id = talentprofiles.name

        create_mira_interaction(
            {
                "talent_id": talent_id,
                "interaction_type": "SMS_SENT",
                "source_action": action.name,
            }
        )

        if not talentprofiles.phone:
            frappe.throw("Candidate does not have a phone number.")
        action.executed_at = now_datetime()
        action.status = "EXECUTED"
        action.result = {
            "status": "Success",
            "message": f"[EMAIL] Sent to {talentprofile_id} — step: {step} — candidate: {talentprofile_id}",
        }

        action.save(ignore_permissions=True)
        frappe.db.commit()
    except Exception as e:
        frappe.logger("campaign").error(f"[SMS ERROR] {phone} — {str(e)}")
        raise


def render_template(template_str, context):
    from urllib.parse import urlencode
    from frappe.utils import get_url

    if not template_str:
        return "Xin chào bạn"
    talentprofiles, action, step = context
    origin = frappe.request.headers.get("Origin")
    protocol = frappe.request.scheme
    host = frappe.request.host
    base_url = f"{protocol}://{host}"
    if origin:
        base_url = origin
    params = {
        "candidate_id": talentprofiles.name,
        "action": action.name,
        "url": f"{base_url}/mbw_mira/ladi?campaign={step.campaign}",
    }

    context_parse = {"candidate_name": talentprofiles.full_name}

    sig = make_signature(params)

    # dùng urllib để encode query string
    query = urlencode({**params, "sig": sig})

    context_parse["tracking_pixel_url"] = (
        f"{base_url}/api/method/mbw_mira.api.interaction.tracking_pixel?{query}"
    )
    context_parse["tracking_link"] = (
        f"{base_url}/api/method/mbw_mira.api.interaction.click_redirect?{query}"
    )
    context_parse["unsubscribe_link"] = (
        f"{base_url}/mbw_mira/unsubscribe?{query}"
    )

    context_parse["register_link"] = (
        f"{base_url}/mbw_mira/register?campaign={step.campaign}"
    )
    context_parse["ladi_link"] = (
        f"{base_url}/mbw_mira/ladi?campaign={step.campaign}"
    )
    context_parse["apply_link"] = (
        f"{base_url}/mbw_mira/application?campaign={step.campaign}&email={talentprofiles.email}&name={talentprofiles.full_name}"
    )
    

    return frappe.render_template(template_str, context_parse)


def make_signature(data) -> str:
    # data = f"candidate_id={candidate_id}&action={action}&url={url}"
    SECRET_KEY = (
        frappe.conf.get("tracking_secret_key")
        or "email_track_aff07b5a10af788e14e6fedb38ce39d9"
    )
    return hmac.new(
        SECRET_KEY.encode(), json.dumps(data).encode(), hashlib.sha256
    ).hexdigest()


def verify_signature(data, sig):
    expected = make_signature(data)
    return hmac.compare_digest(expected, sig)


# Tìm candidate khớp với talentsegment
def find_candidates_fuzzy(criteria=None, segment_name=None, min_score=50):
    """
    Tìm các ứng viên có mức độ khớp >= min_score (0–100) theo fuzzy matching
    giữa candidate.skills và talent_segment.criteria.skills.
    """
    try:
        # --- Load tiêu chí kỹ năng ---
        criteria_skills = []
        criteria_tags = []
        criteria_source = ''
        if segment_name:
            criteria = frappe.db.get_value("Mira Segment", segment_name, "criteria")

        if criteria:
            try:
                criteria_dict = json.loads(criteria or "{}")
                raw_skills = criteria_dict.get("skills", [])
                raw_tags = criteria_dict.get("tags", [])
                criteria_source = criteria_dict.get("source", [])
                if isinstance(raw_skills, str):
                    criteria_skills = [unquote(s.strip().lower()) for s in raw_skills.split(",")]
                elif isinstance(raw_skills, list):
                    criteria_skills = [unquote(s.strip().lower()) for s in raw_skills]

                if isinstance(raw_tags, str):
                    criteria_tags = [unquote(s.strip().lower()) for s in raw_tags.split(",")]
                elif isinstance(raw_tags, list):
                    criteria_tags = [unquote(s.strip().lower()) for s in raw_tags]
            except Exception as e:
                frappe.log_error(f"Lỗi khi đọc criteria JSON: {e}")
                return []
        
        if not criteria_skills and not criteria_tags and not criteria_source:
            frappe.throw(
                f"Không tìm thấy kỹ năng trong tiêu chí segment '{segment_name}'"
            )

        # --- Lấy danh sách ứng viên ---
        talent_profiles = frappe.get_all(
            "Mira Talent",
            # filters={"status": "NEW"},
            fields=["name", "contact_email", "full_name", "skills","tags","source"],
        )
        

        results = []

        for c in talent_profiles:
            talent_skills = c.get("skills")
            talent_tags = c.get("tags")
            talent_source = c.get("source")
            # if not talent_skills or not talent_tags or not talent_source:
            #     continue

            
            # Chuyển skills thành list nếu là chuỗi
            if talent_skills:
                if isinstance(talent_skills, str):
                    candidate_skills = [unquote(s.strip().lower()) for s in talent_skills.split(",")]
                elif isinstance(talent_skills, list):
                    candidate_skills = [unquote(s.strip().lower()) for s in talent_skills]
            
            if talent_tags:
                if isinstance(talent_tags, str):
                    candidate_tags = [unquote(s.strip().lower()) for s in talent_tags.split(",")]
                elif isinstance(talent_tags, list):
                    candidate_tags = [unquote(s.strip().lower()) for s in talent_tags]
            

            
            # --- Tính điểm fuzzy ---
            total_score = 0
            if criteria_skills:                
                for crit_skill in criteria_skills:                    
                    best_score = max(
                        [
                            fuzz.token_sort_ratio(crit_skill, cand_skill)
                            for cand_skill in candidate_skills
                        ],
                        default=0,
                    )
                    total_score += best_score
                    
            if criteria_tags:
                
                for criteria_tag in criteria_tags:
                    best_score = max(
                        [
                            fuzz.token_sort_ratio(criteria_tag, candidate_tag)
                            for candidate_tag in candidate_tags
                        ],
                        default=0,
                    )
                    total_score += best_score
                    
            if talent_source:
                best_score = fuzz.token_sort_ratio(talent_source, criteria_source) or 0
                total_score += best_score
            
            avg_score = total_score / len(criteria_skills)
            # frappe.log_error(f"Score {avg_score}")
            if avg_score >= min_score:
                results.append(
                    {
                        "name": c.name,
                        "email": c.contact_email,
                        "full_name": c.full_name,
                        "skills": candidate_skills,
                        "criteria_skills": criteria_skills,
                        "tags":criteria_tags,
                        "source":criteria_source,
                        "score": round(avg_score, 2),
                    }
                )

        # Sắp xếp theo điểm giảm dần
        results.sort(key=lambda x: x["score"], reverse=True)
        return results

    except Exception as e:
        return []

def render_merge_tags(html: str, context: dict) -> str:
    import re
    def replacer(match):
        tag = match.group(1).strip()
        return context.get(tag, f"{{{{ {tag} }}}}")  # nếu không có thì giữ nguyên

    return re.sub(r"\{\{\s*(.*?)\s*\}\}", replacer, html)
def convert_po_to_csv(po_path, csv_path):
    import polib
    po = polib.pofile(po_path)
    with open(csv_path, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        for entry in po:
            if entry.msgid:
                writer.writerow([entry.msgid, entry.msgstr])

# def translate_po_file(input_po_path, output_po_path):
#     from deep_translator import GoogleTranslator
#     import polib
#     # Load file .po gốc
#     po = polib.pofile(input_po_path)
#     # Dịch từng msgid nếu msgstr rỗng
#     for entry in po:
#         if entry.msgid and not entry.msgstr:
#             try:
#                 translated = GoogleTranslator(source='en', target='vi').translate(entry.msgid)
#                 entry.msgstr = translated
#             except Exception as e:
#                 print(f"Lỗi dịch '{entry.msgid}': {e}")
#                 entry.msgstr = ""  # fallback

#     # Ghi ra file mới
#     po.save(output_po_path)
#     print(f"Đã dịch và lưu: {output_po_path}")