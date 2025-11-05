# Copyright (c) 2025, MBWCloud Co. and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
import json


class MiraFlow(Document):
	pass


@frappe.whitelist()
def remove_child_action(flow_name, parent_action_name, trigger_key):
	"""
	Disable a child action (set is_disabled = 1) instead of deleting it.
	
	Args:
		flow_name: Name of the Mira Flow
		parent_action_name: Name of the parent Mira Flow Action
		trigger_key: Trigger key (e.g., "email_open")
	
	Returns:
		Dict with success status
	"""
	try:
		# Get the flow document
		flow = frappe.get_doc("Mira Flow", flow_name)
		
		# Find parent action
		parent_action = None
		for action in flow.action_id:
			if action.name == parent_action_name:
				parent_action = action
				break
		
		if not parent_action:
			frappe.throw(f"Parent action {parent_action_name} not found")
		
		# Get parent metadata
		parent_params = json.loads(parent_action.action_parameters or "{}")
		additional_actions = parent_params.get("additional_actions", {})
		
		# Get action_id from metadata
		if trigger_key not in additional_actions:
			frappe.throw(f"Trigger {trigger_key} not found in metadata")
		
		action_id = additional_actions[trigger_key].get("action_id")
		
		# ✅ Disable child action instead of deleting
		if action_id:
			for action in flow.action_id:
				if action.name == action_id:
					# Set is_disabled in action_parameters
					child_params = json.loads(action.action_parameters or "{}")
					child_params["is_disabled"] = 1
					action.action_parameters = json.dumps(child_params)
					break
		
		# Remove from parent metadata
		del additional_actions[trigger_key]
		parent_params["additional_actions"] = additional_actions
		parent_action.action_parameters = json.dumps(parent_params)
		
		# Save the flow
		flow.save()
		
		return {
			"success": True,
			"message": "Child action disabled successfully"
		}
		
	except Exception as e:
		frappe.log_error(f"Error disabling child action: {str(e)}")
		return {
			"success": False,
			"error": str(e)
		}


@frappe.whitelist()
def add_child_action(flow_name, parent_action_name, action_data):
	"""
	Add a child action to a parent action in a flow.
	
	Args:
		flow_name: Name of the Mira Flow
		parent_action_name: Name of the parent Mira Flow Action
		action_data: Dict containing action configuration
			{
				"action_type": "ADD_TAG",
				"channel_type": "Email",
				"action_parameters": {...},
				"trigger_key": "email_open",
				"trigger_label": "Email Opened"
			}
	
	Returns:
		Dict with success status and created action name
	"""
	try:
		# Parse action_data if it's a string
		if isinstance(action_data, str):
			action_data = json.loads(action_data)
		
		# Get the flow document
		flow = frappe.get_doc("Mira Flow", flow_name)
		
		# Find parent action
		parent_action = None
		parent_index = None
		for idx, action in enumerate(flow.action_id):
			if action.name == parent_action_name:
				parent_action = action
				parent_index = idx
				break
		
		if not parent_action:
			frappe.throw(f"Parent action {parent_action_name} not found")
		
		# Create new child action
		child_action = flow.append("action_id", {
			"action_type": action_data.get("action_type"),
			"channel_type": action_data.get("channel_type", "Email"),
			"action_parameters": json.dumps(action_data.get("action_parameters", {})),
			"parent_action_id": parent_action_name,
			"order": len(flow.action_id) + 1,
			"trigger_id": None,
			"next_flow": "",
			"sequence": "",
			"delay_minutes": 0,
			"condition": ""
		})
		
		# Update parent action's additional_actions metadata
		parent_params = json.loads(parent_action.action_parameters or "{}")
		if "additional_actions" not in parent_params:
			parent_params["additional_actions"] = {}
		
		trigger_key = action_data.get("trigger_key")
		if trigger_key:
			parent_params["additional_actions"][trigger_key] = {
				"trigger_event": trigger_key,
				"trigger_label": action_data.get("trigger_label", ""),
				"action_type": action_data.get("action_type"),
				"action_id": None,  # Will be set after save
				"configured": True
			}
		
		parent_action.action_parameters = json.dumps(parent_params)
		
		# Save the flow
		flow.save()
		
		# Update metadata with actual child action name
		if trigger_key:
			parent_params["additional_actions"][trigger_key]["action_id"] = child_action.name
			parent_action.action_parameters = json.dumps(parent_params)
			flow.save()
		
		return {
			"success": True,
			"child_action_name": child_action.name,
			"parent_action_name": parent_action_name
		}
		
	except Exception as e:
		frappe.log_error(f"Error adding child action: {str(e)}")
		return {
			"success": False,
			"error": str(e)
		}
