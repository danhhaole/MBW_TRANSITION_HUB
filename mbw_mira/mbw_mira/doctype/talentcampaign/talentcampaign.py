# Copyright (c) 2025, MBWCloud Co. and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe.utils import now_datetime


class TalentCampaign(Document):
    pass

    def validate(self):
        # Check trùng talent_id,candidate_id
        validate_unique_candidate_campaign(self)


def validate_unique_candidate_campaign(doc):
    """
    Kiểm tra xem đã tồn tại TalentCampaign với cùng
    talent_id + candidate_id (ngoại trừ chính nó) hay chưa.
    """
    filters = {
        "talent_id": doc.talent_id,
        "candidate_id": doc.candidate_id,
    }

    existing = frappe.db.exists("TalentCampaign", filters)

    if existing and existing != doc.name:
        frappe.throw(
            frappe._(
                "A TalentCampaign with Campaign <b>{0}</b> and Candidate <b>{1}</b> already exists: <a href='/app/candidate-campaign/{2}'>{2}</a>"
            ).format(doc.talent_id, doc.candidate_id, existing),
            title=frappe._("Duplicate TalentCampaign"),
        )


@frappe.whitelist()
def process_candidate_campaign_active():
    """Lấy danh sách TalentCampaign
    - Kiểm tra bản ghi thỏa mãn điều kiện để tạo ra Action
    """
    candidate_campaigns = _get_active_candidate_campaigns()
    action_names = []
    if candidate_campaigns:
        for can_campaign in candidate_campaigns:
            # Lấy step theo Campaign
            step = frappe.db.get_value(
                "CampaignStep",
                {
                    "campaign": can_campaign.campaign_id,
                    "step_order": can_campaign.current_step_order,
                },
                ["*"],
                as_dict=1,
            )
            # Format status action để phân loại tự động hay thủ công
            status_action = (
                "SCHEDULED"
                if step.action_type in ["SEND_EMAIL", "SEND_SMS", "SEND_NOTIFICATION"]
                else "PENDING_MANUAL"
            )

            action = frappe.new_doc("Action")
            action.update(
                {
                    "candidate_campaign_id": can_campaign.name,
                    "campaign_step": step.name,
                    "status": status_action,
                    "scheduled_at": now_datetime(),
                }
            )
            action.insert(ignore_permissions=True)
            action.reload()
            action_names.append(action.name)
    return action_names


def _get_active_candidate_campaigns() -> dict:
    """
    Lấy danh sách TalentCampaign:
    - status = ACTIVE
    - next_action_at <= hôm nay
    """

    candidate_campaigns = frappe.get_all(
        "TalentCampaign",
        filters={"status": "ACTIVE", "next_action_at": ["<=", now_datetime()]},
        fields=["*"],
    )

    return candidate_campaigns
