import frappe
from frappe.utils import now_datetime


def create_action_for_talent_campaign(talent_campaign_id):
    """
    Worker: Tạo Action cho Mira Talent Campaign ở bước hiện tại.
    """
    try:
        tc = frappe.db.get_value("Mira Talent Campaign", talent_campaign_id,["name","campaign_social"],as_dict=1)
        
        # lấy CampaignStep hiện tại
        step = get_campaign_social(tc.campaign_social)
        
        if not step:
            return

        status_action = "SCHEDULED"
        # (
        #             "SCHEDULED"
        #             if step.action_type in ["SEND_EMAIL", "SEND_SMS", "SEND_NOTIFICATION"]
        #             else "PENDING_MANUAL"
        #         )
        # tạo Action
        action_type = ""
        if step.platform == 'Email':
            action_type = "SEND_EMAIL"
        elif step.platform == 'Facebook':
            action_type = 'POST_FACEBOOK'
        elif step.platform == 'Zalo':
            action_type == 'SEND_ZALO'
        elif step.platform == 'Linkedin':
            action_type = 'SEND_LINKEDIN'
        elif step.platform == 'TopCV':
            action_type = 'POST_TOPCV'
        
        
        if not check_exists(tc.name,step.name) and action_type in ["SEND_EMAIL","SEND_ZALO"]:
            action = frappe.get_doc({
                "doctype": "Mira Action",
                "talent_campaign_id": tc.name,
                "campaign_social": step.name,
                "action_type":action_type,
                "status": status_action,
                "scheduled_at": now_datetime(),
                "executed_at": None,
                "result": None,
                "assignee_id": frappe.session.user  # optional: nếu muốn phân công tự động
            })
            action.insert(ignore_permissions=True)
            frappe.db.commit()
            
            #frappe.publish_realtime('action_created', message={'talent_campaign': talent_campaign_id})
            return action.name
        else:
            return None
        
    except Exception as e:
        frappe.log_error(str(e))
        return None

def check_exists(talent_campaign_id,campaign_social):
    action_exists = frappe.db.exists("Mira Action",{"talent_campaign_id":talent_campaign_id,"campaign_social":campaign_social})
    if action_exists:
        return True
    else:
        return False


def get_campaign_social(campaign_social):
    """
    Lấy CampaignStep theo campaign + campaign_social
    """
    step = frappe.db.get_value(
        "Mira Campaign Social",
        campaign_social,
        ["*"], as_dict=1
    )
    return step
