# Copyright (c) 2025, MBWCloud Co. and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class Interaction(Document):
	pass

	def create_interaction(self,**kwargs):
		"""Tạo interaction
			candidate_id: str,
			interaction_type: str,
			source_action: str = None,
			url: str = None,
			description: str = None,
		"""
		candidate_id = kwargs.get('candidate_id')
		interaction_type = kwargs.get('interaction_type')
		source_action = kwargs.get('source_action')
		url = kwargs.get('url')
		description = kwargs.get('description')
		frappe.get_doc(
			{
				"doctype": self.doctype,
				"candidate_id": candidate_id,
				"interaction_type": interaction_type,
				"action": source_action,
				"url": url,
				"description": description,
			}
		).insert(ignore_permissions=True)
		frappe.db.commit()
