# Copyright (c) 2025, MBWCloud Co. and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe.utils import now
from mbw_mira.utils import find_candidates_fuzzy

class Campaign(Document):
	pass

	def on_update(self):
		"""Hook kiểm tra khi có 1 campain
		"""
def process_campaign_from_candidate():
	campaigns = _get_active_campaigns()

def process_campaign_active():
	"""Lấy danh sách Campaign active hiệu lực
		Kiểm tra thông tin phân khúc lấy ra candidate theo phân khúc
		Nếu có phân khúc được lưu từ talentsegment thì ưu tiên và tìm ứng viên theo phân khúc này, sau đó thêm vào CandidateSegment
		Nếu chỉ có mô tả tiêu chỉ trong campaign thì quét tim
	"""
	from mbw_mira.utils import find_candidates_fuzzy
	campaigns = _get_active_campaigns()

	if not campaigns:
		frappe.logger("campaign").info("[SKIP] No active campaigns found.")
		return

	for campaign in campaigns:
		if not campaign.target_segment:
			frappe.logger("campaign").info(f"[SKIP] Campaign {campaign} has no target segment.")
			continue

		# Mỗi campaign sẽ có thông tin segment,
		# lấy danh sách candidate từ CandidateSegment
		#candidate_ids = candidate_segment_by_campaign(campaign.target_segment)

		#Lấy danh sách Candidate từ AI 
		candidate_ids = []
		candidate_segments = find_candidates_fuzzy(campaign.target_segment)
		if candidate_segments:
			candidate_ids = [s.get("candidate_name") for s in candidate_segments]
		
		if not candidate_ids:
			frappe.logger("campaign").info(f"[SKIP] No candidates found for segment {campaign.target_segment}.")
			continue
		print("=======================handle_candidate_segment============================= ",campaign.target_segment)
		# Insert vào CandidateSegment
		frappe.enqueue(
			"mbw_mira.services.candidate_service.insert_candidate_segment",
			queue="default",
			timeout=300,
			candidates=candidate_ids,
			segment=campaign.target_segment,
			campaign= campaign.name,
			job_name = "insert_candidate_segment"
		)


def _get_active_campaigns(source):
    """
    Lấy danh sách Campaign:
    - status = ACTIVE
    - is_active = 1
    - start_date <= hôm nay
    - end_date >= hôm nay
    """
    current_date = now()  # yyyy-mm-dd
    campaigns = frappe.get_all(
        "Campaign",
        filters={
            "status": "ACTIVE",
            "is_active": 1,
            "start_date": ["<=", current_date],
            "end_date": [">=", current_date]
        },
        fields=[
            "name",
            "campaign_name",
            "start_date",
            "end_date",
            "status",
            "is_active",
            "target_segment"
        ],
        order_by="start_date asc"
    )

    return campaigns