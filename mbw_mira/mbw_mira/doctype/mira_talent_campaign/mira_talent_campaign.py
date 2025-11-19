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
    Kiểm tra xem đã tồn tại Mira Talent Campaign với cùng
    talent_id + campaign_id (ngoại trừ chính nó) hay chưa.
    """
    filters = {
        "talent_id": doc.talent_id,
        "campaign_id": doc.campaign_id,
    }

    existing = frappe.db.exists("Mira Talent Campaign", filters)

    if existing and existing != doc.name:
        frappe.throw(
            frappe._(
                "A Mira Talent Campaign with Campaign <b>{0}</b> and Candidate <b>{1}</b> already exists: <a href='/app/candidate-campaign/{2}'>{2}</a>"
            ).format(doc.campaign_id, doc.talent_id, existing),
            title=frappe._("Duplicate Mira Talent Campaign"),
        )

