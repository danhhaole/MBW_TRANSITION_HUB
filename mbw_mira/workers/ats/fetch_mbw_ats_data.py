#Nhập campaign từ ATS
import frappe
import logging
from mbw_mira.integrations.ats.frappe_site_provider import FrappeSiteProvider
from datetime import datetime

logger = logging.getLogger(__name__)

def fetch_mbw_ats_data(campaign_name):
    """
    Worker: Fetch ACTIVE campaign data from MBW ATS and save to TalentPool.
    """
    logger.info(f"[MBW ATS] Start fetching data for campaign: {campaign_name}")

    # Lấy thông tin Campaign
    campaign = frappe.get_doc("Campaign", campaign_name)
    source_name = campaign.source
    segment_id = campaign.target_segment

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
            fields = criteria.get("fields", ["name", "can_full_name", "can_email", "can_phone"])
            logger.info(f"[MBW ATS] Fetching candidates with filters={filters}, fields={fields}")
            candidates = provider.get_list("Candidate", filters=filters, fields=fields)

            save_candidates_to_talent_pool(candidates, campaign, source_name, segment_id)

            logger.info(f"[MBW ATS] Done fetching & saving {len(candidates)} candidates for campaign: {campaign.campaign_name}")

        except Exception as e:
            logger.error(f"[MBW ATS] Failed fetching data for campaign: {campaign.campaign_name} — {str(e)}", exc_info=True)


def save_candidates_to_talent_pool(candidates, campaign, source_name, segment_id):
    """
    Chuẩn hóa & lưu danh sách ứng viên vào TalentPool
    """
    count = 0
    for record in candidates:
        doc_data = map_mbw_ats_to_talentpool(
            record,
            campaign_name=campaign.name,
            source_name=source_name,
            segment_id=segment_id
        )
        try:
            doc = frappe.get_doc(doc_data)
            doc.insert()
            frappe.db.commit()
            logger.info(f"[TalentPool] Inserted: {doc.full_name} / {doc.email}")
            count += 1
        except Exception as e:
            logger.error(f"[TalentPool] Failed to save {doc_data.get('full_name')} — {str(e)}", exc_info=True)
    logger.info(f"[TalentPool] Total inserted: {count}")


def map_mbw_ats_to_talentpool(record, campaign_name, source_name, segment_id=None):
    """
    Chuẩn hóa dữ liệu từ MBW ATS → TalentPool
    """
    status = "Active" if record.get("status") == "Ứng tuyển" else "Inactive"

    notes_parts = []
    if record.get("can_referral"):
        notes_parts.append(f"Referral: {record['can_referral']}")
    if record.get("can_cv"):
        notes_parts.append(f"CV: {record['can_cv']}")
    notes = "\n".join(notes_parts)

    skills = []
    if record.get("major_id"):
        skills.append(record["major_id"])

    current_position = record.get("can_last_workplace") or record.get("major_id")

    return {
        "doctype": "TalentPool",
        "full_name": record.get("can_full_name"),
        "email": record.get("can_email"),
        "phone": record.get("can_phone"),
        "source": source_name,
        "skills": skills,
        "location": record.get("can_address") or record.get("can_region"),
        "experience_years": 0,
        "current_position": current_position,
        "status": status,
        "campaign_id": campaign_name,
        "segment_id": segment_id,
        "synced_at": datetime.now(),
        "notes": notes
    }
