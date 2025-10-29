# Copyright (c) 2025, mbwcloud.com and contributors
# For license information, please see license.txt

import frappe
import secrets
from datetime import datetime, timedelta
from frappe.model.document import Document


class MiraAccessToken(Document):
	pass

def create_token(talent: str, validity_hours: int = 24) -> str:
    """
    Tạo token bảo mật cho ứng viên làm bài test.
    """
    token = secrets.token_urlsafe(32)

    ip = frappe.local.request_ip
    #user_agent = frappe.request.headers.get("User-Agent")

    doc = frappe.get_doc({
        "doctype": "Mira Access Token",
        "talent": talent,
        "token": token,
        "expiry_date": datetime.now() + timedelta(hours=validity_hours),
        "ip_address": ip or "",
        "user_agent": "",
        "is_used": 0
    })
    doc.insert(ignore_permissions=True)
    frappe.db.commit()
    return token

def validate_test_token(token: str) -> dict:
    """
    Kiểm tra token truy cập bài thi.
    Trả về dict chứa thông tin nếu hợp lệ, hoặc raise lỗi.
    """
    token_doc = frappe.get_all(
        "Mira Access Token",
        filters={
            "token": token,
            "is_used": 0
        },
        fields=["name", "talent", "expiry_date"]
    )

    if not token_doc:
        frappe.throw("Token không hợp lệ.")
        return

    token_doc = token_doc[0]

    if token_doc.expiry_date < frappe.utils.now_datetime():
        frappe.throw("Token đã hết hạn.")

    return token_doc