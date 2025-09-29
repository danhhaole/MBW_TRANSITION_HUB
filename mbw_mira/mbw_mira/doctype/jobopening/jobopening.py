# Copyright (c) 2025, MBWCloud Co. and contributors
# For license information, please see license.txt

import frappe
import random
import string
from frappe.model.document import Document


class JobOpening(Document):
	def before_insert(self):
		"""Tự động sinh job_code khi tạo mới nếu chưa có"""
		if not self.job_code:
			self.job_code = self.generate_job_code()
	
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
