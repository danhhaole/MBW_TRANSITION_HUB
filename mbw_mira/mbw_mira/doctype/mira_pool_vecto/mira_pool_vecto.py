# Copyright (c) 2025, MBWCloud Co. and contributors
# For license information, please see license.txt

import json
import frappe
from frappe.model.document import Document
from mbw_mira.utils.ai import get_vector_embeddings


class MiraPoolVecto(Document):
	def before_insert(self):
		# Hàm được gọi ngay trước khi DocType được lưu lần đầu (INSERT)
		calculate_and_set_vector(self)

	def before_save(self):
		# Hàm được gọi ngay trước khi DocType được lưu (UPDATE hoặc INSERT)
		# Đảm bảo vector được cập nhật nếu text nguồn thay đổi
		calculate_and_set_vector(self)

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
    """
    Tạo chuỗi embedding_text (từ các trường của doc), gọi API, và gán embedding_vector.
    Hàm này được thiết kế để hoạt động trên Mira Pool Vecto.
    """
    text_source_parts = []
    
    # 1. Gộp các trường Pool Vecto để tạo text nguồn
    if doc.embedding_text: # Trường này đã được tạo ra trong hàm insert/update
        text_source_parts.append(doc.embedding_text)
    
    # Bổ sung các thông tin khác (chỉ dùng nếu embedding_text chưa đủ)
    if doc.min_yoe:
        text_source_parts.append(f"Min YOE: {doc.min_yoe}")
    
    # Chuyển JSON skills/location thành chuỗi để embed
    if doc.skills_must_have:
        text_source_parts.append(f"Required Skills: {doc.skills_must_have}")
    if doc.location:
        text_source_parts.append(f"Target Location: {doc.location}")
        
    text_source = " | ".join(text_source_parts)

    if text_source:
        embeddings_list = get_vector_embeddings([text_source])
        
        if embeddings_list and embeddings_list[0]:
            doc.embedding_vector = json.dumps(embeddings_list[0])
        else:
            frappe.log_error(title="Vector Calc Failed", message=f"API returned no vector for Pool: {doc.name}")
            doc.embedding_vector = None 
    else:
        doc.embedding_vector = None

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

