# Copyright (c) 2025, MBWCloud Co. and contributors
# For license information, please see license.txt

import json
import frappe
from frappe.model.document import Document
from mbw_mira.utils.ai import get_vector_embeddings


class MiraPoolVecto(Document):
	def on_update(self):
		try:
			if self.embedding_text:
				frappe.enqueue(
                        "mbw_mira.mbw_mira.doctype.mira_pool_vecto.mira_pool_vecto.set_vecto_and_compare",
                        queue="default",
                        doc=self.as_dict()
                    )
		except Exception as e:
			frappe.log_error(f"Lỗi compare {str(e)}")
			pass


def parse_segment_criteria(criteria_value, key):
    """
    Phân tích cú pháp mảng filters/JSON từ trường 'criteria' và trích xuất giá trị cho 'key'.
    Đã sửa lỗi trả về list rỗng cho trường 'skills'.
    """
    if not criteria_value: return None
        
    criteria_list = []
    
    try:
        criteria_list = json.loads(criteria_value) if isinstance(criteria_value, str) else criteria_value
        if not isinstance(criteria_list, list):
            return None
    except json.JSONDecodeError:
        return None
        
    extracted_conditions = []
    
    # Các toán tử so sánh để phân biệt với giá trị thô
    comparison_operators = ['==', '=', '>', '>=', '<', '<=']

    for item in criteria_list:
        if isinstance(item, list) and len(item) == 3:
            field, op, value = item
            op_lower = op.lower()
            
            if field.lower() == key.lower():
                
                # --- Trường hợp 1: Đa giá trị (IN, LIKE, hoặc là trường SKILLS) ---
                if op_lower in ('in', 'like') or key.lower() == 'skills':
                    if isinstance(value, str):
                        # Tách và làm sạch các giá trị (ví dụ: 'python, django' -> ['python', 'django'])
                        values = [v.strip() for v in value.split(',') if v.strip()]
                        extracted_conditions.extend(values)
                    else:
                        extracted_conditions.append(value)
                
                # --- Trường hợp 2: So sánh (YOE, Salary, Rating) ---
                elif op_lower in comparison_operators:
                    # Lưu trữ điều kiện so sánh để xử lý tính toán sau
                    extracted_conditions.append(f"{op} {value}")
                    
                # --- Trường hợp 3: Toán tử khác ---
                else:
                    extracted_conditions.append(f"{op} {value}")


    if not extracted_conditions: return None
    
    # --- LOGIC SỬA LỖI: Tách biệt giá trị và điều kiện ---
    
    # Nếu đang tìm SKILLS (hoặc bất kỳ trường nào dùng IN/LIKE)
    if key.lower() == 'skills':
        # Chỉ trả về các giá trị thô (không có toán tử so sánh)
        return list(set(extracted_conditions)) 

    # Nếu đang tìm các điều kiện so sánh (YOE, Salary)
    return extracted_conditions


def set_vecto_and_compare(doc):
    embedding_vector= get_vector_embeddings([json.dumps(doc.embedding_text)])
    if embedding_vector:
        frappe.db.set_value("Mira Pool Vecto",doc.name, 'embedding_vector',json.dumps(embedding_vector[0]))

#==================================================
#Tìm talent pool phục vụ cho 2 việc
#1. Enroll talent vào pool 
#2. Disenroll talent ra khỏi pool nếu không phù hợp
#==================================================
def get_talent_pool(pool_id):
    talent_pool = frappe.get_all("Mira Talent Pool", filters={"segment_id":pool_id},fields=["talent_id"])
    #Lấy danh sách talent trong pool
    if talent_pool:
        for talent in talent_pool:
            #Kiểm tra talent có vecto không
            pass