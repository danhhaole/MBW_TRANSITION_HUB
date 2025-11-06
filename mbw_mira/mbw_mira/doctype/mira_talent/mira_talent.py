# Copyright (c) 2025, MBWCloud Co. and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe.utils import cstr, cint, flt, add_days, nowdate, get_datetime,now_datetime
from mbw_mira.api.common import get_filter_options, get_form_data, get_list_data
import json

from mbw_mira.mbw_mira.doctype.mira_task_definition.mira_task_definition import create_task_definitions_from_event

class MiraTalent(Document):

    def after_insert(doc, method):
        create_task_definitions_from_event(
            event_trigger="ON_CREATE",
            target_type="Talent",
            target_id=doc.name,
            event_payload=doc.as_dict()
        )
    def on_update(self):
        if not self.get("__islocal"):  # nghĩa là UPDATE, không phải INSERT
            # self.on_talent_update()
            old_doc = self.get_doc_before_save()
            if old_doc.crm_status != self.crm_status:
                self.on_status_changed(old_doc.crm_status,self.crm_status)
            if old_doc.tags != self.tags:
                self.on_tag_added()
            
    def on_talent_update(self):
        create_task_definitions_from_event(
                event_trigger="ON_UPDATE",
                target_type="Talent",
                target_id=self.name,
                event_payload=self.as_dict()
            )
    
    def on_tag_added(self):
        create_task_definitions_from_event(
            event_trigger="ON_TAG_ADDED",
            target_type="Talent",
            target_id=self.name,
            event_payload={"tags": self.tags}
        )
    def on_status_changed(self,old_status, new_status):
        create_task_definitions_from_event(
            event_trigger="ON_STATUS_CHANGED",
            target_type="Talent",
            target_id=self.name,
            event_payload={
                "old_status": old_status,
                "new_status": new_status
            }
        )
    def after_save(self):
        pass
        #Tạo Talent Campaign
        # if hasattr(self,"campaign_id"): 
        #     self.create_talent_campaign()

    # def create_talent_campaign(self):
    #     try:           
    #         first_step = get_first_campaign_step(self.campaign_id)
    #         if first_step:
    #             next_action_at = add_days(now_datetime(), first_step.get("delay_in_days") or 0)
    #             doc = frappe.get_doc(
    #             {
    #                 "doctype": "Mira Talent Campaign",
    #                 "campaign_id": self.campaign_id,
    #                 "talent_id": self.talent_id,
    #                 "status": "ACTIVE",
    #                 "enrolled_at": now_datetime(),
    #                 "current_step_order": first_step.get("step_order")  or 1,
    #                 "next_action_at": next_action_at,
    #             }
    #             )
    #             doc.insert(ignore_permissions=True)
    #             frappe.db.commit()
    #     except Exception as e:
    #         pass
# def check_exists(email):
#     exists = frappe.db.exists("Mira Contact",{"email":email})
#     if exists:
#         return True
#     else:
#         return False

@frappe.whitelist(allow_guest=True)
def submit_job_application():
    """
    Handle job application form submission
    Allow guest access and ignore permissions for this endpoint
    """
    try:
        # Get form data from request
        form_data = frappe.form_dict
        files = frappe.request.files
        
        # Handle file upload if exists
        if 'resume' in files:
            file = files['resume']
            file_doc = frappe.get_doc({
                'doctype': 'File',
                'file_name': file.filename,
                'content': file.stream.read(),
                'attached_to_doctype': 'Mira Talent',
                'attached_to_name': None,  # Will be set after creating the prospect
                'attached_to_field': 'resume'
            })
            file_doc.save(ignore_permissions=True)
            form_data['resume'] = file_doc.file_url

        # Basic validation
        required_fields = ['full_name', 'email', 'phone']
        for field in required_fields:
            if not form_data.get(field):
                return {"success": False, "error": f"Missing required field: {field}"}

        # Map form data to document fields
        doc_data = {
            'full_name': form_data.get('full_name'),
            'email': form_data.get('email'),
            'phone': form_data.get('phone'),
            'current_company': form_data.get('current_company', ''),
            'current_designation': form_data.get('current_designation', ''),
            'experience_years': form_data.get('experience_years'),
            'linkedin_profile': form_data.get('linkedin_profile', ''),
            'notes': form_data.get('notes', '')
        }
        
        # Add resume if exists
        if 'resume' in form_data:
            doc_data['resume'] = form_data['resume']

        # Create new prospect document
        doc = frappe.new_doc("Mira Talent")
        doc.update(doc_data)
        
        # Map form data to document fields
        field_mapping = {
            'full_name': 'full_name',
            'email': 'email',
            'phone': 'phone',
            'current_designation': 'current_position',
            'current_company': 'current_company',
            'experience_years': 'years_of_experience',
            'linkedin_profile': 'linkedin_profile',
            'notes': 'notes'
        }

        for form_field, doc_field in field_mapping.items():
            if form_field in form_data:
                doc.set(doc_field, form_data[form_field])

        doc.date = nowdate()

        # Handle file upload if exists
        if 'resume' in form_data and form_data['resume']:
            # You might want to handle file upload separately using frappe.upload_file()
            # For now, we'll just store the file name
            doc.resume = form_data['resume'].name

        # Save the document with ignore_permissions
        doc.flags.ignore_permissions = True
        doc.insert(ignore_permissions=True)

        # If there's a resume file, you might want to attach it here
        # This is a placeholder for file attachment logic
        # if 'resume' in form_data and form_data['resume']:
        #     attach_file_to_doc("Mira Prospect", doc.name, form_data['resume'])

        return {
            "success": True,
            "message": "Ứng tuyển thành công! Cảm ơn bạn đã nộp đơn.",
            "prospect_id": doc.name
        }

    except Exception as e:
        frappe.log_error(
            title="Job Application Error",
            message=f"Error in submit_job_application: {str(e)}\nForm Data: {form_data}"
        )
        return {
            "success": False,
            "error": "Có lỗi xảy ra khi gửi đơn ứng tuyển. Vui lòng thử lại sau."
        }

