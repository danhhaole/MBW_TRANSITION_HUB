# Copyright (c) 2025, MBWCloud Co. and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe.utils import now_datetime


class CandidateCampaign(Document):
    pass


@frappe.whitelist()
def process_candidate_campaign_active():
	"""Lấy danh sách CandidateCampaign
	- Kiểm tra bản ghi thỏa mãn điều kiện để tạo ra Action
	"""
	candidate_campaigns = _get_active_candidate_campaigns()
	action_names =[]
	for can_campaign in candidate_campaigns:
		segment = frappe.get_value(
			"Campaign", can_campaign.campaign_id, "target_segment"
		)
		if not segment:
			continue
		# Lấy step theo Campaign
		step = frappe.get_value(
			"CampaignStep",
			{
				"campaign": can_campaign.campaign_id,
				"step_order": can_campaign.current_step_order,
			},
			["*"],
			as_dict=1,
		)
		#Format status action để phân loại tự động hay thủ công
		status_action = (
			"SCHEDULED"
			if step.action_type in ["SEND_EMAIL", "SEND_SMS", "SEND_NOTIFICATION"]
			else "PENDING_MANUAL"
		)

		if action_exists(can_campaign,step):
			action = frappe.new_doc("Action")
			action.update({
                "candidate_campaign_id": can_campaign.name,
                "campaign_step": step.name,
                "status": status_action,
                "scheduled_at": now_datetime()
			})
			action.insert(ignore_permissions=True)
			action.reload()
			action_names.append(action.name)
	return action_names
		
        
def action_exists(doc,step):
    action_exists = frappe.db.exists("Action",{"candidate_campaign_id":doc.name,"campaign_step":step.name})
    if action_exists:
        return True
    else:
        return False


def _get_active_candidate_campaigns() -> dict:
    """
    Lấy danh sách CandidateCampaign:
    - status = ACTIVE
    - next_action_at <= hôm nay
    """

    candidate_campaigns = frappe.get_all(
        "CandidateCampaign",
        filters={"status": "ACTIVE", "next_action_at": ["<=", now_datetime()]},
        fields=["*"],
    )

    return candidate_campaigns
