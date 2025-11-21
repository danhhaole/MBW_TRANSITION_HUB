"""
Helper functions for storing and retrieving Campaign Builder Page data
"""
import frappe
from frappe import _


@frappe.whitelist()
def save_builder_page_data(page_id, campaign_id=None, template_id=None, created_from=None, **kwargs):
    """
    Save or update builder page data in Mira Campaign Builder Page doctype
    
    Args:
        page_id: Page ID from Hireos CMS
        campaign_id: Optional campaign ID to link
        template_id: Template ID if created from template
        created_from: "Template" or "Published Page"
        **kwargs: All page data fields
    """
    try:
        # Check if record already exists
        existing = frappe.db.exists("Mira Campaign Builder Page", {"page_id": page_id})
        
        if existing:
            # Update existing record
            doc = frappe.get_doc("Mira Campaign Builder Page", existing)
            frappe.logger().info(f"Updating existing builder page record: {existing}")
        else:
            # Create new record
            doc = frappe.new_doc("Mira Campaign Builder Page")
            doc.page_id = page_id
            doc.created_from = created_from or "Template"
            frappe.logger().info(f"Creating new builder page record for page_id: {page_id}")
        
        # Update campaign link if provided
        if campaign_id:
            doc.campaign_id = campaign_id
        
        # Update meta fields
        if template_id:
            doc.template_id = template_id
        
        # Update basic info
        if kwargs.get('page_title'):
            doc.page_title = kwargs.get('page_title')
        if kwargs.get('url_public_page'):
            doc.url_public_page = kwargs.get('url_public_page')
        if kwargs.get('page_builder_id'):
            doc.page_builder_id = kwargs.get('page_builder_id')
        
        # Determine status
        if kwargs.get('url_public_page'):
            doc.status = "Published"
        else:
            doc.status = "Draft"
        
        # Update company info
        for field in ['company_name', 'company_logo', 'company_slogan', 'company_short_description',
                     'company_vision', 'company_mission', 'web_favicon']:
            if kwargs.get(field):
                setattr(doc, field, kwargs.get(field))
        
        # Update job info
        for field in ['job_title', 'work_address', 'employment_type', 'salary', 'hiring_quantity',
                     'application_deadline', 'published_date', 'job_description', 
                     'job_requirements', 'job_benefits']:
            if kwargs.get(field):
                setattr(doc, field, kwargs.get(field))
        
        # Update contact info
        for field in ['company_number_one', 'company_number_two', 'company_email_one',
                     'company_email_two', 'head_office', 'company_website']:
            if kwargs.get(field):
                setattr(doc, field, kwargs.get(field))
        
        # Update social media
        for field in ['company_fb', 'company_linkedin', 'company_youtube', 
                     'company_zalo_oa', 'company_tiktok']:
            if kwargs.get(field):
                setattr(doc, field, kwargs.get(field))
        
        doc.save()
        frappe.db.commit()
        
        frappe.logger().info(f"Successfully saved builder page data for page_id: {page_id}")
        
        return {
            "status": "success",
            "message": "Builder page data saved successfully",
            "data": {
                "name": doc.name,
                "page_id": doc.page_id
            }
        }
        
    except Exception as e:
        frappe.logger().error(f"Error saving builder page data: {str(e)}")
        frappe.log_error(f"Error saving builder page data: {str(e)}")
        return {
            "status": "error",
            "message": str(e)
        }


