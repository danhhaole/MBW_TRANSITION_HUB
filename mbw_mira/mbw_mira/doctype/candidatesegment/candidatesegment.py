# Copyright (c) 2025, MBWCloud Co. and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class CandidateSegment(Document):
	pass

	def validate(self):
		validate_unique_candidate_segment(self)


def validate_unique_candidate_segment(doc):
    """
    Kiểm tra xem đã tồn tại CandidateSegment với cùng
    candidate_id + segment_id (ngoại trừ chính nó) hay chưa.
    """
    filters = {
        "candidate_id": doc.candidate_id,
        "segment_id": doc.segment_id,
    }

    existing = frappe.db.exists("CandidateSegment", filters)

    if existing and existing != doc.name:
        frappe.throw(
            frappe._("A CandidateSegment with Candidate <b>{0}</b> and Segment <b>{1}</b> already exists: <a href='/app/candidate-segment/{2}'>{2}</a>").format(
                doc.candidate_id,
                doc.segment_id,
                existing
            ),
            title=frappe._("Duplicate CandidateSegment")
        )