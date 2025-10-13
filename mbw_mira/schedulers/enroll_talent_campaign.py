import frappe
from datetime import datetime


def run():
    """
    Scan ACTIVE campaigns and enqueue enrollment tasks.
    """
    today = datetime.now()
    campaigns = frappe.get_all(
        "Mira Campaign",
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
            continue

        frappe.enqueue(
            "mbw_mira.workers.talent_campaign_enrollment.enroll_talent_for_campaign",
            campaign_id=c.name,
            job_name=c.name,
            queue="default",
            
        )
    return True

