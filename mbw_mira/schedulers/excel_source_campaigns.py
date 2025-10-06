import frappe
from datetime import date

def run():
    """
    Scan ACTIVE campaigns with source = File and enqueue data fetching.
    """
    today = date.today()
    campaigns = frappe.get_all(
        "Campaign",
        filters={
            "is_active": 1,
            "source_type":"File",
            "status": "ACTIVE",
            "start_date": ("<=", today),
            "end_date": (">=", today)
        },
        fields=["name", "campaign_name", "source"]
    )
    for c in campaigns:
        frappe.enqueue(
            "mbw_mira.workers.import_excel_for_talent.import_prospect_from_file",
            campaign_name=c.name,
            job_name=c.name,
            source_target=c.source_target,
            queue="short"
        )
    return True
