# Copyright (c) 2025, MBWCloud Co. and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class Mira MiraInteraction(Document):
	pass

	def on_update(self):
		#Nếu có tương tác thì update trạng thái trong ứng viên
		if self.mira_interaction_type == 'EMAIL_CLICKED':
			frappe.db.set_value("Mira Prospect",self.talent_id,"status","ENGAGED")
			frappe.db.commit()





def create_mira_interaction(args):
	"""Tạo mira_interaction
		talent_id: str,
		mira_interaction_type: str,
		source_action: str = None,
		url: str = None,
		description: str = None,
	"""
	talent_id = args.get('talent_id')
	mira_interaction_type = args.get('mira_interaction_type')
	source_action = args.get('source_action',"")
	url = args.get('url', "")
	description = args.get('description',"")
	frappe.get_doc(
		{
			"doctype": "Mira MiraInteraction",
			"talent_id": talent_id,
			"mira_interaction_type": mira_interaction_type,
			"action": source_action,
			"url": url,
			"description": description,
		}
	).insert(ignore_permissions=True)
	frappe.db.commit()
