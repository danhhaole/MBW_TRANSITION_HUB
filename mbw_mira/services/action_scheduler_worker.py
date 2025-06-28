# services/action_scheduler_worker.py

import frappe
from frappe.utils import now_datetime
from mbw_mira.models.action import Action

def process_candidate_campaign(candidate_campaign_id: str):
    """
    Worker xử lý ứng viên đến hạn trong chiến dịch ATTRACTION.
    Tạo bản ghi Action tương ứng với bước tiếp theo trong CampaignStep.
    """
    now = now_datetime()
    candidate_campaign = frappe.get_doc("CandidateCampaign", candidate_campaign_id)

    campaign_id = candidate_campaign.campaign
    current_order = candidate_campaign.current_step_order

    # 1. Lấy bước kế tiếp trong Campaign
    next_step = frappe.get_value("CampaignStep", {
        "campaign": campaign_id,
        "step_order": current_order + 1
    }, ["name", "action_type"])

    if not next_step:
        # Không còn bước nào, có thể đánh dấu COMPLETED ở nơi khác
        return

    step_name, action_type = next_step

    # 2. Xác định trạng thái và người phụ trách (nếu là manual)
    status = "SCHEDULED" if action_type in ["SEND_EMAIL", "SEND_SMS"] else "PENDING_MANUAL"
    assignee_id = None

    if status == "PENDING_MANUAL":
        assignee_id = get_assignee_for_manual_action(campaign_id)

    # 3. Tạo bản ghi Action
    action = Action(
        candidate_campaign_id=candidate_campaign.name,
        campaign_step=step_name,
        status=status,
        scheduled_at=now,
        assignee_id=assignee_id
    )

    frappe.get_doc({
        "doctype": "Action",
        "candidate_campaign_id": action.candidate_campaign_id,
        "campaign_step": action.campaign_step,
        "status": action.status,
        "scheduled_at": action.scheduled_at,
        "assignee_id": action.assignee_id
    }).insert(ignore_permissions=True)

    frappe.logger().info(f"[Attraction] Created Action for {candidate_campaign.name} at step {current_order + 1}")


def get_assignee_for_manual_action(campaign_id: str):
    """
    Trả về assignee mặc định từ Campaign nếu có (cho hành động thủ công)
    """
    return frappe.get_value("Campaign", campaign_id, "default_assignee")
