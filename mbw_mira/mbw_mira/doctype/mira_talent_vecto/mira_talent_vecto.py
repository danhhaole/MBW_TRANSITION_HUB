# Copyright (c) 2025, MBWCloud Co. and contributors
# For license information, please see license.txt

import frappe
import json
from frappe.model.document import Document
from mbw_mira.utils.ai import get_vector_embeddings


class MiraTalentVecto(Document):
	def before_insert(self):
		# Hàm được gọi ngay trước khi DocType được lưu lần đầu (INSERT)
		self.calculate_and_set_vector()

	def before_save(self):
		# Hàm được gọi ngay trước khi DocType được lưu (UPDATE hoặc INSERT)
		# Đảm bảo vector được cập nhật nếu text nguồn thay đổi
		self.calculate_and_set_vector()
	

	def create_talent_summary_text(doc):
		"""
		Tạo chuỗi summary_text bằng cách tổng hợp các trường liên quan từ Candidate DocType.
		"""
		profile_parts = []
		
		# Các trường chính tạo vector
		if doc.summary_text:
			profile_parts.append(doc.summary_text)
		if doc.yoe:
			profile_parts.append(f"Years of Experience (YOE): {doc.yoe}")
		if doc.skills:
			profile_parts.append(f"Candidate Skills: {doc.skills}")
		if doc.location:
			profile_parts.append(f"Candidate Location: {doc.location}")
			
		return " | ".join(profile_parts)

	def calculate_and_set_vector(doc):
		"""
		Quy trình chung: 
		1. Tạo chuỗi summary_text.
		2. Gọi API để tạo vector từ chuỗi đó.
		3. Lưu vector (JSON string) vào doc.embedding_vector.
		"""

		# 1. Tạo chuỗi embedding_text dựa trên loại DocType
		text_source = doc.create_talent_embedding_text()
		doc.summary_text = text_source
		if text_source:
			try:
				# 2. Gọi API tạo vector
				embeddings_list = get_vector_embeddings([text_source])
				
				if embeddings_list and embeddings_list[0]:
					# 3. Lưu vector
					vector_array = embeddings_list[0]
					doc.embedding_vector = json.dumps(vector_array)
				else:
					frappe.log_error(title="Vector Generation Failed", message=f"API returned no vector for {doc.name}")
					doc.embedding_vector = None 
					
			except Exception as e:
				frappe.log_error(title="Vector API Error", message=f"{doc.name}: {e}")
		else:
			doc.embedding_vector = None


def insert_mira_talent(data):

    if hasattr(data,'criteria') and data.criteria:
        criteria_parse = json.loads(data.criteria)
    print(criteria_parse)
    try:
        pool_doc = frappe.get_doc({
            "doctype": "Mira Talent Vecto",
            "yoe": data.get("yoe"),
            "skills": data.get("skills"),
            "location": data.get("location"),
            "summary_text": data.get("summary_text"),
            "mira_segment": data.get("mira_segment")
        })
                
        pool_doc.insert(ignore_permissions=True)
        
        return pool_doc.name

    except Exception as e:
        frappe.log_error(title="Insert Pool Failed", message=str(e))
        frappe.throw(f"Không thể chèn bản ghi Mira Talent Pool: {e}")