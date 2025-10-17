#Kiểm tra các actions đang pending quá lâu, gửi thông báo nhắc nhở cho người được giao (assigned_to).
import frappe
from datetime import datetime, timedelta

def run():
    """
    Check for pending actions too long (not SEND_EMAIL/SEND_SMS).
    """
    now = datetime.now()
    threshold = now - timedelta(minutes=30)

    actions = frappe.get_all(
        "Mira Action",
        filters={
            "status": "SCHEDULED",
            "scheduled_at": ["<=", threshold],
        },
        fields=["name", "campaign_step"]
    )

    for a in actions:
        step = frappe.get_value("Mira Campaign Step", a.campaign_step, "action_type")
        if step not in ("SEND_EMAIL", "SEND_SMS"):
            frappe.enqueue(
                "mbw_mira.workers.process_action.check_pending_action",
                queue="short",
                job_name=a.name,
                action_name=a.name
            )

    return True
