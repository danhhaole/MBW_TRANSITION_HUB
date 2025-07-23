import frappe
from frappe.utils import now_datetime
from mbw_mira.utils import send_email_job, send_sms_job

def process_email_action(action_name):
    """
    Worker: thực hiện SEND_EMAIL action
    """
    now = now_datetime()
    action = frappe.db.get_value("Action", action_name,["name","talent_campaign_id","campaign_step"],as_dict=1)
    try:

        # TODO: Thực hiện gửi email ở đây
        # Ví dụ:
        # frappe.sendmail(recipients=..., subject=..., message=...)
        #Lấy talentprofile 
        talent_id = frappe.db.get_value("TalentProfilesCampaign", action.talent_campaign_id,"talent_id")
        send_email_job(talent_id,action_name,action.campaign_step)
        frappe.publish_realtime('action_executed', data={'talent_campaign': action.talent_campaign_id, "action":action_name})
        return True

    except Exception as e:
        frappe.log_error(f"Error processing SEND_EMAIL action {action.name}: {e}")
        return True

def process_sms_action(action_name):
    """
    Worker: thực hiện SEND_SMS action
    """
    now = now_datetime()
    action = frappe.db.get_value("Action", action_name,["name","talent_campaign_id","campaign_step"],as_dict=1)
    try:

        # TODO: Thực hiện gửi SMS ở đây
        # Ví dụ: gọi API SMS gateway
        talent_id = frappe.db.get_value("TalentProfilesCampaign", action.talent_campaign_id,"talent_id")
        send_sms_job(talent_id,action_name,action.campaign_step)
        frappe.publish_realtime('action_executed', data={'talent_campaign': action.talent_campaign_id, "action":action_name})
        return True

    except Exception as e:
        frappe.log_error(f"Error processing SEND_SMS action {action.name}: {e}")
        return True

def check_pending_action(action_name):
    """
    Worker: cảnh báo Action pending quá lâu
    """
    action = frappe.get_doc("Action", action_name)
    step_type = frappe.get_value("CampaignStep", action.campaign_step, "action_type")
    try:
        return step_type

        # Optionally: gửi email/notification cảnh báo
        # frappe.sendmail(...)

    except Exception as e:
        frappe.log_error(f"Error while checking pending Action {action.name}: {e}")
        return True
