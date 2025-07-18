import frappe
from datetime import date

def run():
    """
    Scan ACTIVE campaigns with Social source = Facebook and enqueue data fetching.
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
        if is_facebook_source(c.source):
            frappe.enqueue(
                "mbw_mira.workers.social.fetch_facebook_data.fetch_facebook_data",
                campaign_name=c.name,
                queue="default",
                job_name=c.name,
                
            )
            frappe.logger().info(f"Enqueued Facebook fetch for campaign: {c.campaign_name}")

def is_facebook_source(source):
    return frappe.db.get_value("CandidateDataSource", source, "source_name") == "Facebook"
