# Copyright (c) 2025, MBWCloud Co. and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class CampaignStep(Document):
	pass

	def after_insert(self):
		if self.campaign:
			update_total_campaign_step(self)

	
	def after_delete(self):
		if self.campaign:
			update_total_campaign_step(self)

def update_total_campaign_step(self):
	campaign = frappe.get_doc("Campaign",self.campaign)
	total_step = frappe.db.count("CampaignStep",{"campaign":self.campaign})
	campaign.update({
		"total":total_step
    })
	campaign.save(ignore_permissions=True)
	frappe.db.commit()