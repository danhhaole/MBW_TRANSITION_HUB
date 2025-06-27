import frappe
from frappe.utils import add_days, now_datetime

class PostActionProcessor:
    def __init__(self, action_id):
        self.action = frappe.get_doc("Action", action_id)

    def trigger_next_step(self):
        if self.action.status != "EXECUTED":
            return

        cc = frappe.get_doc("CandidateCampaign", self.action.candidate_campaign)
        next_order = cc.current_step_order + 1

        next_step = frappe.get_value("CampaignStep", {
            "campaign": cc.campaign,
            "step_order": next_order
        }, ["delay_in_days"])

        if next_step:
            next_action_at = add_days(now_datetime(), next_step.delay_in_days)
            cc.db_set({
                "current_step_order": next_order,
                "next_action_at": next_action_at
            })
