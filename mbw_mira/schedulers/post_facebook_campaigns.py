import frappe
from datetime import datetime
from frappe.utils import now_datetime, add_to_date
def run():
    """
    Scan ACTIVE campaigns with ATS source = MBW ATS and enqueue data fetching.
    e780ec0fa468879
    """
    today = datetime.now()
    now = now_datetime()
    before_60s = add_to_date(now, seconds=-60)
    after_60s = add_to_date(now, seconds=60)
    campaigns = frappe.get_all(
        "Mira Campaign Social",
        filters={
            "status":"Pending",
            
            "post_schedule_time":["between", [before_60s, after_60s]]
        },
        fields=["*"]
    )
    for c in campaigns:
        if c.social_page_id and c.social_page_name and c.post_schedule_time:         
           
            frappe.enqueue(
                "mbw_mira.workers.process_action.process_facebook_action",
                social=c,
                campaign_id=c.campaign_id,                
                queue="short"
            )
    return True

