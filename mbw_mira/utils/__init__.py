import frappe
import hmac
import hashlib
import json
from rapidfuzz import fuzz
from frappe.utils import now_datetime
from mbw_mira.mbw_mira.doctype.interaction.interaction import (create_interaction)

def send_email_job(candidate_id, action_id,step_id):
    from mbw_mira.utils.email import send_email
    """
    Gửi email cho ứng viên, hỗ trợ cả message raw hoặc template.
    """

    #Lấy thông tin candidate
    candidate = frappe.get_cached_doc("Candidate",candidate_id)
    action = frappe.get_doc("Action",action_id)
    step = frappe.get_cached_doc("CampaignStep",step_id)

    
    logger = frappe.logger("campaign")
    if not candidate.email:
        frappe.throw("Candidate does not have an email.")
    # Nếu ứng viên đã unsubcrible
    if candidate.email_opt_out:
        logger.error("Candidate unsubcrible")
        return

    
    context = (candidate,action,step)
    message = render_template(step.template, context)
    
    config_step = json.loads(step.config)
    subject = ""
    if config_step and hasattr(config_step,'subject'):
        subject = render_template(config_step.get("subject"), context)
    candidate_email = candidate.email
    candidate_id = candidate.name   
    template = None
    template_args = None
    if not candidate_email:
        logger.error("[EMAIL ERROR] Missing candidate_email")
        return

    if not subject:
        logger.error(f"[EMAIL ERROR] Missing subject for {candidate_email}")
        return

    if not message and not template:
        logger.error(f"[EMAIL ERROR] Neither message nor template provided for {candidate_email}")
        return
    
    action.executed_at = now_datetime()
    try:
        result = send_email(
            recipients=[candidate_email],
            subject=subject,
            content=message if not template else None,
            template=template,
            template_args=template_args
        )
        create_interaction(
                candidate_id=candidate_id,
                interaction_type="EMAIL_SENT",
                source_action=action.name,
            )
        if result:
            action.status = "EXECUTED"
            action.result={
                    "status": "Success",
                    "message": f"[EMAIL] Sent to {candidate_email} — step: {step} — candidate: {candidate_id}"
                }
        else:
            action.status = "FAILED"
            action.result = {"error": f"[EMAIL] Error Sent to {candidate_email} — step: {step} — candidate: {candidate_id}", "traceback": frappe.get_traceback()}
        action.save(ignore_permissions=True)
        frappe.db.commit()
    except Exception as e:
        frappe.log_error(frappe.get_traceback(), "[EMAIL ERROR] send_email_job")
        action.status = "FAILED"
        action.result = {"error": str(e), "traceback": frappe.get_traceback()}
        action.save(ignore_permissions=True)
        frappe.db.commit()
        raise

def send_sms_job(candidate,action, step):
    try:
        # Gửi thật nếu có provider
        phone = candidate.phone
        message = None
        candidate_id = candidate.name

        create_interaction(
                candidate_id=candidate_id,
                interaction_type="SMS_SENT",
                source_action=action.name,
            )
        
        if not candidate.phone:
            frappe.throw("Candidate does not have a phone number.")

        
    except Exception as e:
        frappe.logger("campaign").error(f"[SMS ERROR] {phone} — {str(e)}")
        raise

def render_template(template_str, context):
    from urllib.parse import urlencode
    from frappe.utils import get_url
    if not template_str:
        return "Xin chào bạn"
    candidate,action, step = context
    base_url = get_url()
    params = {
        "candidate_id": candidate.name,
        "action": action.name,
        "url": f"{base_url}/mbw_mira"
    }

    context_parse ={
        "candidate_name":candidate.full_name
        }
    
    sig = make_signature(params)

    # dùng urllib để encode query string
    query = urlencode({**params, "sig": sig})

    
    context_parse["tracking_pixel_url"] = (
        f"{base_url}/api/method/mbw_mira.api.interaction.tracking_pixel?{query}"
    )
    context_parse["tracking_link"] = (
        f"{base_url}/api/method/mbw_mira.api.interaction.click_redirect?{query}"
    )
    context_parse['url_link'] = (
        f"{base_url}/api/method/mbw_mira.api.interaction.unsubscribe?{query}"
    )

    return frappe.render_template(template_str, context_parse)


def make_signature(data) -> str:
    #data = f"candidate_id={candidate_id}&action={action}&url={url}"
    SECRET_KEY = frappe.conf.get("tracking_secret_key") or "email_track_aff07b5a10af788e14e6fedb38ce39d9"
    return hmac.new(SECRET_KEY.encode(), json.dumps(data).encode(), hashlib.sha256).hexdigest()
def verify_signature(data, sig):
    expected = make_signature(data)
    return hmac.compare_digest(expected, sig)

#Tìm candidate khớp với talentsegment
def find_candidates_fuzzy(criteria, segment_name = None, min_score=50):
    """
    Tìm các ứng viên có mức độ khớp >= min_score (0–100) theo fuzzy matching
    giữa candidate.skills và talent_segment.criteria.skills.
    """
    try:
        criteria_skills =[]
        #Nếu có segment
        if segment_name:
            segment = frappe.get_cached_doc("TalentSegment", segment_name)
            criteria_segment = json.loads(segment.criteria or "{}")
            if criteria_segment:
                criteria_skills = criteria_segment.get('skills')
        elif criteria:
            cret = json.loads(criteria or {})
            
            if cret:
                criteria_skills = cret.get('skills')
                
        if not len(criteria_skills) > 0:
            frappe.throw(f"{segment_name} No skills criteria defined.{str(criteria_skills)}")

        
        talent_profiles = frappe.get_all(
            "TalentProfiles",
            filters={"status":"NEW"},
            fields=["name", "full_name", "skills"]
        )
        results = []
        
        for c in talent_profiles:
            
            if not c.get('skills'):
                continue
            
            try:
                candidate_skills = c.get('skills')
            except Exception:
                continue
            
            if not candidate_skills:
                continue
            
            # fuzzy match từng kỹ năng của criteria với từng kỹ năng của ứng viên
            total_score = 0
            for crit_skill in criteria_skills:
                # tìm điểm cao nhất của crit_skill so với tất cả skills của candidate
                best_score = max(
                    [fuzz.token_sort_ratio(crit_skill, cand_skill) for cand_skill in candidate_skills],
                    default=0
                )
                total_score += best_score

            avg_score = total_score / len(criteria_skills)
            frappe.log_error(str(avg_score),str(min_score))
            if avg_score >= min_score:
                results.append({
                    "name": c.name,
                    "full_name": c.full_name,
                    "skills": candidate_skills,
                    "criteria_skills": criteria_skills,
                    "score": round(avg_score, 2)
                })

        # sắp xếp giảm dần theo điểm
        results.sort(key=lambda x: x["score"], reverse=True)

        return results

    except Exception as e:
        frappe.log_error(f"Error in get candidate segment: {str(e)}")
        return None
