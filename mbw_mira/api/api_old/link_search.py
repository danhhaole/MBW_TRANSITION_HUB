import frappe
from frappe import _
import json
import re
from frappe.utils import cint, cstr, unique
from frappe.utils.data import make_filter_tuple
from frappe.model.db_query import get_order_by


# Backup logic từ core search.py
def build_for_autosuggest_custom(res, doctype, display_field=None):
    """
    Backup và cải tiến logic từ core build_for_autosuggest
    """
    def to_string(parts):
        return ", ".join(
            unique(_(cstr(part)) for part in parts if part)
        )

    results = []
    meta = frappe.get_meta(doctype)
    
    for item in res:
        item = list(item)
        
        # Luôn lấy name làm value
        value = item[0]
        
        # Xử lý description
        if len(item) > 1:
            # Nếu có display_field được chỉ định và khác name
            if display_field and len(item) >= 2:
                description = item[1] if item[1] != value else ""
            else:
                description = to_string(item[1:])
        else:
            description = ""
        
        # Tạo label (hiển thị chính)
        label = value
        
        autosuggest_row = {
            "value": value,
            "label": label,
            "description": description
        }
        
        results.append(autosuggest_row)
    
    return results


@frappe.whitelist()
def search_link_custom(
    doctype,
    txt="",
    display_field=None,
    filters=None,
    page_length=20,
    searchfield=None,
    ignore_user_permissions=False
):
    """
    Custom search link dựa trên logic core nhưng có thể chỉ định display_field
    
    Args:
        doctype: DocType cần search
        txt: Text tìm kiếm
        display_field: Field để hiển thị làm description
        filters: Filters để lọc dữ liệu
        page_length: Số lượng kết quả trả về
        searchfield: Field để search (mặc định là name)
        ignore_user_permissions: Bỏ qua permission check
    
    Returns:
        List of dict với format: {value: name, label: name, description: display_field_value}
    """
    
    if not doctype:
        return []
    
    # Parse filters
    if isinstance(filters, str):
        filters = json.loads(filters) if filters else []
    
    if not filters:
        filters = []
    
    # Validate doctype exists
    if not frappe.db.exists("DocType", doctype):
        frappe.throw(_("DocType {0} does not exist").format(doctype))
    
    # Get meta
    meta = frappe.get_meta(doctype)
    
    # Determine fields to fetch - luôn bắt đầu với name
    fields = ["name"]
    
    # Add display_field if specified and exists
    if display_field and meta.has_field(display_field):
        fields.append(display_field)
    else:
        # Auto detect display field based on doctype
        auto_field = get_auto_display_field(doctype, meta)
        if auto_field and meta.has_field(auto_field):
            fields.append(auto_field)
            display_field = auto_field
    
    # Determine search fields
    search_fields = ["name"]
    if searchfield and meta.has_field(searchfield):
        search_fields = [searchfield]
    elif meta.search_fields:
        search_fields.extend([f.strip() for f in meta.search_fields.split(",")])
    
    # Add search fields to fetch fields if not already included
    for field in search_fields:
        if field not in fields and meta.has_field(field):
            fields.append(field)
    
    # Convert string filters to proper format
    if isinstance(filters, dict):
        filters = [make_filter_tuple(doctype, key, value) for key, value in filters.items()]
    
    # Build or_filters for search
    or_filters = []
    if txt:
        field_types = {
            "Data",
            "Text", 
            "Small Text",
            "Long Text",
            "Link",
            "Select",
            "Read Only",
            "Text Editor",
        }
        
        for field in search_fields:
            if meta.has_field(field):
                fmeta = meta.get_field(field)
                if fmeta and fmeta.fieldtype in field_types:
                    or_filters.append([doctype, field, "like", f"%{txt}%"])
    
    # Add standard filters
    if meta.has_field("enabled"):
        filters.append([doctype, "enabled", "=", 1])
    if meta.has_field("disabled"):
        filters.append([doctype, "disabled", "!=", 1])
    
    # Format fields for query
    formatted_fields = [f"`tab{meta.name}`.`{f.strip()}`" for f in fields]
    
    # Check permissions
    ignore_permissions = ignore_user_permissions and frappe.has_permission(
        doctype, "read"
    )
    
    # Order by
    order_by_based_on_meta = get_order_by(doctype, meta)
    order_by = f"`tab{doctype}`.idx desc, {order_by_based_on_meta}"
    
    # Add relevance sorting if searching
    if txt and not meta.get("translated_doctype"):
        _txt = frappe.db.escape((txt or "").replace("%", "").replace("@", ""))
        _relevance = f"(1 / nullif(locate({_txt}, `tab{doctype}`.`name`), 0))"
        formatted_fields.append(f"""{_relevance} as `_relevance`""")
        
        if frappe.db.db_type == "mariadb":
            order_by = f"ifnull(_relevance, -9999) desc, {order_by}"
        elif frappe.db.db_type == "postgres":
            order_by = f"{len(formatted_fields)} desc nulls last, {order_by}"
    
    try:
        # Get data using frappe.get_list
        values = frappe.get_list(
            doctype,
            filters=filters,
            fields=formatted_fields,
            or_filters=or_filters if txt else None,
            limit_page_length=page_length,
            order_by=order_by,
            ignore_permissions=ignore_permissions,
            as_list=True,
            strict=False,
        )
        
        # Remove _relevance column if exists
        if txt and not meta.get("translated_doctype"):
            values = [r[:-1] for r in values]
        
        # Build results for autosuggest
        results = build_for_autosuggest_custom(values, doctype, display_field)
        
        return results
        
    except Exception as e:
        frappe.log_error(f"Error in search_link_custom: {str(e)}")
        return []


def get_auto_display_field(doctype, meta):
    """Auto detect display field based on doctype"""
    
    # DocType specific mappings
    doctype_fields = {
        "User": "full_name",
        "Customer": "customer_name", 
        "Supplier": "supplier_name",
        "Company": "company_name",
        "Item": "item_name",
        "Project": "project_name",
        "Campaign": "campaign_name",
        "Employee": "employee_name",
        "Contact": "full_name",
        "Address": "address_title",
        "Territory": "territory_name",
        "Sales Order": "title",
        "Purchase Order": "title",
        "Lead": "lead_name",
        "Opportunity": "title"
    }
    
    if doctype in doctype_fields:
        field = doctype_fields[doctype]
        if meta.has_field(field):
            return field
    
    # Check for title field
    if meta.title_field and meta.has_field(meta.title_field):
        return meta.title_field
    
    # Common fallback fields
    common_fields = ["title", "full_name", "description", "subject", "customer_name", "supplier_name"]
    for field in common_fields:
        if meta.has_field(field):
            return field
    
    return None


@frappe.whitelist()
def get_doctype_display_fields(doctype):
    """Get available display fields for a doctype"""
    
    if not frappe.db.exists("DocType", doctype):
        return []
    
    meta = frappe.get_meta(doctype)
    
    # Get text/data fields that could be used as display fields
    display_fields = []
    
    for field in meta.fields:
        if field.fieldtype in ["Data", "Text", "Small Text", "Text Editor"] and field.fieldname != "name":
            display_fields.append({
                "fieldname": field.fieldname,
                "label": field.label or field.fieldname
            })
    
    return display_fields 