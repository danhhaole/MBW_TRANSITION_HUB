import frappe
from datetime import datetime

def run():
    """
    Scan ACTIVE campaigns with JobBoard source = VietnamWorks and enqueue data fetching.
    """
    today = datetime.now()
    campaigns = frappe.get_all(
        "Mira Campaign",
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
        if is_vietnamworks_source(c.source):
            frappe.enqueue(
                "mbw_mira.schedulers.jobboard.fetch_vietnamworks_data.fetch_vietnamworks_data",
                campaign_name=c.name,
                queue="default",
                job_name=c.name,
                
            )
    return True

def is_vietnamworks_source(source):
    return frappe.db.get_value("Mira Data Source", source, "source_name") == "VietnamWorks"