def insert_mira_pool_vecto(segment_id):
    """
    Tạo một bản ghi Mira Pool Vecto mới dựa trên dữ liệu chuẩn hóa từ Mira Segment.
    Hàm này đảm bảo các trường phái sinh được tính toán đầy đủ và chuẩn hóa.
    
    :param segment_id: Tên (ID) của Mira Segment.
    :return: Tên (ID) của bản ghi Mira Pool Vecto mới.
    """
    if not segment_id:
        frappe.throw("Segment ID là bắt buộc.")

    try:
        # 1. Tải DocType Mira Segment gốc
        segment_doc = frappe.get_doc("Mira Segment", segment_id)
        criteria = segment_doc.get("criteria")

        # 2. Chuẩn hóa và Ánh xạ các trường dữ liệu
        
        # a. Min YOE (Ánh xạ từ experience_years, lấy giá trị > lớn nhất)
        yoe_conditions = parse_segment_criteria(criteria, 'experience_years')
        
        min_yoe_value = 0 
        if isinstance(yoe_conditions, list):
            for cond in yoe_conditions:
                if isinstance(cond, str) and cond.startswith('>'):
                     try:
                         min_yoe_value = max(min_yoe_value, int(cond.replace('>', '').replace('=', '').strip()))
                     except ValueError:
                         pass # Bỏ qua nếu không parse được số
        
        # b. Skills Must Have
        skills_list = parse_segment_criteria(criteria, 'skills')
        
        # c. Location (Ánh xạ từ City hoặc Country)
        location_list = parse_segment_criteria(criteria, 'city') or parse_segment_criteria(criteria, 'country')

        # d. Tạo chuỗi Embedding Text Source (Tạo embedding_text ngay lập tức)
        embedding_text_parts = [
            f"Segment Title: {segment_doc.title}",
            f"Segment Description: {segment_doc.description}"
        ]
        
        if skills_list:
            # Lưu ý: Giữ định dạng JSON cho list skills để embedding model hiểu rõ cấu trúc
            embedding_text_parts.append(f"Required Skills: {json.dumps(skills_list, ensure_ascii=False)}")
        if location_list:
            embedding_text_parts.append(f"Target Locations: {json.dumps(location_list, ensure_ascii=False)}")
        if min_yoe_value > 0:
             embedding_text_parts.append(f"Minimum YOE: {min_yoe_value}")
             
        final_embedding_text = " | ".join(embedding_text_parts)

        # 3. Tạo đối tượng DocType Mira Pool Vecto mới
        pool_doc = frappe.get_doc({
            "doctype": "Mira Pool Vecto",
            # Các trường được phái sinh
            "min_yoe": min_yoe_value,
            "skills_must_have": json.dumps(skills_list) if skills_list else None,
            "location": json.dumps(location_list) if location_list else None,
            "embedding_text": final_embedding_text, 
            "mira_segment": segment_id, # Liên kết bắt buộc
            
        })
        
        # 4. Tính toán và gán vector embedding
        # Hàm này sử dụng final_embedding_text để gọi API và gán embedding_vector
        calculate_and_set_vector(pool_doc)
        
        # 5. Chèn bản ghi vào cơ sở dữ liệu
        pool_doc.insert(ignore_permissions=True)
        print("pool_doc",pool_doc)
        return pool_doc.name

    except frappe.DoesNotExistError:
        frappe.throw(f"Mira Segment '{segment_id}' không tồn tại.")
    except Exception as e:
        frappe.db.rollback()
        # Log lỗi chi tiết để debug
        frappe.log_error(title="Insert Pool Vecto Failed", message=str(e))
        frappe.throw(f"Không thể chèn bản ghi Mira Pool Vecto từ Segment '{segment_id}': {e}")

