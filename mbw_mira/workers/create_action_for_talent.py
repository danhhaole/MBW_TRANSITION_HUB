import frappe
from frappe.utils import now_datetime


def create_action_for_talent_campaign(talent_campaign_id):
    """
    Worker: Tạo Action cho TalentProfilesCampaign ở bước hiện tại.
    """
    tc = frappe.get_doc("TalentProfilesCampaign", talent_campaign_id)

    # lấy CampaignStep hiện tại
    step = get_campaign_step(tc.campaign_id, tc.current_step_order)

    if not step:
        frappe.logger().warning(
            f"⚠ No CampaignStep found for TalentProfilesCampaign {tc.name} at order {tc.current_step_order}"
        )
        return

    status_action = (
                "SCHEDULED"
                if step.action_type in ["SEND_EMAIL", "SEND_SMS", "SEND_NOTIFICATION"]
                else "PENDING_MANUAL"
            )
    # tạo Action
    action = frappe.get_doc({
        "doctype": "Action",
        "talent_campaign_id": tc.name,
        "campaign_step": step.name,
        "status": status_action,
        "scheduled_at": now_datetime(),
        "executed_at": None,
        "result": None,
        "assignee_id": None  # optional: nếu muốn phân công tự động
    })
    action.insert(ignore_permissions=True)
    frappe.db.commit()

    frappe.logger().info(
        f"✨ Created Action {action.name} for TalentProfilesCampaign {tc.name} | Step: {step.name}"
    )


def get_campaign_step(campaign_id, step_order):
    """
    Lấy CampaignStep theo campaign + step_order
    """
    step = frappe.db.value(
        "CampaignStep",
        filters={
            "campaign": campaign_id,
            "step_order": step_order
        },
        fields=["name", "step_order", "action_type", "template", "delay_in_days", "action_config"]
    )
    return step
