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
        frappe.logger().info(f"🚀 Creating campaign from template: {template_id}")
        
        # 1. Get template data
        template = frappe.get_doc("Mira Campaign Template", template_id)
        
        # Parse configuration_json
        config = {}
        if template.configuration_json:
            try:
                config = json.loads(template.configuration_json) if isinstance(template.configuration_json, str) else template.configuration_json
            except:
                config = {}
        
        # 2. Create campaign
        campaign_data = {
            "doctype": "Mira Campaign",
            "campaign_name": campaign_name or template.template_name,
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
        
        frappe.logger().info(f"✅ Campaign created: {campaign.name}")
        
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
            
        frappe.logger().info(f"✅ Copied {len(social_contents)} social contents")
        
        # 4. Copy flows/triggers from template
        template_flows = frappe.get_all(
            "Mira Flow",
            filters={"campaign_template_id": template_id},
            fields=["*"]
        )
        
        frappe.logger().info(f"🔄 Found {len(template_flows)} template flows to copy")
        
        for flow in template_flows:
            frappe.logger().info(f"📋 Copying flow: {flow.get('name')} - {flow.get('title')}")
            # Create new flow for campaign
            new_flow = frappe.get_doc({
                "doctype": "Mira Flow",
                "title": flow.get("title"),
                "campaign_id": campaign.name,
                "campaign_template_id": None,  # Clear template reference
                "description": flow.get("description"),
                "status": "Draft",
                "type": "Campaign",
                "target_type": flow.get("target_type"),
                "channel": flow.get("channel"),
                "owner_id": frappe.session.user
            })
            new_flow.insert(ignore_permissions=True)
            
            # Copy triggers
            template_triggers = frappe.get_all(
                "Mira Flow Trigger",
                filters={"flow_id": flow.get("name")},
                fields=["*"]
            )
            
            for trigger in template_triggers:
                new_trigger = frappe.get_doc({
                    "doctype": "Mira Flow Trigger",
                    "flow_id": new_flow.name,
                    "trigger_type": trigger.get("trigger_type"),
                    "target_type": "Campaign",
                    "status": trigger.get("status", "ACTIVE"),
                    "conditions": trigger.get("conditions"),
                    "schedule_time": trigger.get("schedule_time"),
                    "channel": trigger.get("channel")
                })
                new_trigger.insert(ignore_permissions=True)
                
            # Copy actions
            template_actions = frappe.get_all(
                "Mira Flow Action",
                filters={"parent": flow.get("name")},
                fields=["*"]
            )
            
            for action in template_actions:
                new_action = frappe.get_doc({
                    "doctype": "Mira Flow Action",
                    "parent": new_flow.name,
                    "parenttype": "Mira Flow",
                    "parentfield": "action_id",
                    "action_type": action.get("action_type"),
                    "channel_type": action.get("channel_type"),
                    "content": action.get("content"),
                    "delay_minutes": action.get("delay_minutes", 0),
                    "action_parameters": action.get("action_parameters"),
                    "status": action.get("status", "ACTIVE")
                })
                new_action.insert(ignore_permissions=True)
                
        frappe.logger().info(f"✅ Copied {len(template_flows)} flows with triggers and actions")
        
        # 5. Update template usage statistics
        frappe.db.set_value("Mira Campaign Template", template_id, {
            "usage_count": (template.usage_count or 0) + 1,
            "last_used_at": datetime.now()
        })
        
        frappe.db.commit()
        
        return {
            "success": True,
            "message": _("Campaign created successfully from template"),
            "data": {
                "campaign_id": campaign.name,
                "campaign_name": campaign.campaign_name,
                "type": campaign.type,
                "status": campaign.status,
                "social_contents_count": len(social_contents),
                "flows_count": len(template_flows)
            }
        }
        
    except frappe.DoesNotExistError:
        return {
            "success": False,
            "error": _("Template not found")
        }
    except Exception as e:
        frappe.log_error(f"Error creating campaign from template: {str(e)}")
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
            filters={"parent": template_id}
        )
        
        # Count flows
        flow_count = frappe.db.count(
            "Mira Flow",
            filters={"campaign_template_id": template_id}
        )
        
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
                "target_pool": config.get("target_pool", ""),
                "social_contents_count": social_count,
                "flows_count": flow_count,
                "has_landing_page": bool(template.ladipage_url or template.ladipage_id),
                "is_premium": template.is_premium
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
