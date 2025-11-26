import frappe
import json
from frappe import _
from datetime import datetime


@frappe.whitelist()
def save_campaign_as_template(campaign_id, template_name, description=""):
    """
    Save an existing campaign as a template.
    
    Args:
        campaign_id: The campaign ID to convert to template
        template_name: Name for the new template
        description: Optional description for the template
        
    Returns:
        dict: Success/error response with template data
    """
    try:
        print(f"🚀 Starting save_campaign_as_template for: {campaign_id}")
        
        # Get campaign
        campaign = frappe.get_doc("Mira Campaign", campaign_id)
        print(f"📋 Campaign loaded: {campaign.campaign_name}, type: {campaign.type}")
        
        # Create template
        template = frappe.new_doc("Mira Campaign Template")
        template.template_name = template_name
        template.description = description or f"Template created from campaign: {campaign.campaign_name}"
        template.campaign_type = campaign.type
        template.scope_type = "PRIVATE"  # User's private template
        template.is_default = 0
        template.is_premium = 0
        template.is_suggestion = 0
        template.is_active = 1
        template.created_by = frappe.session.user
        
        # Copy basic campaign data
        template.objective = getattr(campaign, 'objective', '') or ''
        template.target_pool = getattr(campaign, 'target_pool', '') or ''
        template.ladipage_url = getattr(campaign, 'ladipage_url', '') or ''
        template.ladipage_id = getattr(campaign, 'ladipage_id', '') or ''
            
        # Build configuration JSON
        config_data = {
            "objective": getattr(campaign, "objective", "") or "",
            "target_pool": getattr(campaign, "target_pool", "") or "",
            "config_data": getattr(campaign, "config_data", "") or "",
            "conditions": getattr(campaign, "conditions", "") or "",
            "candidate_count": getattr(campaign, "candidate_count", 0) or 0,
            "campaign_tags": getattr(campaign, "campaign_tags", "") or "",
            "created_from_campaign": campaign_id,
            "created_at": datetime.now().isoformat()
        }
        template.configuration_json = json.dumps(config_data, indent=2, ensure_ascii=False)
        print(f"📝 Configuration JSON: {template.configuration_json}")
        
        # Save template first to get name
        template.insert(ignore_permissions=True)
        frappe.db.commit()
        print(f"✅ Created template: {template.name}")
        
        # Copy social contents from Mira Campaign Social
        social_contents = frappe.get_all(
            "Mira Campaign Social",
            filters={"campaign_id": campaign_id},
            fields=["name", "platform", "template_content", "subject", "social_media_images", 
                    "social_page_id", "external_connection", "mjml_content", "block_content", "post_file"]
        )
        
        print(f"📱 Found {len(social_contents)} social contents for campaign {campaign_id}")
        
        social_count = 0
        for social in social_contents:
            print(f"  Processing social: {social.name}, platform: {social.platform}, content length: {len(social.template_content or '')}")
            
            # Get content
            content = social.template_content or ""
            
            # Skip if no content
            if not content:
                print(f"  ⚠️ Skipping social content with no content: {social.name}")
                continue
            
            # Map platform to valid options
            platform = social.platform or "Email"
            if platform.lower() == "facebook":
                platform = "Facebook"
            elif platform.lower() == "zalo":
                platform = "Zalo"
            elif platform.lower() == "email":
                platform = "Email"
            elif platform.lower() == "sms":
                platform = "SMS"
            else:
                platform = "Email"  # Default
            
            social_data = {
                "doctype": "Mira Campaign Template Social",
                "template_id": template.name,
                "platform": platform,
                "template_content": content,
                "subject": social.subject or "",
                "social_media_images": social.social_media_images or None,
                "page_id": social.social_page_id or "",
                "connection_id": social.external_connection or "",
                "is_active": 1,
                "mjml_content": social.mjml_content or "",
                "block_content": social.block_content or "",
                "post_file": social.post_file or None
            }
            
            print(f"  📤 Creating template social with data: platform={platform}, content_len={len(content)}")
            
            try:
                social_doc = frappe.get_doc(social_data)
                social_doc.insert(ignore_permissions=True)
                frappe.db.commit()
                social_count += 1
                print(f"  ✅ Copied social content: {social.name} -> {social_doc.name}")
            except Exception as e:
                print(f"  ❌ Error copying social content {social.name}: {str(e)}")
                import traceback
                traceback.print_exc()
                continue
            
        print(f"✅ Copied {social_count} social contents")
        
        # Copy flows as flow_config JSON
        # Try both Active and active status
        flows = frappe.get_all(
            "Mira Flow",
            filters={"campaign_id": campaign_id},
            fields=["name", "title", "description", "status"]
        )
        
        print(f"🔄 Found {len(flows)} flows for campaign {campaign_id}")
        for f in flows:
            print(f"  Flow: {f.name}, status: {f.status}")
        
        triggers = []
        flows_count = 0
        
        for flow in flows:
            try:
                flow_doc = frappe.get_doc("Mira Flow", flow.name)
                print(f"  Processing flow: {flow.name}")
                print(f"    Triggers count: {len(flow_doc.trigger_id) if flow_doc.trigger_id else 0}")
                print(f"    Actions count: {len(flow_doc.action_id) if flow_doc.action_id else 0}")
                
                # Get triggers from flow
                if flow_doc.trigger_id:
                    for trigger in flow_doc.trigger_id:
                        trigger_data = {
                            "trigger_type": trigger.trigger_type,
                            "status": "active",
                            "conditions": trigger.conditions or "",
                            "actions": []
                        }
                        
                        # Get actions from flow
                        if flow_doc.action_id:
                            for action in flow_doc.action_id:
                                # Parse action_parameters JSON
                                action_params = {}
                                if action.action_parameters:
                                    try:
                                        if isinstance(action.action_parameters, str):
                                            action_params = json.loads(action.action_parameters)
                                        else:
                                            action_params = action.action_parameters
                                        print(f"      Action params: {action_params}")
                                    except Exception as parse_err:
                                        print(f"      ⚠️ Error parsing action_parameters: {parse_err}")
                                        action_params = {}
                                
                                action_data = {
                                    "action_type": getattr(action, 'action_type', '') or "",
                                    "channel_type": getattr(action, 'channel_type', '') or "",
                                    "delay_minutes": getattr(action, 'delay_minutes', 0) or 0
                                }
                                
                                # Get email fields from action_parameters
                                if action_data["action_type"] == "EMAIL":
                                    action_data.update({
                                        "email_subject": action_params.get('email_subject', '') or action_params.get('subject', '') or "",
                                        "email_content": action_params.get('email_content', '') or action_params.get('template_content', '') or "",
                                        "block_content": action_params.get('block_content', '') or "",
                                        "template_content": action_params.get('template_content', '') or "",
                                        "mjml_content": action_params.get('mjml_content', '') or "",
                                        "sender_account": action_params.get('sender_account', '') or "",
                                        "action_parameters": action_params
                                    })
                                    print(f"      📧 Email action: subject={action_data['email_subject'][:50] if action_data['email_subject'] else 'empty'}")
                                else:
                                    # For non-email actions, just copy action_parameters
                                    action_data["action_parameters"] = action_params
                                
                                trigger_data["actions"].append(action_data)
                        
                        triggers.append(trigger_data)
                        flows_count += 1
                        print(f"    ✅ Added trigger: {trigger.trigger_type}")
                    
            except Exception as flow_error:
                print(f"  ❌ Error processing flow {flow.name}: {str(flow_error)}")
                import traceback
                traceback.print_exc()
                continue
        
        print(f"📊 Total triggers collected: {len(triggers)}")
        
        # Save flow_config JSON - always save even if empty
        flow_config = {
            "triggers": triggers,
            "created_from_campaign": campaign_id,
            "updated_at": datetime.now().isoformat()
        }
        template.flow_config = json.dumps(flow_config, indent=2, ensure_ascii=False)
        template.save(ignore_permissions=True)
        frappe.db.commit()
        print(f"✅ Saved flow_config with {len(triggers)} triggers")
        print(f"📝 Flow config: {template.flow_config[:500]}...")
        
        print(f"🎉 Campaign saved as template: {template.name}")
        
        return {
            "success": True,
            "message": _("Campaign saved as template successfully"),
            "data": {
                "template_id": template.name,
                "template_name": template.template_name,
                "campaign_type": template.campaign_type,
                "social_contents_count": social_count,
                "triggers_count": len(triggers)
            }
        }
        
    except frappe.DoesNotExistError:
        print(f"❌ Campaign not found: {campaign_id}")
        return {
            "success": False,
            "error": _("Campaign not found")
        }
    except Exception as e:
        print(f"❌ Error saving campaign as template: {str(e)}")
        frappe.db.rollback()
        return {
            "success": False,
            "error": str(e)
        }
