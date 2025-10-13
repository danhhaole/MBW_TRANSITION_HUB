#Nhập campaign từ ATS
import frappe
import logging
from mbw_mira.integrations.ats.frappe_site_provider import FrappeSiteProvider
from datetime import datetime
import json
from urllib.parse import unquote

logger = logging.getLogger(__name__)

def fetch_mbw_ats_data(campaign_name):
    """
    Worker: Fetch ACTIVE campaign data from MBW ATS and save to Mira Prospect.
    """

    # Lấy thông tin Campaign
    campaign = frappe.get_doc("Mira Campaign", campaign_name)
    source_name = campaign.source
    segment_id = campaign.target_segment

    with FrappeSiteProvider(source_name) as provider:
        if provider.sync_direction not in ("Pull", "Both"):
            return

        criteria = campaign.criteria or {}
        if isinstance(criteria, str):
            criteria = json.loads(criteria)
        total =0
        try:
            filters = criteria.get("filters", {})
            fields = criteria.get("fields", ["name"])
            candidates = provider.get_list("ATS_Candidate", filters=filters, fields=fields)
            
            if candidates:
                total = save_candidates_to_talent_pool(provider,candidates, campaign, source_name, segment_id)

            frappe.publish_realtime('fetch_data_integrations_ats', message={'campaign': campaign_name, "segment":segment_id})

            return total
        except Exception as e:
            logger.error(f"[MBW ATS] Failed fetching data for campaign: {campaign.campaign_name} — {str(e)}", exc_info=True)
            return total


def save_candidates_to_talent_pool(provider,candidates, campaign, source_name, segment_id):
    """
    Chuẩn hóa & lưu danh sách ứng viên vào Mira Prospect
    """
    count = 0
    if candidates:
        for record in candidates:
            record = provider.get_doc("ATS_Candidate",record.get('name'))
            doc_data = map_mbw_ats_to_talentprofiles(
                record,
                campaign_name=campaign.name,
                source_name=source_name,
                segment_id=segment_id
            )
            try:
                doc = frappe.get_doc(doc_data)
                doc.insert(ignore_permissions=True)
                frappe.db.commit()
                count += 1
            except Exception as e:
                logger.error(f"[Mira Prospect] Failed to save {doc_data.get('full_name')} — {str(e)}", exc_info=True)
                continue
    return count


def map_mbw_ats_to_talentprofiles(record, campaign_name, source_name, segment_id=None):
    """
    Chuẩn hóa dữ liệu từ MBW ATS → Mira Prospect
    """

    # Chuyển đổi status
    status_map = {
        "Ứng tuyển": "ENGAGED",
        "Tiềm năng": "NURTURING",
        "Mới": "NEW",
        "Đã liên hệ": "SOURCED",
        "Không phù hợp": "ARCHIVED",
    }
    status = "NEW"

    # Gộp ghi chú thành ai_summary nếu muốn giữ lại
    ai_summary_parts = []
    if record.get("can_referral"):
        ai_summary_parts.append(f"Referral: {record['can_referral']}")
    if record.get("can_cv"):
        ai_summary_parts.append(f"CV: {record['can_cv']}")
    ai_summary = "\n".join(ai_summary_parts) or None

    # Kỹ năng
    skills = []
    if record.get("candidate_skill"):
        for skill in record["candidate_skill"]:
            skills.append(unquote(skill.get("can_skill_name")))
    skills_json_string = json.dumps(skills) if skills else "[]"

    # Headline (current position)
    headline = record.get("can_last_workplace") or record.get("major_id")

    return {
        "doctype": "Mira Prospect",
        "full_name": record.get("can_full_name"),
        "email": record.get("can_email"),
        "phone": record.get("can_phone"),
        "source": source_name,
        "dob":record.get("can_dob"),
        "skills": skills_json_string,
        "avatar": None,
        "headline": headline,
        "cv_original_url": None,
        "profile_data": None,
        "ai_summary": ai_summary,
        "status": status,
        "last_interaction": datetime.now(),
        "email_opt_out": 0
    }