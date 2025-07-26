# Copyright (c) 2025, MBWCloud Co. and contributors
# For license information, please see license.txt

import frappe
from frappe import _
from frappe.model.document import Document
from mbw_mira.utils import find_candidates_fuzzy


class TalentSegment(Document):
	pass

@frappe.whitelist()
def find_talentprofile_by_segment():
	data = frappe.local.form_dict or frappe.request.json
	if not data:
		frappe.throw(_("No data submitted"))
	try:
		# Lấy các trường chính
		segment_id = data.get("segment_id")
		min_score = data.get("min_score") or 50
		if not segment_id:
			frappe.throw(_("Segment required"))
			return []
		
		talent_profiles = find_candidates_fuzzy(None,segment_id,min_score)
		return talent_profiles
	except Exception as e:
		frappe.throw(_(f"Cannot find talentprofiles. Error {str(e)}"))
		return []