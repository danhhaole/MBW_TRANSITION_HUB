import frappe

def enqueue_action_worker(action_id):
    frappe.enqueue("mbw_mira.services.enqueue_worker.run_action_worker", action_id=action_id)

def run_action_worker(action_id):
    from mbw_mira.services.action_worker import ActionWorker
    ActionWorker(action_id).process()
