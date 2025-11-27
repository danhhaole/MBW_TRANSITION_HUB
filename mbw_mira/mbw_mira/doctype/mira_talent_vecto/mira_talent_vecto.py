# Copyright (c) 2025, MBWCloud Co. and contributors
# For license information, please see license.txt

import frappe
import json
from frappe.model.document import Document
from mbw_mira.utils.ai import get_vector_embeddings
from mbw_mira.utils.embedding import compare_vector_with_list


class MiraTalentVecto(Document):
	def before_insert(self):
		# Hàm được gọi ngay trước khi DocType được lưu lần đầu (INSERT)
		calculate_and_set_vector(self)

	def before_save(self):
		# Hàm được gọi ngay trước khi DocType được lưu (UPDATE hoặc INSERT)
		# Đảm bảo vector được cập nhật nếu text nguồn thay đổi
		calculate_and_set_vector(self)

	def on_update(self):
		compare_talent_pool_vecto(self.name)
	

def compare_talent_pool_vecto(talent_id) -> float:
    #Lấy danh sách pool vecto
    pool_vecto = frappe.get_all("Mira Pool Vecto",fields=["embedding_vector"])
    #Lấy ra
    talent_vecto = frappe.db.get_value("Mira Talent Vecto",{"mira_talent": talent_id}, "embedding_vector")
    list_vecto = parse_vector_list(pool_vecto)
    score = compare_vector_with_list(talent_vecto,list_vecto,0.5)
    print("score", score)
    return score
	
    
def parse_vector_list(records):
    """
    Chuyển list dict [{'embedding_vector': '...'}]
    → list[list[float]]
    """
    return [json.loads(r["embedding_vector"]) for r in records]

def create_talent_summary_text(talent_doc):
	"""
	Tổng hợp dữ liệu từ Mira Talent DocType thành summary_text (text nguồn cho embedding).
	"""
	parts = []
	
	# --- Dữ liệu Core (Quan trọng nhất) ---
	if hasattr(talent_doc,"latest_title") and talent_doc.latest_title:
		parts.append(f"Latest Title: {talent_doc.latest_title}")
	if hasattr(talent_doc,"latest_company") and talent_doc.latest_company:
		parts.append(f"Latest Company: {talent_doc.latest_company}")
	if hasattr(talent_doc,"total_years_of_experience") and talent_doc.total_years_of_experience:
		parts.append(f"YOE: {talent_doc.total_years_of_experience} years")
	if hasattr(talent_doc,"desired_role") and talent_doc.desired_role:
		parts.append(f"Desired Role: {talent_doc.desired_role}")
		
	# --- Kỹ năng và Chuyên môn ---
	if hasattr(talent_doc,"skills") and talent_doc.skills:
		parts.append(f"Skills: {talent_doc.skills}")
	if hasattr(talent_doc,"domain_expertise") and talent_doc.domain_expertise:
		parts.append(f"Domain: {talent_doc.domain_expertise}")
	if hasattr(talent_doc,"hard_skills") and talent_doc.hard_skills:
		parts.append(f"Hard Skills: {talent_doc.hard_skills}")
	if hasattr(talent_doc,"soft_skills") and talent_doc.soft_skills:
		parts.append(f"Soft Skills: {talent_doc.soft_skills}")

	# --- Dữ liệu Cấu trúc (JSON/Code Fields) ---
	
	# 1. Kinh nghiệm làm việc (Title - Company)
	exp_summary = standardize_json_field(talent_doc, 'experience', ['title', 'company'])
	if exp_summary:
		parts.append(f"Work History: {exp_summary}")
		
	# 2. Học vấn (Degree - Institution)
	edu_summary = standardize_json_field(talent_doc, 'education', ['degree', 'institution', 'field_of_study'])
	if edu_summary:
		parts.append(f"Education: {edu_summary}")

	# 3. Ngôn ngữ
	lang_summary = standardize_json_field(talent_doc, 'languages', ['language', 'proficiency'])
	if lang_summary:
		parts.append(f"Languages: {lang_summary}")

	# --- Dữ liệu Địa lý và Trạng thái ---
	if hasattr(talent_doc,"current_city") and talent_doc.current_city:
		parts.append(f"City: {talent_doc.current_city}")
	if hasattr(talent_doc,"preferred_work_model") and talent_doc.preferred_work_model:
		parts.append(f"Work Model: {talent_doc.preferred_work_model}")
		
	return " | ".join(parts)

