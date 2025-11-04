# Copyright (c) 2025, MBWCloud Co. and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
import json


class MiraSequence(Document):
	pass


@frappe.whitelist()
def get_sequence_with_flows(sequence_id):
	"""
	Get sequence with all flows and actions in one API call
	Returns sequence data with steps containing full flow details
	"""
	try:
		# Get sequence
		sequence = frappe.get_doc('Mira Sequence', sequence_id)
		
		# Parse steps JSON
		steps_json = []
		try:
			steps_json = json.loads(sequence.steps) if sequence.steps else []
		except:
			steps_json = []
		
		# Get all flows for this sequence
		flows = frappe.get_all(
			'Mira Flow',
			filters={
				'sequence_id': sequence_id,
				'type': 'Sequence'
			},
			fields=['name'],
			order_by='creation asc'
		)
		
		# Get full flow details with actions and triggers
		flows_with_actions = []
		for flow in flows:
			flow_doc = frappe.get_doc('Mira Flow', flow.name)
			flows_with_actions.append({
				'name': flow_doc.name,
				'title': flow_doc.title,
				'channel': flow_doc.channel,
				'status': flow_doc.status,
				'type': flow_doc.type,
				'sequence_id': flow_doc.sequence_id,
				'creation': flow_doc.creation,
				'modified': flow_doc.modified,
				'action_id': [
					{
						'name': action.name,
						'action_type': action.action_type,
						'channel_type': action.channel_type,
						'action_parameters': action.action_parameters,
						'trigger_id': action.trigger_id if hasattr(action, 'trigger_id') else None,
						'order': action.order if hasattr(action, 'order') else 0
					}
					for action in (flow_doc.action_id or [])
				],
				'trigger_id': [
					{
						'name': trigger.name,
						'trigger_type': trigger.trigger_type,
						'status': trigger.status,
						'channel': trigger.channel,
						'conditions': trigger.conditions
					}
					for trigger in (flow_doc.trigger_id or [])
				]
			})
		
		# Combine steps with flows
		combined_steps = []
		for i, step_json in enumerate(steps_json):
			flow_data = flows_with_actions[i] if i < len(flows_with_actions) else None
			combined_steps.append({
				'delay': step_json.get('delay', '1 day'),
				'flow_id': step_json.get('flow_id'),
				'flow': flow_data
			})
		
		# Return combined data
		return {
			'name': sequence.name,
			'title': sequence.title,
			'purpose': sequence.purpose,
			'status': sequence.status,
			'enrollment_source': sequence.enrollment_source,
			'enrollment_count': sequence.enrollment_count,
			'owner_id': sequence.owner_id,
			'created_at': sequence.created_at,
			'creation': sequence.creation,
			'modified': sequence.modified,
			'steps': combined_steps
		}
		
	except Exception as e:
		frappe.log_error(f"Error getting sequence with flows: {str(e)}")
		frappe.throw(f"Failed to get sequence: {str(e)}")
