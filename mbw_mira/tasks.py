# Scheduler jobs
import frappe
from frappe.utils import now_datetime, now
from mbw_mira.mbw_mira.doctype.action.action import (process_action_email_active,process_action_sms_active)
from mbw_mira.mbw_mira.doctype.candidatecampaign.candidatecampaign import (process_candidate_campaign_active)

#Lịch chạy quét Campaign active
def do_campaign_scheduler():
    print("===============VÀO run_campaign_scheduler====================")
    #frappe.logger("Chạy schedule run_campaign_scheduler thời gian: " + now_datetime())
    frappe.enqueue(
        "mbw_mira.campaign.controller.handle_campaign",queue="default", timeout=300,job_name="handle_campaign"
    )

#Lịch chạy quét CandidateCampaign
def do_candidate_campaign_scheduler():
    print("===============VÀO do_candidate_campaign_scheduler====================")
    process_candidate_campaign_active()

#Chạy quét action gửi email
def do_email_scheduler():
    process_action_email_active()

#Chạy quét action gửi sms
def do_sms_scheduler():
    process_action_sms_active()