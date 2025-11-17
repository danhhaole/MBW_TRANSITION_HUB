# Copyright (c) 2025, MBW and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class MiraCampaignQR(Document):
	def validate(self):
		"""Validate QR code data before saving"""
		if not self.campaign_id:
			frappe.throw("Campaign ID is required")
		
		if not self.qr_name:
			frappe.throw("QR Name is required")
		
		# Set UTM campaign to campaign_id if not set
		if not self.utm_campaign:
			self.utm_campaign = self.campaign_id
	
	def before_save(self):
		"""Update QR URL with UTM parameters"""
		if self.landing_page_url and self.utm_source and self.utm_medium:
			# Build QR URL with UTM parameters
			utm_params = f"?utm_campaign={self.utm_campaign or self.campaign_id}&utm_source={self.utm_source}&utm_medium={self.utm_medium}"
			self.qr_url = f"{self.landing_page_url}{utm_params}"
