# Copyright (c) 2025, MBWCloud Co. and contributors
# For license information, please see license.txt

import frappe
from frappe.utils import nowdate,now_datetime
from frappe.model.document import Document
from mbw_mira.mbw_mira.doctype.mira_task_definition.mira_task_definition import create_task_definitions_from_event
from mbw_mira.workers import resume_event



class MiraInteraction(Document):

	def before_save(self):
		self.auto_tracking()

	def on_update(self):
		"""Tự động xử lý logic tương ứng với interaction_type"""

		if not self.talent_id:
			frappe.logger().warning(f"[Mira Interaction] Missing talent_id for {self.name}")
			return

		# Ánh xạ interaction_type → hàm xử lý
		self.interaction_handle()


	# AUTO TRACKING
	def auto_tracking(self):
		INTERACTION_SCORE = {
			"EMAIL_OPENED": 2,
			"ON_LINK_CLICK": 5,
			"EMAIL_REPLIED": 10,
			"PAGE_VISITED": 1,
			"FORM_SUBMITTED": 15,
			"APPLICATION_SUBMITTED": 30,
			"TEST_COMPLETED": 20,
			"INTERVIEW_CONFIRMED": 25,
			"FB_MESSAGE": 5,
			"FB_COMMENT": 3,
			"FB_REACTION": 1,
			"ZALO_MESSAGE": 5,
			"ZALO_CLICK": 3,
			"ZALO_FORM_SUBMITTED": 15,
			"CALL_COMPLETED": 10,
			"SMS_REPLIED": 4
		}
		now = now_datetime()

		# --- 1) Lần tương tác đầu tiên của Talent ---
		first_interaction = frappe.db.get_value(
			"Mira Interaction",
			{"talent_id": self.talent_id},
			"creation",
			order_by="creation asc"
		)

		# Nếu chưa có tương tác nào => đây là lần đầu
		if not first_interaction:
			self.first_interaction_at = now
		else:
			self.first_interaction_at = first_interaction

		# --- 2) Lấy tương tác trước đó để tính interval ---
		previous = frappe.db.get_value(
			"Mira Interaction",
			{
				"talent_id": self.talent_id,
				"name": ["!=", self.name]
			},
			"creation",
			order_by="creation desc"
		)

		if previous:
			self.previous_interaction_at = previous
		else:
			self.previous_interaction_at = self.first_interaction_at

		# --- 3) Tính Engagement Timeline (Days) ---
		timeline_days = (now - self.first_interaction_at).days
		self.engagement_timeline = timeline_days

		# --- 4) Gán điểm tương tác ---
		self.interaction_weight = INTERACTION_SCORE.get(self.interaction_type, 1)

		# --- 5) Tính tổng score tích lũy của Talent ---
		total_score = frappe.db.sql(
			"""
			SELECT SUM(interaction_weight)
			FROM `tabMira Interaction`
			WHERE talent_id = %s
			""",
			self.talent_id
		)[0][0] or 0

		self.engagement_score = total_score + self.interaction_weight

	# ==========================================================
	# ============== EMAIL HANDLERS =============================
	# ==========================================================

	def interaction_handler(self):
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
 
	def handle_email_sent(self):
		"""Ghi nhận khi gửi email thành công."""
		resume_event("email_sent", self.talent_id)
  
		# create_task_definitions_from_event(
		# 		event_trigger="ON_SEND_SUCCESS",
		# 		target_type="Mira Talent",
		# 		target_id=self.talent_id,
		# 		event_payload={"talent_id": self.talent_id}
		# 	)
			

	def handle_email_delivered(self):
		"""Ghi nhận khi email được gửi đến hộp thư người nhận."""
		pass

	def handle_email_bounced(self):
		"""Hard bounce – đánh dấu email invalid."""
		frappe.db.set_value("Mira Talent",self.talent_id,"email_id_invalid", 1)

	def handle_email_engagement(self):
		"""Email opened hoặc clicked."""
		self._update_talent_interaction("Quan tâm AI")
		resume_event("email_open", self.talent_id)
		# create_task_definitions_from_event(
		# 	event_trigger="ON_LINK_CLICK",
		# 	target_type="Mira Talent",
		# 	target_id=self.talent_id,
		# 	event_payload={"url": self.url}
		# )

	def handle_email_unsubscribe(self):
		"""Người dùng hủy đăng ký."""
		frappe.db.set_value("Mira Talent",self.talent_id,"email_opt_out", 1)

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

