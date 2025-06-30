# Scheduler jobs
import frappe
from frappe.utils import now_datetime


def run_campaign_scheduler():
    print("================================================VÀO====================")
    candidates = frappe.get_all(
        "CandidateCampaign",
        filters={"status": "ACTIVE", "next_action_at": ["<=", now_datetime()]},
        pluck="name",
    )
    
    for cc_id in candidates:
        frappe.enqueue(
            "mbw_mira.campaign.background_jobs.process_next_step",
            candidate_campaign_id=cc_id,
        )
