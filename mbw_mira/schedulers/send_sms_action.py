import frappe
from datetime import datetime

def run():
    """
    Process scheduled SEND_SMS actions.
    """
    now = datetime.now()

    actions = frappe.get_all(
        "Mira Action",
        filters={
            "status": "SCHEDULED",
            "scheduled_at": ["<=", now],
        },
        fields=["name", "campaign_step"]
    )

    for a in actions:
        step = frappe.db.get_value("Mira Campaign Step", a.campaign_step, "action_type")
        if step == "SEND_SMS":
            frappe.enqueue(
                "mbw_mira.workers.process_action.process_sms_action",
                queue="short",
                timeout=300,
                action_name=a.name
            )
    return True