@frappe.whitelist()
def get_builder_page_data(page_id):
    """
    Get builder page data from Mira Campaign Builder Page doctype
    
    Args:
        page_id: Page ID from Hireos CMS
    """
    try:
        if not page_id:
            return {"status": "error", "message": "page_id is required"}
        
        # Find record by page_id
        doc_name = frappe.db.get_value("Mira Campaign Builder Page", {"page_id": page_id})
        
        if not doc_name:
            return {
                "status": "error",
                "message": f"No builder page record found for page_id: {page_id}"
            }
        
        doc = frappe.get_doc("Mira Campaign Builder Page", doc_name)
        
        # Get receive data configs from CMS API
        receive_data_configs = []
        form_config_id = None
        
        try:
            from mbw_mira.integrations.cms_page import get_link_accounts_by_page
            link_accounts_response = get_link_accounts_by_page(doc.page_id)
            
            frappe.logger().info(f"📧 Link accounts response: {link_accounts_response}")
            
            if (link_accounts_response and 
                link_accounts_response.get('message', {}).get('status') == 'success' and 
                link_accounts_response.get('message', {}).get('data')):
                
                accounts_data = link_accounts_response['message']['data']
                if accounts_data and len(accounts_data) > 0:
                    # Get first account's data
                    account = accounts_data[0]
                    form_config_id = account.get('form_config_id')
                    receive_data_configs = account.get('receive_data_configs', [])
                    
                    frappe.logger().info(f"✅ Found form_config_id: {form_config_id}")
                    frappe.logger().info(f"✅ Found {len(receive_data_configs)} receive data configs")
                else:
                    frappe.logger().info("⚠️ No accounts data found")
            else:
                frappe.logger().info("⚠️ Failed to get link accounts or no data")
                
        except Exception as e:
            frappe.logger().error(f"❌ Error getting receive data configs: {str(e)}")
            # Continue without receive data configs if API fails
        
        # Return all data as dict
        data = {
            "page_id": doc.page_id,
            "template_id": doc.template_id,
            "created_from": doc.created_from,
            "status": doc.status,
            "page_title": doc.page_title,
            "url_public_page": doc.url_public_page,
            "page_builder_id": doc.page_builder_id,
            "campaign_id": doc.campaign_id,
            
            # Form configuration
            "form_config_id": form_config_id,
            "receive_data_configs": receive_data_configs,
            
            # Company info
            "company_name": doc.company_name,
            "company_logo": doc.company_logo,
            "company_slogan": doc.company_slogan,
            "company_short_description": doc.company_short_description,
            "company_vision": doc.company_vision,
            "company_mission": doc.company_mission,
            "web_favicon": doc.web_favicon,
            
            # Job info
            "job_title": doc.job_title,
            "work_address": doc.work_address,
            "employment_type": doc.employment_type,
            "salary": doc.salary,
            "hiring_quantity": doc.hiring_quantity,
            "application_deadline": str(doc.application_deadline) if doc.application_deadline else None,
            "published_date": str(doc.published_date) if doc.published_date else None,
            "job_description": doc.job_description,
            "job_requirements": doc.job_requirements,
            "job_benefits": doc.job_benefits,
            
            # Contact info
            "company_number_one": doc.company_number_one,
            "company_number_two": doc.company_number_two,
            "company_email_one": doc.company_email_one,
            "company_email_two": doc.company_email_two,
            "head_office": doc.head_office,
            "company_website": doc.company_website,
            
            # Social media
            "company_fb": doc.company_fb,
            "company_linkedin": doc.company_linkedin,
            "company_youtube": doc.company_youtube,
            "company_zalo_oa": doc.company_zalo_oa,
            "company_tiktok": doc.company_tiktok
        }
        
        return {
            "status": "success",
            "message": "Builder page data retrieved successfully",
            "data": data
        }
        
    except Exception as e:
        frappe.logger().error(f"Error getting builder page data: {str(e)}")
        frappe.log_error(f"Error getting builder page data: {str(e)}")
        return {
            "status": "error",
            "message": str(e)
        }


@frappe.whitelist()
def get_campaign_builder_pages(campaign_id):
    """
    Get all builder pages linked to a campaign
    
    Args:
        campaign_id: Campaign ID
    """
    try:
        if not campaign_id:
            return {"status": "error", "message": "campaign_id is required"}
        
        pages = frappe.get_all(
            "Mira Campaign Builder Page",
            filters={"campaign_id": campaign_id},
            fields=["name", "page_id", "page_title", "status", "url_public_page", "created_from"]
        )
        
        return {
            "status": "success",
            "message": "Builder pages retrieved successfully",
            "data": pages
        }
        
    except Exception as e:
        frappe.logger().error(f"Error getting campaign builder pages: {str(e)}")
        frappe.log_error(f"Error getting campaign builder pages: {str(e)}")
        return {
            "status": "error",
            "message": str(e)
        }
