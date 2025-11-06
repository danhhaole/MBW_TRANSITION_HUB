import frappe
from frappe.utils import now_datetime
from datetime import timedelta

from mbw_mira.helpers.date_time import get_business_hours_schedule, get_user_timezone_string
from mbw_mira.mbw_mira.doctype.mira_task.mira_task import create_mira_task_from_event


def handle_start_flow(task):
    """
    START_FLOW: Khởi chạy 1 flow mới dựa trên action.next_flow
    """
    action = frappe.get_doc("Mira Flow Action", task.action_value)

    if not action.next_flow:
        frappe.log_error(
            f"START_FLOW missing next_flow in action {action.name}",
            "Mira START_FLOW"
        )
        task.status = "Failed"
        task.save(ignore_permissions=True)
        return

    # Target = cùng talent / applicant / pool với task hiện tại
    target_type = task.related_type
    target_id = task.related_talent

    # -> Xác định thời gian chạy
    user_timezone = get_user_timezone_string()
    scheduled_time = get_business_hours_schedule(user_timezone)

    if action.delay_minutes:
        scheduled_time = scheduled_time + timedelta(minutes=action.delay_minutes)


    # Gọi lại pipeline tạo task dựa trên flow mới
    create_mira_task_from_event(
        event_trigger="ON_FLOW_STARTED",
        target_type=target_type,
        target_id=target_id,
        event_payload={"source_task": task.name, "source_flow": task.flow}
    )

    # Đánh dấu task này hoàn thành
    task.status = "Completed"
    task.completed_at = now_datetime()
    task.save(ignore_permissions=True)
