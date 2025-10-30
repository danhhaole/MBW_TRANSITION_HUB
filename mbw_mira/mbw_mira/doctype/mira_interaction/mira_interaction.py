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

	# def on_update(self):
		
	# 	# Kiểm tra loại interaction cần quan tâm
	# 	if self.interaction_type not in ["EMAIL_OPENED", "EMAIL_CLICKED"]:
	# 		return

	# 	if not self.talent_id:
	# 		frappe.logger().warning(f"[Mira Interaction] Missing talent_id for {self.name}")
	# 		return

	# 	# Lấy bản ghi talent
	# 	talent = frappe.get_doc("Mira Talent", self.talent_id)

	# 	# --- Cập nhật last_interaction_date ---
	# 	talent.last_interaction_date = nowdate()

	# 	# --- Cập nhật interaction_notes ---
	# 	# Nếu có description, thêm vào ghi chú
	# 	note_entry = f"{nowdate()} - {self.interaction_type}"
	# 	if self.description:
	# 		note_entry += f": {self.description}"
	# 	note_entry += "\n"

	# 	# Ghép thêm vào interaction_notes cũ (nếu có)
	# 	old_notes = talent.interaction_notes or ""
	# 	talent.interaction_notes = old_notes + note_entry

	# 	# --- Cập nhật tags ---
	# 	existing_tags = set((talent.tags or "").split("\n"))  # tách theo dòng
	# 	new_tag = "Quan tâm AI"
	# 	if new_tag not in existing_tags:
	# 		existing_tags.add(new_tag)
	# 	# Gộp lại thành chuỗi (Frappe Select multi-line)
	# 	talent.tags = "\n".join([t for t in existing_tags if t.strip()])

	# 	# Lưu lại
	# 	talent.save(ignore_permissions=True)

	# 	frappe.logger().info(f"[Mira Interaction] Updated Talent {talent.name} for {self.interaction_type}")
	
	def on_update(self):
		"""Xử lý khi Interaction được cập nhật."""
		if not self.talent_id:
			frappe.logger().warning(f"[Mira Interaction] Missing talent_id for {self.name}")
			return

		# Map interaction_type -> function xử lý tương ứng
		handler_map = {
			"EMAIL_OPENED": self.handle_email_opened,
			"EMAIL_CLICKED": self.handle_email_clicked,
		}

		handler = handler_map.get(self.interaction_type)
		if handler:
			handler()  # gọi hàm xử lý tương ứng
		else:
			frappe.logger().info(f"[Mira Interaction] No handler for type {self.interaction_type}")

	# ==========================================================
	# ============== HANDLERS CHO TỪNG LOẠI TYPE ===============
	# ==========================================================

	def handle_email_opened(self):
		"""Xử lý khi Talent mở email nurturing."""
		self._update_talent_interaction("Quan tâm AI")

	def handle_email_clicked(self):
		"""Xử lý khi Talent click vào email nurturing."""
		self._update_talent_interaction("Quan tâm AI")

	# ==========================================================
	# ============== HÀM PHỤ DÙNG CHUNG ========================
	# ==========================================================

	def _update_talent_interaction(self, new_tag=None):
		"""Cập nhật chung cho Talent: last_interaction_date, notes, tags."""
		talent = frappe.get_doc("Mira Talent", self.talent_id)

		# --- Cập nhật last_interaction_date ---
		talent.last_interaction_date = nowdate()

		# --- Ghi chú interaction ---
		note_entry = f"{nowdate()} - {self.interaction_type}"
		if self.description:
			note_entry += f": {self.description}"
		note_entry += "\n"

		old_notes = talent.interaction_notes or ""
		talent.interaction_notes = old_notes + note_entry

		# --- Thêm tag mới (nếu có) ---
		if new_tag:
			existing_tags = set((talent.tags or "").split("\n"))
			if new_tag not in existing_tags:
				existing_tags.add(new_tag)
			talent.tags = "\n".join(t.strip() for t in existing_tags if t.strip())

		talent.save(ignore_permissions=True)
		frappe.logger().info(f"[Mira Interaction] Updated Talent {talent.name} for {self.interaction_type}")


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
