# Copyright (c) 2025, MBW Vietnam and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class MiraCampaignTemplateSocial(Document):
	def validate(self):
		"""Validate template social media content"""
		if not self.template_content:
			frappe.throw("Template content is required")
		
		# Validate platform-specific requirements
		if self.platform == "Email" and not self.subject:
			frappe.throw("Subject is required for email templates")
		
		# Set channel type based on platform
		if not self.channel_type:
			self.channel_type = self.platform.lower()
	
	def before_save(self):
		"""Process template content before saving"""
		# Clean up template content
		if self.template_content:
			self.template_content = self.template_content.strip()
		
		# Process template variables if any
		if self.content_variables:
			self.validate_template_variables()
	
	def validate_template_variables(self):
		"""Validate template variables format"""
		try:
			if isinstance(self.content_variables, str):
				import json
				json.loads(self.content_variables)
		except Exception:
			frappe.throw("Invalid template variables format")
	
	@frappe.whitelist()
	def get_template_preview(self, sample_data=None):
		"""Generate preview of template with sample data"""
		content = self.template_content
		
		if sample_data and self.content_variables:
			# Replace template variables with sample data
			for key, value in sample_data.items():
				content = content.replace(f"{{{key}}}", str(value))
		
		return {
			"platform": self.platform,
			"subject": self.subject,
			"content": content,
			"images": self.social_media_images,
			"attachments": self.attachments
		}
