import frappe
from datetime import date

def run():
    """
    Scan ACTIVE campaigns with ATS source = MBW ATS and enqueue data fetching.
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
        if is_mbw_ats_source(c.source):
            frappe.enqueue(
                method="mbw_mira.schedulers.ats.fetch_mbw_ats_data",
                campaign_name=c.name,
                queue="default",
                timeout=600
            )
            frappe.logger().info(f"Enqueued MBW ATS fetch for campaign: {c.campaign_name}")

def is_mbw_ats_source(source):
    return frappe.db.get_value("CandidateDataSource", source, "name") == "MBW ATS"
