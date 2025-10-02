# Copyright (c) 2025, MBWCloud Co. and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class MiraTalentPoolCampaign(Document):
	pass

	def validate(self):
		# Check trùng talent_id + campaign_id
		self.validate_unique_candidate_campaign()


	def validate_unique_candidate_campaign(self):
		"""
		Kiểm tra xem đã tồn tại Mira Talent Campaign với cùng
		talent_id + campaign_id (ngoại trừ chính nó) hay chưa.
		"""
		filters = {
			"talentpool_id": self.talentpool_id,
			"campaign_id": self.campaign_id,
		}

		existing = frappe.db.exists("Mira Talent Campaign", filters)

		if existing and existing != self.name:
			frappe.throw(
				frappe._(
					"A Mira Talent Pool Campaign with Campaign <b>{0}</b> and Candidate <b>{1}</b> already exists: <a href='/app/candidate-campaign/{2}'>{2}</a>"
				).format(self.campaign_id, self.talentpool_id, existing),
				title=frappe._("Duplicate Mira Talent Campaign"),
        )
