import frappe
from frappe.utils import nowdate, getdate
from datetime import datetime
import json
from dateutil.relativedelta import relativedelta 


def map_resume_json_to_talent(json_data):
    """
    Ánh xạ dữ liệu hồ sơ từ JSON vào một bản ghi mới của DocType Mira Talent.
    :param json_data: JSON string hoặc dictionary chứa dữ liệu hồ sơ.
    :return: Tên (name) của DocType đã tạo.
    """
    if isinstance(json_data, str):
        try:
            data_dict = json.loads(json_data)
        except json.JSONDecodeError:
            frappe.throw("Dữ liệu đầu vào không phải là JSON hợp lệ.")
            return
    else:
        data_dict = json_data

    # Dữ liệu hồ sơ chính nằm trong key 'data' hoặc là root object
    data = data_dict.get("data", data_dict)
    
    # 1. Trích xuất thông tin cơ bản
    personal_info = data.get("personal_info", {})
    full_name = personal_info.get("can_full_name") or personal_info.get("name")
    email = personal_info.get("can_email") or personal_info.get("email")
    phone = personal_info.get("can_phone") or personal_info.get("phone")
    address = personal_info.get("address")
    
    # Kiểm tra trường bắt buộc
    if not full_name:
        frappe.throw("Không tìm thấy Tên đầy đủ (Full Name).")

    # 2. Xử lý các trường tổng hợp phức tạp
    work_experience = data.get("work_experience", [])
    education = data.get("education", [])
    
    # a. Tổng hợp Skills
    skills_string = _aggregate_skills(data)
    
    # b. Thông tin gần nhất
    latest_company, latest_title = _extract_latest_info(work_experience)
    
    # c. Tính toán Kinh nghiệm
    total_years_of_experience = _calculate_years_of_experience(work_experience)

    # d. Bằng cấp cao nhất
    highest_education = education[0].get("institution") if education else None

    # 3. Tạo bản ghi mới trong DocType Mira Talent
    doc = frappe.new_doc("Mira Talent")
    
    # --- Ánh xạ các trường ---
    
    # Thông tin Cá nhân
    doc.full_name = full_name
    doc.email = email
    doc.phone = phone
    doc.current_city = address
    
    # Thông tin Tổng hợp
    doc.skills = skills_string # Small Text
    doc.total_years_of_experience = total_years_of_experience # Float
    doc.latest_company = latest_company # Small Text
    doc.latest_title = latest_title # Text
    doc.highest_education = highest_education # Small Text
    
    # Mảng JSON (Lưu trữ dưới dạng chuỗi JSON/Code)
    doc.education = json.dumps(education) 
    doc.experience = json.dumps(work_experience)
    doc.certifications = json.dumps(data.get("certificates", []))
    doc.languages = json.dumps(data.get("languages", []))
    
    # Thông tin Bổ sung
    doc.notes = data.get("career_objective") or data.get("additional_info")
    
    # Lưu toàn bộ JSON gốc
    doc.resume_extract = json.dumps(data) # JSON Field
    
    try:
        doc.insert()
        frappe.db.commit()
        return doc.as_dict()
    except Exception as e:
        frappe.db.rollback()
        frappe.throw(f"Lỗi khi lưu bản ghi DocType Mira Talent: {e}")

# --- Hàm Hỗ trợ ---

def _calculate_years_of_experience(work_experience_data):
    """Tính toán tổng số năm kinh nghiệm."""
    total_months = 0
    today = getdate(nowdate())

    for job in work_experience_data:
        try:
            start_date_str = job.get('work_experience_start') or job.get('start_date')
            end_date_str = job.get('work_experience_end') or job.get('end_date')

            if not start_date_str: continue

            # Hỗ trợ định dạng MM/YYYY hoặc YYYY
            def parse_date(date_str, is_end=False):
                if date_str.lower() == 'present': return today
                if len(date_str) == 4: # YYYY
                    date_format = '%Y'
                    # Đối với YYYY, giả định là ngày 01/01 (start) hoặc 31/12 (end)
                    day_month_str = "01/01" if not is_end else "31/12"
                    return getdate(f"{day_month_str}/{date_str}")
                else: # MM/YYYY
                    return getdate(f"01/{date_str}", '%d/%m/%Y')

            start_date = parse_date(start_date_str)
            end_date = parse_date(end_date_str, is_end=True) if end_date_str else today
            
            if end_date > start_date:
                # Sử dụng relativedelta để tính khoảng cách chính xác
                diff = relativedelta(end_date, start_date)
                months = diff.years * 12 + diff.months + (1 if diff.days > 0 else 0)
                total_months += months
                
        except Exception:
            # Bỏ qua các mục kinh nghiệm bị lỗi ngày tháng
            continue

    return round(total_months / 12, 2)

