import frappe
from datetime import datetime

from mbw_mira.workers.import_excel_for_source import import_contact_from_file

def run():
    """
    Scan ACTIVE campaigns with source = File and enqueue data fetching.
    """
    today = datetime.now()
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
        if c.source_target == 'contact':
            frappe.enqueue(
                "mbw_mira.workers.import_excel_for_source.import_contact_from_file",
                campaign_name=c.name,
                job_name=c.name,
                source_target='contact',
                queue="short"
            )
        elif c.source_target == 'talent':            
            # import_contact_from_file(c.name)
            frappe.enqueue(
                "mbw_mira.workers.import_excel_for_source.import_talent_from_file",
                campaign_name=c.name,
                job_name=c.name,
                source_target='talent',
                queue="short"
            )
    return True
