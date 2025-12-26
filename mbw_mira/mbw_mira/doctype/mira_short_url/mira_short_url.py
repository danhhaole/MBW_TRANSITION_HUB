# Copyright (c) 2025, MBWCloud Co. and contributors
# For license information, please see license.txt

import frappe
import random
import string
from frappe.model.document import Document

try:
    import gdshortener
    GD_SHORTENER_AVAILABLE = True
    frappe.log_error("gdshortener imported successfully", "gdshortener import success")
except ImportError as e:
    GD_SHORTENER_AVAILABLE = False
    frappe.log_error(f"gdshortener package not installed. Error: {str(e)}. Install it with: pip install gdshortener", "gdshortener import error")
except Exception as e:
    GD_SHORTENER_AVAILABLE = False
    frappe.log_error(f"Unexpected error importing gdshortener: {str(e)}", "gdshortener import error")


class MiraShortURL(Document):
	pass

	# def validate(self):
	# 	duplicate_long_url(self.long_url)
	# def before_insert(self):
	# 	self.short_code = generate_short_code(10)


def duplicate_long_url(url):
    short_exists = frappe.db.exists("Mira Short URL",{"long_url":url})
    if short_exists:
        frappe.throw("Duplicate Short URL")


# def generate_short_code(length=6):
#     return ''.join(random.choices(string.ascii_letters + string.digits, k=length)).lower()

@frappe.whitelist()
def shorten_url(long_url, short_url):
    # Check for duplicate long_url
    if frappe.db.exists("Mira Short URL", {"long_url": long_url}):
        existing_doc = frappe.get_doc("Mira Short URL", {"long_url": long_url})
        return {
            "success": False,
            "message": "Short URL đã tồn tại",
            "existing": True,
            "short_code": existing_doc.short_code,
            "short_url": short_url,  # Use the currenxisting_doc.name
        }
    short_code = short_url
    if short_url.startswith('http'):
        # Get the last part after the last slash
        short_code = short_url

    if frappe.db.exists("Mira Short URL", {"short_code": short_code}):
        existing_doc = frappe.get_doc("Mira Short URL", {"short_code": short_code})
        return {
            "success": False,
            "message": "Short code đã tồn tại",
            "existing": True,
            "short_code": existing_doc.short_code,
            "short_url": short_url,  # Return the current short_url
            "name": existing_doc.name
        }

    doc = frappe.get_doc({
        "doctype": "Mira Short URL",
        "short_code": short_code,  # Only save the extracted code
        "long_url": long_url
    })
    doc.insert(ignore_permissions=True)

    return {
        "short_code": doc.short_code,
        "short_url": short_url,  # Return the original short_url parameter
        "name": doc.name
    }


@frappe.whitelist()
def create_short_url_with_gdshortener(long_url):
    if not long_url:
        return {
            "success": False,
            "message": "Long URL is required",
            "short_url": None
        }
    
    # Thử import lại một lần nữa nếu chưa có
    gdshortener_module = None
    if not GD_SHORTENER_AVAILABLE:
        try:
            import gdshortener as gdshortener_module
            frappe.log_error("gdshortener imported successfully on retry", "gdshortener import retry success")
        except ImportError as e:
            frappe.log_error(f"gdshortener still not available on retry. Error: {str(e)}", "gdshortener import retry error")
            return {
                "success": False,
                "message": f"gdshortener package is not installed. Error: {str(e)}. Please install it with: pip install gdshortener and restart Frappe bench.",
                "short_url": None
            }
    else:
        gdshortener_module = gdshortener
    
    try:
        # Khởi tạo ISGDShortener
        s = gdshortener_module.ISGDShortener()
        
        # Tạo short URL (trả về tuple (short_url, None))
        result = s.shorten(url=long_url)
        
        # Lấy phần tử đầu tiên của tuple (short_url)
        if result and isinstance(result, tuple):
            short_url = result[0] if result[0] else None
        else:
            short_url = result
        
        # Loại bỏ khoảng trắng ở đầu/cuối
        if short_url:
            short_url = str(short_url).strip()
            return {
                "success": True,
                "short_url": short_url,
                "long_url": long_url
            }
        else:
            return {
                "success": False,
                "message": "Failed to create short URL",
                "short_url": None
            }
    except Exception as e:
        frappe.log_error(f"Error creating short URL with gdshortener: {str(e)}", "gdshortener error")
        return {
            "success": False,
            "message": f"Error creating short URL: {str(e)}",
            "short_url": None
        }
