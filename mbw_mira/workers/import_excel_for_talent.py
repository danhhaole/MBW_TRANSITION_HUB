import frappe
import pandas as pd
import json
from datetime import datetime
import ast

def import_talentprofile_from_file(campaign_name: str):
    logger = frappe.logger("import_candidates")

    # 1. Lấy thông tin campaign
    campaign = frappe.db.get_value(
        "Campaign",
        campaign_name,
        [
            "campaign_name", "is_active", "status",
            "start_date", "end_date", "target_segment",
            "source_file", "source_config"
        ],
        as_dict=True
    )

    if not campaign:
        frappe.log_error("Import TalentProfile", f"Campaign not found: {campaign_name}")
        return

    # 2. Kiểm tra trạng thái hợp lệ
    today = datetime.today().date()
    if not campaign.is_active or campaign.status != "ACTIVE" \
            or not campaign.start_date or not campaign.end_date \
            or campaign.start_date > today or campaign.end_date < today:
        frappe.log_error("Import TalentProfile", f"Campaign is not active or out of range: {campaign_name}")
        return

    # 3. Parse source_config JSON
    try:
        source_config = json.loads(campaign.source_config or "{}")
    except Exception as e:
        frappe.log_error("Import TalentProfile", f"Failed to parse source_config JSON: {e}")
        return

    file_name = campaign.source_file.split("/")[-1]
    field_mapping = source_config.get("field_mapping", [])

    if not file_name or not field_mapping:
        frappe.log_error("Import TalentProfile", f"Missing file name or field mapping for campaign: {campaign_name}")
        return

    # 4. Tìm file đã upload trong File doctype
    file_url = frappe.db.get_value("File", {"file_name": file_name}, "file_url")
    if not file_url:
        frappe.log_error("Import TalentProfile", f"File not found in File doctype: {file_name}")
        return

    file_path = frappe.get_site_path("public", file_url.lstrip("/"))

    # 5. Đọc file bằng pandas
    try:
        if file_name.endswith(".csv"):
            df = pd.read_csv(file_path)
        elif file_name.endswith((".xls", ".xlsx")):
            df = pd.read_excel(file_path)
        else:
            frappe.log_error("Import TalentProfile", f"Unsupported file format: {file_name}")
            return

        # Convert NaN thành None
        df = df.where(pd.notnull(df), None)
    except Exception as e:
        frappe.log_error("Import TalentProfile", f"Error reading file {file_name}: {e}")
        return

    inserted = 0
    if df is not None and not df.empty:
        for _, row in df.iterrows():
            # 6. Map dữ liệu theo cấu hình
            raw_data = {}
            for mapping in field_mapping:
                source_col = mapping.get("column_name")
                target_field = mapping.get("field_name")
                raw_data[target_field] = row.get(source_col)

            # 7. Chuẩn hóa dữ liệu: xử lý skills
            skills_value = raw_data.get("skills") or "[]"
            skills_list = []

            if isinstance(skills_value, list):
                skills_list = skills_value
            elif isinstance(skills_value, str):
                try:
                    # Ưu tiên parse JSON
                    skills_list = json.loads(skills_value)
                    if not isinstance(skills_list, list):
                        raise ValueError
                except:
                    try:
                        skills_list = ast.literal_eval(skills_value)
                        if not isinstance(skills_list, list):
                            raise ValueError
                    except:
                        skills_list = [s.strip() for s in skills_value.split(",") if s.strip()]
            else:
                skills_list = []
            profile_data = raw_data.get("profile_data")
            profile_data = None if pd.isna(profile_data) else profile_data
            # 8. Chuẩn bị dữ liệu TalentProfiles
            doc_data = {
                "doctype": "TalentProfiles",
                "full_name": raw_data.get("full_name"),
                "email": raw_data.get("email"),
                "phone": raw_data.get("phone"),
                "source": raw_data.get("source") or "Excel Import",
                "skills": json.dumps(skills_list),
                "avatar": "",
                "headline": raw_data.get("headline") or "",
                "cv_original_url": raw_data.get("cv_original_url") or "",
                "profile_data": profile_data,
                "ai_summary": raw_data.get("ai_summary")  or "",
                "status": "NEW",
                "last_interaction": None,
                "email_opt_out": 0
            }

            # 9. Insert nếu chưa tồn tại
            try:
                if not check_exists(raw_data.get("email")):
                    doc = frappe.get_doc(doc_data)
                    doc.insert(ignore_permissions=True)
                    frappe.db.commit()
                    inserted += 1
            except Exception as e:
                frappe.log_error("Failed to insert", f"Failed to insert: {doc_data.get('full_name')} — {doc_data}")

        # 10. Gửi sự kiện realtime nếu cần
        frappe.publish_realtime('import_talentprofile_from_file', message={'campaign': campaign_name})
        logger.info(f"Imported {inserted} profiles for campaign {campaign_name}")
        return True

