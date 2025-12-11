# Copyright (c) 2025, MBWCloud Co. and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class MiraCampaign(Document):
	pass

	def on_update(self):
		old_doc = self.get_doc_before_save()
		# self.notify_update()

		if hasattr(old_doc, 'status') and hasattr(self, 'status') and old_doc.status != self.status:

			self.update_status_social()

			# Gửi email khi campaign chuyển sang ACTIVE
			# Note: Email sending được gọi từ frontend (CampaignTable.vue) để tránh gửi 2 lần
			# if self.status == 'ACTIVE':
			#	self.trigger_campaign_emails()

	def update_status_social(self):
		is_active = 0
		if self.status == 'ACTIVE':
			is_active =1
		else:
			is_active = 0
		social_campaign = frappe.get_all("Mira Campaign Social",{"campaign_id":self.name},pluck='name')
		if social_campaign:
			for scp in social_campaign:
				frappe.db.set_value("Mira Campaign Social",scp,"is_active", is_active)

			frappe.db.commit()

	def trigger_campaign_emails(self):
		"""
		Gửi email cho tất cả ứng viên trong campaign khi campaign chuyển sang ACTIVE
		"""
		try:
			frappe.logger("campaign").info(f"🚀 [TRIGGER] Starting trigger_campaign_emails for {self.name}")

			# Gọi hàm gửi email trực tiếp
			from mbw_mira.api.campaign import send_campaign_welcome_emails
			result = send_campaign_welcome_emails(self.name)

			frappe.logger("campaign").info(f"✅ [TRIGGER] Email send result: {result}")

		except Exception as e:
			frappe.logger("campaign").error(f"❌ [TRIGGER] Error in trigger_campaign_emails: {str(e)}")
			import traceback
			frappe.logger("campaign").error(traceback.format_exc())
