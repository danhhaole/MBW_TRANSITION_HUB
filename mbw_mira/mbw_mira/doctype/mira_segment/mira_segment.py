# Copyright (c) 2025, MBWCloud Co. and contributors
# For license information, please see license.txt

import json
import frappe
from frappe import _
from frappe.model.document import Document
from mbw_mira.mbw_mira.doctype.mira_pool_vecto.mira_pool_vecto import insert_mira_pool_vecto,update_mira_pool_vecto
from mbw_mira.utils import find_candidates_fuzzy


class MiraSegment(Document):

	def after_insert(self):
		insert_mira_pool_vecto(self.name)

	def on_update(self):
		if not self.flags.in_insert:
			try:
				update_mira_pool_vecto(self.name,self.as_dict())
				# meta_fields =  self.meta.fields
				# old_doc = self.get_doc_before_save()
				# field_update = None
				# if meta_fields:
				# 	for field in meta_fields:
				# 		changed_fields = self.has_value_changed(field.fieldname)
				# 		if changed_fields and hasattr(old_doc,field.fieldname):
				# 			new = self.get(field.fieldname)
							
				# 			field_update.update({field.fieldname,new})
				# if field_update:
				# 	update_mira_pool_vecto(self.name,field_update)
			except Exception as e:
				print(str(e))          


@frappe.whitelist()
def find_talentprofile_by_segment():
	data = frappe.local.form_dict or frappe.request.json
	if not data:
		frappe.throw(_("No data submitted"))
	try:
		# Lấy các trường chính
		segment_id = data.get("segment_id")
		min_score = data.get("min_score")
		if not segment_id:
			frappe.throw(_("Segment required"))
			return []
		
		talent_profiles = find_candidates_fuzzy(None,segment_id,min_score)
		return talent_profiles
	except Exception as e:
		frappe.throw(_(f"Cannot find talentprofiles. Error {str(e)}"))
		return []