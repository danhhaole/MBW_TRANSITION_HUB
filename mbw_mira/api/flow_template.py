import frappe
from frappe import _
import json


def normalize_action_type(action_type):
    """
    Normalize action type from various formats to standard Mira Flow Action type
    
    Args:
        action_type: Action type string (can be lowercase, uppercase, or legacy format)
        
    Returns:
        str: Normalized action type
    """
    if not action_type:
        return 'MESSAGE'
    
    # Convert to uppercase for comparison
    action_type_upper = str(action_type).upper()
    
    # Mapping from legacy/template formats to standard formats
    type_mapping = {
        'ADD_TAG': 'ADD_TAG',
        'REMOVE_TAG': 'REMOVE_TAG',
        'NEXT_FLOW': 'START_FLOW',  # ✅ Legacy format
        'START_FLOW': 'START_FLOW',
        'ADD_TO_SEQUENCE': 'SUBSCRIBE_TO_SEQUENCE',
        'SUBSCRIBE_TO_SEQUENCE': 'SUBSCRIBE_TO_SEQUENCE',
        'SMART_DELAY': 'SMART_DELAY',
        'ADD_CUSTOM_FIELD': 'ADD_CUSTOM_FIELD',
        'REMOVE_CUSTOM_FIELD': 'REMOVE_CUSTOM_FIELD',
        'EMAIL': 'EMAIL',
        'SMS': 'SMS',
        'ZALO': 'ZALO',
        'MESSAGE': 'MESSAGE',
        'LEAD_SCORE': 'LEAD_SCORE',
        'EXTERNAL_REQUEST': 'EXTERNAL_REQUEST',
        'SENT_NOTIFICATION': 'SENT_NOTIFICATION',
        'UNSUBSCRIBE': 'UNSUBSCRIBE',
        'UN_SUBSCRIBE_TO_SEQUENCE': 'UN_SUBSCRIBE_TO_SEQUENCE',
    }
    
    return type_mapping.get(action_type_upper, action_type_upper)


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
        # next_flow, sequence, delay_minutes, condition, order, parent_action_id
        if template.template_actions:
            # Track created actions to handle parent-child relationships
            action_mapping = {}  # template_action.name -> created_action.name
            
            for template_action in template.template_actions:
                # Create main action
                action = flow_doc.append("action_id", {})
                # ✅ Normalize action type
                action.action_type = normalize_action_type(template_action.action_type)
                action.channel_type = template_action.channel_type
                action.order = template_action.order or 0
                
                # Copy action parameters (email content, additional actions, etc.)
                if template_action.action_parameters:
                    action.action_parameters = template_action.action_parameters
                
                # Store mapping for later use
                action_mapping[template_action.name] = action
                
                # ✅ Handle additional_actions: Create child actions
                if template_action.action_parameters:
                    try:
                        params = json.loads(template_action.action_parameters)
                        additional_actions = params.get('additional_actions', {})
                        
                        if additional_actions and isinstance(additional_actions, dict):
                            # Process each additional action
                            for trigger_key, action_config in additional_actions.items():
                                if not action_config.get('configured'):
                                    continue  # Skip unconfigured actions
                                
                                # Create child action
                                child_action = flow_doc.append("action_id", {})
                                
                                # ✅ Get action_type from either 'action_type' or 'type' field and normalize it
                                raw_action_type = action_config.get('action_type') or action_config.get('type', '').upper()
                                child_action.action_type = normalize_action_type(raw_action_type)
                                child_action.channel_type = None  # Child actions don't have channel
                                child_action.order = action.order + 0.1  # Slightly after parent
                                
                                # Set parent relationship
                                # Note: We'll set parent_action_id after insert when we have the actual name
                                child_action.parent_trigger = trigger_key
                                
                                # ✅ Build child action parameters (only action-specific data, no metadata)
                                child_params = {}
                                
                                # Store parent info temporarily for relationship setup (not in parameters)
                                child_action._temp_parent_template_name = template_action.name
                                
                                # Copy action-specific data from template
                                # Template structure: {type: 'add_tag', data: {selected_tags: [...]}, configured: true}
                                action_type = action_config.get('action_type') or action_config.get('type', '').upper()
                                action_data = action_config.get('data', {})
                                
                                if action_type in ['ADD_TAG', 'add_tag']:
                                    # Support both formats: selected_tags (array) or tag_name (string)
                                    if 'selected_tags' in action_data:
                                        child_params['selected_tags'] = action_data.get('selected_tags', [])
                                    elif 'tag_name' in action_config:
                                        child_params['tag_name'] = action_config.get('tag_name', '')
                                    elif 'tag_name' in action_data:
                                        child_params['tag_name'] = action_data.get('tag_name', '')
                                        
                                elif action_type in ['REMOVE_TAG', 'remove_tag']:
                                    if 'selected_tags' in action_data:
                                        child_params['selected_tags'] = action_data.get('selected_tags', [])
                                    elif 'tag_name' in action_config:
                                        child_params['tag_name'] = action_config.get('tag_name', '')
                                    elif 'tag_name' in action_data:
                                        child_params['tag_name'] = action_data.get('tag_name', '')
                                        
                                elif action_type in ['ADD_CUSTOM_FIELD', 'add_custom_field']:
                                    child_params['field_name'] = action_data.get('field_name', action_config.get('field_name', ''))
                                    child_params['field_value'] = action_data.get('field_value', action_config.get('field_value', ''))
                                    
                                elif action_type in ['SMART_DELAY', 'smart_delay']:
                                    child_params['duration'] = action_data.get('duration', action_config.get('duration', '1 day'))
                                    
                                elif action_type in ['START_FLOW', 'start_flow']:
                                    child_params['flow_id'] = action_data.get('flow_id', action_config.get('flow_id', ''))
                                    
                                elif action_type in ['SUBSCRIBE_TO_SEQUENCE', 'subscribe_to_sequence']:
                                    child_params['sequence_id'] = action_data.get('sequence_id', action_config.get('sequence_id', ''))
                                
                                child_action.action_parameters = json.dumps(child_params)
                                
                                # Store mapping for parent relationship
                                action_mapping[f"{template_action.name}_{trigger_key}"] = child_action
                                
                    except Exception as e:
                        frappe.log_error(f"Error processing additional_actions for {template_action.name}: {str(e)}")
                        pass
        
        # Insert the flow
        flow_doc.insert()
        
        # ✅ Update parent_action_id for child actions after insert
        # Now we have the actual action.name values
        for action in flow_doc.action_id:
            if hasattr(action, 'parent_trigger') and action.parent_trigger:
                # Find parent action using temporary attribute
                try:
                    parent_template_name = getattr(action, '_temp_parent_template_name', None)
                    
                    if parent_template_name and parent_template_name in action_mapping:
                        parent_action = action_mapping[parent_template_name]
                        action.parent_action_id = parent_action.name
                        
                        # Update parent's additional_actions metadata with child action_id
                        if parent_action.action_parameters:
                            parent_params = json.loads(parent_action.action_parameters)
                            additional_actions = parent_params.get('additional_actions', {})
                            
                            if action.parent_trigger in additional_actions:
                                additional_actions[action.parent_trigger]['action_id'] = action.name
                                parent_params['additional_actions'] = additional_actions
                                parent_action.action_parameters = json.dumps(parent_params)
                        
                        # Clean up temporary attribute
                        if hasattr(action, '_temp_parent_template_name'):
                            delattr(action, '_temp_parent_template_name')
                except Exception as e:
                    frappe.log_error(f"Error updating parent_action_id: {str(e)}")
                    pass
        
        # Save updated relationships
        flow_doc.save()
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
