import frappe
import pandas as pd
import json
from datetime import datetime
import os

def import_candidates_from_file(campaign_id: str):
    logger = frappe.logger("import_candidates")

    # 1. Lấy thông tin campaign
    campaign = frappe.db.get_value(
        "Campaign",
        campaign_id,
        ["campaign_name", "is_active", "status", "start_date", "end_date", "target_segment","source_file", "source_config"],
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
        logger.warning(f"Campaign '{campaign.campaign_name}' is not currently valid for import")
        return

    # 3. Parse source_config JSON
    try:
        source_config = json.loads(campaign.source_config or "{}")
    except Exception as e:
        logger.error(f"Failed to parse source_config JSON: {e}", exc_info=True)
        return

    file_name = campaign.source_file.split("/").pop()
    field_mapping = source_config.get("field_mapping", [])

    if not file_name or not field_mapping:
        logger.warning(f"Campaign '{campaign.campaign_name}' is missing file_name or field_mapping in source_config")
        return

    # 4. Tìm file đã upload trong File doctype
    file_url = frappe.db.get_value("File", {"file_name": file_name}, "file_url")
    if not file_url:
        logger.warning(f"File not found in File doctype: {file_name}")
        return

    file_path = frappe.get_site_path("public", file_url.lstrip("/"))

    # 5. Đọc file bằng pandas
    try:
        if file_name.endswith(".csv"):
            df = pd.read_csv(file_path)
        elif file_name.endswith((".xls", ".xlsx")):
            df = pd.read_excel(file_path)
        else:
            logger.warning(f"Unsupported file format: {file_name}")
            return
    except Exception as e:
        logger.error(f"Error reading file {file_name}: {str(e)}", exc_info=True)
        return


    inserted = 0
    if df and df.iterrows():
        for _, row in df.iterrows():
            # 6. Map dữ liệu theo cấu hình
            raw_data = {}
            for mapping in field_mapping:
                source_col = mapping.get("column_name")
                target_field = mapping.get("field_name")
                raw_data[target_field] = row.get(source_col)

                    # 7. Chuẩn hóa field cho TalentPool
            doc_data = {
                "doctype": "TalentPool",
                "full_name": raw_data.get("full_name"),
                "email": raw_data.get("email"),
                "phone": raw_data.get("phone"),
                "source": raw_data.get("source") or "Excel Import",
                "skills": raw_data.get("skills") or "",  # CHỈ sửa dòng này
                "location": raw_data.get("location"),
                "experience_years": float(raw_data.get("experience_years") or 0),
                "current_position": raw_data.get("current_position") or raw_data.get("major_id"),
                "status": raw_data.get("status") if raw_data.get("status") in ["Active", "Inactive"] else "Inactive",
                "campaign_id": campaign_id,
                "segment_id": campaign.target_segment,
                "synced_at": datetime.now(),
                "notes": raw_data.get("notes")
            }


            # 8. Insert
            try:
                doc = frappe.get_doc(doc_data)
                doc.insert()
                frappe.db.commit()
                logger.info(f"[TalentPool] Inserted: {doc.full_name} / {doc.email}")
                inserted += 1
            except Exception as e:
                logger.error(f"[TalentPool] Failed: {doc_data.get('full_name')} — {str(e)}", exc_info=True)

        logger.info(f"[TalentPool] Total inserted from '{file_name}': {inserted}")

