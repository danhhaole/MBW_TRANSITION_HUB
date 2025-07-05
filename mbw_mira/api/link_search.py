import frappe
from frappe import _


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
    Custom search link với khả năng chỉ định field hiển thị
    
    Args:
        doctype: DocType cần search
        txt: Text tìm kiếm
        display_field: Field để hiển thị làm description (vd: full_name, title, etc.)
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
        import json
        filters = json.loads(filters) if filters else []
    
    if not filters:
        filters = []
    
    # Validate doctype exists
    if not frappe.db.exists("DocType", doctype):
        frappe.throw(_("DocType {0} does not exist").format(doctype))
    
    # Get meta
    meta = frappe.get_meta(doctype)
    
    # Determine fields to fetch
    fields = ["name"]
    
    # Add display_field if specified and exists
    if display_field:
        if meta.has_field(display_field):
            fields.append(display_field)
        else:
            # Fallback to common fields
            common_fields = ["title", "full_name", "description", "subject"]
            for field in common_fields:
                if meta.has_field(field):
                    fields.append(field)
                    display_field = field
                    break
    else:
        # Auto detect display field based on doctype
        display_field = get_auto_display_field(doctype, meta)
        if display_field and meta.has_field(display_field):
            fields.append(display_field)
    
    # Determine search fields
    search_fields = ["name"]
    if searchfield and meta.has_field(searchfield):
        search_fields = [searchfield]
    elif meta.search_fields:
        search_fields.extend([f.strip() for f in meta.search_fields.split(",")])
    
    # Add search fields to fetch fields
    for field in search_fields:
        if field not in fields and meta.has_field(field):
            fields.append(field)
    
    # Remove duplicates
    fields = list(set(fields))
    
    # Build or_filters for search
    or_filters = []
    if txt:
        for field in search_fields:
            if meta.has_field(field):
                or_filters.append([doctype, field, "like", f"%{txt}%"])
    
    # Add standard filters
    if meta.has_field("enabled"):
        filters.append([doctype, "enabled", "=", 1])
    if meta.has_field("disabled"):
        filters.append([doctype, "disabled", "!=", 1])
    
    # Check permissions
    ignore_permissions = ignore_user_permissions and frappe.has_permission(
        doctype, "read"
    )
    
    try:
        # Get data
        data = frappe.get_list(
            doctype,
            fields=fields,
            filters=filters,
            or_filters=or_filters if txt else None,
            limit_page_length=page_length,
            order_by="name asc",
            ignore_permissions=ignore_permissions
        )
        
        # Transform data
        results = []
        for item in data:
            result = {
                "value": item.name,
                "label": item.name
            }
            
            # Add description if display_field exists and different from name
            if display_field and display_field in item:
                desc_value = item[display_field]
                if desc_value and str(desc_value).strip() and str(desc_value) != item.name:
                    result["description"] = str(desc_value)
                else:
                    result["description"] = ""
            else:
                result["description"] = ""
            
            results.append(result)
        
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