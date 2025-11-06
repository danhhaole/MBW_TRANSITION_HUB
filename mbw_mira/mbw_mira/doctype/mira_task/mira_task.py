# Copyright (c) 2025, MBWCloud Co. and contributors
# For license information, please see license.txt

from datetime import timedelta
import frappe
from frappe.model.document import Document
from frappe.utils import now_datetime,add_to_date
from mbw_mira.helpers.date_time import get_user_timezone_string,get_business_hours_schedule
from mbw_mira.mbw_mira.doctype.mira_task_definition.mira_task_definition import run_next_action

class MiraTask(Document):
	
	def validate(self):
		if self.related_talent:
			exists_talent = frappe.db.exists("Mira Talent",{"related_talent":self.related_talent})
			if exists_talent:
				frappe.throw("Talent exists")
def create_mira_task_from_event(event_trigger: str, target_type: str, target_id: str, event_payload=None):
    """
    event_trigger  = ON_CREATE, ON_UPDATE, ON_LINK_CLICK, ...
    target_type    = Talent | Talent Pool | Applicant | Campaign
    target_id      = name of the record (Talent-0001)
    event_payload  = dict (data đi kèm nếu cần kiểm tra điều kiện)
    """
    # Prevent re-trigger same flow from itself
    if event_trigger == "ON_FLOW_STARTED" and event_payload and event_payload.get("source_flow") == trigger.parent:
        return
    # 1) Tìm danh sách trigger phù hợp
    triggers = frappe.get_all(
        "Mira Flow Trigger",
        filters={
            "trigger_type": event_trigger,
            "target_type": target_type,
            "status": "ACTIVE"
        },
        fields=["name", "parent", "conditions"]
    )
    
    if not triggers:
        return

    for trigger in triggers:
        # 2) Evaluate conditions (nếu có)
        
        if trigger.conditions:
            try:
                ctx = {"doc": event_payload or {}, "frappe": frappe}
                
                # if not safe_eval(trigger.conditions, ctx):
                #     continue
                
            except:
                frappe.log_error("Trigger condition evaluation failed", trigger.name)
                # continue
       
        # 3) Lấy action thuộc flow
        actions = frappe.get_all(
            "Mira Flow Action",
            filters={"parent": trigger.parent},
            fields=[
                "name", "action_type", "channel_type", "action_parameters",
                "delay_minutes", "next_flow", "sequence", "'order' as sort_order"
            ],
            order_by="sort_order asc"
        )
        user_timezone = get_user_timezone_string()
        scheduled_time = get_business_hours_schedule(user_timezone)
        # print("actions",actions)      
		
        # 4) Tạo task cho từng action
        for action in actions:
            if action.delay_minutes:
                scheduled_time = (scheduled_time + timedelta(minutes=action.delay_minutes))
            try:
                task = frappe.get_doc({
					"doctype": "Mira Task",
					"subject": f"{event_trigger}_{action.action_type}",
					"related_type": target_type,
					"related_talent": target_id,
					"trigger_type": event_trigger,
					"trigger": trigger.name,
					"action_value": action.next_flow,
					"action_type": action.action_type,
					"flow":action.parent,
					"status": "Pending",
					"condition":action.action_parameters,
					"order": action.order,
					"scheduled_at": scheduled_time
				})
                task.insert(ignore_permissions=True)
                print('scheduled_at',scheduled_time)
            except Exception as e:
                frappe.log_error("Lỗi lưu Task",str(e))
                print(e)
                pass
        frappe.db.commit()
                

def complete_action(task_name, success=True, error_message=None):
    task = frappe.get_doc("Mira Task", task_name)
    task_definition = frappe.get_doc("Mira Task Definition", task.task_definition)

    # Tìm runtime action tương ứng trong child table
    action = None
    for a in task_definition.task_actions:
        if a.task_id == task.name:
            action = a
            break

    if not action:
        frappe.throw(f"Runtime action for task {task.name} not found")

    # Cập nhật trạng thái task runtime
    if success:
        task.status = "Completed"
        task.executed_at = now_datetime()
        task.save(ignore_permissions=True)
        action.status = "Completed"
    else:
        task.status = "Failed"
        task.error_log = error_message or "Unknown error"
        task.executed_at = now_datetime()
        task.save(ignore_permissions=True)
        action.status = "Failed"
        task_definition.status = "Failed"
        task_definition.completed_at = now_datetime()
        task_definition.save(ignore_permissions=True)
        frappe.db.commit()
        return  # dừng flow

    # Nếu action cần chờ event → chuyển sang trạng thái chờ, không chạy tiếp
    if action.trigger_event and action.trigger_event != "none":
        action.status = "Waiting Event"
        task_definition.status = "Waiting Event"
        task_definition.save(ignore_permissions=True)
        frappe.db.commit()
        return  # Dừng flow ở đây → resume khi event đến

    # Nếu có next action → chuyển tiếp
    if action.next_action_id:
        task_definition.current_action = action.next_action_id
        task_definition.status = "Running"
        task_definition.save(ignore_permissions=True)

        frappe.db.commit()

        # Gọi engine để chạy step tiếp theo
        run_next_action(task_definition.name)

        return

    # Nếu không có action tiếp theo → flow kết thúc
    task_definition.status = "Completed"
    task_definition.completed_at = now_datetime()
    task_definition.save(ignore_permissions=True)
    frappe.db.commit()
    
@frappe.whitelist()
def create_task_for_action(task_definition_name, action):
    task = frappe.new_doc("Mira Task")
    task.subject = f"{action.action_type} - {task_definition_name}"
    task.task_definition = task_definition_name
    task.flow_action = action.flow_action_id
    task.related_talent = frappe.db.get_value("Mira Task Definition", task_definition_name, "talent")
    task.action_type = action.action_type
    task.status = "Pending"
    task.insert(ignore_permissions=True)

    action.task_id = task.name
    action.save(ignore_permissions=True)

    return task
