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

			# Không gửi tracking email khi ACTIVE - chỉ log
			if self.status == 'ACTIVE':
				frappe.logger("campaign").info(f"📋 Campaign {self.name} activated - tracking emails disabled")

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

	def trigger_tracking_emails(self):
		"""
		Gửi tracking email cho tất cả ứng viên trong campaign khi campaign chuyển sang ACTIVE
		"""
		try:
			frappe.logger("campaign").info(f"🚀 [AUTO-TRIGGER] Starting tracking emails for campaign {self.name}")

			# Gọi hàm gửi tracking email
			from mbw_mira.api.email_tracking_test import test_send_tracked_email_to_pool
			result = test_send_tracked_email_to_pool(
				target_pool=self.target_pool,
				subject=f"Chào mừng bạn tham gia chiến dịch {self.campaign_name}",
				content=f"""
Xin chào,

Chúng tôi rất vui mừng thông báo bạn đã được chọn tham gia chiến dịch "{self.campaign_name}".

Đây là email tracking để theo dõi mức độ quan tâm của bạn đối với chiến dịch này.

Nếu bạn không tương tác với email này trong vòng 1 phút, hệ thống sẽ tự động dừng gửi email tiếp theo để tôn trọng sự riêng tư của bạn.

Trân trọng,
MOBIWORK Team
"""
			)

			frappe.logger("campaign").info(f"✅ [AUTO-TRIGGER] Tracking email result: {result}")

		except Exception as e:
			frappe.logger("campaign").error(f"❌ [AUTO-TRIGGER] Error sending tracking emails: {str(e)}")

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
