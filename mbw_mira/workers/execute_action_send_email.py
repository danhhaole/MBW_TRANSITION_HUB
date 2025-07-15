#Xử lý và gửi các email marketing đã được lên lịch
import frappe
from mbw_mira.mbw_mira.doctype.action.action import get_action_worker

def process_action_email_active():
	"""Worker quét action là gửi email và status là Scheduled
	"""
	actions = get_action_worker("SEND_EMAIL")
	if actions:
		for action in actions:
			frappe.enqueue(
				"mbw_mira.utils.send_email_job",
				queue="short",
				job_name="send_email_job",
				candidate_id=action.candidate_campaign_id,
				action_id=action.name,
				step_id=action.campaign_step
			)
	return True