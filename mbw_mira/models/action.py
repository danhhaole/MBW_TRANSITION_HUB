#Lớp riêng để tạo action
# models/action.py
import frappe
class ActionCreator:
    def __init__(self, candidate_campaign_id, campaign_id, current_step_order):
        self.candidate_campaign_id = candidate_campaign_id
        self.campaign_id = campaign_id
        self.current_step_order = current_step_order

    def create_action(self):
        step = frappe.get_value("CampaignStep", {
            "campaign": self.campaign_id,
            "step_order": self.current_step_order
        }, ["name", "action_type"])

        if not step:
            return

        status = "SCHEDULED" if step.action_type in ("SEND_EMAIL", "SEND_SMS") else "PENDING_MANUAL"

        frappe.get_doc({
            "doctype": "Action",
            "candidate_campaign": self.candidate_campaign_id,
            "campaign_step": step.name,
            "scheduled_at": frappe.utils.now_datetime(),
            "status": status
        }).insert()
