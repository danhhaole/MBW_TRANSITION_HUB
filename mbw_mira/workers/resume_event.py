import frappe
from frappe.utils import now_datetime
from mbw_mira.mbw_mira.doctype.mira_task.mira_task import create_task_for_action


def resume_event(event_type, talent_id, payload=None):
    """Resume a paused workflow step when trigger event occurs."""

    # Tìm tất cả Task Definition của Talent đang chờ event
    task_defs = frappe.get_all(
        "Mira Task Definition",
        filters={
            "talent": talent_id,
            "status": "Waiting Event"
        },
        fields=["name"]
    )

    if not task_defs:
        return  # Không có flow nào đang chờ event

    for td_row in task_defs:
        td = frappe.get_doc("Mira Task Definition", td_row.name)

        waiting_action = None
        for action in td.task_actions:
            if action.status == "Waiting Event" and action.trigger_event == event_type:
                waiting_action = action
                break

        if not waiting_action:
            continue  # Flow này không chờ event ta đang resume

        # Đánh dấu runtime action đã sẵn sàng chạy
        waiting_action.status = "Ready"
        td.current_action = waiting_action.name
        td.status = "Running"
        td.save(ignore_permissions=True)

        # Tạo task mới từ action
        task = create_task_for_action(td.name, waiting_action)
        task.scheduled_at = now_datetime()
        task.save(ignore_permissions=True)

        frappe.db.commit()

        # Để scheduler xử lý task đó
        frappe.logger().info(f"[Resume Event] Resumed {td.name} at action {waiting_action.name}")


    return True
