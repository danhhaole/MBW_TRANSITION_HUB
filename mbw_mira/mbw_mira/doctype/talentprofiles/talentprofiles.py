# Copyright (c) 2025, MBWCloud Co. and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class TalentProfiles(Document):
	pass

	def validate(self):
		# Check trùng talent_id,candidate_id
		self.validate_unique_talent_profiles()

	def validate_unique_talent_profiles(self):
		"""
		Kiểm tra xem đã tồn tại TalentProfiles với cùng
		talent_id + candidate_id (ngoại trừ chính nó) hay chưa.
		"""
		filters = {
			"email": self.email
		}

		existing = frappe.db.exists("TalentProfiles", filters)

		if existing and existing != self.name:
			frappe.throw(
            frappe._(
                "A TalentProfiles with Email <b>{0}</b> already exists: <a href='/app/TalentProfiles/{1}'>{1}</a>"
            ).format(self.email, existing),
            title=frappe._("Duplicate TalentProfiles"),
        )
