import frappe
from datetime import datetime

def run():
    """
    Process scheduled SEND_SMS actions.
    """
    now = datetime.now()
    frappe.logger().info(f"[SEND_SMS Scheduler] Running at {now}")

    actions = frappe.get_all(
        "Action",
        filters={
            "status": "SCHEDULED",
            "scheduled_at": ["<=", now],
        },
        fields=["name", "campaign_step"]
    )

    for a in actions:
        step = frappe.get_value("CampaignStep", a.campaign_step, "action_type")
        if step == "SEND_SMS":
            frappe.enqueue(
                method="your_app.workers.process_action.process_sms_action",
                queue="short",
                timeout=300,
                action_name=a.name
            )
            frappe.logger().info(f"Enqueued SEND_SMS Action: {a.name}")
