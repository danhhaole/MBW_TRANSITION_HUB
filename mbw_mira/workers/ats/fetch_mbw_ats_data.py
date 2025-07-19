#Nhập campaign từ ATS
import frappe
import logging
from mbw_mira.integrations.ats.frappe_site_provider import FrappeSiteProvider
from datetime import datetime
import json

logger = logging.getLogger(__name__)

def fetch_mbw_ats_data(campaign_name):
    """
    Worker: Fetch ACTIVE campaign data from MBW ATS and save to TalentProfiles.
    """
    logger.info(f"[MBW ATS] Start fetching data for campaign: {campaign_name}")

    # Lấy thông tin Campaign
    campaign = frappe.get_doc("Campaign", campaign_name)
    source_name = campaign.source
    segment_id = campaign.target_segment
    print("[MBW ATS] Start fetching data for campaign",campaign)

    with FrappeSiteProvider(source_name) as provider:
        if provider.sync_direction not in ("Pull", "Both"):
            logger.warning(f"[MBW ATS] Sync direction '{provider.sync_direction}' does not allow Pull.")
            return

        criteria = campaign.criteria or {}
        if isinstance(criteria, str):
            import json
            criteria = json.loads(criteria)

        try:
            filters = criteria.get("filters", {})
            fields = criteria.get("fields", ["name", "can_full_name", "can_email", "can_phone","candidate_skill"])
            logger.info(f"[MBW ATS] Fetching candidates with filters={filters}, fields={fields}")
            candidates = provider.get_list("ATS_Candidate", filters=filters, fields=fields)
            if candidates:
                save_candidates_to_talent_pool(candidates, campaign, source_name, segment_id)

                logger.info(f"[MBW ATS] Done fetching & saving {len(candidates)} candidates for campaign: {campaign.campaign_name}")

        except Exception as e:
            logger.error(f"[MBW ATS] Failed fetching data for campaign: {campaign.campaign_name} — {str(e)}", exc_info=True)


def save_candidates_to_talent_pool(candidates, campaign, source_name, segment_id):
    """
    Chuẩn hóa & lưu danh sách ứng viên vào TalentProfiles
    """
    count = 0
    if candidates:
        for record in candidates:
            doc_data = map_mbw_ats_to_talentprofiles(
                record,
                campaign_name=campaign.name,
                source_name=source_name,
                segment_id=segment_id
            )
            try:
                doc = frappe.get_doc(doc_data)
                doc.insert()
                frappe.db.commit()
                logger.info(f"[TalentProfiles] Inserted: {doc.full_name} / {doc.email}")
                count += 1
            except Exception as e:
                logger.error(f"[TalentProfiles] Failed to save {doc_data.get('full_name')} — {str(e)}", exc_info=True)
    logger.info(f"[TalentProfiles] Total inserted: {count}")


def map_mbw_ats_to_talentprofiles(record, campaign_name, source_name, segment_id=None):
    """
    Chuẩn hóa dữ liệu từ MBW ATS → TalentProfiles
    """

    # Chuyển đổi status
    status_map = {
        "Ứng tuyển": "ENGAGED",
        "Tiềm năng": "NURTURING",
        "Mới": "NEW",
        "Đã liên hệ": "SOURCED",
        "Không phù hợp": "ARCHIVED",
    }
    status = status_map.get(record.get("status"), "NEW")

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
        skills.append(record["candidate_skill"])
    skills_json_string = json.dumps(skills) if skills else "[]"

    # Headline (current position)
    headline = record.get("can_last_workplace") or record.get("major_id")

    return {
        "doctype": "TalentProfiles",
        "full_name": record.get("can_full_name"),
        "email": record.get("can_email"),
        "phone": record.get("can_phone"),
        "source": source_name,
        "skills": skills_json_string,
        "avatar": None,
        "headline": headline,
        "cv_original_url": None,
        "profile_data": None,
        "ai_summary": ai_summary,
        "status": status,
        "last_interaction": datetime.now(),
        "email_opt_out": 0
        # Các field như campaign_name hay segment_id bạn có thể gắn thêm bằng cách mở rộng doctype nếu cần
    }