#Kiểm tra các actions đang pending quá lâu, gửi thông báo nhắc nhở cho người được giao (assigned_to).
import frappe
from datetime import datetime, timedelta

def run():
    """
    Check for pending actions too long (not SEND_EMAIL/SEND_SMS).
    """
    now = datetime.now()
    threshold = now - timedelta(minutes=30)
    frappe.logger().info(f"[Pending Actions Checker] Running at {now}")

    actions = frappe.get_all(
        "Action",
        filters={
            "status": "SCHEDULED",
            "scheduled_at": ["<=", threshold],
        },
        fields=["name", "campaign_step"]
    )

    for a in actions:
        step = frappe.get_value("CampaignStep", a.campaign_step, "action_type")
        if step not in ("SEND_EMAIL", "SEND_SMS"):
            frappe.enqueue(
                "mbw_mira.workers.process_action.check_pending_action",
                queue="short",
                timeout=120,
                job_name=a.name,
                action_name=a.name
            )
            frappe.logger().warn(f"Pending too long: {a.name} ({step})")
