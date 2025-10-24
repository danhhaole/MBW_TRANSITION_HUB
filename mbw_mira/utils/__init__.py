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
    talentprofiles = frappe.get_cached_doc("Mira Talent", talentprofile_id)
    action = frappe.get_doc("Mira Action", action_id)
    step = frappe.get_cached_doc("Mira Campaign Step", step_id)

    logger = frappe.logger("campaign")
    if not talentprofiles.contact_email:
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
        action = frappe.get_doc("Mira Action", action_id)
        step = frappe.get_cached_doc("Mira Campaign Step", step_id)
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
    giữa candidate và talent_segment conditions.
    """
    try:
        # Convert min_score to float
        min_score = float(min_score) if min_score else 50.0
        
        # --- Load conditions từ segment ---
        conditions = []
        if segment_name:
            conditions_str = frappe.db.get_value("Mira Segment", segment_name, "criteria")
            if conditions_str:
                try:
                    conditions = json.loads(conditions_str or "[]")
                except Exception as e:
                    frappe.log_error(f"Lỗi khi đọc conditions JSON: {e}")
                    return []
        
        if not conditions or len(conditions) == 0:
            frappe.throw(
                f"Không tìm thấy điều kiện trong segment '{segment_name}'"
            )
        
        # --- Parse conditions thành criteria ---
        criteria_skills = []
        criteria_tags = []
        criteria_filters = {}
        
        print(f"\n=== PARSING CONDITIONS ===")
        print(f"Total conditions: {len(conditions)}")
        
        for condition in conditions:
            if len(condition) < 3:
                continue
                
            field, operator, value = condition[0], condition[1], condition[2]
            print(f"Condition: {field} {operator} {value}")
            
            # Parse skills
            if field == "skills" and value:
                if isinstance(value, str):
                    criteria_skills = [unquote(s.strip().lower()) for s in value.split(",") if s.strip()]
                elif isinstance(value, list):
                    criteria_skills = [unquote(s.strip().lower()) for s in value if s.strip()]
                print(f"  → Parsed skills: {criteria_skills}")
            
            # Parse tags
            elif field == "tags" and value:
                if isinstance(value, str):
                    criteria_tags = [unquote(s.strip().lower()) for s in value.split(",") if s.strip()]
                elif isinstance(value, list):
                    criteria_tags = [unquote(s.strip().lower()) for s in value if s.strip()]
                print(f"  → Parsed tags: {criteria_tags}")
            
            # Parse other fields
            else:
                criteria_filters[field] = {"operator": operator, "value": value}
                print(f"  → Added filter: {field} {operator} {value}")
        
        print(f"\n=== CRITERIA SUMMARY ===")
        print(f"Skills: {criteria_skills}")
        print(f"Tags: {criteria_tags}")
        print(f"Filters: {criteria_filters}")
        
        if not criteria_skills and not criteria_tags and not criteria_filters:
            frappe.throw(
                f"Không tìm thấy tiêu chí hợp lệ trong segment '{segment_name}'"
            )

        # --- Lấy danh sách ứng viên ---
        talent_profiles = frappe.get_all(
            "Mira Talent",
            # filters={"status": "NEW"},
            fields=["name", "email", "full_name", "skills","tags","source"],
        )
        

        results = []
        
        print(f"\n=== PROCESSING {len(talent_profiles)} CANDIDATES ===")

        for idx, c in enumerate(talent_profiles):
            talent_skills = c.get("skills")
            talent_tags = c.get("tags")
            talent_source = c.get("source")
            candidate_skills =[]
            candidate_tags =[]
            
            print(f"\n--- Candidate {idx + 1}: {c.get('full_name')} ---")
            
            # Chuyển skills thành list nếu là chuỗi
            if talent_skills:
                if isinstance(talent_skills, str):
                    # Try to parse as JSON first (in case it's stored as string like "['skill1', 'skill2']")
                    try:
                        # Replace single quotes with double quotes for valid JSON
                        json_str = talent_skills.replace("'", '"')
                        parsed = json.loads(json_str)
                        if isinstance(parsed, list):
                            candidate_skills = [unquote(str(s).strip().lower()) for s in parsed if s]
                        else:
                            candidate_skills = [unquote(s.strip().lower()) for s in talent_skills.split(",") if s.strip()]
                    except Exception as e:
                        print(f"  Error parsing skills JSON: {e}, trying comma-separated")
                        # Not JSON, treat as comma-separated
                        candidate_skills = [unquote(s.strip().lower()) for s in talent_skills.split(",") if s.strip()]
                elif isinstance(talent_skills, list):
                    # Clean each skill - remove brackets and quotes
                    cleaned_skills = []
                    for s in talent_skills:
                        if s:
                            # Remove leading/trailing brackets and quotes: "['linux'" -> "linux"
                            cleaned = str(s).strip().strip("[]'\"").strip()
                            if cleaned:
                                cleaned_skills.append(unquote(cleaned.lower()))
                    candidate_skills = cleaned_skills
                print(f"Candidate skills: {candidate_skills}")
            
            if talent_tags:
                if isinstance(talent_tags, str):
                    # Try to parse as JSON first
                    try:
                        # Replace single quotes with double quotes for valid JSON
                        json_str = talent_tags.replace("'", '"')
                        parsed = json.loads(json_str)
                        if isinstance(parsed, list):
                            candidate_tags = [unquote(str(s).strip().lower()) for s in parsed if s]
                        else:
                            candidate_tags = [unquote(s.strip().lower()) for s in talent_tags.split(",") if s.strip()]
                    except Exception as e:
                        print(f"  Error parsing tags JSON: {e}, trying comma-separated")
                        # Not JSON, treat as comma-separated
                        candidate_tags = [unquote(s.strip().lower()) for s in talent_tags.split(",") if s.strip()]
                elif isinstance(talent_tags, list):
                    # Clean each tag - remove brackets and quotes
                    cleaned_tags = []
                    for t in talent_tags:
                        if t:
                            # Remove leading/trailing brackets and quotes
                            cleaned = str(t).strip().strip("[]'\"").strip()
                            if cleaned:
                                cleaned_tags.append(unquote(cleaned.lower()))
                    candidate_tags = cleaned_tags
                print(f"Candidate tags: {candidate_tags}")
            
            # --- Tính điểm fuzzy ---
            total_score = 0
            score_breakdown = []
            if criteria_skills:
                print(f"Checking skills...")
                for crit_skill in criteria_skills:
                    try:
                        best_score = max(
                            [
                                fuzz.token_sort_ratio(crit_skill, cand_skill) or 0
                                for cand_skill in candidate_skills
                            ],
                            default=0,
                        )
                        total_score += best_score
                        score_breakdown.append(f"Skill '{crit_skill}': {best_score}")
                        print(f"  Skill '{crit_skill}' → best match score: {best_score}")
                    except Exception as e:
                        print(f"  Error matching skill: {e}")
            
            if criteria_tags:
                print(f"Checking tags...")
                for criteria_tag in criteria_tags:
                    best_score = max(
                        [
                            fuzz.token_sort_ratio(criteria_tag, candidate_tag)
                            for candidate_tag in candidate_tags
                        ],
                        default=0,
                    )
                    total_score += best_score
                    score_breakdown.append(f"Tag '{criteria_tag}': {best_score}")
                    print(f"  Tag '{criteria_tag}' → best match score: {best_score}")
                    
            # Check other filters
            if criteria_filters:
                print(f"Checking filters...")
                for field, filter_data in criteria_filters.items():
                    operator = filter_data.get("operator")
                    value = filter_data.get("value")
                    talent_value = c.get(field)
                    
                    if not talent_value:
                        print(f"  Filter '{field}': No value in candidate")
                        continue
                    
                    # Simple matching for now
                    matched = False
                    if operator in ["==", "equals"]:
                        if str(talent_value).lower() == str(value).lower():
                            total_score += 100
                            matched = True
                    elif operator in ["like", "contains"]:
                        if str(value).lower() in str(talent_value).lower():
                            total_score += 100
                            matched = True
                    
                    score_breakdown.append(f"Filter '{field}' {operator} '{value}': {100 if matched else 0}")
                    print(f"  Filter '{field}' {operator} '{value}' → {'MATCH' if matched else 'NO MATCH'}")
            
            # Calculate average score
            total_criteria = len(criteria_skills) + len(criteria_tags) + len(criteria_filters)
            if total_criteria == 0:
                continue
                
            avg_score = total_score / total_criteria
            
            print(f"Total score: {total_score} / {total_criteria} criteria = {avg_score:.2f}")
            print(f"Min score required: {min_score}")
            print(f"Result: {'✓ PASS' if avg_score >= min_score else '✗ FAIL'}")
            
            if avg_score >= min_score:
                results.append(
                    {
                        "name": c.name,
                        "email": c.email,
                        "full_name": c.full_name,
                        "skills": candidate_skills,
                        "tags": candidate_tags,
                        "criteria_skills": criteria_skills,
                        "criteria_tags": criteria_tags,
                        "score": round(avg_score, 2),
                    }
                )

        # Sắp xếp theo điểm giảm dần
        results.sort(key=lambda x: x["score"], reverse=True)
        
        print(f"\n=== FINAL RESULTS ===")
        print(f"Total candidates matched: {len(results)}")
        for r in results[:5]:  # Show top 5
            print(f"  {r['full_name']}: {r['score']}")
        
        return results

    except Exception as e:
        print(f"\n=== ERROR ===")
        print(f"Exception: {str(e)}")
        import traceback
        traceback.print_exc()
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