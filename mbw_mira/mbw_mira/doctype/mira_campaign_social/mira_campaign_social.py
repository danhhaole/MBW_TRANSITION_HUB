# Copyright (c) 2025, MBWCloud Co. and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class MiraCampaignSocial(Document):

	def before_save(self):
		# Nếu không có post_schedule_time thì lấy từ campaign
		if not self.post_schedule_time:
			start_date = frappe.db.get_value("Mira Campaign",self.campaign_id,"start_date")
			if start_date:
				self.post_schedule_time = start_date

	def on_update(self):
		#Đếm social update vào campaign
		self._count_total_social_step_campaign()
		#Nếu Social thực hiện thì update trạng thái campaign
		if self.has_value_changed("executed_at") and self.executed_at:
			self._update_status_campaign()

	def after_delete(self):
		#Đếm lại social nếu bị xóa
		self._count_total_social_step_campaign()

	def _count_total_social_step_campaign(self):
		total = frappe.db.count("Mira Campaign Social",{"campaign_id":self.campaign_id})
		#Set lại tổng trong campaign
		frappe.db.set_value("Mira Campaign",self.campaign_id,"total",total)
		frappe.db.commit()
	
	def _update_status_campaign(self):
		campaign = frappe.get_doc("Mira Campaign",self.campaign_id)
		campaign.current = campaign.current + 1
		campaign.save(ignore_permissions=True)
		frappe.db.commit()



