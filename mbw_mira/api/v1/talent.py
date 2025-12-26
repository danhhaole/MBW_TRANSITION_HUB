import frappe
import requests
import os
from urllib.parse import urlparse
from frappe.utils import now_datetime, today, get_files_path

DT_TALENT = "Mira Talent"
DT_TALENT_CAMPAIGN = "Mira Talent Campaign"


def download_cv_from_cms(cv_url):
    """
    Download CV from CMS server and save locally.
    
    Args:
        cv_url: URL like https://hireos.fastwork.vn/private/files/cv_upload_xxx.pdf
    
    Returns:
        Local file URL or None if failed
    """
    if not cv_url:
        return None
    
    try:
        print(f"📥 Downloading CV from: {cv_url}")
        
        # Get CMS config
        cms_base_url = frappe.get_conf().get("ladipage_base_url")
        api_key = frappe.get_conf().get("ladipage_api_key")
        api_secret = frappe.get_conf().get("ladipage_api_secret")
        
        if not cms_base_url:
            print("⚠️ No ladipage_base_url configured, keeping original URL")
            return cv_url
        
        # Parse the original URL to get the file path
        parsed = urlparse(cv_url)
        file_path = parsed.path  # e.g., /private/files/cv_upload_xxx.pdf
        
        # Build the correct URL without port
        download_url = f"{cms_base_url}{file_path}"
        print(f"📥 Corrected download URL: {download_url}")
        
        # Prepare headers with API auth
        headers = {}
        if api_key and api_secret:
            headers["Authorization"] = f"token {api_key}:{api_secret}"
        
        # Download file
        response = requests.get(download_url, headers=headers, timeout=30, verify=False)
        
        if response.status_code != 200:
            print(f"⚠️ Failed to download CV: HTTP {response.status_code}")
            return cv_url
        
        # Get filename from URL
        filename = os.path.basename(file_path)
        if not filename:
            filename = f"cv_{frappe.generate_hash()[:8]}.pdf"
        
        # Save file locally
        files_path = get_files_path()
        local_file_path = os.path.join(files_path, filename)
        
        with open(local_file_path, 'wb') as f:
            f.write(response.content)
        
        # Create File document in Frappe
        file_doc = frappe.get_doc({
            "doctype": "File",
            "file_name": filename,
            "file_url": f"/files/{filename}",
            "is_private": 0,
            "folder": "Home"
        })
        file_doc.insert(ignore_permissions=True)
        
        local_url = file_doc.file_url
        print(f"✅ CV saved locally: {local_url}")
        
        return local_url
        
    except Exception as e:
        print(f"⚠️ Error downloading CV: {e}")
        import traceback
        traceback.print_exc()
        # Return original URL if download fails
        return cv_url


