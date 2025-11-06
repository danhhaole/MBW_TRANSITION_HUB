import frappe
from mbw_mira.utils import send_email_job
from frappe.utils import now_datetime
from mbw_mira.workers.action_handlers.start_flow import handle_start_flow

def process_task(task_id):
    task = frappe.get_doc("Mira Task", task_id)

    if task.status != "Pending":
        return

    task.status = "In Progress"
    task.save(ignore_permissions=True)
    frappe.db.commit()

    try:
        run_action(task)
        
    except Exception:
        task.status = "Failed"
        task.error_log = frappe.get_traceback()
    task.executed_at = now_datetime()
    task.save(ignore_permissions=True)
    frappe.db.commit()

def run_action(task):
    handler = ACTION_HANDLER_MAP.get(task.action_type)
    if not handler:
        frappe.log_error(f"Missing handler for action_type: {task.action_type}", "Mira Task Handler")
        return

    return handler(task)


# ========================
# ACTION HANDLERS (PLACEHOLDERS)
# ========================

def handle_message(task): pass
def handle_sms(task): pass
def handle_email(task):
    #TODO: Implement send email
    
    send_email_job(task)
    

def handle_zalo(task): pass
def handle_zalo_care(task): pass
def handle_zalo_zns(task): pass

def handle_subscribe_to_sequence(task): pass
def handle_unsubscribe_to_sequence(task): pass

def handle_smart_delay(task): pass
def handle_ai_call(task): pass

def handle_add_tag(task): pass
def handle_remove_tag(task): pass

def handle_add_custom_field(task): pass
def handle_remove_custom_field(task): pass

def handle_lead_score(task): pass
def handle_external_request(task): pass

def handle_email_ai(task): pass
def handle_content_ai(task): pass

def handle_sent_notification(task): pass
def handle_unsubscribe(task): pass

# ======================
# ACTION ROUTING TABLE
# ======================

ACTION_HANDLER_MAP = {
    "MESSAGE": handle_message,
    "SMS": handle_sms,
    "EMAIL": handle_email,

    "ZALO": handle_zalo,
    "ZALO_CARE": handle_zalo_care,
    "ZALO_ZNS": handle_zalo_zns,

    "START_FLOW": handle_start_flow,
    "SUBSCRIBE_TO_SEQUENCE": handle_subscribe_to_sequence,
    "UN_SUBSCRIBE_TO_SEQUENCE": handle_unsubscribe_to_sequence,

    "SMART_DELAY": handle_smart_delay,
    "AI_CALL": handle_ai_call,

    "ADD_TAG": handle_add_tag,
    "REMOVE_TAG": handle_remove_tag,

    "ADD_CUSTOM_FIELD": handle_add_custom_field,
    "REMOVE_CUSTOM_FIELD": handle_remove_custom_field,

    "LEAD_SCORE": handle_lead_score,
    "EXTERNAL_REQUEST": handle_external_request,

    "EMAIL_AI": handle_email_ai,
    "CONTENT_AI": handle_content_ai,

    "SENT_NOTIFICATION": handle_sent_notification,
    "UNSUBSCRIBE": handle_unsubscribe,
}
    
