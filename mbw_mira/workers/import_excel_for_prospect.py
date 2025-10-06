import frappe
import pandas as pd
import json
import ast
from datetime import datetime

def import_prospect_from_file(campaign_name: str):
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
        frappe.log_error("Import Talent", f"Campaign not found: {campaign_name}")
        return

    # 2. Kiểm tra trạng thái hợp lệ
    today = datetime.today().date()
    if not campaign.is_active or campaign.status != "ACTIVE" \
            or not campaign.start_date or not campaign.end_date \
            or campaign.start_date > today or campaign.end_date < today:
        frappe.log_error("Import Talent", f"Campaign is not active or out of range: {campaign_name}")
        return

    # 3. Parse source_config JSON
    try:
        source_config = json.loads(campaign.source_config or "{}")
    except Exception as e:
        frappe.log_error("Import Talent", f"Failed to parse source_config JSON: {e}")
        return

    file_name = campaign.source_file.split("/")[-1]
    field_mapping = source_config.get("field_mapping", [])

    if not file_name or not field_mapping:
        frappe.log_error("Import Talent", f"Missing file name or field mapping for campaign: {campaign_name}")
        return

    # 4. Tìm file đã upload trong File doctype
    file_url = frappe.db.get_value("File", {"file_name": file_name}, "file_url")
    if not file_url:
        frappe.log_error("Import Talent", f"File not found in File doctype: {file_name}")
        return

    file_path = frappe.get_site_path("public", file_url.lstrip("/"))

    # 5. Đọc file bằng pandas
    try:
        if file_name.endswith(".csv"):
            df = pd.read_csv(file_path)
        elif file_name.endswith((".xls", ".xlsx")):
            df = pd.read_excel(file_path)
        else:
            frappe.log_error("Import Talent", f"Unsupported file format: {file_name}")
            return

        df = df.where(pd.notnull(df), None)  # Convert NaN thành None
    except Exception as e:
        frappe.log_error("Import Talent", f"Error reading file {file_name}: {e}")
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
            skills_value = raw_data.get("skills") or ""
            if isinstance(skills_value, list):
                skills_text = ", ".join(skills_value)
            elif isinstance(skills_value, str):
                try:
                    parsed = json.loads(skills_value)
                    if isinstance(parsed, list):
                        skills_text = ", ".join(parsed)
                    else:
                        skills_text = skills_value
                except:
                    try:
                        parsed = ast.literal_eval(skills_value)
                        if isinstance(parsed, list):
                            skills_text = ", ".join(parsed)
                        else:
                            skills_text = skills_value
                    except:
                        skills_text = skills_value
            else:
                skills_text = ""
            def parse_json_field(val):
                if not val:
                    return "[]"
                if isinstance(val, (list, dict)):
                    return json.dumps(val, ensure_ascii=False)
                if isinstance(val, str):
                    try:
                        parsed = json.loads(val)
                        return json.dumps(parsed, ensure_ascii=False)
                    except:
                        try:
                            parsed = ast.literal_eval(val)
                            return json.dumps(parsed, ensure_ascii=False)
                        except:
                            return "[]"
                return "[]"
            # 8. Chuẩn bị dữ liệu cho Mira Contact mới
            doc_data = {
                "doctype": "Mira Talent",
                "full_name": raw_data.get("full_name"),
                "gender": raw_data.get("gender"),
                "date_of_birth": raw_data.get("date_of_birth"),
                "contact_email": raw_data.get("contact_email"),
                "contact_phone": raw_data.get("contact_phone"),
                "linkedin_profile": raw_data.get("linkedin_profile"),
                "facebook_profile": raw_data.get("facebook_profile"),
                "zalo_profile": raw_data.get("zalo_profile"),
                "current_location": raw_data.get("current_location"),
                "preferred_location": raw_data.get("preferred_location"),
                "skills": skills_text,
                "experience_years": raw_data.get("experience_years"),
                "education": parse_json_field(raw_data.get("education")),
                "experience": parse_json_field(raw_data.get("experience")),
                "certifications": parse_json_field(raw_data.get("certifications")),
                "languages": parse_json_field(raw_data.get("languages")),
                "resume": raw_data.get("resume"),
                "current_status": raw_data.get("current_status") or "Active",
                "talent_pool": raw_data.get("talent_pool"),
                "notes": raw_data.get("notes") or ""
            }

            # 6. Insert nếu chưa tồn tại
            try:
                if not check_talent_exists(raw_data.get("contact_email")):
                    doc = frappe.get_doc(doc_data)
                    doc.insert(ignore_permissions=True)
                    frappe.db.commit()
                    inserted += 1
            except Exception as e:
                frappe.log_error("Failed to insert Talent", f"{doc_data.get('full_name')} — {e}")

        # 10. Gửi sự kiện realtime nếu cần
        frappe.publish_realtime('import_Prospect_from_file', message={'campaign': campaign_name})
        logger.info(f"Imported {inserted} profiles for campaign {campaign_name}")
        return True


def check_talent_exists(email):
    if not email:
        return False
    return frappe.db.exists("Mira Talent", {"contact_email": email}) is not None