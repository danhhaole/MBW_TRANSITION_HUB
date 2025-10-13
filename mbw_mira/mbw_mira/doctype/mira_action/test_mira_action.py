# Copyright (c) 2025, MBWCloud Co. and Contributors
# See license.txt

import frappe
from frappe.tests.utils import FrappeTestCase


class TestMiraAction(FrappeTestCase):
	pass
	def test_duplicate_mira_action(self):
		doc1 = frappe.get_doc({
			"doctype": "MiraAction",
			"candidate_campaign_id": "CAN-CPG-250708-00144",
			"campaign_step": "CPG_STEP-250630-00012",
			"status": "SCHEDULED"
		}).insert(ignore_permissions=True)

		with self.assertRaises(frappe.ValidationError):
			doc2 = frappe.get_doc({
				"doctype": "MiraAction",
				"candidate_campaign_id": "CAN-CPG-250708-00144",
				"campaign_step": "CPG_STEP-250630-00012",
				"status": "SCHEDULED"
			}).insert(ignore_permissions=True)
