# Copyright (c) 2025, MBWCloud Co. and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe.utils import now_datetime

class Action(Document):
	pass

	def on_update(self):
		"""Khi có event update xử lý các luồng
		"""
		pass

def create_action(self, **kwargs):
	"""Tạo action từ CandidateCampaign và lấy step từ CampaignStep
	- candidate_campaign_id
	- campaign_step
	- status_action
	"""
	campaign_step = kwargs.get('campaign_step')
	candidate_campaign_id = kwargs.get('candidate_campaign_id')
	status_action = kwargs.get('status_action')
	frappe.get_doc(
		{
			"doctype": self.doctype,
			"candidate_campaign_id": candidate_campaign_id,
			"campaign_step": campaign_step,
			"status": status_action,
			"scheduled_at": now_datetime()
		}
	).insert(ignore_permissions=True)
	frappe.db.commit()

	
		
