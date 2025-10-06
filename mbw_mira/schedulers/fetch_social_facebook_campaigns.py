import frappe
from datetime import datetime

def run():
    """
    Scan ACTIVE campaigns with Social source = Facebook and enqueue data fetching.
    """
    today = datetime.now()
    campaigns = frappe.get_all(
        "Campaign",
        filters={
            "is_active": 1,
            "status": "ACTIVE",
            "source_type":"DataSource",
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
    return True

def is_facebook_source(source):
    return frappe.db.get_value("CandidateDataSource", source, "source_name") == "Facebook"
