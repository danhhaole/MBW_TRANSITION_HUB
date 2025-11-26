import frappe
from frappe import _
import json
from datetime import datetime


@frappe.whitelist()
def create_campaign_from_template(template_id, campaign_name=None, start_date=None, target_pool=None):
    """
    Create a new campaign from a template.
    Copies all template data including social contents and flows.
    
    Args:
        template_id: The template ID to create campaign from
        campaign_name: Optional custom campaign name (defaults to template name)
        start_date: Optional start date for the campaign
        target_pool: Optional target pool override
        
    Returns:
        dict: Success status and created campaign data
    """
    try:
        print(f"🚀 Creating campaign from template: {template_id}")
        
        # 1. Get template data
        template = frappe.get_doc("Mira Campaign Template", template_id)
        
        # Parse configuration_json
        config = {}
        if template.configuration_json:
            try:
                config = json.loads(template.configuration_json) if isinstance(template.configuration_json, str) else template.configuration_json
            except:
                config = {}
        
        # 2. Create campaign with unique name (template name + datetime)
        timestamp = datetime.now().strftime("%d/%m/%Y %H:%M")
        default_name = f"{template.template_name} - {timestamp}"
        
        campaign_data = {
            "doctype": "Mira Campaign",
            "campaign_name": campaign_name or default_name,
            "type": template.campaign_type,
            "status": "DRAFT",
            "is_active": 0,
            "description": template.description,
            "target_pool": target_pool or config.get("target_pool", ""),
            "ladipage_url": template.ladipage_url,
            "ladipage_id": template.ladipage_id,
            "source_type": "Search",  # Default source type
            "owner_id": frappe.session.user
        }
        
        if start_date:
            campaign_data["start_date"] = start_date
            
        # Add criteria/conditions from config
        if config.get("conditions"):
            campaign_data["criteria"] = json.dumps(config.get("conditions"))
            
        campaign = frappe.get_doc(campaign_data)
        campaign.insert(ignore_permissions=True)
        frappe.db.commit()
        
        print(f"✅ Campaign created: {campaign.name}")
        
        # 3. Copy social contents from template
        social_contents = frappe.get_all(
            "Mira Campaign Template Social",
            filters={"template_id": template_id},
            fields=["*"]
        )
        
        for social in social_contents:
            # Create campaign social content
            # Map template fields to campaign fields
            social_data = {
                "doctype": "Mira Campaign Social",
                "campaign_id": campaign.name,
                "platform": social.get("platform"),
                "template_content": social.get("template_content"),
                "subject": social.get("subject"),
                "social_media_images": social.get("social_media_images"),
                "social_page_id": social.get("page_id"),
                "external_connection": social.get("connection_id"),
                "mjml_content": social.get("mjml_content"),
                "block_content": social.get("block_content"),
                "status": "Pending",  # Valid options: Pending, Processing, Success, Failed, Cancelled
                "is_active": 1
            }
            
            social_doc = frappe.get_doc(social_data)
            social_doc.insert(ignore_permissions=True)
            
        print(f"✅ Copied {len(social_contents)} social contents")
        
        # 4. Create flows from template flow_config if exists
        flows_created = 0
        if template.flow_config:
            try:
                flow_config = json.loads(template.flow_config) if isinstance(template.flow_config, str) else template.flow_config
                print(f"📋 Flow config from template: {flow_config}")
                
                # Get triggers from flow_config
                triggers = flow_config.get('triggers', [])
                print(f"🔄 Creating {len(triggers)} flows from template...")
                
                # Import the flow creation function
                from mbw_mira.api.campaign_flow import create_flow_from_trigger
                
                # Create flow for each trigger
                for trigger in triggers:
                    try:
                        result = create_flow_from_trigger(campaign.name, trigger)
                        if result.get('success'):
                            flows_created += 1
                            print(f"✅ Created flow: {result.get('flow_id')}")
                        else:
                            print(f"⚠️ Failed to create flow: {result.get('error')}")
                    except Exception as flow_error:
                        print(f"❌ Error creating flow from trigger: {flow_error}")
                        
                print(f"🎯 Successfully created {flows_created}/{len(triggers)} flows")
            except Exception as e:
                print(f"⚠️ Could not parse flow_config: {e}")
        
        # 5. Update template usage statistics
        frappe.db.set_value("Mira Campaign Template", template_id, {
            "usage_count": (template.usage_count or 0) + 1,
            "last_used_at": datetime.now()
        })
        
        frappe.db.commit()
        
        print(f"🎉 Campaign creation completed: {campaign.name}")
        
        return {
            "success": True,
            "message": _("Campaign created successfully from template"),
            "data": {
                "campaign_id": campaign.name,
                "campaign_name": campaign.campaign_name,
                "campaign_type": campaign.type,
                "status": campaign.status,
                "social_contents_count": len(social_contents),
                "flows_created": flows_created
            }
        }
        
    except frappe.DoesNotExistError:
        print(f"❌ Template not found: {template_id}")
        return {
            "success": False,
            "error": _("Template not found")
        }
    except Exception as e:
        print(f"❌ Error creating campaign from template: {str(e)}")
        frappe.db.rollback()
        return {
            "success": False,
            "error": str(e)
        }


