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


@frappe.whitelist()
def delete_segment(name=None):
	"""
	Xóa một segment sau khi unlink các tham chiếu
	
	Args:
		name: Tên của Mira Segment document cần xóa (từ request body)
	
	Returns:
		dict: Kết quả thực hiện
	"""
	try:
		# Lấy data từ request nếu không có name
		if not name:
			data = frappe.local.form_dict
			name = data.get("name")
		
		if not name:
			return {
				"status": "error",
				"message": _("Segment name is required")
			}
		
		# Kiểm tra document có tồn tại không
		if not frappe.db.exists("Mira Segment", name):
			return {
				"status": "error",
				"message": _("Segment {0} does not exist").format(name)
			}
		
		# Load document
		doc = frappe.get_doc("Mira Segment", name)
		
		# Kiểm tra quyền xóa
		if not frappe.has_permission("Mira Segment", "delete", doc=doc):
			frappe.throw(_("No permission to delete Segment {0}").format(name))
		
		# Lấy meta để kiểm tra links
		meta = frappe.get_meta("Mira Segment")
		
		# Kiểm tra và unlink các tham chiếu
		unlink_segment_references(doc, meta)
		
		# Sau khi unlink, xóa segment
		frappe.delete_doc("Mira Segment", name, force=0, ignore_permissions=False)
		
		frappe.db.commit()
		
		return {
			"status": "success",
			"message": _("Segment {0} deleted successfully").format(name)
		}
		
	except Exception as e:
		frappe.db.rollback()
		frappe.log_error(message=frappe.get_traceback(), title=f"Delete Segment Error: {name}")
		return {
			"status": "error",
			"message": str(e)
		}


def unlink_segment_references(doc, meta):
	"""
	Unlink tất cả các tham chiếu của segment trước khi xóa
	
	Args:
		doc: Mira Segment document
		meta: Meta object của Mira Segment
	"""
	try:
		# Lấy danh sách các doctype có link đến Mira Segment
		linked_doctypes = get_segment_linked_doctypes(meta)
		
		if not linked_doctypes:
			return
		
		# Duyệt qua từng doctype có link
		for link_info in linked_doctypes:
			doctype = link_info.get("parent")
			fieldname = link_info.get("fieldname")
			
			if not doctype or not fieldname:
				continue
			
			# Xử lý đặc biệt cho Mira Pool Vecto (required field - cần xóa)
			if doctype == "Mira Pool Vecto" and fieldname == "mira_segment":
				# Tìm và xóa các Mira Pool Vecto liên quan
				pool_vecto_docs = frappe.get_all(
					"Mira Pool Vecto",
					filters={fieldname: doc.name},
					fields=["name"]
				)
				
				for pool_doc in pool_vecto_docs:
					try:
						frappe.delete_doc("Mira Pool Vecto", pool_doc.name, ignore_permissions=True, force=True)
					except Exception as e:
						frappe.log_error(
							message=frappe.get_traceback(),
							title=f"Delete Pool Vecto Error: {pool_doc.name}"
						)
						continue
				continue
			
			# Tìm các document tham chiếu đến segment này (optional fields)
			linked_docs = frappe.get_all(
				doctype,
				filters={fieldname: doc.name},
				fields=["name"]
			)
			
			# Unlink từng document
			for linked_doc in linked_docs:
				try:
					ref_doc = frappe.get_doc(doctype, linked_doc.name)
					
					# Kiểm tra quyền write
					if not frappe.has_permission(doctype, "write", doc=ref_doc):
						continue
					
					# Set field về None/empty để unlink
					ref_doc.set(fieldname, None)
					ref_doc.flags.ignore_validate = True
					ref_doc.flags.ignore_mandatory = True
					ref_doc.save(ignore_permissions=False)
					
				except Exception as e:
					frappe.log_error(
						message=frappe.get_traceback(),
						title=f"Unlink Error: {doctype} - {linked_doc.name}"
					)
					continue
					
	except Exception as e:
		frappe.log_error(
			message=frappe.get_traceback(),
			title=f"Unlink Segment References Error: {doc.name}"
		)
		raise


def get_segment_linked_doctypes(meta):
	"""
	Lấy danh sách các doctype có link field trỏ đến Mira Segment
	
	Args:
		meta: Meta object
		
	Returns:
		list: Danh sách các doctype có link
	"""
	linked_doctypes = []
	
	# Tìm trong DocField
	links = frappe.get_all(
		"DocField",
		filters={
			"fieldtype": "Link",
			"options": meta.name
		},
		fields=["parent", "fieldname"]
	)
	
	linked_doctypes.extend(links)
	
	# Tìm trong Custom Field
	custom_links = frappe.get_all(
		"Custom Field",
		filters={
			"fieldtype": "Link",
			"options": meta.name
		},
		fields=["dt as parent", "fieldname"]
	)
	
	linked_doctypes.extend(custom_links)
	
	return linked_doctypes


@frappe.whitelist()
def check_segment_links(name=None):
	"""
	Kiểm tra các link references của một segment
	
	Args:
		name: Tên của Mira Segment (từ request body)
		
	Returns:
		dict: Danh sách các tham chiếu
	"""
	try:
		# Lấy data từ request nếu không có name
		if not name:
			data = frappe.local.form_dict
			name = data.get("name")
		
		if not name:
			return {
				"status": "error",
				"message": _("Segment name is required")
			}
		
		if not frappe.db.exists("Mira Segment", name):
			return {
				"status": "error",
				"message": _("Segment {0} does not exist").format(name)
			}
		
		doc = frappe.get_doc("Mira Segment", name)
		meta = frappe.get_meta("Mira Segment")
		
		linked_doctypes = get_segment_linked_doctypes(meta)
		
		references = []
		for link_info in linked_doctypes:
			doctype = link_info.get("parent")
			fieldname = link_info.get("fieldname")
			
			if not doctype or not fieldname:
				continue
			
			linked_docs = frappe.get_all(
				doctype,
				filters={fieldname: doc.name},
				fields=["name", "modified"],
				limit=100
			)
			
			if linked_docs:
				references.append({
					"doctype": doctype,
					"fieldname": fieldname,
					"count": len(linked_docs),
					"documents": [d.name for d in linked_docs]
				})
		
		return {
			"status": "success",
			"segment": name,
			"has_references": len(references) > 0,
			"references": references
		}
		
	except Exception as e:
		frappe.log_error(
			message=frappe.get_traceback(),
			title=f"Check Segment Links Error: {name}"
		)
		return {
			"status": "error",
			"message": str(e)
		}