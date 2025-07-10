# Copyright (c) 2025, MBWCloud Co. and Contributors
# See license.txt

import frappe
from frappe.tests.utils import FrappeTestCase


class TestCandidateCampaign(FrappeTestCase):
	pass

	def test_duplicate_candidate_campaign(self):
		doc1 = frappe.get_doc({
			"doctype": "CandidateCampaign",
			"candidate_id": "CAN-2506-00005",
			"campaign_id": "CPG-250630-00011",
			"status": "ACTIVE"
		}).insert(ignore_permissions=True)

		with self.assertRaises(frappe.ValidationError):
			doc2 = frappe.get_doc({
				"doctype": "CandidateCampaign",
				"candidate_id": "CAN-2506-00005",
				"campaign_id": "CPG-250630-00011",
				"status": "ACTIVE"
			}).insert(ignore_permissions=True)
