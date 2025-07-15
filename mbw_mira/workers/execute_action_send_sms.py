
import frappe
from mbw_mira.mbw_mira.doctype.action.action import get_action_worker


def process_action_sms_active():
	"""Worker quét action là gửi sms và status là SCHEDULED
	"""
	result = None
	actions = get_action_worker("SEND_SMS")
	if actions:
		for action in actions:
			frappe.enqueue(
				"mbw_mira.utils.send_sms_job",
				queue="short",
				job_name="send_sms_job",
				candidate_id=action.candidate_campaign_id,
				action_id=action.name,
				step_id=action.campaign_step
			)
	return True