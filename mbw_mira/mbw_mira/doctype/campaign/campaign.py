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

#Lấy danh sách ứng viên theo tiêu chí từ các nguồn, xử lý trong queue do quét nhiều ứng viên
def run_candidate_by_criteria(source,campaign:dict):
    criteria = campaign.get("criteria",{})
    segment_name = campaign.get("segment_name")
    candidates = find_candidates_fuzzy(source,criteria,segment_name)
    if candidates and len(candidates) > 0:
        for can in candidates:
            #Nếu chọn tiêu chỉ theo segment thì insert vào CandidateSegment
            can_seg = frappe.get_doc("CandidateSegment")
            can_seg.candidate_id = can.name
            can_seg.segment_id = segment_name
            can_seg.added_at = now_datetime()
            can_seg.added_by = frappe.session.user
            can_seg.save(ignore_permissions=True)
            frappe.db.commit()

            #Tạo CandidateCampaign
            step = get_campaign_step(campaign.name)
            if step:
                can_campaign = frappe.get_doc("CandidateCampaign")
                next_action_at = add_days(now_datetime, step["delay_in_days"] or 0)
                status = "ACTIVE"
                enrolled_at = now_datetime
                current_step_order = step["step_order"] or 1
                can_campaign.campaign_id = campaign.name
                can_campaign.candidate_id = can.name
                can_campaign.segment_id = segment_name or ""
                can_campaign.status = status
                can_campaign.enrolled_at = enrolled_at
                can_campaign.current_step_order = current_step_order
                can_campaign.next_action_at = next_action_at
                can_campaign.save(ignore_permissions=True)
                frappe.db.commit()
            else:
                continue
    return True
				

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