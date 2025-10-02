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
            "end_date": (">=", today),
            "mira_prospect":["is", "set"]
        },
        fields=["name", "campaign_name", "target_segment"]
    )

    for c in campaigns:
        if not c.target_segment:
            continue

        frappe.enqueue(
            "mbw_mira.workers.prospect_campaign_enrollment.enroll_prospect_for_campaign",
            campaign_id=c.name,
            job_name=c.name,
            queue="default",
            
        )
    return True

