# Scheduler jobs
import frappe
from frappe.utils import now_datetime, now

#Lịch chạy quét Campaign active
def run_campaign_scheduler():
    campaigns = get_active_campaigns()

    for cp in campaigns:
        frappe.enqueue(
            "mbw_mira.campaign.background_jobs.add_candidate_to_talentsegment",
            campaign=cp.name,
            segment=cp.target_segment
        )

    
def get_active_campaigns():
    """
    Lấy danh sách Campaign:
    - status = ACTIVE
    - is_active = 1
    - start_date <= hôm nay
    - end_date >= hôm nay
    """
    current_date = now()  # yyyy-mm-dd

    campaigns = frappe.get_all(
        "Campaign",
        filters={
            "status": "ACTIVE",
            "is_active": 1,
            "start_date": ["<=", current_date],
            "end_date": [">=", current_date]
        },
        fields=[
            "name",
            "campaign_name",
            "start_date",
            "end_date",
            "status",
            "is_active",
            "target_segment"
        ],
        order_by="start_date asc"
    )

    return campaigns

#Lích chạy quét CandidateCampaign
def run_candidate_campaign_scheduler():
    print("===============VÀO====================")
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
