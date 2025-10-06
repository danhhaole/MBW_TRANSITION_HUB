# mbw_mira/api/email_api.py

import frappe
from frappe import _
from frappe.utils import now, get_url
import json
import base64
import os
from frappe.core.doctype.file.file import create_new_folder
from mbw_mira.api.mail import send_email

@frappe.whitelist()
def get_email_templates(unit_name=None, template_type=None, is_active=1):
    """
    Lấy danh sách email templates
    
    Args:
        unit_name (str): Tên đơn vị (optional)
        template_type (str): Loại template (optional) - confirm-email, invited-email, reject-email, other-email
        is_active (int): Trạng thái active (default: 1)
    
    Returns:
        list: Danh sách email templates
    """
    try:
        filters = {
            "is_active": is_active
        }
        
        if unit_name:
            filters["unit_name"] = unit_name
            
        if template_type:
            filters["template_type"] = template_type
        
        templates = frappe.get_all(
            "MIRA_Email_Template",
            filters=filters,
            fields=[
                "name",
                "template_id", 
                "template_name",
                "template_type",
                "subject",
                "message",
                "html_content",
                "css_content",
                "attachment",
                "auto_send",
                "default_template",
            ],
            order_by="default_template desc, template_name asc"
        )
        
        return {
            "success": True,
            "data": templates,
            "count": len(templates)
        }
        
    except Exception as e:
        frappe.log_error(f"Error getting email templates: {str(e)}")
        return {
            "success": False,
            "message": _("Error retrieving email templates"),
            "error": str(e)
        }

@frappe.whitelist()
def get_email_template(template_id):
    """
    Lấy chi tiết một email template
    
    Args:
        template_id (str): ID của template
    
    Returns:
        dict: Thông tin chi tiết template
    """
    try:
        template = frappe.get_doc("MIRA_Email_Template", template_id)
        
        return {
            "success": True,
            "data": {
                "name": template.name,
                "template_id": template.template_id,
                "template_name": template.template_name,
                "template_type": template.template_type,
                "subject": template.subject,
                "message": template.message,
                "html_content": template.html_content,
                "css_content": template.css_content,
                "attachment": template.attachment,
                "auto_send": template.auto_send,
                "default_template": template.default_template,
            }
        }
        
    except frappe.DoesNotExistError:
        return {
            "success": False,
            "message": _("Template not found")
        }
    except Exception as e:
        frappe.log_error(f"Error getting email template: {str(e)}")
        return {
            "success": False,
            "message": _("Error retrieving email template"),
            "error": str(e)
        }

@frappe.whitelist()
def send_candidate_email(**kwargs):
    """
    Gửi email cho ứng viên
    
    Args:
        template_id (str): ID template email
        candidate_id (str): ID ứng viên
        to_emails (str): Email người nhận (separated by comma)
        cc_emails (str): Email CC (optional)
        bcc_emails (str): Email BCC (optional)
        subject (str): Tiêu đề email
        content (str): Nội dung email
        attachments (str): JSON string của attachments
        job_opening_id (str): ID job opening (optional)
        
    Returns:
        dict: Kết quả gửi email
    """
    try:
        # Parse parameters
        template_id = kwargs.get('template_id')
        candidate_id = kwargs.get('candidate_id')
        to_emails = kwargs.get('to_emails', '').strip()
        cc_emails = kwargs.get('cc_emails', '').strip()
        bcc_emails = kwargs.get('bcc_emails', '').strip()
        subject = kwargs.get('subject', '').strip()
        content = kwargs.get('content', '').strip()
        attachments_json = kwargs.get('attachments', '[]')
        job_opening_id = kwargs.get('job_opening_id')
        
        # Validate required fields
        if not to_emails:
            return {
                "success": False,
                "message": _("Recipient email is required")
            }
            
        if not subject:
            return {
                "success": False,
                "message": _("Email subject is required")
            }
            
        if not content:
            return {
                "success": False,
                "message": _("Email content is required")
            }
        
        # Parse email lists
        to_list = [email.strip() for email in to_emails.split(',') if email.strip()]
        cc_list = [email.strip() for email in cc_emails.split(',') if cc_emails and email.strip()]
        bcc_list = [email.strip() for email in bcc_emails.split(',') if bcc_emails and email.strip()]
        
                
        # Process attachments
        file_attachments = []
        try:
            attachments_list = json.loads(attachments_json) if attachments_json else []
            for attachment in attachments_list:
                if isinstance(attachment, dict) and 'content' in attachment and 'filename' in attachment:
                    # Decode base64 content and save as file
                    file_content = base64.b64decode(attachment['content'])
                    file_doc = frappe.get_doc({
                        "doctype": "File",
                        "file_name": attachment['filename'],
                        "content": file_content,
                        "is_private": 1,
                        "folder": "Home/Attachments"
                    })
                    file_doc.insert()
                    file_attachments.append(file_doc.file_url)
        except Exception as e:
            frappe.log_error(f"Error processing attachments: {str(e)}")
        
        # Get template attachment if exists
        if template_id:
            try:
                template = frappe.get_doc("MIRA_Email_Template", template_id)
                if template.attachment:
                    file_attachments.append(template.attachment)
            except:
                pass
        
        # Send email
        # frappe.sendmail(
        #     recipients=to_list,
        #     cc=cc_list,
        #     bcc=bcc_list,
        #     subject=subject,
        #     message=content,
        #     attachments=file_attachments,
        #     now=True
        # )

        send_email("MIRA_Candidate",candidate_id,to_list,subject,content,cc_list,bcc_list,file_attachments)
        
        # # Create email log
        # email_log = frappe.get_doc({
        #     "doctype": "Email Queue",
        #     "recipients": to_emails,
        #     "cc": cc_emails,
        #     "bcc": bcc_emails,
        #     "subject": subject,
        #     "message": content,
        #     "status": "Sent",
        #     "creation": now(),
        #     "reference_doctype": "MIRA_Candidate" if candidate_id else None,
        #     "reference_name": candidate_id if candidate_id else None
        # })
        # email_log.insert(ignore_permissions=True)
        
        # # Create communication record
        # if candidate_id:
        #     comm = frappe.get_doc({
        #         "doctype": "Communication",
        #         "subject": subject,
        #         "content": content,
        #         "communication_type": "Communication",
        #         "communication_medium": "Email",
        #         "sent_or_received": "Sent",
        #         "reference_doctype": "MIRA_Candidate",
        #         "reference_name": candidate_id,
        #         "recipients": to_emails,
        #         "cc": cc_emails,
        #         "bcc": bcc_emails,
        #         "status": "Linked",
        #         "sender": frappe.session.user
        #     })
        #     comm.insert(ignore_permissions=True)
        
        return {
            "success": True,
            "message": _("Email sent successfully"),
            "data": {
                "email_queue_id": "",
                "sent_to": to_list,
                "sent_at": now()
            }
        }
        
    except Exception as e:
        frappe.log_error(f"Error sending email: {str(e)}")
        return {
            "success": False,
            "message": _("Failed to send email"),
            "error": str(e)
        }

