import frappe
from frappe.utils import now_datetime


def create_action_for_talent_campaign(talent_campaign_id):
    """
    Worker: Tạo Action cho TalentProfilesCampaign ở bước hiện tại.
    """
    try:
        tc = frappe.db.get_value("TalentProfilesCampaign", talent_campaign_id,["name","campaign_id","current_step_order"],as_dict=1)

        # lấy CampaignStep hiện tại
        step = get_campaign_step(tc.campaign_id, tc.current_step_order)

        if not step:
            return

        status_action = (
                    "SCHEDULED"
                    if step.action_type in ["SEND_EMAIL", "SEND_SMS", "SEND_NOTIFICATION"]
                    else "PENDING_MANUAL"
                )
        # tạo Action
        if not check_exists(tc.name,step.name):
            action = frappe.get_doc({
                "doctype": "Action",
                "talent_campaign_id": tc.name,
                "campaign_step": step.name,
                "status": status_action,
                "scheduled_at": now_datetime(),
                "executed_at": None,
                "result": None,
                "assignee_id": frappe.session.user  # optional: nếu muốn phân công tự động
            })
            action.insert(ignore_permissions=True)
            frappe.db.commit()
            return action.name
        else:
            return None
        
    except Exception as e:
        frappe.log_error(str(e))
        return None

def check_exists(talent_campaign_id,campaign_step):
    action_exists = frappe.db.exists("Action",{"talent_campaign_id":talent_campaign_id,"campaign_step":campaign_step})
    if action_exists:
        return True
    else:
        return False


def get_campaign_step(campaign_id, step_order):
    """
    Lấy CampaignStep theo campaign + step_order
    """
    step = frappe.db.get_value(
        "CampaignStep",
        {
            "campaign": campaign_id,
            "step_order": step_order
        },
        ["name", "step_order", "action_type", "template", "delay_in_days", "action_config"], as_dict=1
    )
    return step
