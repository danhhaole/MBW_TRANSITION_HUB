import frappe
import json
from frappe import _

@frappe.whitelist()
def create_flow_from_trigger(campaign_id, trigger):
    """
    Create Mira Flow from campaign trigger
    
    Args:
        campaign_id: Mira Campaign ID
        trigger: Trigger configuration dict
            {
                "trigger_type": "MESSAGE_RECEIVED",
                "actions": [
                    {
                        "action_type": "FACEBOOK",
                        "channel_type": "Messenger",
                        "content": "<p>Message content</p>",
                        "delay_minutes": 0
                    }
                ]
            }
    
    Returns:
        {
            "success": True,
            "flow_id": "FLOW-001",
            "message": "Flow created successfully"
        }
    """
    try:
        # Parse trigger if string
        if isinstance(trigger, str):
            trigger = json.loads(trigger)
        
        # Get campaign
        campaign = frappe.get_doc("Mira Campaign", campaign_id)
        
        # Map trigger type
        trigger_type_map = {
            "MESSAGE_RECEIVED": "ON_USER_RESPONSE",
            "LINK_CLICKED": "ON_LINK_CLICK",
            "COMMENT_RECEIVED": "ON_USER_RESPONSE"
        }
        
        # Create Flow
        flow = frappe.new_doc("Mira Flow")
        flow.title = f"{campaign.campaign_name} - {get_trigger_label(trigger.get('trigger_type'))}"
        flow.description = f"Auto-generated flow for campaign {campaign.campaign_name}"
        flow.status = "Active"
        flow.type = "Campaign"
        flow.campaign_id = campaign_id
        
        # Add trigger to trigger_id child table
        flow.append("trigger_id", {
            "trigger_type": trigger_type_map.get(trigger.get("trigger_type"), "CUSTOM_EVENT"),
            "status": "ACTIVE",
            "target_type": "Campaign"
        })
        
        # Add actions to action_id child table
        for idx, action in enumerate(trigger.get("actions", []), start=1):
            action_type = action.get("action_type")
            
            # Store content in action_parameters as JSON
            action_parameters = {
                "content": action.get("content", ""),
                "template_id": None
            }
            
            flow.append("action_id", {
                "action_type": action_type,  # FACEBOOK, ZALO, SMS
                "channel_type": action.get("channel_type"),
                "action_parameters": json.dumps(action_parameters),
                "delay_minutes": action.get("delay_minutes", 0),
                "order": idx
            })
        
        flow.insert()
        frappe.db.commit()
        
        return {
            "success": True,
            "flow_id": flow.name,
            "message": _("Flow created successfully")
        }
        
    except Exception as e:
        frappe.log_error(f"Error creating flow from trigger: {str(e)}")
        return {
            "success": False,
            "error": str(e)
        }


def get_trigger_label(trigger_type):
    """Get human-readable label for trigger type"""
    labels = {
        "MESSAGE_RECEIVED": "Message Received",
        "LINK_CLICKED": "Link Clicked",
        "COMMENT_RECEIVED": "Comment on Post"
    }
    return labels.get(trigger_type, trigger_type)


@frappe.whitelist()
def get_campaign_flows(campaign_id):
    """
    Get all flows for a campaign and convert to trigger format
    
    Args:
        campaign_id: Mira Campaign ID
    
    Returns:
        {
            "success": True,
            "data": [
                {
                    "trigger_type": "MESSAGE_RECEIVED",
                    "actions": [...]
                }
            ]
        }
    """
    try:
        # Get all flows for this campaign
        flows = frappe.get_all(
            "Mira Flow",
            filters={"campaign_id": campaign_id},
            fields=["name", "title", "status"]
        )
        
        triggers = []
        
        for flow_info in flows:
            # Get full flow doc
            flow = frappe.get_doc("Mira Flow", flow_info.name)
            
            # Get trigger type from flow
            trigger_type = None
            if flow.trigger_id and len(flow.trigger_id) > 0:
                flow_trigger = flow.trigger_id[0]
                # Map back to frontend trigger type
                trigger_type_map = {
                    "ON_USER_RESPONSE": "MESSAGE_RECEIVED",
                    "ON_LINK_CLICK": "LINK_CLICKED"
                }
                trigger_type = trigger_type_map.get(flow_trigger.trigger_type, "MESSAGE_RECEIVED")
            
            # Get actions
            actions = []
            if flow.action_id:
                for action in flow.action_id:
                    # Parse action_parameters JSON
                    action_params = {}
                    if action.action_parameters:
                        try:
                            action_params = json.loads(action.action_parameters)
                        except:
                            action_params = {}
                    
                    actions.append({
                        "action_type": action.action_type,
                        "channel_type": action.channel_type,
                        "content": action_params.get("content", ""),
                        "delay_minutes": action.delay_minutes or 0
                    })
            
            if trigger_type:
                triggers.append({
                    "trigger_type": trigger_type,
                    "status": flow.status.lower() if flow.status else "active",
                    "actions": actions
                })
        
        return {
            "success": True,
            "data": triggers
        }
        
    except Exception as e:
        frappe.log_error(f"Error getting campaign flows: {str(e)}")
        return {
            "success": False,
            "error": str(e),
            "data": []
        }


