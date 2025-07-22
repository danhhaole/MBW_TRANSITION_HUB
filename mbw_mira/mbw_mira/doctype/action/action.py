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
		if self.status in ["EXECUTED","FAILED"]:
			update_step_result_talent_campaign(self)


def update_step_result_talent_campaign(doc):
	"""Update trạng thái TalentProfilesCampaign khi action đã thực hiện

	Args:
		doc (dict): _description_
	""" 
	#Action có 2 trạng thái này thì update TalentProfilesCampaign
	talent_campaign = frappe.get_doc("TalentProfilesCampaign", doc.talent_campaign_id)
	if talent_campaign.status != "ACTIVE":
		return

	current_order = talent_campaign.current_step_order
	next_step = frappe.get_all(
		"CampaignStep",
		filters={"campaign": talent_campaign.campaign_id, "step_order": current_order + 1},
		fields=["name", "step_order", "delay_in_days"],
		limit=1,
	)

	if not next_step:
		talent_campaign.status = "COMPLETED"
		talent_campaign.next_action_at = None
	else:
		step_info = next_step[0]
		talent_campaign.current_step_order = step_info.step_order
		talent_campaign.next_action_at = add_days(now_datetime(), step_info.delay_in_days or 0)

	talent_campaign.save()
	return True




#Hàm lấy ra action theo action_type trong step campaign
def get_action_worker(step):
	"""Lấy danh sách action có status là SCHEDULED và step tương ứng

	Args:
		step (SEND_EMAIL/SEND_SMS): _description_
	"""
	actions = frappe.get_list("Action",filters={"status":"SCHEDULED", "scheduled_at":["<=", now_datetime()]})
	#Duyệt danh sách actions, tìm step nào có action_type là gửi email
	actions_name =[]
	for action in actions:
		step_exists = frappe.db.exists("CampaignStep",{"name":action.campaign_step, "action_type":step})
		if step_exists:
			actions_name.append(action)
	return actions_name

def check_duplicate_action(doc):
    filters = {
        "talent_campaign_id": doc.talent_campaign_id,
        "campaign_step": doc.campaign_step,
    }

    existing = frappe.db.exists("Action", filters)

    if existing and existing != doc.name:  # ← tránh trùng với chính mình khi update
        frappe.throw(
            frappe._(
                "An Action with Candidate Campaign <b>{0}</b> and Campaign Step <b>{1}</b> already exists: <a href='/app/action/{2}'>{2}</a>"
            ).format(
                doc.talent_campaign_id,
                doc.campaign_step,
                existing
            ),
            title=frappe._("Duplicate Action")
        )


	
		
