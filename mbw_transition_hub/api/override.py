import frappe
from frappe.model.db_query import DatabaseQuery

@frappe.whitelist()
def get_list_with_links(
    doctype,
    fields=None,
    filters=None,
    order_by=None,
    limit_start=0,
    limit_page_length=20,
    as_list=False,
    ignore_permissions=False
):
    """
    Override của frappe.client.get_list: tự động bổ sung dữ liệu từ các field kiểu Link.
    """

    # 1. Lấy danh sách bản ghi chính
    data = frappe.get_all(
        doctype,
        fields=fields,
        filters=filters,
        order_by=order_by,
        limit_start=limit_start,
        limit_page_length=limit_page_length,
        as_list=as_list,
        ignore_permissions=ignore_permissions,
    )

    # Nếu không yêu cầu lấy field hoặc không có dữ liệu → return luôn
    if not fields or not data:
        return data

    # 2. Lấy metadata để xác định các field kiểu Link
    meta = frappe.get_meta(doctype)
    link_fields = {
        df.fieldname: df.options
        for df in meta.fields
        if df.fieldtype == "Link" and df.fieldname in fields
    }

    # 3. Tập hợp dữ liệu từ các DocType liên kết
    for fieldname, linked_doctype in link_fields.items():
        link_ids = list({d.get(fieldname) for d in data if d.get(fieldname)})
        if not link_ids:
            continue

        linked_meta = frappe.get_meta(linked_doctype)
        title_field = "title" if linked_meta.has_field("title") else "name"

        linked_rows = frappe.get_all(
            linked_doctype,
            filters={"name": ["in", link_ids]},
            fields=["name", title_field],
        )

        # Mapping ID → title
        link_map = {r["name"]: r.get(title_field) for r in linked_rows}

        # Gán vào mỗi bản ghi
        for d in data:
            val = d.get(fieldname)
            if val:
                d[f"{fieldname}_title"] = link_map.get(val)

    return data