@frappe.whitelist()
def save_email_draft(**kwargs):
    """
    Lưu email draft
    
    Args:
        Similar to send_candidate_email but saves as draft
        
    Returns:
        dict: Kết quả lưu draft
    """
    try:
        draft_data = {
            "doctype": "Email Draft", # Custom doctype cần tạo
            "template_id": kwargs.get('template_id'),
            "candidate_id": kwargs.get('candidate_id'),
            "to_emails": kwargs.get('to_emails'),
            "cc_emails": kwargs.get('cc_emails'),
            "bcc_emails": kwargs.get('bcc_emails'),
            "subject": kwargs.get('subject'),
            "content": kwargs.get('content'),
            "attachments": kwargs.get('attachments'),
            "job_opening_id": kwargs.get('job_opening_id'),
            "created_by": frappe.session.user,
            "creation": now()
        }
        
        # Create or update draft
        draft_id = kwargs.get('draft_id')
        if draft_id:
            draft = frappe.get_doc("Email Draft", draft_id)
            draft.update(draft_data)
            draft.save()
        else:
            draft = frappe.get_doc(draft_data)
            draft.insert()
        
        return {
            "success": True,
            "message": _("Draft saved successfully"),
            "data": {
                "draft_id": draft.name
            }
        }
        
    except Exception as e:
        frappe.log_error(f"Error saving email draft: {str(e)}")
        return {
            "success": False,
            "message": _("Failed to save draft"),
            "error": str(e)
        }

@frappe.whitelist()
def get_email_variables():
    """
    Lấy danh sách các biến có thể sử dụng trong email template
    
    Returns:
        dict: Danh sách variables
    """
    return {
        "success": True,
        "data": {
            "candidate_variables": [
                {"key": "candidate_name", "label": "Candidate Name", "description": "Full name of the candidate"},
                {"key": "candidate_email", "label": "Candidate Email", "description": "Email address of the candidate"},
                {"key": "candidate_phone", "label": "Candidate Phone", "description": "Phone number of the candidate"}
            ],
            "job_variables": [
                {"key": "job_title", "label": "Job Title", "description": "Title of the job position"},
                {"key": "company_name", "label": "Company Name", "description": "Name of the company"},
                {"key": "department", "label": "Department", "description": "Department name"}
            ],
            "system_variables": [
                {"key": "current_date", "label": "Current Date", "description": "Current date"},
                {"key": "current_time", "label": "Current Time", "description": "Current time"}
            ]
        }
    }

@frappe.whitelist()
def get_template_types():
    """
    Lấy danh sách các loại template
    
    Returns:
        list: Danh sách template types
    """
    return {
        "success": True,
        "data": [
            {"value": "confirm-email", "label": "Confirmation Email"},
            {"value": "invited-email", "label": "Interview Invitation"},
            {"value": "reject-email", "label": "Rejection Email"},
            {"value": "other-email", "label": "Other Email"}
        ]
    }