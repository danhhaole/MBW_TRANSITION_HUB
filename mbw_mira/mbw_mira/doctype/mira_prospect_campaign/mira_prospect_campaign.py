# Copyright (c) 2025, MBWCloud Co. and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class MiraProspectCampaign(Document):
	pass

	def create_prospect_campaign(self, prospect_id, campaign_id):
		if not self.prospect_campaign_exists(prospect_id,campaign_id):
			doc = frappe.new_doc("Mira Prospect Campaign")
			

	def prospect_campaign_exists(prospect_id, campaign_id)->bool:
		filters = {
        "prospect_id": prospect_id,
        "campaign_id": campaign_id,
		}

		existing = frappe.db.exists("Mira Prospect Campaign", filters)
		if existing:
			return True
		else:
			return False		