@frappe.whitelist()
def create():
    """
    Create a new Mira Talent and optionally link to a Campaign.
    
    Flow:
    1. Parse incoming data from landing page
    2. Create or find existing Mira Talent (by email)
    3. Create Mira Talent Campaign record (link talent to campaign)
    """
    try:
        # Parse request data properly
        raw_data = frappe.request.data
        print("📥 Raw request data:", raw_data)
        
        # Handle bytes
        if isinstance(raw_data, bytes):
            raw_data = raw_data.decode('utf-8')
        
        data = frappe.parse_json(raw_data)
        print("📋 Parsed data:", data)
        
        # Extract campaign ID from utm_campaign
        campaign_id = data.pop('utm_campaign', None)
        
        # Extract UTM fields for talent record
        utm_source = data.pop('utm_source', None)
        utm_medium = data.pop('utm_medium', None)
        utm_term = data.pop('utm_term', None)
        utm_content = data.pop('utm_content', None)
        
        # Remove non-talent fields
        non_talent_fields = [
            'form_id', 'page_id', 'form_url', 'custom_field', 'phone_number'
        ]
        for field in non_talent_fields:
            data.pop(field, None)
        
        # Download CV from CMS and save locally
        if data.get('resume'):
            local_cv_url = download_cv_from_cms(data['resume'])
            data['resume'] = local_cv_url
        
        # Map Mira Talent fields
        talent_data = {
            'full_name': data.get('full_name', ''),
            'email': data.get('email', ''),
            'phone': data.get('phone', ''),
            'resume': data.get('resume', ''),
            'linkedin_profile': data.get('linkedin_profile', ''),
            'current_city': data.get('current_city', ''),
            'notes': data.get('notes', ''),
            'skills': data.get('skills', ''),
            'date_of_birth': data.get('date_of_birth', None),
            'source': data.get('source', 'Nurturing Interaction'),
            'latest_company': data.get('latest_company', ''),
            # Store UTM params
            'utm_source': utm_source,
            'utm_medium': utm_medium,
            'utm_campaign': campaign_id,
            'utm_term': utm_term,
            'utm_content': utm_content,
            # Default status
            'current_status': 'Active'
        }
        
        # Remove None values
        talent_data = {k: v for k, v in talent_data.items() if v is not None and v != ''}
        
        print("📝 Final talent data:", talent_data)
        
        # Check if talent already exists by email
        existing_talent = None
        if talent_data.get('email'):
            existing_talent = frappe.db.get_value(DT_TALENT, 
                {"email": talent_data['email']}, "name")
        
        if existing_talent:
            # Update existing talent (except email)
            print(f"ℹ️ Found existing talent: {existing_talent}")
            talent_doc = frappe.get_doc(DT_TALENT, existing_talent)
            
            # Update fields that have new values
            for field, value in talent_data.items():
                if field != 'email' and value:  # Don't update email
                    talent_doc.set(field, value)
            
            talent_doc.save(ignore_permissions=True)
            print(f"✅ Updated existing talent: {talent_doc.name}")
        else:
            # Create new talent
            talent_doc = frappe.get_doc({"doctype": DT_TALENT, **talent_data})
            talent_doc.insert(ignore_permissions=True)
            print(f"✅ Created new talent: {talent_doc.name}")
        
        # If campaign exists, create Mira Talent Campaign link
        talent_campaign_doc = None
        if campaign_id and frappe.db.exists("Mira Campaign", campaign_id):
            talent_campaign_doc = link_talent_to_campaign(talent_doc.name, campaign_id)
        else:
            print(f"⚠️ Campaign not found or not provided: {campaign_id}")
        
        frappe.db.commit()
        frappe.response.http_status_code = 201
        
        response_data = {
            "talent_id": talent_doc.name,
            "talent": talent_doc.as_dict()
        }
        
        if talent_campaign_doc:
            response_data["talent_campaign_id"] = talent_campaign_doc.name
            response_data["talent_campaign"] = talent_campaign_doc.as_dict()
        
        return {
            "status": "success",
            "message": "Talent created successfully" if not existing_talent else "Talent updated successfully",
            "data": response_data
        }
        
    except Exception as e:
        frappe.log_error(title="Talent Create Error", message=str(e)[:500])
        print(f"❌ Error creating talent: {e}")
        import traceback
        traceback.print_exc()
        frappe.throw(f"Error creating talent: {str(e)}")


def link_talent_to_campaign(talent_id, campaign_id):
    """
    Link a talent to a campaign by creating Mira Talent Campaign record.
    
    Args:
        talent_id: Mira Talent ID
        campaign_id: Mira Campaign ID
    
    Returns:
        Created Mira Talent Campaign doc or existing one
    """
    
    # Check if already linked
    existing = frappe.db.exists(DT_TALENT_CAMPAIGN, {
        "talent_id": talent_id,
        "campaign_id": campaign_id
    })
    
    if existing:
        print(f"ℹ️ Talent already linked to campaign: {existing}")
        return frappe.get_doc(DT_TALENT_CAMPAIGN, existing)
    
    now = now_datetime()
    
    # Create talent campaign link
    talent_campaign = frappe.get_doc({
        "doctype": DT_TALENT_CAMPAIGN,
        "talent_id": talent_id,
        "campaign_id": campaign_id,
        "status": "ACTIVE",
        "current_step_order": 1,
        "enrolled_at": now
    })
    
    talent_campaign.insert(ignore_permissions=True)
    print(f"✅ Talent Campaign created: {talent_campaign.name}")
    
    return talent_campaign


@frappe.whitelist()
def list():
    """List all talents"""
    fields = [
        "name", "full_name", "email", "phone", "source", 
        "current_status", "skills", "resume", "creation"
    ]
    return {"data": frappe.get_all(DT_TALENT, fields=fields, order_by="modified desc")}


@frappe.whitelist()
def get(id: str):
    """Get a talent by ID"""
    return frappe.get_doc(DT_TALENT, id).as_dict()


@frappe.whitelist()
def update(id: str):
    """Update a talent"""
    raw_data = frappe.request.data
    if isinstance(raw_data, bytes):
        raw_data = raw_data.decode('utf-8')
    data = frappe.parse_json(raw_data)
    
    doc = frappe.get_doc(DT_TALENT, id)
    doc.update(data)
    doc.save()
    return doc.as_dict()


@frappe.whitelist()
def delete(id: str):
    """Delete a talent"""
    frappe.delete_doc(DT_TALENT, id)
    frappe.response.http_status_code = 204
