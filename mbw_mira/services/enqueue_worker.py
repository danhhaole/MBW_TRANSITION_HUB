import frappe


def enqueue_scheduler_worker(candidate_campaign_id):
    frappe.enqueue(
        "mbw_mira.services.action_scheduler_worker.process_candidate_campaign",
        queue="default",
        now=True,
        candidate_campaign_id=candidate_campaign_id,
    )


def enqueue_nurturing_collector_worker(campaign_id):
    frappe.enqueue(
        "mbw_mira.services.nurturing_collector_worker.process_nurturing_campaign",
        queue="default",
        now=True,
        campaign_id=campaign_id,
    )