@frappe.whitelist()
def get_template_preview(template_id):
    """
    Get template preview data for confirmation before creating campaign.
    
    Args:
        template_id: The template ID to preview
        
    Returns:
        dict: Template preview data
    """
    try:
        template = frappe.get_doc("Mira Campaign Template", template_id)
        
        # Count social contents
        social_count = frappe.db.count(
            "Mira Campaign Template Social",
            filters={"template_id": template_id}
        )
        
        # Count triggers from flow_config
        triggers_count = 0
        if template.flow_config:
            try:
                flow_config = json.loads(template.flow_config) if isinstance(template.flow_config, str) else template.flow_config
                triggers_count = len(flow_config.get('triggers', []))
            except:
                triggers_count = 0
        
        has_triggers = triggers_count > 0
        
        # Parse config
        config = {}
        if template.configuration_json:
            try:
                config = json.loads(template.configuration_json) if isinstance(template.configuration_json, str) else template.configuration_json
            except:
                config = {}
        
        return {
            "success": True,
            "data": {
                "template_id": template.name,
                "template_name": template.template_name,
                "campaign_type": template.campaign_type,
                "description": template.description,
                "thumbnail": template.thumbnail,
                "target_pool": config.get("target_pool", ""),
                "social_contents_count": social_count,
                "triggers_count": triggers_count,
                "has_triggers": has_triggers,
                "has_landing_page": bool(template.ladipage_url or template.ladipage_id),
                "is_premium": template.is_premium,
                "usage_count": template.usage_count or 0
            }
        }
        
    except frappe.DoesNotExistError:
        return {
            "success": False,
            "error": _("Template not found")
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }


@frappe.whitelist()
def get_template_data(template_id):
    """
    Get full template data for populating wizard fields.
    
    Args:
        template_id: The template ID to get data from
        
    Returns:
        dict: Full template data including social contents and flow config
    """
    try:
        print(f"📋 Getting template data: {template_id}")
        
        template = frappe.get_doc("Mira Campaign Template", template_id)
        
        # Get social contents
        social_contents = frappe.get_all(
            "Mira Campaign Template Social",
            filters={"template_id": template_id},
            fields=["name", "platform", "template_content", "subject", 
                    "social_media_images", "page_id", "connection_id",
                    "mjml_content", "block_content", "post_file"]
        )
        
        print(f"✅ Found {len(social_contents)} social contents")
        
        return {
            "success": True,
            "data": {
                "template_id": template.name,
                "template_name": template.template_name,
                "campaign_type": template.campaign_type,
                "description": template.description,
                "objective": template.objective,
                "target_pool": template.target_pool,
                "ladipage_url": template.ladipage_url,
                "ladipage_id": template.ladipage_id,
                "thumbnail": template.thumbnail,
                "configuration_json": template.configuration_json,
                "flow_config": template.flow_config,
                "social_contents": social_contents,
                "is_default": template.is_default,
                "is_premium": template.is_premium
            }
        }
        
    except frappe.DoesNotExistError:
        print(f"❌ Template not found: {template_id}")
        return {
            "success": False,
            "error": _("Template not found")
        }
    except Exception as e:
        print(f"❌ Error getting template data: {str(e)}")
        return {
            "success": False,
            "error": str(e)
        }
