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
        return {
            "success": False,
            "message": "Short URL đã tồn tại",
            "existing": True
        }

    # Extract short_code from short_url (last part after /)
    short_code = short_url

    doc = frappe.get_doc({
        "doctype": "Mira Short URL",
        "short_code": short_code,
        "long_url": long_url
    })
    doc.insert(ignore_permissions=True)

    return {
        "short_code": doc.short_code,
        "short_url": short_url,
        "name": doc.name
    }
