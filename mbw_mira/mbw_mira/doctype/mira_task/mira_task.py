# Copyright (c) 2025, MBWCloud Co. and contributors
# For license information, please see license.txt

from datetime import timedelta
import frappe
from frappe.model.document import Document
from frappe.utils import now_datetime
from frappe.utils.safe_exec import safe_eval
from mbw_mira.helpers.date_time import get_next_working_time

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
        scheduled_time = get_next_working_time()      
		
        # 4) Tạo task cho từng action
        for action in actions:
            if action.delay_minutes:
                scheduled_time = scheduled_time + timedelta(minutes=action.delay_minutes)
            try:
                task = frappe.get_doc({
					"doctype": "Mira Task",
					"subject": f"{event_trigger}_{action.action_type}",
					"related_type": target_type,
					"related_talent": target_id,
					"trigger_type": event_trigger,
					"trigger": trigger.name,
					"action": action.name,
					"action_type": action.action_type,
					"action_parameters": action.action_parameters,
					"flow":action.parent,
					"status": "Pending",
					"condition":action.condition,
					"order": action.order,
					"scheduled_at": scheduled_time
				})
                task.insert(ignore_permissions=True)
            except Exception as e:
                print(e)
                pass
        frappe.db.commit()
                