@frappe.whitelist()
def create_or_update_flow(campaign_id, trigger):
    """
    Create or update Mira Flow from trigger data
    - If flow exists for this campaign + trigger_type → Update
    - If flow doesn't exist → Create new
    
    Args:
        campaign_id: Mira Campaign ID
        trigger: Trigger configuration dict with status field
    
    Returns:
        {
            "success": True,
            "flow_id": "FLOW-001",
            "action": "created" or "updated"
        }
    """
    try:
        # Parse trigger if string
        if isinstance(trigger, str):
            trigger = json.loads(trigger)
        
        trigger_type = trigger.get('trigger_type')
        if not trigger_type:
            return {'success': False, 'message': 'trigger_type is required'}
        
        # Map trigger type to flow trigger type
        trigger_type_map = {
            "MESSAGE_RECEIVED": "ON_USER_RESPONSE",
            "LINK_CLICKED": "ON_LINK_CLICK",
            "COMMENT_RECEIVED": "ON_USER_RESPONSE"
        }
        flow_trigger_type = trigger_type_map.get(trigger_type, "CUSTOM_EVENT")
        
        # Find existing flow for this campaign and trigger type
        existing_flows = frappe.get_all(
            "Mira Flow",
            filters={"campaign_id": campaign_id},
            fields=["name"]
        )
        
        existing_flow_id = None
        for flow_info in existing_flows:
            flow = frappe.get_doc("Mira Flow", flow_info.name)
            if flow.trigger_id and len(flow.trigger_id) > 0:
                if flow.trigger_id[0].trigger_type == flow_trigger_type:
                    existing_flow_id = flow.name
                    break
        
        if existing_flow_id:
            # Update existing flow
            flow = frappe.get_doc("Mira Flow", existing_flow_id)
            
            # Update status
            flow.status = trigger.get('status', 'active').capitalize()
            
            # Clear and rebuild actions
            flow.action_id = []
            for idx, action in enumerate(trigger.get("actions", []), start=1):
                action_parameters = {
                    "content": action.get("content", ""),
                    "template_id": None
                }
                
                flow.append("action_id", {
                    "action_type": action.get("action_type"),
                    "channel_type": action.get("channel_type"),
                    "action_parameters": json.dumps(action_parameters),
                    "delay_minutes": action.get("delay_minutes", 0),
                    "order": idx
                })
            
            flow.save(ignore_permissions=True)
            frappe.db.commit()
            
            return {
                "success": True,
                "flow_id": existing_flow_id,
                "action": "updated"
            }
        else:
            # Create new flow
            result = create_flow_from_trigger(campaign_id, trigger)
            if result.get("success"):
                # Update status if specified
                if trigger.get('status'):
                    flow = frappe.get_doc("Mira Flow", result.get("flow_id"))
                    flow.status = trigger.get('status').capitalize()
                    flow.save(ignore_permissions=True)
                    frappe.db.commit()
                
                return {
                    "success": True,
                    "flow_id": result.get("flow_id"),
                    "action": "created"
                }
            else:
                return result
            
    except Exception as e:
        frappe.log_error(f"Error in create_or_update_flow: {str(e)}")
        return {
            "success": False,
            "message": str(e)
        }


@frappe.whitelist()
def sync_campaign_flows(campaign_id, triggers):
    """
    Sync all flows for a campaign in one API call
    - Create new flows for new triggers
    - Update existing flows for changed triggers
    - Delete flows that are no longer in triggers
    
    Args:
        campaign_id: Mira Campaign ID
        triggers: List of trigger configurations
    
    Returns:
        {
            "success": True,
            "created": 2,
            "updated": 1,
            "deleted": 1
        }
    """
    try:
        # Parse triggers if string
        if isinstance(triggers, str):
            triggers = json.loads(triggers)
        
        # Map trigger types
        trigger_type_map = {
            "MESSAGE_RECEIVED": "ON_USER_RESPONSE",
            "LINK_CLICKED": "ON_LINK_CLICK",
            "COMMENT_RECEIVED": "ON_USER_RESPONSE"
        }
        
        # Get existing flows
        existing_flows = frappe.get_all(
            "Mira Flow",
            filters={"campaign_id": campaign_id},
            fields=["name"]
        )
        
        # Track current trigger types
        current_trigger_types = set()
        for trigger in triggers:
            trigger_type = trigger.get('trigger_type')
            if trigger_type:
                flow_trigger_type = trigger_type_map.get(trigger_type, "CUSTOM_EVENT")
                current_trigger_types.add(flow_trigger_type)
        
        # Delete flows that are no longer in triggers
        deleted_count = 0
        for flow_info in existing_flows:
            flow = frappe.get_doc("Mira Flow", flow_info.name)
            if flow.trigger_id and len(flow.trigger_id) > 0:
                flow_trigger_type = flow.trigger_id[0].trigger_type
                
                if flow_trigger_type not in current_trigger_types:
                    frappe.delete_doc("Mira Flow", flow.name, ignore_permissions=True)
                    deleted_count += 1
        
        # Create/Update flows
        created_count = 0
        updated_count = 0
        
        for trigger in triggers:
            result = create_or_update_flow(campaign_id, trigger)
            if result.get("success"):
                if result.get("action") == "created":
                    created_count += 1
                elif result.get("action") == "updated":
                    updated_count += 1
        
        frappe.db.commit()
        
        return {
            "success": True,
            "created": created_count,
            "updated": updated_count,
            "deleted": deleted_count
        }
        
    except Exception as e:
        frappe.log_error(f"Error in sync_campaign_flows: {str(e)}")
        return {
            "success": False,
            "message": str(e)
        }
