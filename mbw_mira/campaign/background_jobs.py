# Các task enqueue
import frappe
from mbw_mira.campaign import controller, manual_task_handler

def process_next_step(candidate_campaign_id):
    frappe.enqueue(controller.handle_step, queue="default", candidate_campaign_id=candidate_campaign_id)

def execute_action(action_id):
    frappe.enqueue(controller.execute_action_logic, queue="default", action_id=action_id)

def step_executed(action_id):
    frappe.enqueue(controller.process_step_result, queue="default", action_id=action_id)
@frappe.whitelist()
def complete_manual(action_id, note=None, user=None):
    frappe.enqueue(manual_task_handler.complete_manual_action, queue="default",
                   action_id=action_id, note=note, user=user)


