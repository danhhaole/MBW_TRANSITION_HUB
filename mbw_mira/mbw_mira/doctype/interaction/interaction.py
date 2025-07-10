# Copyright (c) 2025, MBWCloud Co. and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class Interaction(Document):
	pass

def create_interaction(args):
	"""Tạo interaction
		candidate_id: str,
		interaction_type: str,
		source_action: str = None,
		url: str = None,
		description: str = None,
	"""
	candidate_id = args.get('candidate_id')
	interaction_type = args.get('interaction_type')
	source_action = args.get('source_action',"")
	url = args.get('url', "")
	description = args.get('description',"")
	frappe.get_doc(
		{
			"doctype": "Interaction",
			"candidate_id": candidate_id,
			"interaction_type": interaction_type,
			"action": source_action,
			"url": url,
			"description": description,
		}
	).insert(ignore_permissions=True)
	frappe.db.commit()
