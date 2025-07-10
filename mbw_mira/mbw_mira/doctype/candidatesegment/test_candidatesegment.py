# Copyright (c) 2025, MBWCloud Co. and Contributors
# See license.txt

import frappe
from frappe.tests.utils import FrappeTestCase


class TestCandidateSegment(FrappeTestCase):
	pass

	def test_duplicate_candidate_segment(self):
			doc1 = frappe.get_doc({
				"doctype": "CandidateSegment",
				"candidate_id": "CAN-2506-00005",
				"segment_id": "SEG-250630-00006",
				"added_by": "Administrator"
			}).insert(ignore_permissions=True)

			with self.assertRaises(frappe.ValidationError):
				doc2 = frappe.get_doc({
					"doctype": "CandidateSegment",
					"candidate_id": "CAN-2506-00005",
					"segment_id": "SEG-250630-00006",
					"added_by": "Administrator"
				}).insert(ignore_permissions=True)