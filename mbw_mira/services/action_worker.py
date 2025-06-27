import frappe
from frappe.utils import now_datetime
from mbw_mira.services.post_action_trigger import PostActionProcessor

class ActionWorker:
    def __init__(self, action_id):
        self.action = frappe.get_doc("Action", action_id)

    def process(self):
        try:
            if self.action.campaign_step.action_type == "SEND_EMAIL":
                result = self.send_email()
            elif self.action.campaign_step.action_type == "SEND_SMS":
                result = self.send_sms()
            else:
                result = {}

            self.action.db_set({
                "status": "EXECUTED",
                "executed_at": now_datetime(),
                "result": result
            })

            PostActionProcessor(self.action.name).trigger_next_step()

        except Exception as e:
            self.action.db_set({
                "status": "FAILED",
                "result": {"error": str(e)}
            })

    def send_email(self):
        # Replace this with real email logic
        return {"message_id": "email123"}

    def send_sms(self):
        # Replace this with real SMS logic
        return {"sms_id": "sms456"}
