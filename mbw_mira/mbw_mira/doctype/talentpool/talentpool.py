# Copyright (c) 2025, MBWCloud Co. and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class TalentPool(Document):
	pass

	def validate(self):
		if frappe.db.exists("TalentPool", {"email": self.email, "name": ["!=", self.name]}):
			frappe.throw(f"Email {self.email} đã tồn tại trong TalentPool.")
