# Copyright (c) 2025, MBWCloud Co. and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe.utils import now_datetime


class MiraTalentCampaign(Document):
    pass

    def validate(self):
        # Check trùng talent_id + campaign_id
        validate_unique_candidate_campaign(self)


def validate_unique_candidate_campaign(doc):
    """
    Kiểm tra xem đã tồn tại MiraTalentCampaign với cùng
    talent_id + campaign_id (ngoại trừ chính nó) hay chưa.
    """
    filters = {
        "talent_id": doc.talent_id,
        "campaign_id": doc.campaign_id,
    }

    existing = frappe.db.exists("MiraTalentCampaign", filters)

    if existing and existing != doc.name:
        frappe.throw(
            frappe._(
                "A MiraTalentCampaign with Campaign <b>{0}</b> and Candidate <b>{1}</b> already exists: <a href='/app/candidate-campaign/{2}'>{2}</a>"
            ).format(doc.campaign_id, doc.talent_id, existing),
            title=frappe._("Duplicate MiraTalentCampaign"),
        )


@frappe.whitelist()
def process_candidate_campaign_active():
    """Lấy danh sách MiraTalentCampaign
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
    Lấy danh sách MiraTalentCampaign:
    - status = ACTIVE
    - next_action_at <= hôm nay
    """

    candidate_campaigns = frappe.get_all(
        "MiraTalentCampaign",
        filters={"status": "ACTIVE", "next_action_at": ["<=", now_datetime()]},
        fields=["*"],
    )

    return candidate_campaigns
