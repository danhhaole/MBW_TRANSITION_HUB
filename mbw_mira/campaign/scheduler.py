# Scheduler jobs
import frappe
from frappe.utils import now_datetime, now

#Lịch chạy quét Campaign active
def run_campaign_scheduler():
    
    print("===============VÀO CAMP====================")
    print("Campaigns found:", len(campaigns))
    
    frappe.enqueue(
        "mbw_mira.campaign.background_jobs.process_campaign",queue="default", timeout=300
    )


#Lích chạy quét CandidateCampaign
def run_candidate_campaign_scheduler():
    print("===============VÀO CANCOM====================")
    candidates = frappe.get_all(
        "CandidateCampaign",
        filters={"status": "ACTIVE", "next_action_at": ["<=", now_datetime()]},
        pluck="name",
    )
    
    for cc_id in candidates:
        print("CC_ID",cc_id)
        frappe.enqueue(
            "mbw_mira.campaign.background_jobs.process_next_step",
            candidate_campaign_id=cc_id,
        )