def calculate_and_set_vector(doc):
	"""
	Quy trình chung: 
	1. Tạo chuỗi summary_text.
	2. Gọi API để tạo vector từ chuỗi đó.
	3. Lưu vector (JSON string) vào doc.embedding_vector.
	"""

	# 1. Tạo chuỗi embedding_text dựa trên loại DocType
	text_source = create_talent_summary_text(doc)
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

def standardize_json_field(doc, fieldname, primary_keys):
    """
    Chuẩn hóa trường kiểu Code/JSON array thành một chuỗi tóm tắt.
    
    :param doc: Đối tượng Mira Talent Doc.
    :param fieldname: Tên trường (ví dụ: 'education').
    :param primary_keys: List các key quan trọng cần trích xuất (ví dụ: ['title', 'company']).
    :return: Chuỗi tóm tắt dữ liệu.
    """
    data = doc.get(fieldname)
    if not data:
        return ""
        
    try:
        data_list = json.loads(data) if isinstance(data, str) else data
        if not isinstance(data_list, list):
            return ""
        
        summary_parts = []
        for item in data_list:
            if isinstance(item, dict):
                # Tạo chuỗi từ các khóa chính (ví dụ: "Degree at University")
                parts = [str(item.get(k)) for k in primary_keys if item.get(k)]
                if parts:
                    summary_parts.append(" - ".join(parts))
                    
        return "; ".join(summary_parts)
        
    except json.JSONDecodeError as e:
        frappe.log_error(title=f"{fieldname} JSON Error", message=f"Lỗi parse JSON: {e}")
        return str(data) # Trả về nguyên mẫu nếu lỗi

def create_talent_vector(talent_name):
	"""
	Tạo hoặc cập nhật bản ghi Mira Talent Vecto cho một Mira Talent cụ thể.

	:param talent_name: Tên (ID) của Mira Talent DocType.
	:return: Tên (ID) của bản ghi Mira Talent Vecto.
	"""
	if not talent_name:
		frappe.throw("Talent ID là bắt buộc.")
		
	# frappe.db.begin()
	try:
		# 1. Tải DocType Mira Talent gốc
		talent_doc = frappe.get_doc("Mira Talent", talent_name)

		# 2. Tìm kiếm hoặc tạo DocType Mira Talent Vecto liên quan

		# Talent Vecto thường là 1-1 với Talent. Kiểm tra xem nó đã tồn tại chưa.
		existing_vector_name = frappe.db.get_value(
			"Mira Talent Vecto",
			{"mira_talent": talent_name},
			"name"
		)

		if existing_vector_name:
			vector_doc = frappe.get_doc("Mira Talent Vecto", existing_vector_name)
		else:
			vector_doc = frappe.new_doc("Mira Talent Vecto")
			vector_doc.mira_talent = talent_name
			# Gán YOE trực tiếp nếu có
			vector_doc.yoe = talent_doc.total_years_of_experience


		# 3. Tạo Summary Text (Văn bản nguồn cho Embedding)
		summary_text = create_talent_summary_text(talent_doc.as_dict())

		# Cập nhật các trường cần thiết (YOE, Summary Text)
		if hasattr(talent_doc,"skills"):
			vector_doc.yoe = talent_doc.total_years_of_experience

		vector_doc.summary_text = summary_text

		if hasattr(talent_doc,"skills"):
			vector_doc.skills = talent_doc.skills # Đồng bộ skills nếu cần

		if hasattr(talent_doc,"current_city"):
			vector_doc.location =  talent_doc.current_city # Đồng bộ location

		calculate_and_set_vector(vector_doc.as_dict())

		# 4. Tính toán và gán vector embedding
		# Hàm này sẽ gọi API và gán giá trị vào vector_doc.embedding_vector
		# 


		# 5. Lưu DocType
		if existing_vector_name:
			vector_doc.save(ignore_permissions=True, ignore_version=True)
		else:
			vector_doc.insert(ignore_permissions=True)
			
		frappe.db.commit()
		return vector_doc.name

	except frappe.DoesNotExistError:
		# frappe.db.rollback()
		frappe.throw(f"Mira Talent '{talent_name}' không tồn tại.")
	except Exception as e:
		# frappe.db.rollback()
		frappe.log_error(title="Create Talent Vector Failed", message=str(e))
		frappe.throw(f"Lỗi khi tạo/cập nhật Talent Vector cho '{talent_name}': {e}")