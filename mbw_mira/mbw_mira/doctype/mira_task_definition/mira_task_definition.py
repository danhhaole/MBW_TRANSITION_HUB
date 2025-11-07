# Copyright (c) 2025, MBWCloud Co. and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from mbw_mira.helpers.date_time import get_business_hours_schedule, get_user_timezone_string
from frappe.utils import now_datetime
from mbw_mira.mbw_mira.doctype.mira_task.mira_task import run_next_action

class MiraTaskDefinition(Document):
	pass
def create_task_definitions_from_event(event_trigger, target_type, target_id, event_payload=None):
    """
    Hàm được gọi mỗi khi có sự kiện trong hệ thống:
    - talent update
    - add tag
    - email open
    - link click
    """

    # Tìm Flow Trigger tương ứng với event
    triggers = frappe.get_all(
        "Mira Flow Trigger",
        filters={"trigger_type": event_trigger, "status": "ACTIVE"},
        fields=["name", "flow_id", "conditions"]
    )

    if not triggers:
        return

    for trg in triggers:

        # Evaluate điều kiện (nếu có)
        if trg.conditions:
            ctx = {
                "record": frappe.get_doc(target_type, target_id),
                "payload": event_payload
            }
            try:
                if not eval(trg.conditions, {}, ctx):
                    continue
            except Exception:
                frappe.log_error(f"Invalid condition in Flow Trigger {trg.name}", "Flow Condition Error")
                continue

        # 1) Tạo Mira Task Definition runtime
        task_def = frappe.new_doc("Mira Task Definition")
        task_def.talent = target_id
        task_def.flow = trg.flow_id
        task_def.trigger_type = event_trigger
        task_def.created_from_event = event_payload or {}
        task_def.status = "Pending"
        task_def.started_at = now_datetime()
        task_def.insert(ignore_permissions=True)

        # 2) Tạo runtime actions (snapshot từ Flow Action)
        generate_runtime_actions(task_def)

        # 3) Xác định action đầu (entry point)
        set_entry_action(task_def)

        # 4)  Tạo Task đầu tiên theo entry action
        run_next_action(task_def.name)

        frappe.db.commit()

        
def generate_runtime_actions(task_def):
    # Lấy danh sách action từ Flow Action
    flow_actions = frappe.get_all(
        "Mira Flow Action",
        filters={"flow_id": task_def.flow},
        fields=["name", "action_type", "channel_type", "action_parameters", "delay_minutes", "order_no", "next_action_id"],
        order_by="order_no asc"
    )

    # Map giữ tương ứng Flow Action → Runtime child row
    action_map = {}

    # 1) Tạo runtime actions (snapshot)
    for fa in flow_actions:
        row = task_def.append("task_actions", {
            "flow_action_id": fa.name,
            "action_type": fa.action_type,
            "channel_type": fa.channel_type,
            "action_parameters": fa.action_parameters,
            "delay_minutes": fa.delay_minutes or 0,
            "order_no": fa.order_no or 0,
            "trigger_event": "none",
            "status": "Pending"
        })
        action_map[fa.name] = row.name  # lưu tên runtime row

    task_def.save(ignore_permissions=True)

    # 2) Gán next_action_id
    task_def.reload()

    for action_row in task_def.task_actions:
        source_next = frappe.db.get_value("Mira Flow Action", action_row.flow_action_id, "next_action_id")
        if source_next and source_next in action_map:
            action_row.next_action_id = action_map[source_next]

    task_def.save(ignore_permissions=True)

    return task_def



def set_entry_action(task_def):
    entry = sorted(task_def.task_actions, key=lambda x: x.order_no)[0]
    task_def.current_action = entry.name
    task_def.status = "Running"
    task_def.save(ignore_permissions=True)




