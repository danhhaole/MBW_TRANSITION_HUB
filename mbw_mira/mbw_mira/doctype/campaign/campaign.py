# Copyright (c) 2025, MBWCloud Co. and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class Campaign(Document):
    pass

    def on_update(self):
        #Kiểm tra nếu có campaign_steps = [];
        if hasattr(self, 'campaign_steps'):
            insert_campaign_step(self.campaign_steps,self.name)
    def on_trash(self):
        #Kiểm tra trạng thái là draff hoặc chưa active 
        if self.status == "DRAFT" or not self.is_active:
            #Kiểm tra xem có step chưa để xóa CampaignStep trước
            pass

def insert_campaign_step(steps,campaign_name):
    """_summary_

    Args:
         "campaign_step_name",
        "campaign",
        "step_order",
        "action_type",
        "delay_in_days",
        "template",
        "action_config"
    """
    try:
        step_name =[]
        for step in steps:
            if step.get("campaign_step_name"):
                campaign_step =frappe.get_doc({
                    "doctype": "CampaignStep",
                    "campaign_step_name": step.get("campaign_step_name"),
                    "campaign": campaign_name,
                    "step_order": int(step.get("step_order")),
                    "action_type": step.get("action_type"),
                    "delay_in_days": int(step.get("delay_in_days")),
                    "template": step.get("template_content"),
                    "action_config": step.get("action_config")  # optional: nếu muốn phân công tự động
                })
                campaign_step.insert(ignore_permissions=True)
                frappe.db.commit()
                step_name.append(campaign_step.name)
        return step_name            
    except Exception as e:
        frappe.log_error(f"Lỗi {str(e)}")
        return None


def delete_campaign_step():
    pass