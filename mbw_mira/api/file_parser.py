import frappe
import pandas as pd
from frappe import _

@frappe.whitelist()
def parse_uploaded_file():
    form = frappe.local.form_dict
    file_name = form.get("file_name")
    meta_doctype = form.get("meta_doctype")  # Tên doctype cần import

    if not file_name:
        frappe.throw(_("Thiếu 'file_name' trong request."))

    if not meta_doctype:
        frappe.throw(_("Thiếu 'meta_doctype' trong request."))

    # Lấy file document
    file_doc = frappe.get_doc("File", {"file_name": file_name})
    if not file_doc:
        frappe.throw(_("Không tìm thấy file với tên: {0}").format(file_name))

    file_url = file_doc.file_url
    file_path = frappe.get_site_path("public", file_url.lstrip("/"))

    # Đọc file
    if file_name.endswith(".csv"):
        df = pd.read_csv(file_path)
    elif file_name.endswith((".xls", ".xlsx")):
        df = pd.read_excel(file_path)
    else:
        frappe.throw(_("Định dạng file không hỗ trợ."))

    headers = df.columns.tolist()
    rows = df.fillna("").values.tolist()

    # Meta column
    meta_columns = []
    for col in df.columns:
        meta_columns.append({
            "column": col,
            "dtype": str(df[col].dtype),
            "null_count": int(df[col].isnull().sum()),
            "sample_values": df[col].dropna().unique().tolist()[:5]
        })

    # Lấy metadata từ DocType đích để map
    try:
        meta = frappe.get_meta(meta_doctype)
    except frappe.DoesNotExistError:
        frappe.throw(_("Không tìm thấy DocType '{0}'").format(meta_doctype))

    target_fields = []
    for field in meta.fields:
        if field.fieldtype not in ["Section Break", "Column Break", "Tab Break", "HTML"]:
            target_fields.append({
                "fieldname": field.fieldname,
                "label": field.label,
                "fieldtype": field.fieldtype,
                "reqd": field.reqd
            })

    return {
        "headers": headers,
        "rows": rows,
        "meta_columns": meta_columns,
        "target_fields": target_fields
    }
