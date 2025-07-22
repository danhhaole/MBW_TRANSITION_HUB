import frappe
from datetime import date

def run():
    """
    Scan ACTIVE campaigns with Social source = LinkedIn and enqueue data fetching.
    """
    today = date.today()
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
        if is_linkedin_source(c.source):
            frappe.enqueue(
                "mbw_mira.workers.social.fetch_linkedin_data.fetch_linkedin_data",
                campaign_name=c.name,
                queue="default",
                job_name=c.name,
                
            )
    return True

def is_linkedin_source(source):
    return frappe.db.get_value("CandidateDataSource", source, "source_name") == "LinkedIn"
