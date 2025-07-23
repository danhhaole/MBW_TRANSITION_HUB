import frappe
import pandas as pd
import json
from datetime import datetime
import os

def import_talentprofile_from_file(campaign_id: str):
    logger = frappe.logger("import_candidates")

    # 1. Lấy thông tin campaign
    campaign = frappe.db.get_value(
        "Campaign",
        campaign_id,
        [
            "campaign_name", "is_active", "status",
            "start_date", "end_date", "target_segment",
            "source_file", "source_config"
        ],
        as_dict=True
    )

    if not campaign:
        logger.error(f"Campaign not found: {campaign_id}")
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
            skills_raw = raw_data.get("skills")
            if isinstance(skills_raw, str):
                skills_list = [skill.strip() for skill in skills_raw.split(",") if skill.strip()]
            elif isinstance(skills_raw, list):
                skills_list = skills_raw
            else:
                skills_list = []

            status_map = {
                "Ứng tuyển": "ENGAGED",
                "Tiềm năng": "NURTURING",
                "Mới": "NEW",
                "Đã liên hệ": "SOURCED",
                "Không phù hợp": "ARCHIVED",
                "Active": "ENGAGED",
                "Inactive": "ARCHIVED"
            }
            status = status_map.get(raw_data.get("status"), "NEW")

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
                doc = frappe.get_doc(doc_data)
                doc.insert(ignore_permissions=True)
                frappe.db.commit()
                inserted += 1
            except Exception as e:
                logger.error(f"[TalentProfiles] Failed: {doc_data.get('full_name')} — {str(e)}", exc_info=True)
        frappe.publish_realtime('import_talentprofile_from_file', message={'campaign': campaign_id})
        return True
