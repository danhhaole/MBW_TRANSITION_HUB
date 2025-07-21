# Copyright (c) 2025, MBWCloud Co. and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class TalentProfilesSegment(Document):
    pass

    def validate(self):
        validate_unique_candidate_segment(self)

    def on_update(self):
        count_candidate_segment(self.segment_id)

def validate_unique_candidate_segment(doc):
    """
    Kiểm tra xem đã tồn tại TalentProfilesSegment với cùng
    talent_id + segment_id (ngoại trừ chính nó) hay chưa.
    """
    filters = {
        "talent_id": doc.talent_id,
        "segment_id": doc.segment_id,
    }

    existing = frappe.db.exists("TalentProfilesSegment", filters)

    if existing and existing != doc.name:
        frappe.throw(
            frappe._("A TalentProfilesSegment with Candidate <b>{0}</b> and Segment <b>{1}</b> already exists: <a href='/app/candidate-segment/{2}'>{2}</a>").format(
                doc.talent_id,
                doc.segment_id,
                existing
            ),
            title=frappe._("Duplicate TalentProfilesSegment")
        )

def count_candidate_segment(segment_id):
    try:
        total_candidate = frappe.db.count("TalentProfilesSegment",filters={"segment_id":segment_id})
        print("===========total_candidate==============",total_candidate)
        if total_candidate and total_candidate > 0:
            frappe.db.set_value("TalentSegment",segment_id,"candidate_count",total_candidate)
            frappe.db.commit()
    except Exception as e:
        pass