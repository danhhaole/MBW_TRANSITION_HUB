import hmac
import hashlib
import frappe
import json
from rapidfuzz import fuzz


def make_signature(data) -> str:
    #data = f"candidate_id={candidate_id}&action={action}&url={url}"
    SECRET_KEY = frappe.conf.get("tracking_secret_key") or "email_track_aff07b5a10af788e14e6fedb38ce39d9"
    return hmac.new(SECRET_KEY.encode(), json.dumps(data).encode(), hashlib.sha256).hexdigest()
def verify_signature(data, sig):
    expected = make_signature(data)
    return hmac.compare_digest(expected, sig)

#Tìm candidate khớp với talentsegment
def find_candidates_fuzzy(segment_name, min_score=50):
    """
    Tìm các ứng viên có mức độ khớp >= min_score (0–100) theo fuzzy matching
    giữa candidate.skills và talent_segment.criteria.skills.
    """
    segment = frappe.get_doc("TalentSegment", segment_name)
    criteria = json.loads(segment.criteria or "{}")
    criteria_skills = criteria.get("skills", [])
    
    if not criteria_skills:
        frappe.throw("No skills criteria defined in this Talent Segment.")

    candidates = frappe.get_all(
        "Candidate",
        fields=["name", "full_name", "skills"]
    )

    results = []

    for c in candidates:
        if not c.skills:
            continue
        
        try:
            candidate_skills = json.loads(c.skills)
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

        if avg_score >= min_score:
            results.append({
                "candidate_name": c.name,
                "full_name": c.full_name,
                "skills": candidate_skills,
                "criteria_skills": criteria_skills,
                "score": round(avg_score, 2)
            })

    # sắp xếp giảm dần theo điểm
    results.sort(key=lambda x: x["score"], reverse=True)

    return results