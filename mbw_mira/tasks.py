# Scheduler jobs
import frappe
from frappe.utils import now_datetime, now
from mbw_mira.mbw_mira.doctype.action.action import (process_action_email_active,process_action_sms_active)
from mbw_mira.mbw_mira.doctype.candidatecampaign.candidatecampaign import (process_candidate_campaign_active)
from mbw_mira.mbw_mira.doctype.campaign.campaign import (process_campaign_sync_source_from_ats,process_campaign_source_from_entry,process_campaign_sync_source_from_jobboard,process_campaign_sync_source_from_other,process_campaign_sync_source_from_social)

#=============================Scheduler chạy campaign đồng bộ dữ liệu=================================
#Lịch chạy quét đồng bộ từ nguồn ATS
def do_campaign_sync_source_ats_scheduler():
    process_campaign_sync_source_from_ats()

#Lịch chạy quét đồng bộ từ nguồn sàn tuyển dụng
def do_campaign_sync_source_jobboard_scheduler():
    process_campaign_sync_source_from_jobboard()

#Lịch chạy quét đồng bộ từ nguồn mạng xã hội
def do_campaign_sync_source_social_scheduler():
    process_campaign_sync_source_from_social()

#Lịch chạy quét đồng bộ từ nguồn khác
def do_campaign_sync_source_other_scheduler():
    process_campaign_sync_source_from_other()

#=============================Scheduler chạy campaign từ nguồn thủ công=======================
#Lịch chạy quét Campaign từ nguồn có sẵn
def do_campaign_source_entry_scheduler():
    process_campaign_source_from_entry()

#==============================Scheduler chạy CandidateCampaign========================
#Lịch chạy quét CandidateCampaign
def do_candidate_campaign_scheduler():
    print("===============VÀO do_candidate_campaign_scheduler====================")
    process_candidate_campaign_active()

#=====================================Scheduler chạy action================================
#Chạy quét action gửi email
def do_email_scheduler():
    process_action_email_active()

#Chạy quét action gửi sms
def do_sms_scheduler():
    process_action_sms_active()