import frappe
from frappe.utils import now_datetime

def complete_manual_action(action_id: str, user: str = None, note: str = ""):
    action = frappe.get_doc("Action", action_id)
    if action.status != "PENDING_MANUAL":
        frappe.throw("Chỉ có thể xử lý các hành động thủ công (PENDING_MANUAL).")
    action.status = "EXECUTED"
    action.executed_at = now_datetime()
    action.result = action.result or {}
    action.result.update({
        "manual_completed_by": user or frappe.session.user,
        "manual_note": note,
        "manual_completed_at": now_datetime()
    })
    action.save(ignore_permissions=True)
    #Publish event action from server
    frappe.publish_realtime('manual_action_complete', data=action)

    frappe.enqueue("mbw_mira.campaign.background_jobs.step_executed", job_name="step_executed",action_id=action.name)