def _extract_latest_info(work_experience_data):
    """Lấy thông tin công việc gần nhất."""
    if not work_experience_data: return None, None
    
    # Giả định công việc gần nhất là phần tử cuối cùng trong mảng
    latest_job = work_experience_data[-1]

    company = latest_job.get('work_experience_place') or latest_job.get('company')
    title = latest_job.get('work_experience_role') or latest_job.get('position')
    
    return company, title

def _aggregate_skills(data):
    """Tổng hợp tất cả kỹ năng từ nhiều nguồn."""
    skills_set = set()
    
    # 1. Kỹ năng từ mảng 'skills'
    for skill_group in data.get("skills", []):
        if skill_group.get("details"):
            for detail in skill_group["details"].split(', '):
                skills_set.add(detail.strip())
        elif skill_group.get("name"):
            skills_set.add(skill_group["name"].strip())

    # 2. Công nghệ từ mảng 'projects'
    for project in data.get("projects", []):
        for tech in project.get("technologies", []):
            skills_set.add(tech.strip())
            
    # Lọc bỏ các giá trị rỗng hoặc None
    skills_set.discard(None)
    skills_set.discard('')

    return ", ".join(sorted(list(skills_set)))


# Trường hợp 1: Dữ liệu JSON đầu tiên
json_case_1 = {
  "data": {
    "personal_info": {
      "can_full_name": "Do Van An",
      "can_email": "vanando110897@gmail.com",
      "can_phone": "0982119296",
      "job_title": "",
      "address": ""
    },
    "career_objective": "",
    "education": [
      {
        "institution": "Post and Telecommunications Institute of Technology",
        "major": "Electronics and Telecommunications",
        "degree": "",
        "start_date": "08/2015",
        "end_date": "03/2020",
        "gpa": 0
      }
    ],
    "work_experience": [
      {
        "work_experience_place": "NashTech",
        "work_experience_role": "Software Engineer",
        "work_experience_start": "01/2021",
        "work_experience_end": "Present",
        "responsibilities": ["..."]
      },
      {
        "work_experience_place": "Htn Soft",
        "work_experience_role": "Software Engineer",
        "work_experience_start": "08/2019",
        "work_experience_end": "12/2020",
        "responsibilities": ["..."]
      }
    ],
    "skills": [
      {"can_skill_name": "Programming Languages", "details": "Python, PHP, JavaScript"},
      {"can_skill_name": "Frameworks", "details": "Django, Laravel, Selenium, jQuery"},
      {"can_skill_name": "Databases", "details": "MySQL"},
      {"can_skill_name": "Other", "details": "OOP, SOLID, MVC, Data Structures and Algorithms, Agile, Scrum"}
    ],
    "certificates": [],
    "projects": [],
    "additional_info": ""
  }
}

# Trường hợp 2: Dữ liệu JSON thứ hai
json_case_2 = {
  "personal_info": {
    "name": "Trần Quang Huy",
    "email": "tranhuy20012000@gmail.com",
    "phone": "0854803099",
    "job_title": "",
    "address": "Xa Dan, Ha Noi"
  },
  "career_objective": "I am a programmer with experience in programming languages such as Java, C++, Typescript, Python and web technologies like HTML, CSS, JavaScript. My goal is to continue developing my programming skills and contribute to the company.",
  "education": [
    {
      "institution": "Hanoi University of Science, VNU",
      "major": "",
      "degree": "",
      "start_date": "2019",
      "end_date": "2023",
      "gpa": 0.0
    }
  ],
  "work_experience": [
    {
      "company": "Luvina Software Company",
      "position": "",
      "start_date": "1/2023",
      "end_date": "6/2023",
      "responsibilities": ["..."]
    },
    {
      "company": "Snine Joint Stock Company",
      "position": "",
      "start_date": "7/2023",
      "end_date": "12/2023",
      "responsibilities": ["..."]
    },
    {
      "company": "Entrust Consulting Group",
      "position": "",
      "start_date": "1/2024",
      "end_date": "7/2024",
      "responsibilities": ["..."]
    }
  ],
  "skills": [
    { "name": "Teamwork", "details": "" },
    { "name": "Problem Solving", "details": "" },
  ],
  "projects": [
    {
      "name": "Burndown Chart Implementation",
      "role": "Developer",
      "technologies": ["JavaScript", "Owl framework", "Python"],
      "descriptions": "..."
    }
  ],
  "certificates": [],
  "additional_info": ""
}

# --- Thực thi ---
def test():
    print("--- Kết quả Mapping cho Trường hợp 1 (Do Van An) ---")
    result_1 = map_resume_json_to_talent(json_case_1)
    print(json.dumps(result_1, indent=2, ensure_ascii=False))

    print("\n" + "="*50 + "\n")

    print("--- Kết quả Mapping cho Trường hợp 2 (Trần Quang Huy) ---")
    result_2 = map_resume_json_to_talent({"data": json_case_2}) # Bọc lại để phù hợp với cấu trúc chung
    print(json.dumps(result_2, indent=2, ensure_ascii=False))