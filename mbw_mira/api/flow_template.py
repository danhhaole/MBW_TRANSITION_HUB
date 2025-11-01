import frappe
from frappe import _
import json


@frappe.whitelist()
def create_flow_from_template(template_name, flow_title=None):
    """
    Create a new Mira Flow from a Flow Template
    
    Args:
        template_name: Name of the Flow Template
        flow_title: Optional custom title for the new flow
        
    Returns:
        dict: Created flow document
    """
    try:
        # Get the template
        template = frappe.get_doc("Mira Flow Template", template_name)
        
        if not template:
            frappe.throw(_("Template not found"))
        
        # Create new flow
        flow_doc = frappe.new_doc("Mira Flow")
        
        # Map template type to flow type
        # Template: FLOW, SEQUENCE, CAMPAIGN
        # Mira Flow: Automation, Sequence, Campaign
        type_mapping = {
            'FLOW': 'Automation',
            'SEQUENCE': 'Sequence',
            'CAMPAIGN': 'Campaign'
        }
        
        # Set basic fields
        flow_doc.title = flow_title or f"{template.name_template} - {frappe.utils.now()}"
        flow_doc.description = template.description
        flow_doc.type = type_mapping.get(template.type, 'Automation')  # Default to Automation
        flow_doc.channel = template.channel
        flow_doc.target_type = template.target_type
        flow_doc.status = "Draft"
        flow_doc.owner_id = frappe.session.user
        flow_doc.created_at = frappe.utils.now()
        
        # Copy triggers from template
        # Mira Flow Trigger fields: flow_id, target_type, trigger_type, status, owner_id, tags, 
        # is_sharing, updated_at, conditions, schedule_time, channel
        if template.template_triggers:
            for template_trigger in template.template_triggers:
                trigger = flow_doc.append("trigger_id", {})
                trigger.trigger_type = template_trigger.trigger_type
                trigger.target_type = template_trigger.target_type or 'Talent'
                trigger.channel = template_trigger.channel
                trigger.status = template_trigger.status or 'ACTIVE'
                trigger.owner_id = frappe.session.user
                
                # Parse configuration_json to extract conditions
                if template_trigger.configuration_json:
                    try:
                        config = json.loads(template_trigger.configuration_json)
                        # Extract conditions - support both 'Conditional_Split' and 'conditions'
                        if 'Conditional_Split' in config and config['Conditional_Split']:
                            trigger.conditions = json.dumps(config['Conditional_Split'])
                        elif 'conditions' in config and config['conditions']:
                            trigger.conditions = json.dumps(config['conditions'])
                        # Extract schedule_time if exists
                        if 'schedule_time' in config:
                            trigger.schedule_time = config['schedule_time']
                    except Exception as e:
                        frappe.log_error(f"Error parsing trigger config: {str(e)}")
                        pass
        
        # Copy actions from template
        # Mira Flow Action fields: flow_id, action_type, channel_type, action_parameters,
        # next_flow, sequence, delay_minutes, condition, order
        if template.template_actions:
            for template_action in template.template_actions:
                action = flow_doc.append("action_id", {})
                action.action_type = template_action.action_type
                action.channel_type = template_action.channel_type
                action.order = template_action.order or 0
                
                # Copy action parameters (email content, additional actions, etc.)
                if template_action.action_parameters:
                    action.action_parameters = template_action.action_parameters
        
        # Insert the flow
        flow_doc.insert()
        frappe.db.commit()
        
        # Increment usage count for template
        frappe.db.set_value("Mira Flow Template", template_name, "usage_count", 
                           (template.usage_count or 0) + 1)
        frappe.db.commit()
        
        return {
            "success": True,
            "message": _("Flow created successfully from template"),
            "flow_name": flow_doc.name,
            "flow": flow_doc.as_dict()
        }
        
    except Exception as e:
        frappe.log_error(f"Error creating flow from template: {str(e)}")
        return {
            "success": False,
            "message": str(e)
        }
