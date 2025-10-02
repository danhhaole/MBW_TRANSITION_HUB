# Copyright (c) 2025, MBWCloud Co. and contributors
# For license information, please see license.txt

import frappe
import random
import string
from frappe.model.document import Document
import unicodedata,re
from frappe import _
import frappe.utils
import json

class JobOpening(Document):
	def before_insert(self):
		"""Tự động sinh các giá trị mặc định khi tạo mới"""
		# Tạo job_code nếu chưa có
		if not self.job_code:
			self.job_code = self.generate_job_code()
		
		# Tạo job_url_cms từ job_title nếu chưa có
		if self.job_title and not self.job_url_cms:
			base_slug = to_slug(self.job_title)
			self.job_url_cms = self.generate_unique_slug(base_slug)

	def generate_unique_slug(self, base_slug):
		"""Tạo slug duy nhất cho job_url_cms"""
		slug = base_slug
		count = 1
		
		# Kiểm tra xem slug đã tồn tại chưa
		while frappe.db.exists("JobOpening", {"job_url_cms": slug, "name": ["!=", self.name or ""]}):
			slug = f"{base_slug}-{count}"
			count += 1
		
		return slug
	
	def generate_job_code(self):
		"""Tạo mã công việc duy nhất"""
		def create_code():
			# Tạo mã với format: JO + năm (2 chữ số cuối) + tháng + ngày + mã ngẫu nhiên 4 ký tự
			year_month_day = frappe.utils.now_datetime().strftime('%y%m%d')
			random_suffix = ''.join(random.choices(string.ascii_uppercase + string.digits, k=4))
			return f"JO{year_month_day}{random_suffix}"
		
		# Đảm bảo mã không trùng lặp
		max_attempts = 10
		for attempt in range(max_attempts):
			code = create_code()
			if not frappe.db.exists("Job Opening", {"job_code": code}):
				return code
		
		# Nếu vẫn trùng sau max_attempts, thêm timestamp
		timestamp = int(frappe.utils.time.time())
		return create_code() + str(timestamp)[-4:]


def to_slug(text: str) -> str:
    # Chuẩn hóa Unicode (NFD tách dấu)
    text = unicodedata.normalize("NFD", text)
    # Bỏ dấu (loại bỏ ký tự combining marks)
    text = "".join([c for c in text if not unicodedata.combining(c)])
    # Thay thế đ/Đ
    text = text.replace("đ", "d").replace("Đ", "D")
    # Chuyển lowercase
    text = text.lower()
    # Bỏ ký tự không phải chữ cái, số, khoảng trắng, hoặc -
    text = re.sub(r"[^a-z0-9\s-]", "", text)
    # Thay khoảng trắng, _ và nhiều dấu - thành 1 dấu -
    text = re.sub(r"[\s\-_]+", "-", text)
    # Bỏ dấu - ở đầu và cuối
    text = text.strip("-")
    return text