# Copyright (c) 2025, MBWCloud Co. and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe.utils import now, now_datetime, add_days
from mbw_mira.utils import find_candidates_fuzzy

class Campaign(Document):
	pass

	def on_update(self):
		"""Hook kiểm tra khi có 1 campain
		"""
#Lấy Step từ CampaignStep, lấy step đầu tiên
def get_campaign_step(campaign_id):
    step = frappe.get_list(
        "CampaignStep",
        filters={"campaign": campaign_id},
        fields=[
            "*",
        ],
        order_by="step_order asc",
        page_length=1,
    )
    if step:
        return step[0]
    else:
        return None

#Lấy thông tin source kết nối để thực hiện đồng bộ nếu đã kết nối
def get_datasource(source_id):
	source = frappe.get_cached_doc("CandidateDataSource",{"name":source_id,"is_active":1})
	if source:
		return source
	else:
		return None

def _get_active_campaigns(source):
    """
    Lấy danh sách Campaign:
    - status = ACTIVE
    - is_active = 1
    - start_date <= hôm nay
    - end_date >= hôm nay
    - source: ATS / JobBoard / SocialNetwork / Manual / Other
    """
    current_date = now()  # yyyy-mm-dd
    campaigns = frappe.get_list(
        "Campaign",
        filters={
            "status": "ACTIVE",
            "is_active": 1,
            "source":source,
            "start_date": ["<=", current_date],
            "end_date": [">=", current_date]
        },
        fields=[
            "*"            
        ],
        order_by="start_date asc"
    )

    return campaigns