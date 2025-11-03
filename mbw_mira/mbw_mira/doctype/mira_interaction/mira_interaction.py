# Copyright (c) 2025, MBWCloud Co. and contributors
# For license information, please see license.txt

import frappe
from frappe.utils import nowdate
from frappe.model.document import Document


class MiraInteraction(Document):
	pass

	# def on_update(self):
	# 	#Nếu có tương tác thì update trạng thái trong ứng viên
	# 	if self.interaction_type == 'EMAIL_CLICKED':
	# 		frappe.db.set_value("Mira Prospect",self.talent_id,"status","ENGAGED")
	# 		frappe.db.commit()

	def on_update(self):
		"""Tự động xử lý logic tương ứng với interaction_type"""

		if not self.talent_id:
			frappe.logger().warning(f"[Mira Interaction] Missing talent_id for {self.name}")
			return

		# Ánh xạ interaction_type → hàm xử lý
		HANDLER_MAP = {
			# === EMAIL related ===
			"EMAIL_SENT": self.handle_email_sent,
			"EMAIL_DELIVERED": self.handle_email_delivered,
			"EMAIL_BOUNCED": self.handle_email_bounced,
			"EMAIL_OPENED": self.handle_email_engagement,
			"EMAIL_CLICKED": self.handle_email_engagement,
			"EMAIL_UNSUBSCRIBED": self.handle_email_unsubscribe,
			"EMAIL_REPLIED": self.handle_email_replied,

			# === WEBSITE / CONTENT ===
			"PAGE_VISITED": self.handle_website_view,
			"DOWNLOAD_TRIGGERED": self.handle_website_view,

			# === FORM ===
			"FORM_SUBMITTED": self.handle_form_completed,

			# === CHAT ===
			"CHAT_STARTED": self.handle_chat_started,
			"CHAT_MESSAGE_SENT": self.handle_chat_message_sent,
			"CHAT_COMPLETED": self.handle_chat_completed,

			# === CALL ===
			"CALL_MISSED": self.handle_call_missed,
			"CALL_COMPLETED": self.handle_call_completed,

			# === SMS ===
			"SMS_SENT": self.handle_sms_sent,
			"SMS_DELIVERED": self.handle_sms_delivered,
			"SMS_REPLIED": self.handle_sms_replied,

			# === APPLICATION / TEST / INTERVIEW ===
			"APPLICATION_SUBMITTED": self.handle_status_change,
			"DOCUMENT_UPLOADED": self.handle_status_change,
			"TEST_STARTED": self.handle_test_started,
			"TEST_COMPLETED": self.handle_status_change,
			"INTERVIEW_CONFIRMED": self.handle_schedule_next_action,
			"INTERVIEW_RESCHEDULED": self.handle_schedule_next_action,
		}

		handler = HANDLER_MAP.get(self.interaction_type)
		if handler:
			handler()
		else:
			frappe.logger().info(f"[Mira Interaction] No handler found for {self.interaction_type}")

	# ==========================================================
	# ============== EMAIL HANDLERS =============================
	# ==========================================================

	def handle_email_sent(self):
		"""Ghi nhận khi gửi email thành công."""
		pass

	def handle_email_delivered(self):
		"""Ghi nhận khi email được gửi đến hộp thư người nhận."""
		pass

	def handle_email_bounced(self):
		"""Hard bounce – đánh dấu email invalid."""
		pass

	def handle_email_engagement(self):
		"""Email opened hoặc clicked."""
		self._update_talent_interaction("Quan tâm AI")

	def handle_email_unsubscribe(self):
		"""Người dùng hủy đăng ký."""
		pass

	def handle_email_replied(self):
		"""Người dùng phản hồi email."""
		pass

	# ==========================================================
	# ============== WEBSITE / CONTENT =========================
	# ==========================================================

	def handle_website_view(self):
		"""Talent xem nội dung (career page, blog, job description...)."""
		pass

	# ==========================================================
	# ============== FORM / REFERRAL / EVENT ===================
	# ==========================================================

	def handle_form_completed(self):
		"""Talent hoàn tất form (nurturing, sự kiện, khảo sát...)."""
		pass

	# ==========================================================
	# ============== CHAT HANDLERS ==============================
	# ==========================================================

	def handle_chat_started(self):
		"""Bắt đầu chat."""
		pass

	def handle_chat_message_sent(self):
		"""Tin nhắn trong chat."""
		pass

	def handle_chat_completed(self):
		"""Chat kết thúc."""
		pass

	# ==========================================================
	# ============== CALL HANDLERS ==============================
	# ==========================================================

	def handle_call_missed(self):
		"""Cuộc gọi bị nhỡ."""
		pass

	def handle_call_completed(self):
		"""Cuộc gọi hoàn tất."""
		pass

	# ==========================================================
	# ============== SMS HANDLERS ===============================
	# ==========================================================

	def handle_sms_sent(self):
		"""Gửi SMS."""
		pass

	def handle_sms_delivered(self):
		"""SMS đến người nhận."""
		pass

	def handle_sms_replied(self):
		"""Người nhận phản hồi SMS."""
		pass

	# ==========================================================
	# ============== APPLICATION / TEST / INTERVIEW =============
	# ==========================================================

	def handle_status_change(self):
		"""Ứng viên thay đổi trạng thái hồ sơ (apply, upload doc, test done...)."""
		pass

	def handle_test_started(self):
		"""Bắt đầu làm bài test."""
		pass

	def handle_schedule_next_action(self):
		"""Đặt lịch hoặc thay đổi lịch phỏng vấn."""
		pass

	# ==========================================================
	# ============== HÀM DÙNG CHUNG =============================
	# ==========================================================

	def _update_talent_interaction(self, new_tag=None):
		"""Cập nhật cơ bản cho Mira Talent (notes, tags, last_interaction_date)."""
		talent = frappe.get_doc("Mira Talent", self.talent_id)
		talent.last_interaction_date = nowdate()

		# Ghi chú interaction
		note_entry = f"{nowdate()} - {self.interaction_type}"
		if self.description:
			note_entry += f": {self.description}"
		note_entry += "\n"

		old_notes = talent.interaction_notes or ""
		talent.interaction_notes = old_notes + note_entry

		# Cập nhật tag
		if new_tag:
			existing_tags = set((talent.tags or "").split("\n"))
			if new_tag not in existing_tags:
				existing_tags.add(new_tag)
			talent.tags = "\n".join(t.strip() for t in existing_tags if t.strip())

		talent.save(ignore_permissions=True)
		frappe.logger().info(f"[Mira Interaction] Updated Talent {talent.name} ({self.interaction_type})")

def create_mira_interaction(args):
	"""Tạo mira_interaction
		talent_id: str,
		interaction_type: str,
		source_action: str = None,
		url: str = None,
		description: str = None,
	"""
	talent_id = args.get('talent_id')
	interaction_type = args.get('interaction_type')
	source_action = args.get('source_action',"")
	url = args.get('url', "")
	description = args.get('description',"")
	frappe.get_doc(
		{
			"doctype": "Mira Interaction",
			"talent_id": talent_id,
			"interaction_type": interaction_type,
			"action": source_action,
			"url": url,
			"description": description,
		}
	).insert(ignore_permissions=True)
	frappe.db.commit()
