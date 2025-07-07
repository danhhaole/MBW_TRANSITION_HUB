# Các task enqueue
import frappe
from mbw_mira.campaign import controller, manual_task_handler
from mbw_mira.services import candidate_service,campaign_service


def process_next_step(candidate_campaign_id):
    frappe.enqueue(
        controller.handle_step,
        queue="default",
        job_name="handle_step",
        candidate_campaign_id=candidate_campaign_id,
    )


def execute_action(action_id):
    frappe.enqueue(
        controller.execute_action_logic, queue="default", action_id=action_id,job_name="execute_action_logic"
    )


def step_executed(action_id):
    frappe.enqueue(controller.process_step_result, queue="default", action_id=action_id,job_name="process_step_result")

#Queu hoàn thành thủ công nếu action manual
def complete_manual(action_id, note=None, user=None):
    frappe.enqueue(
        manual_task_handler.complete_manual_action,
        queue="default",
        job_name="complete_manual_action",
        action_id=action_id,
        note=note,
        user=user,
    )



def process_campaign_with_steps(data):
    frappe.enqueue(
        campaign_service.process_campaign_with_steps,
        queue="default",
        job_name="process_campaign_with_steps",
        timeout=300,
        data=data,
    )
