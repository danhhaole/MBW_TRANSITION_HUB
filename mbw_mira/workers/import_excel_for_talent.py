import frappe
import pandas as pd
import json
from datetime import datetime
import os

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
        logger.error(f"Campaign not found: {campaign_name}")
        return

    # 2. Kiểm tra trạng thái hợp lệ
    today = datetime.today().date()
    if not campaign.is_active or campaign.status != "ACTIVE" \
            or not campaign.start_date or not campaign.end_date \
            or campaign.start_date > today or campaign.end_date < today:
        return

    # 3. Parse source_config JSON
    try:
        source_config = json.loads(campaign.source_config or "{}")
    except Exception as e:
        logger.error(f"Failed to parse source_config JSON: {e}", exc_info=True)
        return

    file_name = campaign.source_file.split("/")[-1]
    field_mapping = source_config.get("field_mapping", [])

    if not file_name or not field_mapping:
        return

    # 4. Tìm file đã upload trong File doctype
    file_url = frappe.db.get_value("File", {"file_name": file_name}, "file_url")
    if not file_url:
        return

    file_path = frappe.get_site_path("public", file_url.lstrip("/"))

    # 5. Đọc file bằng pandas
    try:
        if file_name.endswith(".csv"):
            df = pd.read_csv(file_path)
        elif file_name.endswith((".xls", ".xlsx")):
            df = pd.read_excel(file_path)
        else:
            return
    except Exception as e:
        logger.error(f"Error reading file {file_name}: {str(e)}", exc_info=True)
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

            # 7. Chuẩn hóa dữ liệu theo TalentProfiles mới
            skills_raw = json.loads(raw_data.get("skills"),[])
            if isinstance(skills_raw, str):
                skills_list = [skill.strip() for skill in skills_raw.split(",") if skill.strip()]
            elif isinstance(skills_raw, list):
                skills_list = skills_raw
            else:
                skills_list = []

            # status_map = {
            #     "Ứng tuyển": "ENGAGED",
            #     "Tiềm năng": "NURTURING",
            #     "Mới": "NEW",
            #     "Đã liên hệ": "SOURCED",
            #     "Không phù hợp": "ARCHIVED",
            #     "Active": "ENGAGED",
            #     "Inactive": "ARCHIVED"
            # }
            status = "NEW"

            doc_data = {
                "doctype": "TalentProfiles",
                "full_name": raw_data.get("full_name"),
                "email": raw_data.get("email"),
                "phone": raw_data.get("phone"),
                "source": raw_data.get("source") or "Excel Import",
                "skills": json.dumps(skills_list),
                "avatar": raw_data.get("avatar"),
                "headline": raw_data.get("current_position") or raw_data.get("major_id"),
                "cv_original_url": raw_data.get("cv_original_url"),
                "profile_data": raw_data.get("profile_data"),  # đảm bảo đây là JSON string hoặc dict
                "ai_summary": raw_data.get("notes"),
                "status": status,
                "last_interaction": datetime.now(),
                "email_opt_out": int(raw_data.get("email_opt_out") or 0)
            }

            # 8. Insert
            try:
                if not check_exists(raw_data.get("email")):
                    doc = frappe.get_doc(doc_data)
                    doc.insert(ignore_permissions=True)
                    frappe.db.commit()
                    inserted += 1
                else:
                    continue
            except Exception as e:
                logger.error(f"[TalentProfiles] Failed: {doc_data.get('full_name')} — {str(e)}", exc_info=True)
        frappe.publish_realtime('import_talentprofile_from_file', message={'campaign': campaign_name})
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
