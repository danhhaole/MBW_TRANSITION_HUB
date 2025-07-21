import frappe
import logging
from mbw_mira.integrations.jobboard.vietnamworks_provider import VietnamWorksProvider

logger = logging.getLogger(__name__)

def fetch_vietnamworks_data(campaign_name):
    """
    Worker: Fetch data for ACTIVE campaign from VietnamWorks via VietnamWorksProvider.
    """
    logger.info(f"[VietnamWorks] Fetching data for campaign: {campaign_name}")

    campaign = frappe.get_doc("Campaign", campaign_name)
    source_name = campaign.source

    with VietnamWorksProvider(source_name) as provider:
        if provider.sync_direction not in ("Pull", "Both"):
            logger.warning(f"[VietnamWorks] Sync direction '{provider.sync_direction}' does not allow Pull.")
            return

        criteria = campaign.criteria or {}
        if isinstance(criteria, str):
            import json
            criteria = json.loads(criteria)

        try:
            filters = criteria.get("filters", {})
            fields = criteria.get("fields", ["name", "email", "mobile_no"])

            logger.info(f"[VietnamWorks] Fetching candidates with filters={filters}, fields={fields}")
            candidates = provider.get_candidates(filters=filters, fields=fields)

            save_candidates(candidates, campaign_name, provider_name="VietnamWorks")

            logger.info(f"[VietnamWorks] Completed fetching {len(candidates)} candidates for campaign: {campaign.campaign_name}")

        except Exception as e:
            logger.error(f"[VietnamWorks] Failed fetching data for campaign: {campaign.campaign_name} — {str(e)}", exc_info=True)


def save_candidates(candidates, campaign_name, provider_name):
    for c in candidates:
        try:
            existing = frappe.db.exists("Candidate", c["name"])
            if not existing:
                doc = frappe.get_doc({
                    "doctype": "Candidate",
                    "name": c["name"],
                    "email": c.get("email"),
                    "mobile_no": c.get("mobile_no"),
                    "source_campaign": campaign_name,
                    "source_provider": provider_name
                })
                doc.insert()
                logger.info(f"[VietnamWorks] Inserted candidate {c['name']}")
            else:
                logger.info(f"[VietnamWorks] Candidate {c['name']} already exists — skipped.")
        except Exception as e:
            logger.error(f"[VietnamWorks] Failed to save candidate {c.get('name')} — {str(e)}", exc_info=True)
