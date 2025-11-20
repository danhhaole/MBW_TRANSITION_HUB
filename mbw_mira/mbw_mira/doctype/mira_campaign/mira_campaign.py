# Copyright (c) 2025, MBWCloud Co. and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class MiraCampaign(Document):
	pass

	def on_update(self):
		old_doc = self.get_doc_before_save()
		if old_doc.status != self.status:
			self.update_status_social()

	def update_status_social(self):
		is_active = 0
		if self.status == 'ACTICE':
			is_active =1
		else:
			is_active = 0
		social_campaign = frappe.get_all("Mira Campaign Social",{"campaign_id":self.name},pluck='name')
		if social_campaign:
			for scp in social_campaign:
				frappe.db.set_value("Mira Campaign Social",scp.name,"is_active", is_active)

			frappe.db.commit()