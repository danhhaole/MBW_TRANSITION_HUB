# Copyright (c) 2025, mbwcloud.com and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class MIRA_Email_Template(Document):
    def before_save(self):
        # Set created_by and creation if this is a new document
        if self.is_new():
            from frappe.utils import now_datetime

            if not self.created_time:
                self.created_time = now_datetime()
            if not self.created_by:
                self.created_by = frappe.session.user

    @classmethod
    def default_list_data(cls):
        columns = [
            {
                "label": "Template Name",
                "type": "Data",
                "key": "template_name",
                "width": "16rem",
            },
            {"label": "Status", "type": "Check", "key": "is_active", "width": "8rem"},
            {"label": "Type", "type": "Data", "key": "template_type", "width": "12rem"},
            {"label": "Subject", "type": "Data", "key": "subject", "width": "24rem"},
            {
                "label": "Created By",
                "type": "Link",
                "key": "created_by",
                "width": "12rem",
            },
            {
                "label": "Created Time",
                "type": "Datetime",
                "key": "created_time",
                "width": "12rem",
            },
        ]

        rows = [
            "template_name",
            "is_active",
            "template_type",
            "subject",
            "message",
            "attachment",
            "auto_send",
            "name",
            "created_time",
            "created_by",
        ]
        return {"columns": columns, "rows": rows}
