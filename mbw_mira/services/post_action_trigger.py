import frappe
from frappe.utils import add_days, now_datetime

class PostActionProcessor:
    def __init__(self, action_id):
        self.action = frappe.get_doc("Action", action_id)

    def update_action_status(self, action_id, status, result=None):
        """
        Cập nhật trạng thái của một Action.
        """
        action = frappe.get_doc("Action", action_id)
        action.status = status
        action.executed_at = now_datetime()
        action.result = result or {}

        # Lưu cập nhật vào cơ sở dữ liệu
        action.db_set({
            "status": status,
            "executed_at": action.executed_at,
            "result": action.result
        })

        if status == "EXECUTED":
            self.trigger_next_step(action)

    def trigger_next_step(self, action):
        """
        Kích hoạt bước tiếp theo sau khi một Action được thực thi thành công.
        """
        candidate_campaign = frappe.get_doc("CandidateCampaign", action.candidate_campaign_id)
        current_step_order = candidate_campaign.current_step_order

        # Tìm bước tiếp theo
        next_step = frappe.get_doc("CampaignStep", {
            "campaign_id": candidate_campaign.campaign,
            "step_order": current_step_order + 1
        })

        if not next_step:
            # Không có bước tiếp theo, kết thúc chiến dịch
            candidate_campaign.db_set({"status": "COMPLETED"})
            return

        # Tính toán next_action_at
        delay_in_days = next_step.delay_in_days or 0
        next_action_at = add_days(now_datetime(), delay_in_days)

        # Cập nhật CandidateCampaign
        candidate_campaign.db_set({
            "current_step_order": current_step_order + 1,
            "next_action_at": next_action_at
        })
