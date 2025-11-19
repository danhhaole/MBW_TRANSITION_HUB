"""
Proxy Unlayer image upload requests to local storage
Intercept requests to api.unlayer.com and save to Frappe instead
"""
import frappe
from frappe import _
from frappe.utils.file_manager import save_file
import requests

@frappe.whitelist(allow_guest=False)
def proxy_image_upload():
    """
    Proxy for Unlayer image uploads
    
    Unlayer sends to: https://api.unlayer.com/v2/images/upload-url
    We intercept and save to Frappe file storage instead
    """
    try:
        # Get uploaded file
        if 'file' not in frappe.request.files:
            return {
                "success": False,
                "error": "No file uploaded"
            }
        
        uploaded_file = frappe.request.files['file']
        
        if not uploaded_file or uploaded_file.filename == '':
            return {
                "success": False,
                "error": "No file selected"
            }
        
        # Read file content
        content = uploaded_file.stream.read()
        filename = uploaded_file.filename
        
        # Save to Frappe file storage
        file_doc = save_file(
            fname=filename,
            content=content,
            dt=None,
            dn=None,
            folder="Home/Email Templates",
            is_private=0  # Public for email images
        )
        
        frappe.db.commit()
        
        # Return in Unlayer expected format
        # Unlayer expects: { success: true, url: "..." }
        return {
            "success": True,
            "url": file_doc.file_url  # This is what Unlayer uses
        }
        
    except Exception as e:
        frappe.log_error(f"Unlayer proxy upload error: {str(e)}", "unlayer_proxy")
        return {
            "success": False,
            "error": str(e)
        }
