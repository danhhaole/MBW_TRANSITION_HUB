# Copyright (c) 2025, MBWCloud Co. and contributors
# For license information, please see license.txt

import frappe
import random
import string
from frappe.model.document import Document


class ShortURL(Document):
	pass

	def validate(self):
		duplicate_long_url(self.long_url)
	def before_insert(self):
		self.short_code = generate_short_code(10)


def duplicate_long_url(url):
    short_exists = frappe.db.exists("Short URL",{"long_url":url})
    if short_exists:
        frappe.throw("Duplicate Short URL")        
    

def generate_short_code(length=6):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length)).lower()

def shorten_url(long_url):
    doc = frappe.get_doc({
        "doctype": "Short URL",
        "short_code": "",
        "long_url": long_url
    })
    doc.insert(ignore_permissions=True)

    return f"/s/{doc.short_code}"