import frappe
from frappe.utils import now_datetime

def process_email_action(action_name):
    """
    Worker: thực hiện SEND_EMAIL action
    """
    now = now_datetime()
    action = frappe.get_doc("Action", action_name)
    try:
        frappe.logger().info(f"[Worker] Processing SEND_EMAIL action: {action.name}")

        # TODO: Thực hiện gửi email ở đây
        # Ví dụ:
        # frappe.sendmail(recipients=..., subject=..., message=...)

        action.db_set("status", "EXECUTED")
        action.db_set("executed_at", now)

        frappe.logger().info(f"[Worker] SEND_EMAIL action executed: {action.name}")

    except Exception as e:
        frappe.log_error(f"Error processing SEND_EMAIL action {action.name}: {e}")
        action.db_set("status", "FAILED")
        action.db_set("executed_at", now)

def process_sms_action(action_name):
    """
    Worker: thực hiện SEND_SMS action
    """
    now = now_datetime()
    action = frappe.get_doc("Action", action_name)
    try:
        frappe.logger().info(f"[Worker] Processing SEND_SMS action: {action.name}")

        # TODO: Thực hiện gửi SMS ở đây
        # Ví dụ: gọi API SMS gateway

        action.db_set("status", "EXECUTED")
        action.db_set("executed_at", now)

        frappe.logger().info(f"[Worker] SEND_SMS action executed: {action.name}")

    except Exception as e:
        frappe.log_error(f"Error processing SEND_SMS action {action.name}: {e}")
        action.db_set("status", "FAILED")
        action.db_set("executed_at", now)

def check_pending_action(action_name):
    """
    Worker: cảnh báo Action pending quá lâu
    """
    action = frappe.get_doc("Action", action_name)
    step_type = frappe.get_value("CampaignStep", action.campaign_step, "action_type")
    try:
        frappe.logger().warn(
            f"[Worker] ⚠️ Action {action.name} ({step_type}) "
            f"has been pending too long (since {action.scheduled_at})"
        )

        # Optionally: gửi email/notification cảnh báo
        # frappe.sendmail(...)

    except Exception as e:
        frappe.log_error(f"Error while checking pending Action {action.name}: {e}")
