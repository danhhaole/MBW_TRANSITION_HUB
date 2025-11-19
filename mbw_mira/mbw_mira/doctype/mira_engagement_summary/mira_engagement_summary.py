# Copyright (c) 2025, MBWCloud Co. and contributors
# For license information, please see license.txt

from datetime import datetime, timedelta
import random
import frappe
from frappe.model.document import Document
from frappe.utils import now_datetime

class MiraEngagementSummary(Document):
	pass


def fake_data():
    # Lấy tất cả talent_id từ Mira Talent
	talents = frappe.get_all("Mira Talent", fields=["name"])

	# Nếu không có talent nào thì dừng
	if not talents:
		frappe.throw("Chưa có dữ liệu Mira Talent để khớp!")

	# Số lượng bản ghi muốn tạo
	NUM_RECORDS = 50

	# Các lựa chọn cho select fields
	readiness_levels = ["Low", "Medium", "High"]
	top_channels = ["Email", "SMS", "WhatsApp", "LinkedIn", "Phone"]

	for _ in range(NUM_RECORDS):
		talent = random.choice(talents)

		first_interaction = datetime.now() - timedelta(days=random.randint(10, 180))
		last_interaction = first_interaction + timedelta(days=random.randint(0, 90))

		total_interactions = random.randint(1, 50)
		click_count = random.randint(0, total_interactions)
		open_count = random.randint(click_count, total_interactions)
		reply_count = random.randint(0, click_count)
		visit_count = random.randint(0, total_interactions)
		conversion_count = random.randint(0, visit_count)

		avg_days_between = (last_interaction - first_interaction).days / max(total_interactions, 1)

		doc = frappe.get_doc({
			"doctype": "Mira Engagement Summary",
			"talent_id": talent.name,
			"total_interactions": total_interactions,
			"total_score": random.randint(10, 500),
			"readiness_level": random.choice(readiness_levels),
			"first_interaction_at": first_interaction,
			"last_interaction_at": last_interaction,
			"engagement_timeline": (datetime.now() - first_interaction).days,
			"top_channel": random.choice(top_channels),
			"click_count": click_count,
			"open_count": open_count,
			"reply_count": reply_count,
			"visit_count": visit_count,
			"conversion_count": conversion_count,
			"avg_days_between_interactions": round(avg_days_between, 2),
			"recent_7d_score": random.randint(0, 50),
			"recent_30d_score": random.randint(0, 150),
			"bounce_rate": round(random.uniform(0, 1), 2)
		})
		doc.insert(ignore_permissions=True)
		# print(doc.name)
	frappe.db.commit()
