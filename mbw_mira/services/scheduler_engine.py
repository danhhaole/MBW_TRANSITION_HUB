# scheduler_engine.py
#Schedule quét định kỳ
import frappe
from frappe.utils import now_datetime
from mbw_mira.services.base_engine import BaseScheduler
from mbw_mira.models.action import ActionCreator

class CampaignSchedulerEngine(BaseScheduler):
    def run(self):
        now = now_datetime()
        candidates = frappe.get_all("CandidateCampaign", filters={
            "status": "ACTIVE",
            "next_action_at": ["<=", now]
        }, fields=["name", "campaign", "current_step_order"])

        for c in candidates:
            creator = ActionCreator(candidate_campaign_id=c.name, campaign_id=c.campaign, current_step_order=c.current_step_order)
            creator.create_action()


