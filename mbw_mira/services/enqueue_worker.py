import frappe
from .scheduler_engine import CampaignSchedulerEngine

def enqueue_action_worker(action_id):
    frappe.enqueue("mbw_mira.services.enqueue_worker.run_action_worker", action_id=action_id)

def run_action_worker(action_id):
    from mbw_mira.services.action_worker import ActionWorker
    ActionWorker(action_id).process()

def enqueue_campaign_scheduler():
    frappe.enqueue(method=run_campaign_scheduler)

def run_campaign_scheduler():
    CampaignSchedulerEngine().run()

def enqueue_scheduler_worker(candidate_campaign_id):
    frappe.enqueue("mbw_mira.services.action_scheduler_worker.process_candidate_campaign", candidate_campaign_id=candidate_campaign_id)

def enqueue_nurturing_collector_worker(campaign_id):
    frappe.enqueue("mbw_mira.services.nurturing_collector_worker.process_nurturing_campaign", campaign_id=campaign_id)
