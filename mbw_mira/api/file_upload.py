"""
Custom file upload API for Unlayer image uploads
"""
import frappe
from frappe import _
from frappe.utils.file_manager import save_file
import base64

@frappe.whitelist(allow_guest=False)
def upload_email_image_base64(filename, content):
    """
    Upload image from base64 content
    Used by Unlayer with frappe-ui call method
    """
    try:
        # Decode base64 content
        file_content = base64.b64decode(content)
        
        # Save file using Frappe's utility
        file_doc = save_file(
            fname=filename,
            content=file_content,
            dt=None,
            dn=None,
            folder="Home/Email Templates",
            is_private=0  # Public for email images
        )
        
        frappe.db.commit()
        
        # Return file URL directly (not wrapped in message)
        # frappe-ui call returns the data directly
        return {
            "file_url": file_doc.file_url,
            "file_name": file_doc.file_name,
            "name": file_doc.name
        }
        
    except Exception as e:
        frappe.log_error(f"Base64 image upload error: {str(e)}", "upload_email_image_base64")
        frappe.throw(_("Failed to upload image: {0}").format(str(e)))

@frappe.whitelist(allow_guest=False)
def upload_email_image():
    """
    Upload image for email templates
    Returns file URL for Unlayer editor
    """
    try:
        # Get uploaded file
        if 'file' not in frappe.request.files:
            frappe.throw(_("No file uploaded"))
        
        uploaded_file = frappe.request.files['file']
        
        if not uploaded_file or uploaded_file.filename == '':
            frappe.throw(_("No file selected"))
        
        # Read file content
        content = uploaded_file.stream.read()
        filename = uploaded_file.filename
        
        # Save file using Frappe's utility (handles everything properly)
        file_doc = save_file(
            fname=filename,
            content=content,
            dt=None,  # Not attached to any doctype
            dn=None,
            folder="Home/Email Templates",
            is_private=0  # Public for email images
        )
        
        frappe.db.commit()
        
        # Return response
        return {
            "success": True,
            "file_url": file_doc.file_url,
            "file_name": file_doc.file_name,
            "name": file_doc.name,
            "file_size": len(content)
        }
        
    except Exception as e:
        frappe.log_error(f"Email image upload error: {str(e)}", "upload_email_image")
        frappe.throw(_("Failed to upload image: {0}").format(str(e)))
