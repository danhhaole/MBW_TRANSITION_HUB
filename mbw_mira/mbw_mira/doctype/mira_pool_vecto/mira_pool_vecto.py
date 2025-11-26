# Copyright (c) 2025, MBWCloud Co. and contributors
# For license information, please see license.txt

import json
import frappe
from frappe.model.document import Document
from mbw_mira.utils.ai import get_vector_embeddings


class MiraPoolVecto(Document):
	def before_insert(self):
		# Hàm được gọi ngay trước khi DocType được lưu lần đầu (INSERT)
		self.calculate_and_set_vector()

	def before_save(self):
		# Hàm được gọi ngay trước khi DocType được lưu (UPDATE hoặc INSERT)
		# Đảm bảo vector được cập nhật nếu text nguồn thay đổi
		self.calculate_and_set_vector()

	def create_pool_embedding_text(doc):
		"""
		Tạo chuỗi embedding_text bằng cách tổng hợp các trường liên quan từ Pool DocType.
		"""
		criteria_parts = []
		
		# Các trường chính tạo vector
		if doc.embedding_text:
			criteria_parts.append(doc.embedding_text)
		if doc.min_yoe:
			criteria_parts.append(f"Min Years of Experience (YOE): {doc.min_yoe}")
		if doc.skills_must_have:
			criteria_parts.append(f"Required Skills: {doc.skills_must_have}")
		if doc.location:
			criteria_parts.append(f"Locations: {doc.location}")
			

		return " | ".join(criteria_parts)

	def calculate_and_set_vector(doc):
		# 1. Tạo chuỗi embedding_text dựa trên loại DocType
		text_source = doc.create_pool_embedding_text()
		doc.embedding_text = text_source
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


def insert_mira_pool(data):
    if not isinstance(data, dict):
        frappe.throw("Dữ liệu đầu vào phải là một đối tượng JSON/Dict hợp lệ.")
    try:
        pool_doc = frappe.get_doc({
            "doctype": "Mira Pool Vecto",
            "min_yoe": data.get("min_yoe"),
            "skills_must_have": data.get("skills_must_have"),
            "location": data.get("location"),
            "embedding_text": data.get("embedding_text"),
            "mira_segment": data.get("mira_segment")
        })
                
        pool_doc.insert(ignore_permissions=True)
        
        return pool_doc.name

    except Exception as e:
        frappe.log_error(title="Insert Pool Failed", message=str(e))
        frappe.throw(f"Không thể chèn bản ghi Mira Talent Pool: {e}")