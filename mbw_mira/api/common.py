import frappe
import json
from frappe.utils import cstr, cint, flt, getdate, nowdate, get_datetime
from frappe import _

# List of field types that don't have values
no_value_fields = [
    "Section Break",
    "Column Break", 
    "HTML",
    "Table",
    "Button",
    "Image",
    "Fold"
]

@frappe.whitelist()
def get_list_data(
    doctype: str,
    filters=None,
    order_by: str = "modified desc",
    page_length=20,
    start=0,
    fields=None
):
    """
    Universal list data API for Mira project
    Simple list view with search, filters, pagination
    """
    try:
        filters = frappe._dict(filters or {})
        
        # Handle search conditions
        search_conditions = []
        if "search_text" in filters:
            search_conditions = filters.pop("search_text")
        
        # Process filter values
        for key in filters:
            value = filters[key]
            if isinstance(value, list):
                if "@me" in value:
                    value[value.index("@me")] = frappe.session.user
            elif value == "@me":
                filters[key] = frappe.session.user
        
        # Default fields if not specified
        if not fields:
            fields = ["name", "modified", "creation"]
        
        # Calculate start position
        start = cint(start)
        page_length = cint(page_length)
        
        # Get data with pagination
        data = frappe.get_list(
            doctype,
            fields=fields,
            filters=filters,
            or_filters=search_conditions,
            order_by=order_by,
            start=start,
            page_length=page_length,
        ) or []
        
        # Get total count for pagination
        total_count = len(frappe.get_list(doctype, filters=filters, or_filters=search_conditions))
        
        # Calculate pagination info
        current_page = (start // page_length) + 1 if page_length > 0 else 1
        total_pages = (total_count + page_length - 1) // page_length if page_length > 0 else 1
        has_next = current_page < total_pages
        has_prev = current_page > 1
        showing_from = start + 1 if total_count > 0 else 0
        showing_to = min(start + page_length, total_count)
        
        return {
            "success": True,
            "data": data,
            "total_count": total_count,
            "pagination": {
                "page": current_page,
                "limit": page_length,
                "total": total_count,
                "pages": total_pages,
                "has_next": has_next,
                "has_prev": has_prev,
                "showing_from": showing_from,
                "showing_to": showing_to
            }
        }
        
    except Exception as e:
        frappe.log_error(f"Error in get_list_data: {str(e)}")
        return {
            "success": False,
            "error": str(e),
            "data": [],
            "total_count": 0,
            "pagination": {
                "page": 1,
                "limit": page_length,
                "total": 0,
                "pages": 0,
                "has_next": False,
                "has_prev": False,
                "showing_from": 0,
                "showing_to": 0
            }
        }


@frappe.whitelist()
def get_form_data(doctype: str, name: str = None):
    """
    Get form data for create/edit
    """
    try:
        if name and name != "new":
            doc = frappe.get_doc(doctype, name)
            data = doc.as_dict()
        else:
            data = frappe.new_doc(doctype).as_dict()
        
        return {
            "success": True,
            "data": data
        }
        
    except Exception as e:
        frappe.log_error(f"Error in get_form_data: {str(e)}")
        return {
            "success": False,
            "error": str(e)
        }


@frappe.whitelist()
def save_doc(doctype: str, data, name: str = None):
    """
    Save document (create or update)
    """
    try:
        if isinstance(data, str):
            data = json.loads(data)
        
        if name and name != "new":
            doc = frappe.get_doc(doctype, name)
            doc.update(data)
        else:
            doc = frappe.new_doc(doctype)
            doc.update(data)
        
        doc.save()
        
        return {
            "success": True,
            "data": doc.as_dict(),
            "message": f"{doctype} {'updated' if name else 'created'} successfully"
        }
        
    except Exception as e:
        frappe.log_error(f"Error in save_doc: {str(e)}")
        return {
            "success": False,
            "error": str(e)
        }


@frappe.whitelist()
def delete_doc(doctype: str, name: str):
    """
    Delete document
    """
    try:
        frappe.delete_doc(doctype, name)
        
        return {
            "success": True,
            "message": f"{doctype} deleted successfully"
        }
        
    except Exception as e:
        frappe.log_error(f"Error in delete_doc: {str(e)}")
        return {
            "success": False,
            "error": str(e)
        }


@frappe.whitelist()
def get_filter_options(doctype: str, field: str):
    """
    Get filter options for a specific field
    """
    try:
        field_meta = frappe.get_meta(doctype).get_field(field)
        
        if field_meta.fieldtype == "Select":
            options = [{"label": option, "value": option} for option in field_meta.options.split("\n") if option]
        elif field_meta.fieldtype == "Link":
            options = frappe.get_all(field_meta.options, fields=["name as value", "name as label"])
        else:
            # Get unique values from database
            values = frappe.get_all(doctype, fields=[field], distinct=True, order_by=field)
            options = [{"label": v[field], "value": v[field]} for v in values if v[field]]
        
        return {"success": True, "options": options}
        
    except Exception as e:
        frappe.log_error(f"Error in get_filter_options: {str(e)}")
        return {"success": False, "options": []} 