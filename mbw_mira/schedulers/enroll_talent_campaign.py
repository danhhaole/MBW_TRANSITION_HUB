import frappe
from datetime import date


def run():
    """
    Scan ACTIVE campaigns and enqueue enrollment tasks.
    """
    today = date.today()
    campaigns = frappe.get_all(
        "Campaign",
        filters={
            "is_active": 1,
            "status": "ACTIVE",
            "start_date": ("<=", today),
            "end_date": (">=", today)
        },
        fields=["name", "campaign_name", "target_segment"]
    )

    for c in campaigns:
        if not c.target_segment:
            frappe.logger().warning(f"⚠ Campaign {c.campaign_name} has no target segment.")
            continue

        frappe.enqueue(
            method="mbw_mira.workers.talent_enrollment.enroll_talent_for_campaign",
            campaign_id=c.name,
            queue="default",
            timeout=600
        )

        frappe.logger().info(f"🕒 Enqueued enrollment worker for campaign: {c.campaign_name}")
