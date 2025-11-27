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


@frappe.whitelist()
def calculate_segment_engagement_rate(segment_id=None, max_expected_score=None):
	"""
	Tính Engagement Rate thực tế cho segment dựa trên:
	- Mira Talent Pool: segment_id -> talent_id
	- Mira Interaction: talent_id -> engagement_score
	
	Args:
		segment_id: ID của Mira Segment
		max_expected_score: Điểm tối đa dự kiến cho 1 talent (để normalize)
		
	Returns:
		dict: Engagement rate và thống kê chi tiết
	"""
	try:
		if not segment_id:
			data = frappe.local.form_dict
			segment_id = data.get("segment_id")
			max_expected_score = data.get("max_expected_score")
		
		if not segment_id:
			return {
				"status": "error",
				"message": _("Segment ID is required")
			}
		
		# Kiểm tra segment có tồn tại không
		if not frappe.db.exists("Mira Segment", segment_id):
			return {
				"status": "error",
				"message": _("Segment {0} does not exist").format(segment_id)
			}
		
		# Lấy danh sách talent trong segment
		talent_pool = frappe.get_all("Mira Talent Pool",
			filters={"segment_id": segment_id},
			fields=["talent_id"]
		)
		
		if not talent_pool:
			return {
				"status": "success",
				"engagement_rate": 0,
				"total_talents": 0,
				"total_interactions": 0,
				"total_engagement_score": 0,
				"average_score_per_talent": 0,
				"talents_with_interactions": 0
			}
		
		talent_ids = [pool.talent_id for pool in talent_pool]
		total_talents = len(talent_ids)
		
		# Lấy tất cả interactions của các talent trong segment
		interactions = frappe.get_all("Mira Interaction",
			filters={"talent_id": ["in", talent_ids]},
			fields=["talent_id", "engagement_score", "interaction_type", "creation"]
		)
		
		# Tính toán thống kê
		total_interactions = len(interactions)
		total_engagement_score = sum(interaction.engagement_score or 0 for interaction in interactions)
		
		# Đếm số talent có ít nhất 1 interaction
		talents_with_interactions = len(set(interaction.talent_id for interaction in interactions))
		
		# Tính engagement rate theo 2 công thức
		# Công thức 1: (Số talent có tương tác / Tổng số talent) * 100
		engagement_rate_by_participation = (talents_with_interactions / total_talents * 100) if total_talents > 0 else 0
		
		# Công thức 2: (Tổng điểm engagement / Tổng số talent) - normalized to percentage
		average_score_per_talent = (total_engagement_score / total_talents) if total_talents > 0 else 0
		
		# Normalize average score to percentage
		# Use provided max_expected_score or default to 100
		max_expected_score_per_talent = float(max_expected_score) if max_expected_score else 100.0
		engagement_rate_by_score = min(100, (average_score_per_talent / max_expected_score_per_talent * 100)) if max_expected_score_per_talent > 0 else 0
		
		# Combined engagement rate (weighted average of both methods)
		engagement_rate = (engagement_rate_by_participation * 0.6 + engagement_rate_by_score * 0.4)
		
		# Thống kê theo loại interaction
		interaction_stats = {}
		for interaction in interactions:
			interaction_type = interaction.interaction_type
			if interaction_type not in interaction_stats:
				interaction_stats[interaction_type] = {
					"count": 0,
					"total_score": 0
				}
			interaction_stats[interaction_type]["count"] += 1
			interaction_stats[interaction_type]["total_score"] += interaction.engagement_score or 0
		
		return {
			"status": "success",
			"engagement_rate": round(engagement_rate, 2),
			"engagement_rate_by_participation": round(engagement_rate_by_participation, 2),
			"engagement_rate_by_score": round(engagement_rate_by_score, 2),
			"total_talents": total_talents,
			"total_interactions": total_interactions,
			"total_engagement_score": total_engagement_score,
			"average_score_per_talent": round(average_score_per_talent, 2),
			"talents_with_interactions": talents_with_interactions,
			"max_expected_score_used": max_expected_score_per_talent,
			"interaction_stats": interaction_stats,
			"segment_id": segment_id,
			"calculation_details": {
				"participation_weight": 0.6,
				"score_weight": 0.4,
				"formula": "engagement_rate = (participation_rate * 0.6) + (score_rate * 0.4)"
			}
		}
		
	except Exception as e:
		frappe.log_error(
			message=frappe.get_traceback(),
			title=f"Calculate Segment Engagement Rate Error: {segment_id}"
		)
		return {
			"status": "error",
			"message": str(e)
		}


@frappe.whitelist()
def get_segments_engagement_rates(segment_ids=None):
	"""
	Lấy engagement rate cho nhiều segment cùng lúc
	
	Args:
		segment_ids: List hoặc JSON string của segment IDs
		
	Returns:
		dict: Engagement rates cho từng segment
	"""
	try:
		if not segment_ids:
			data = frappe.local.form_dict
			segment_ids = data.get("segment_ids")
		
		if not segment_ids:
			return {
				"status": "error",
				"message": _("Segment IDs are required")
			}
		
		# Parse segment_ids nếu là string
		if isinstance(segment_ids, str):
			try:
				segment_ids = json.loads(segment_ids)
			except:
				segment_ids = [s.strip() for s in segment_ids.split(",") if s.strip()]
		
		if not isinstance(segment_ids, list):
			return {
				"status": "error",
				"message": _("Invalid segment IDs format")
			}
		
		results = {}
		for segment_id in segment_ids:
			result = calculate_segment_engagement_rate(segment_id)
			if result.get("status") == "success":
				results[segment_id] = {
					"engagement_rate": result.get("engagement_rate", 0),
					"engagement_rate_by_participation": result.get("engagement_rate_by_participation", 0),
					"engagement_rate_by_score": result.get("engagement_rate_by_score", 0),
					"total_talents": result.get("total_talents", 0),
					"talents_with_interactions": result.get("talents_with_interactions", 0),
					"total_interactions": result.get("total_interactions", 0),
					"average_score_per_talent": result.get("average_score_per_talent", 0)
				}
			else:
				results[segment_id] = {
					"engagement_rate": 0,
					"error": result.get("message", "Unknown error")
				}
		
		return {
			"status": "success",
			"results": results
		}
		
	except Exception as e:
		frappe.log_error(
			message=frappe.get_traceback(),
			title="Get Segments Engagement Rates Error"
		)
		return {
			"status": "error",
			"message": str(e)
		}