# Copyright (c) 2025, MBWCloud Co. and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe.utils import now

class TalentActivityLog(Document):
	pass


@frappe.whitelist()
def create_talent_activity_log(
    talent_id,
    activity_type,
    subject=None,
    description=None,
    campaign_id=None,
    interaction_id=None,
    recruiter_id=None,
    score_change=None,
    trigger_type=None,
    is_system_generated=0,
    source=None,
    reference_doctype=None,
    reference_name=None,
    meta_json=None
):
    """Create a unified talent activity log"""

    doc = frappe.get_doc({
        "doctype": "Talent Activity Log",
        "talent_id": talent_id,
        "activity_type": activity_type,
        "subject": subject,
        "description": description,
        "campaign_id": campaign_id,
        "interaction_id": interaction_id,
        "recruiter_id": recruiter_id or frappe.session.user,
        "score_change": score_change,
        "trigger_type": trigger_type,
        "is_system_generated": is_system_generated,
        "source": source,
        "reference_doctype": reference_doctype,
        "reference_name": reference_name,
        "meta_json": meta_json,
        "date": now()
    })

    doc.insert(ignore_permissions=True)
    frappe.db.commit()

    return doc.name