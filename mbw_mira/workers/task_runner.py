import frappe
from frappe.utils import now_datetime,time_diff_in_seconds
from mbw_mira.utils import send_email_job
from mbw_mira.mbw_mira.doctype.mira_task.mira_task import complete_action
from mbw_mira.workers.action_handlers.start_flow import handle_start_flow


def process_task(task_id):
    task = frappe.get_doc("Mira Task", task_id)

    # Nếu có schedule và chưa đến giờ → không xử lý
    if task.scheduled_at and time_diff_in_seconds(now_datetime(), task.scheduled_at) < 0:
        return
    # Chỉ xử lý task Pending
    if task.status != "Pending":
        return

    # ===== Lấy runtime action =====
    task_def = frappe.get_doc("Mira Task Definition", task.task_definition)

    runtime_action = None
    for a in task_def.task_actions:
        if a.task_id == task.name:
            runtime_action = a
            break

    if not runtime_action:
        # Không tìm thấy action runtime → fail
        task.status = "Failed"
        task.error_log = "Runtime action not found"
        task.executed_at = now_datetime()
        task.save(ignore_permissions=True)
        frappe.db.commit()
        return

    # ===== Xử lý Delay trước khi chạy =====
    if runtime_action.delay_minutes and runtime_action.delay_minutes > 0:
        # Nếu chưa schedule → schedule lần đầu
        if not task.scheduled_at:
            task.scheduled_at = now_datetime()
            task.save(ignore_permissions=True)
            frappe.db.commit()
            return

        # Nếu chưa đến thời điểm chạy → return → scheduler sẽ chạy lại
        if time_diff_in_seconds(now_datetime(), task.scheduled_at) < runtime_action.delay_minutes * 60:
            return

    # ===== Bắt đầu chạy task =====
    task.status = "In Progress"
    task.executed_at = now_datetime()
    task.save(ignore_permissions=True)
    frappe.db.commit()

    try:
        # Run action handler (dựa trên action_type của runtime_action)
        result = run_action(task, runtime_action)
        task.execution_result = str(result) if result else "OK"
        task.status = "Completed"

        # ===== Chuyển sang step tiếp theo =====
        complete_action(task.name)

    except Exception:
        task.status = "Failed"
        task.error_log = frappe.get_traceback()

    task.executed_at = now_datetime()
    task.save(ignore_permissions=True)
    frappe.db.commit()


def run_action(task, runtime_action):
    action_type = runtime_action.action_type
    handler = ACTION_HANDLER_MAP.get(action_type)

    if not handler:
        frappe.log_error(f"Missing handler for action_type: {action_type}", "Mira Task Handler")
        return

    return handler(task, runtime_action)


# ========================
# ACTION HANDLERS
# ========================

def handle_message(task, action): pass
def handle_sms(task, action): pass

def handle_email(task, action):
    send_email_job(task)   # 

def handle_zalo(task, action): pass
def handle_zalo_care(task, action): pass
def handle_zalo_zns(task, action): pass

def handle_subscribe_to_sequence(task, action): pass
def handle_unsubscribe_to_sequence(task, action): pass

def handle_smart_delay(task, action): pass
def handle_ai_call(task, action): pass

def handle_add_tag(task, action): pass
def handle_remove_tag(task, action): pass

def handle_add_custom_field(task, action): pass
def handle_remove_custom_field(task, action): pass

def handle_lead_score(task, action): pass
def handle_external_request(task, action): pass

def handle_email_ai(task, action): pass
def handle_content_ai(task, action): pass

def handle_sent_notification(task, action): pass
def handle_unsubscribe(task, action): pass


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
