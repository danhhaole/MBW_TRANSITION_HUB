# Copyright (c) 2025, MBWCloud Co. and contributors
# For license information, please see license.txt

import frappe
from frappe import _
from frappe.model.document import Document
from mbw_mira.mbw_mira.doctype.mira_talent_vecto.mira_talent_vecto import insert_mira_talent
from mbw_mira.utils import find_candidates_fuzzy


class MiraSegment(Document):

	def after_insert(self):
		insert_mira_talent(self)

	def on_update(self):
		if not self.flags.in_insert: 
			meta_fields =  self.meta.fields
			old_doc = self.get_doc_before_save()
			vecto_doc = frappe.get_doc("Mira Pool Vecto",{"talent_id":self.name})
			field_update = None
			if meta_fields:
				for field in meta_fields:
					changed_fields = self.has_value_changed(field.fieldname)
					if changed_fields and hasattr(old_doc,field.fieldname):
						new = self.get(field.fieldname)
      					
						vecto_doc.update()
      					
						
            



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