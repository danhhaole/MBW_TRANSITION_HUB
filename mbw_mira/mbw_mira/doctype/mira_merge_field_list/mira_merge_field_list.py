# Copyright (c) 2025, mbwcloud.com and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class Mira_Merge_Field_List(Document):
	pass

@frappe.whitelist()
def get_merge_fields(template_type=None):
    """
    Lấy danh sách Merge Fields từ Doctype liên quan và Mira_Merge_Field
    Nếu không truyền template_type -> lấy tất cả các template_type
    """
    fields = []

    # 🔎 1️⃣ Lấy Merge Fields từ Mira_Merge_Field (tùy chỉnh)
    custom_fields = frappe.get_all("Mira_Merge_Field", fields=["field_name", "jinja_variable"])
    for field in custom_fields:
        fields.append({
            "name": field["field_name"],
            "jinja_variable": field["jinja_variable"]
        })

    # 🔎 2️⃣ Lấy danh sách Doctype liên quan từ bảng `Mira_Merge_Field_List`
    config_filters = {}
    if template_type:
        config_filters["template_type"] = template_type

    config_entries = frappe.get_all(
        "Mira_Merge_Field_List",
        filters=config_filters,
        fields=["name"]
    )

    if not config_entries:
        frappe.log_error("Không tìm thấy config nào cho template_type", "get_merge_fields")
        return fields  # Trả về danh sách rỗng nếu không có config

    for config in config_entries:
        doctype_entries = frappe.get_all(
            "Mira_Merger_Field_Doctype",
            filters={"parent": config.name},
            fields=["doctype_list"]
        )

        if not doctype_entries:
            frappe.log_error(f"Không tìm thấy doctype_list trong config {config.name}", "get_merge_fields")
            continue

        for entry in doctype_entries:
            doctype_name = entry.get("doctype_list")
            if not doctype_name:
                frappe.log_error(f"Lỗi: doctype_list bị None trong {config.name}", "get_merge_fields")
                continue

            try:
                meta = frappe.get_meta(doctype_name)
                for field in meta.fields:
                    # Bỏ qua các trường ID, name hoặc không cần thiết
                    if field.fieldtype in ["Data", "Select", "Date", "Datetime", "Int", "Float", "Text", "Small Text", "Long Text"]:
                        if any(kw in field.fieldname.lower() for kw in ["id", "status"]):
                            continue

                        fields.append({
                            "name": f"{field.label}",
                            "jinja_variable": f"{{{{ {field.fieldname} }}}}"
                        })
            except Exception as e:
                frappe.log_error(f"Lỗi khi lấy meta của {doctype_name}: {str(e)}", "get_merge_fields")

    return fields
