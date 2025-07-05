# Scheduler jobs
import frappe
from frappe.utils import now_datetime, now

#Lịch chạy quét Campaign active
def do_campaign_scheduler():
    print("===============VÀO run_campaign_scheduler====================")
    #frappe.logger("Chạy schedule run_campaign_scheduler thời gian: " + now_datetime())
    frappe.enqueue(
        "mbw_mira.campaign.controller.handle_campaign",queue="default", timeout=300
    )

#Lích chạy quét CandidateCampaign
def do_candidate_campaign_scheduler():
    print("===============VÀO run_candidate_campaign_scheduler====================")
    frappe.enqueue(
            "mbw_mira.campaign.controller.handle_candidate_campaign",queue="default", timeout=300
        )