def check_exists(email):
    talent_exists = frappe.db.exists("TalentProfiles",{"email":email})
    if talent_exists:
        return True
    else:
        return False

# def fake_sample_data():
#     import random
#     from faker import Faker
#     import pandas as pd
#     from datetime import datetime

#     fake = Faker('vi_VN')  # Dùng tên tiếng Anh giả lập gần giống tiếng Việt

#     def vietnamize_name(name):
#         parts = name.split()
#         return " ".join(part.capitalize() for part in parts)

#     # Danh sách Talent Pool và kỹ năng tương ứng
#     talent_pools = [
#         ("Software Developers", ["Python", "JavaScript", "SQL", "Git"]),
#         ("Data Professionals", ["Python", "SQL", "Power BI", "Tableau"]),
#         ("Digital Marketing Experts", ["SEO", "Google Ads", "Content Writing"]),
#         ("UI/UX & Product Designers", ["Figma", "Prototyping", "Adobe XD"]),
#         ("Project & Product Managers", ["Agile", "Scrum", "Jira"]),
#         ("Business Analysts", ["BPMN", "SQL cơ bản", "Process Design"]),
#         ("Quality Assurance (QA)", ["Manual Testing", "Selenium", "JIRA"]),
#         ("DevOps & Cloud Engineers", ["Docker", "Kubernetes", "CI/CD"]),
#         ("IT Infrastructure & Security", ["Linux", "Firewall", "Security Policies"]),
#         ("Sales & Account Managers", ["CRM", "Negotiation", "Communication"]),
#         ("Customer Support", ["Ticketing Tools", "Troubleshooting"]),
#         ("HR & Talent Acquisition", ["Sourcing", "Boolean Search"]),
#         ("Finance & Accounting", ["Excel nâng cao", "IFRS"]),
#         ("Operations", ["Logistics", "Inventory Control"]),
#         ("Interns & Fresh Graduates", ["Tin học văn phòng", "Tư duy logic"])
#     ]

#     # Tạo dữ liệu mẫu
#     sample_data = []
#     base_id = 6000

#     for i in range(100):
#         name = vietnamize_name(fake.name())
#         email = fake.email()
#         phone = "0" + fake.msisdn()[1:10]
#         dob = fake.date_of_birth(minimum_age=22, maximum_age=30).strftime('%Y-%m-%d')
#         headline, skills = random.choice(talent_pools)
#         id_str = f"TLP-2507-{base_id + i:05d}"
#         source = "SOURCE-250722-00536"
#         link_cv = f"/files/{name.replace(' ', '_')}-CV.pdf"
#         ai_summary = f"CV của {name} ứng tuyển vị trí {headline.lower()}."
#         last_interaction = datetime(2025, 7, random.randint(1, 23), random.randint(8, 18), random.randint(0, 59))

#         sample_data.append({
#             "Full Name": name,
#             "Email": email,
#             "Phone": phone,
#             "DOB": dob,
#             "Avatar": "",
#             "Headline": headline,
#             "Source": source,
#             "Link CV": link_cv,
#             "Profile Data": "",
#             "Skills": str(skills),
#             "AI Summary": ai_summary,
#             "Status": "NEW",
#             "Last Interaction": None,
#             "Email Opt Out": 0
#         })

#     # Lưu thành file CSV
#     df = pd.DataFrame(sample_data)
#     df.to_csv("TalentProfiles_100_sample.csv", index=False)

#     print("Đã tạo file TalentProfiles_100_sample.csv thành công.")
