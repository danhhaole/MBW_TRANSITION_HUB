import frappe
import logging
from mbw_mira.integrations.ats.frappe_site_provider import FrappeSiteProvider
from datetime import datetime
import json
from urllib.parse import unquote

logger = logging.getLogger(__name__)

def fetch_mbw_ats_data(campaign_name):
    """
    Worker: Fetch ACTIVE campaign data from MBW ATS and save to Mira Talent.
    """
    campaign = frappe.get_doc("Mira Campaign", campaign_name)
    source_name = campaign.source
    segment_id = campaign.target_segment

    with FrappeSiteProvider(source_name) as provider:
        if provider.sync_direction not in ("Pull", "Both"):
            return

        criteria = campaign.criteria or {}
        if isinstance(criteria, str):
            criteria = json.loads(criteria)

        total = 0
        try:
            filters = criteria.get("filters", {})
            fields = criteria.get("fields", ["name"])
            candidates = provider.get_list("ATS_Candidate", filters=filters, fields=fields)

            if candidates:
                total = save_candidates_to_talent_pool(provider, candidates, campaign, source_name, segment_id)

            frappe.publish_realtime(
                'fetch_data_integrations_ats',
                message={'campaign': campaign_name, "segment": segment_id}
            )

            return total
        except Exception as e:
            logger.error(f"[MBW ATS] Failed fetching data for campaign {campaign_name} — {str(e)}", exc_info=True)
            return total


def save_candidates_to_talent_pool(provider, candidates, campaign, source_name, segment_id):
    """
    Chuẩn hóa & lưu danh sách ứng viên vào Mira Talent
    """
    count = 0
    for record in candidates:
        try:
            record = provider.get_doc("ATS_Candidate", record.get('name'))
            doc_data = map_mbw_ats_to_talentprofiles(record, campaign.name, source_name, segment_id)

            # Kiểm tra ứng viên đã tồn tại theo email hoặc sync_id
            existing = None
            if doc_data.get("email"):
                existing = frappe.db.exists("Mira Talent", {"email": doc_data["email"]})
            if not existing and record.get("name"):
                existing = frappe.db.exists("Mira Talent", {"name": record.get("name")})

            if existing:
                doc = frappe.get_doc("Mira Talent", existing)
                doc.update(doc_data)
                doc.save(ignore_permissions=True)
            else:
                doc = frappe.get_doc(doc_data)
                doc.insert(ignore_permissions=True)

            frappe.db.commit()
            count += 1
        except Exception as e:
            logger.error(f"[Mira Talent] Failed to save {record.get('can_full_name')} — {str(e)}", exc_info=True)
            frappe.db.rollback()
            continue

    return count


def map_mbw_ats_to_talentprofiles(record, campaign_name, source_name, segment_id=None):
    """
    Chuẩn hóa dữ liệu từ MBW ATS → Mira Talent
    """

    # --- Mapping giới tính
    gender_map = {"Nam": "Male", "Nữ": "Female"}
    gender = gender_map.get(record.get("can_gender"), "Unknown")

    # --- Trạng thái CRM
    crm_status = "Active" if not record.get("rejected") else "Archived"

    # --- Kỹ năng (Candidate_Skill child table)
    skills = []
    if record.get("candidate_skill"):
        for skill in record["candidate_skill"]:
            name = skill.get("can_skill_name") or ""
            if name:
                skills.append(unquote(name))
    skills_text = ", ".join(skills)

    # --- Education (Candidate_Education)
    education_json = []
    if record.get("candidate_education"):
        for edu in record["candidate_education"]:
            education_json.append({
                "school": edu.get("school_name"),
                "degree": edu.get("degree"),
                "field_of_study": edu.get("major"),
                "start_date": edu.get("from_date"),
                "end_date": edu.get("to_date")
            })

    # --- Experience (Candidate_Work_Experience)
    experience_json = []
    if record.get("candidate_work_experience"):
        for exp in record["candidate_work_experience"]:
            experience_json.append({
                "company": exp.get("company_name"),
                "title": exp.get("job_title"),
                "start_date": exp.get("from_date"),
                "end_date": exp.get("to_date"),
                "description": exp.get("description")
            })

    # --- Certifications
    certs_json = []
    if record.get("candidate_certification"):
        for cert in record["candidate_certification"]:
            certs_json.append({
                "name": cert.get("certificate_name"),
                "issuer": cert.get("issuer"),
                "date": cert.get("issued_date")
            })

    # --- Build data for Mira Talent
    return {
        "doctype": "Mira Talent",
        "full_name": record.get("can_full_name"),
        "gender": gender,
        "date_of_birth": record.get("can_dob"),
        "email": record.get("can_email"),
        "phone": record.get("can_phone"),
        "linkedin_profile": record.get("can_other_links"),
        "current_city": record.get("can_address"),
        "skills": skills_text,
        "source": source_name or record.get("candidatesource_id"),
        "education": json.dumps(education_json),
        "experience": json.dumps(experience_json),
        "certifications": json.dumps(certs_json),
        "latest_company": record.get("can_last_workplace"),
        "highest_education": None,
        "current_status": crm_status,
        "notes": record.get("can_profile"),
        "resume": record.get("can_cv"),
        "recruiter_owner_id": record.get("can_recruiter"),
        "crm_status": crm_status,
        "availability_date": datetime.now().date(),
        "last_interaction_date": datetime.now().date(),
        "priority_level": "Medium",
        "internal_rating": "B",
        "sync_id": record.get("name"),
        "domain_expertise": "",
        "cultural_fit": "",
        "desired_role": "",
        "soft_skills": "",
        "hard_skills": "",
        "languages": "[]",
    }
