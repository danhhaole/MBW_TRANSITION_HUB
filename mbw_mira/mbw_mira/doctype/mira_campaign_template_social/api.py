import frappe
from frappe import _
import json


@frappe.whitelist()
def get_template_with_social_contents(template_id):
    """Get template data with all social contents for editing"""
    try:
        frappe.logger().info(f"Loading template with social contents: {template_id}")
        
        # Get template basic info
        template = frappe.get_doc("Mira Campaign Template", template_id)
        frappe.logger().info(f"Template loaded: {template.name}, type: {template.campaign_type}")
        
        # Get social contents
        social_result = get_template_social_contents(template_id)
        frappe.logger().info(f"Social contents result: {social_result}")
        
        # Parse configuration_json if exists
        config = {}
        if template.configuration_json:
            try:
                config = json.loads(template.configuration_json) if isinstance(template.configuration_json, str) else template.configuration_json
            except:
                config = {}
        
        frappe.logger().info(f"Parsed config: {config}")
        
        # Build response
        template_data = {
            "name": template.name,
            "template_name": template.template_name,
            "description": template.description,
            "campaign_type": template.campaign_type,
            # Get from config or direct fields
            "objective": config.get("objective", getattr(template, "objective", "")),
            "target_pool": config.get("target_pool", getattr(template, "target_pool", "")),
            "config_data": config.get("config_data", getattr(template, "config_data", "")),
            "conditions": config.get("conditions", getattr(template, "conditions", "")),
            "candidate_count": config.get("candidate_count", getattr(template, "candidate_count", 0)),
            "is_active": getattr(template, "is_active", False),
            "is_premium": template.is_premium,
            "is_suggestion": template.is_suggestion,
            "is_default": template.is_default,
            "scope_type": template.scope_type,
            "ladipage_url": template.ladipage_url,
            "ladipage_id": template.ladipage_id,
            # Include full config for reference
            "configuration": config,
            # Social contents
            "selected_channels": social_result.get("selected_channels", []) if social_result.get("success") else [],
            "facebook_content": social_result.get("formatted", {}).get("facebook_content", {}),
            "zalo_content": social_result.get("formatted", {}).get("zalo_content", {}),
            "email_content": social_result.get("formatted", {}).get("email_content", {}),
            "sms_content": social_result.get("formatted", {}).get("sms_content", {}),
            "social_contents_raw": social_result.get("data", [])
        }
        
        # Get tags
        tags = frappe.get_all(
            "Tag Link",
            filters={"document_type": "Mira Campaign Template", "document_name": template_id},
            fields=["tag"]
        )
        template_data["campaign_tags"] = [{"value": t.tag, "label": t.tag} for t in tags]
        
        return {
            "success": True,
            "data": template_data
        }
        
    except frappe.DoesNotExistError:
        return {
            "success": False,
            "error": _("Template not found")
        }
    except Exception as e:
        frappe.log_error(f"Error getting template with social contents: {str(e)}")
        return {
            "success": False,
            "error": str(e)
        }


@frappe.whitelist()
def create_template_social_content(template_id, platform, content_data):
    """Create or update template social content"""
    try:
        # Check if template social content already exists
        existing = frappe.db.get_value(
            "Mira Campaign Template Social",
            {"template_id": template_id, "platform": platform},
            "name"
        )
        
        if existing:
            # Update existing
            doc = frappe.get_doc("Mira Campaign Template Social", existing)
            doc.update(content_data)
            doc.save()
        else:
            # Create new
            doc = frappe.new_doc("Mira Campaign Template Social")
            doc.template_id = template_id
            doc.platform = platform
            doc.update(content_data)
            doc.insert()
        
        return {
            "success": True,
            "name": doc.name,
            "message": _("Template social content saved successfully")
        }
        
    except Exception as e:
        frappe.log_error(f"Error saving template social content: {str(e)}")
        return {
            "success": False,
            "error": str(e)
        }


@frappe.whitelist()
def get_template_social_contents(template_id):
    """Get all social contents for a template"""
    try:
        contents = frappe.get_all(
            "Mira Campaign Template Social",
            filters={"template_id": template_id, "is_active": 1},
            fields=[
                "name", "platform", "channel_type", "template_content", 
                "subject", "social_media_images", "content_variables",
                "mjml_content", "block_content", "post_file",
                "page_id", "connection_id"
            ]
        )
        
        # Format data for frontend
        formatted_contents = {}
        for content in contents:
            platform = content.get("platform", "").lower()
            channel_type = content.get("channel_type", platform)
            
            if platform == "facebook":
                formatted_contents["facebook_content"] = {
                    "content": content.get("template_content", ""),
                    "image": content.get("social_media_images"),
                    "page_id": content.get("page_id"),
                    "connection_id": content.get("connection_id")
                }
            elif platform == "zalo":
                formatted_contents["zalo_content"] = {
                    "content": content.get("template_content", ""),
                    "image": content.get("social_media_images"),
                    "page_id": content.get("page_id"),
                    "connection_id": content.get("connection_id")
                }
            elif platform == "email":
                formatted_contents["email_content"] = {
                    "subject": content.get("subject", ""),
                    "body": content.get("template_content", ""),
                    "content": content.get("template_content", ""),
                    "mjml_content": content.get("mjml_content"),
                    "block_content": content.get("block_content")
                }
            elif platform == "sms":
                formatted_contents["sms_content"] = {
                    "content": content.get("template_content", "")
                }
        
        # Get selected channels
        selected_channels = [c.get("channel_type", c.get("platform", "").lower()) for c in contents]
        
        return {
            "success": True,
            "data": contents,
            "formatted": formatted_contents,
            "selected_channels": selected_channels
        }
        
    except Exception as e:
        frappe.log_error(f"Error getting template social contents: {str(e)}")
        return {
            "success": False,
            "error": str(e)
        }


@frappe.whitelist()
def delete_template_social_content(template_id, platform):
    """Delete template social content"""
    try:
        existing = frappe.db.get_value(
            "Mira Campaign Template Social",
            {"template_id": template_id, "platform": platform},
            "name"
        )
        
        if existing:
            frappe.delete_doc("Mira Campaign Template Social", existing)
            return {
                "success": True,
                "message": _("Template social content deleted successfully")
            }
        else:
            return {
                "success": False,
                "error": _("Template social content not found")
            }
            
    except Exception as e:
        frappe.log_error(f"Error deleting template social content: {str(e)}")
        return {
            "success": False,
            "error": str(e)
        }


@frappe.whitelist()
def bulk_save_template_social_contents(template_id, contents_data):
    """Bulk save multiple social contents for a template"""
    try:
        results = []
        
        for content in contents_data:
            platform = content.get("platform")
            if not platform:
                continue
                
            result = create_template_social_content(
                template_id, 
                platform, 
                content
            )
            results.append(result)
        
        success_count = sum(1 for r in results if r.get("success"))
        
        return {
            "success": True,
            "saved_count": success_count,
            "total_count": len(contents_data),
            "results": results
        }
        
    except Exception as e:
        frappe.log_error(f"Error bulk saving template social contents: {str(e)}")
        return {
            "success": False,
            "error": str(e)
        }
