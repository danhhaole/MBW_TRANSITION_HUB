import frappe
from datetime import date

def run():
    """
    Scan ACTIVE campaigns with JobBoard source = TopCV and enqueue data fetching.
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
        fields=["name", "campaign_name", "source"]
    )

    for c in campaigns:
        if is_topcv_source(c.source):
            frappe.enqueue(
                method="mbw_mira.schedulers.jobboard.fetch_topcv_data",
                campaign_name=c.name,
                queue="default",
                timeout=600
            )
            frappe.logger().info(f"Enqueued TopCV fetch for campaign: {c.campaign_name}")

def is_topcv_source(source):
    return frappe.db.get_value("CandidateDataSource", source, "source_name") == "TopCV"
