# Copyright (c) 2025, MBWCloud Co. and contributors
# For license information, please see license.txt

import frappe
import random
import string
from frappe.model.document import Document


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
    # Extract short_code from external short_url (e.g., "https://is.gd/LvlCXj" -> "LvlCXj")
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
