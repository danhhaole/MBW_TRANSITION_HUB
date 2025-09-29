import frappe
import pandas as pd
import json
import ast
from datetime import datetime

def import_talent_from_file(file_name: str, field_mapping: list, prospect_link_field="prospect"):
    """
    Import Mira Talent từ file CSV/XLSX.
    file_name: tên file (đã upload vào File Doctype).
    field_mapping: list[{column_name, field_name}]
    prospect_link_field: field liên kết đến Prospect nếu có (default="prospect")
    """
    logger = frappe.logger("import_talent")

    # 1. Tìm file đã upload
    file_url = frappe.db.get_value("File", {"file_name": file_name}, "file_url")
    if not file_url:
        frappe.log_error("Import Talent", f"File not found in File doctype: {file_name}")
        return

    file_path = frappe.get_site_path("public", file_url.lstrip("/"))

    # 2. Đọc file
    try:
        if file_name.endswith(".csv"):
            df = pd.read_csv(file_path)
        elif file_name.endswith((".xls", ".xlsx")):
            df = pd.read_excel(file_path)
        else:
            frappe.log_error("Import Talent", f"Unsupported file format: {file_name}")
            return
        df = df.where(pd.notnull(df), None)
    except Exception as e:
        frappe.log_error("Import Talent", f"Error reading file {file_name}: {e}")
        return

    inserted = 0
    if df is not None and not df.empty:
        for _, row in df.iterrows():
            # 3. Map dữ liệu
            raw_data = {}
            for mapping in field_mapping:
                source_col = mapping.get("column_name")
                target_field = mapping.get("field_name")
                raw_data[target_field] = row.get(source_col)

            # 4. Chuẩn hóa dữ liệu đặc biệt
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

            # 5. Chuẩn bị doc_data
            doc_data = {
                "doctype": "Mira Talent",
                "prospect": raw_data.get(prospect_link_field),
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

        logger.info(f"Imported {inserted} talents from {file_name}")
        return True


def check_talent_exists(email):
    if not email:
        return False
    return frappe.db.exists("Mira Talent", {"contact_email": email}) is not None