def derive_pool_fields_from_segment(pool_doc):
    """
    Tải Mira Segment liên kết, tái phân tích trường 'criteria', và cập nhật các 
    trường min_yoe, skills_must_have, location, và embedding_text trên pool_doc.
    
    :param pool_doc: Đối tượng Mira Pool Vecto.
    :return: True nếu có bất kỳ trường phái sinh nào được thay đổi, False nếu không.
    """
    segment_id = pool_doc.mira_segment
    if not segment_id:
        return False

    try:
        segment_doc = frappe.get_doc("Mira Segment", segment_id)
        criteria = segment_doc.get("criteria")
        
        # --- Tái phân tích Criteria ---
        
        # 1. Min YOE (CẬP NHẬT LOGIC)
        yoe_conditions = parse_segment_criteria(criteria, 'experience_years')
        min_yoe_value = 0 
        
        # Nếu có nhiều điều kiện YOE (ví dụ: ["< 10", ">= 5"])
        if isinstance(yoe_conditions, list):
            for cond in yoe_conditions:
                if isinstance(cond, str) and (cond.startswith('>') or cond.startswith('>=')):
                    # Trích xuất số từ chuỗi '>= 5'
                    num_str = cond.replace('>', '').replace('=', '').strip()
                    try:
                        min_yoe_value = max(min_yoe_value, int(num_str))
                    except ValueError:
                        pass # Bỏ qua nếu không phải số
        
        # Nếu chỉ có một điều kiện YOE (ví dụ: ">= 5")
        elif isinstance(yoe_conditions, str) and (yoe_conditions.startswith('>') or yoe_conditions.startswith('>=')):
             num_str = yoe_conditions.replace('>', '').replace('=', '').strip()
             try:
                 min_yoe_value = int(num_str)
             except ValueError:
                 pass
        
        # 2. Skills Must Have
        skills_list = parse_segment_criteria(criteria, 'skills')
        print("skills_list",skills_list)
        # 3. Location
        location_list = parse_segment_criteria(criteria, 'city') or parse_segment_criteria(criteria, 'country')

        # 4. Tạo chuỗi Embedding Text Source MỚI (để so sánh)
        embedding_text_parts = [
            f"Segment Title: {segment_doc.title}",
            f"Segment Description: {segment_doc.description}"
        ]
        
        if skills_list:
            embedding_text_parts.append(f"Required Skills: {json.dumps(skills_list)}")
        if location_list:
            embedding_text_parts.append(f"Target Locations: {json.dumps(location_list)}")
        if min_yoe_value > 0:
             embedding_text_parts.append(f"Minimum YOE: {min_yoe_value}")
             
        final_embedding_text = " | ".join(embedding_text_parts)
        
        # --- Cập nhật và kiểm tra thay đổi ---
        changed = False
        
        if pool_doc.min_yoe != min_yoe_value:
            pool_doc.min_yoe = min_yoe_value
            changed = True
            
        new_skills_str = json.dumps(skills_list) if skills_list else None
        if pool_doc.skills_must_have != new_skills_str:
            pool_doc.skills_must_have = new_skills_str
            changed = True
            
        new_location_str = json.dumps(location_list) if location_list else None
        if pool_doc.location != new_location_str:
            pool_doc.location = new_location_str
            changed = True

        if pool_doc.embedding_text != final_embedding_text:
            pool_doc.embedding_text = final_embedding_text
            changed = True
            
        return changed

    except frappe.DoesNotExistError:
        frappe.log_error(title="Segment Not Found", message=f"Mira Segment '{segment_id}' không tồn tại cho Pool '{pool_doc.name}'.")
        return False
    except Exception as e:
        frappe.log_error(title="Derive Pool Failed", message=f"Lỗi khi xử lý Pool {pool_doc.name}: {e}")
        return False

def update_mira_pool_vecto(pool_name, new_data):
    """
    Cập nhật một bản ghi Mira Pool Vecto hiện có, tự động tái phân tích dữ liệu 
    Segment nếu cần, và tính toán lại vector embedding.
    """
    if not isinstance(new_data, dict) or not pool_name:
        frappe.throw("Dữ liệu đầu vào hoặc Tên Pool không hợp lệ.")

    try:
        # 1. Tải DocType hiện có
        pool_doc = frappe.get_doc("Mira Pool Vecto", {"mira_segment":pool_name})
        has_changed = True
                
        # 3. Tái phân tích Segment và cập nhật các trường phái sinh
        # Đây là bước bổ sung quan trọng để đồng bộ hóa dữ liệu Segment
        if pool_doc.mira_segment:
            derived_changed = derive_pool_fields_from_segment(pool_doc)
            if derived_changed:
                has_changed = True
        
        # 4. Tính toán lại vector embedding nếu dữ liệu liên quan thay đổi
        if has_changed:
            # Hàm calculate_and_set_vector sẽ sử dụng pool_doc.embedding_text mới nhất
            calculate_and_set_vector(pool_doc)
            
            # 5. Lưu DocType
            pool_doc.save(ignore_permissions=True, ignore_version=True)
            frappe.db.commit()
            
            return pool_doc.name
        else:
            frappe.msgprint(f"Bản ghi Pool Vecto '{pool_name}' không có thay đổi nào cần lưu.")
            return pool_doc.name

    except frappe.DoesNotExistError:
        frappe.throw(f"Bản ghi Mira Pool Vecto '{pool_name}' không tồn tại.")
    except Exception as e:
        frappe.db.rollback()
        frappe.log_error(title="Update Pool Vecto Failed", message=str(e))
        frappe.throw(f"Lỗi khi cập nhật bản ghi Mira Pool Vecto '{pool_name}': {e}")