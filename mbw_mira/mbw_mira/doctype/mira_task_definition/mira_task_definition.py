# Copyright (c) 2025, MBWCloud Co. and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from mbw_mira.helpers.date_time import get_business_hours_schedule, get_user_timezone_string
from frappe.utils import now_datetime
from mbw_mira.mbw_mira.doctype.mira_task.mira_task import run_next_action
import json
class MiraTaskDefinition(Document):
    
    def validate(self):
        pass
def create_task_definitions_from_event(event_trigger, target_type, target_id, event_payload=None):
    """
    Hàm được gọi mỗi khi có sự kiện trong hệ thống:
    - talent update
    - add tag
    - email open
    - link click
    """

    triggers = frappe.get_all(
        "Mira Flow Trigger",
        filters={"trigger_type": event_trigger, "status": "ACTIVE"},
        fields=["name", "parent", "conditions"]
    )

    if not triggers:
        return

    for trg in triggers:

        # 0) Check flow đã chạy cho talent chưa (tránh tạo trùng)
        existing = frappe.db.exists(
            "Mira Task Definition",
            {
                "talent": target_id,
                "status": ["in", ["Pending", "Running", "Waiting Event"]]
            }
        )
        if existing:
            # Flow instance hiện tại vẫn đang chạy → không tạo mới
            continue

        # 1) Evaluate điều kiện
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

        # 2) Tạo Mira Task Definition runtime
        task_def = frappe.new_doc("Mira Task Definition")
        task_def.talent = target_id
        task_def.flow = trg.parent
        task_def.trigger_type = event_trigger
        task_def.created_from_event = json.dumps(event_payload) or "{}"
        task_def.status = "Pending"
        task_def.started_at = now_datetime()
        task_def.insert(ignore_permissions=True)

        # 3) Snapshot Flow Actions thành Runtime Actions
        generate_runtime_actions(task_def)

        # 4) Set Entry Action (step đầu)
        set_entry_action(task_def)

        # 5) Tạo Task đầu tiên (scheduled theo giờ hành chính)
        run_next_action(task_def.name)

    frappe.db.commit()


        
def generate_runtime_actions(task_def):
    # Lấy danh sách action từ Flow Action (kịch bản)
    flow_actions = frappe.get_all(
        "Mira Flow Action",
        filters={"parent": task_def.flow},
        fields=["name", "action_type", "channel_type", "action_parameters", "delay_minutes", "'order' as order_no"],
        order_by="order_no asc"
    )

    if not flow_actions:
        frappe.throw(f"No Flow Actions found for Flow {task_def.flow}")

    runtime_map = {}   # map FlowAction → RuntimeRowName
    runtime_rows = []  # giữ runtime row theo thứ tự để chain

    # 1) Snapshot vào Mira Task Definition Action
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
        runtime_map[fa.name] = row.name
        runtime_rows.append(row)

    task_def.save(ignore_permissions=True)
    task_def.reload()

    # 2) Gán next_action_id dựa theo order_no (step chain)
    runtime_rows = sorted(task_def.task_actions, key=lambda x: x.order_no)

    for idx, row in enumerate(runtime_rows):
        if idx < len(runtime_rows) - 1:
            row.next_action_id = runtime_rows[idx + 1].name
        else:
            row.next_action_id = None  # step cuối không có next

    task_def.save(ignore_permissions=True)

    return task_def




def set_entry_action(task_def):
    entry = sorted(task_def.task_actions, key=lambda x: x.order_no)[0]
    task_def.current_action = entry.name
    task_def.status = "Running"
    task_def.save(ignore_permissions=True)




