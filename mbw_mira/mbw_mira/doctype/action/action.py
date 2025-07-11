# Copyright (c) 2025, MBWCloud Co. and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe.utils import now_datetime,add_days

class Action(Document):
	pass

	def validate(self):
		check_duplicate_action(self)
		
	def on_update(self):
		"""Khi có event update xử lý các luồng
		"""
		update_step_result_candidate_campaign(self)


def update_step_result_candidate_campaign(doc):
	"""Update trạng thái CandidateCampaign khi action đã thực hiện

	Args:
		doc (dict): _description_
	""" 
	#Action có 2 trạng thái này thì update CandidateCampaign
	if doc.status in ["EXECUTED","FAILED"]:
		candidate_campaign = frappe.get_doc("CandidateCampaign", doc.candidate_campaign_id)
		if candidate_campaign.status != "ACTIVE":
			return

		current_order = candidate_campaign.current_step_order
		next_step = frappe.get_all(
			"CampaignStep",
			filters={"campaign": candidate_campaign.campaign_id, "step_order": current_order + 1},
			fields=["name", "step_order", "delay_in_days"],
			limit=1,
		)

		if not next_step:
			candidate_campaign.status = "COMPLETED"
			candidate_campaign.next_action_at = None
		else:
			step_info = next_step[0]
			candidate_campaign.current_step_order = step_info.step_order
			candidate_campaign.next_action_at = add_days(now_datetime(), step_info.delay_in_days or 0)

		candidate_campaign.save()
	return True

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

#Hàm lấy ra action theo action_type trong step campaign
def get_action_worker(step):
	"""Lấy danh sách action có status là SCHEDULED và step tương ứng

	Args:
		step (SEND_EMAIL/SEND_SMS): _description_
	"""
	actions = frappe.db.get_list("Action",filters={"status":"SCHEDULED", "scheduled_at":["<=", now_datetime()]})
	#Duyệt danh sách actions, tìm step nào có action_type là gửi email
	actions_name =[]
	for action in actions:
		step_exists = frappe.db.exists("CampaignStep",{"name":action.campaign_step, "action_type":step})
		if step_exists:
			actions_name.append(action)
	return actions_name

def check_duplicate_action(doc):
    filters = {
        "candidate_campaign_id": doc.candidate_campaign_id,
        "campaign_step": doc.campaign_step,
    }

    existing = frappe.db.exists("Action", filters)

    if existing:
        frappe.throw(
            frappe._("An Action with Candidate Campaign <b>{0}</b> and Campaign Step <b>{1}</b> already exists: <a href='/app/action/{2}'>{2}</a>").format(
                doc.candidate_campaign_id,
                doc.campaign_step,
                existing
            ),
            title=frappe._("Duplicate Action")
        )

	
		
