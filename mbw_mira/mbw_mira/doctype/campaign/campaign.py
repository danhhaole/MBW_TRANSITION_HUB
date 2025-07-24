# Copyright (c) 2025, MBWCloud Co. and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe.utils import now, now_datetime, add_days
from mbw_mira.utils import find_candidates_fuzzy

class Campaign(Document):
    pass

    def on_update(self):
        #Kiểm tra nếu có campaign_steps = [];
        if self.campaign_steps and isinstance(self.campaign_steps, dict):
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
            if step.campaign_step_name:
                campaign_step =frappe.get_doc({
                    "doctype": "CampaignStep",
                    "campaign_step_name": step.campaign_step_name,
                    "campaign": campaign_name,
                    "step_order": int(step.step_order),
                    "action_type": step.action_type,
                    "delay_in_days": int(step.delay_in_days),
                    "template": step.template_content,
                    "action_config": step.action_config  # optional: nếu muốn phân công tự động
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