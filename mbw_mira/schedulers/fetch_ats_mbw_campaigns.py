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
            "source_type":"DataSource",
            "status": "ACTIVE",
            "start_date": ("<=", today),
            "end_date": (">=", today)
        },
        fields=["name", "campaign_name", "source"]
    )
    for c in campaigns:
        if is_mbw_ats_source(c.source):
            frappe.enqueue(
                "mbw_mira.workers.ats.fetch_mbw_ats_data.fetch_mbw_ats_data",
                campaign_name=c.name,
                job_name=c.name,
                queue="short"
            )
            frappe.logger().info(f"Enqueued MBW ATS fetch for campaign: {c.campaign_name}")

def is_mbw_ats_source(source):
    return frappe.db.get_value("CandidateDataSource", source, "source_name") == "MBW ATS"
