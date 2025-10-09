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
        fields=["name", "campaign_name", "post_schedule_time","social_page_name","social_page_id","template_content"]
    )
    #from mbw_mira.workers.ats import fetch_mbw_ats_data
    for c in campaigns:
        if c.social_page_id and c.social_page_name and c.post_schedule_time:           
            frappe.enqueue(
                "mbw_mira.workers.social.fetch_facebook_data.post_to_facebook",
                share_name=c.name,
                queue="short"
            )
    return True

