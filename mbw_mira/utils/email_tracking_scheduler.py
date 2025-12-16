"""
Email Tracking Scheduler - Run periodic checks for no-click triggers
"""

import frappe
from frappe.utils import now_datetime
from mbw_mira.api.email_tracking import check_no_click_triggers, check_pool_email_tracking_and_deactivate

def run_email_tracking_check():
    """
    Scheduler function to check for no-click triggers and pool email tracking
    Runs every 5 minutes for testing purposes
    """
    try:
        frappe.logger("email_tracking_scheduler").info("🔍 Starting scheduled email tracking check...")

        # Run the no-click trigger check
        result1 = check_no_click_triggers()

        # Run the pool email tracking and deactivation check
        result2 = check_pool_email_tracking_and_deactivate()

        # Combine results
        combined_result = {
            "success": True,
            "no_click_check": result1,
            "pool_check": result2
        }

        if result1.get("success"):
            stats1 = result1.get("results", {})
            frappe.logger("email_tracking_scheduler").info(f"✅ No-click trigger check completed: {stats1}")

            if stats1.get("triggered", 0) > 0:
                frappe.logger("email_tracking_scheduler").info(
                    f"📧 Triggered {stats1['triggered']} follow-up actions, "
                    f"sent {stats1['emails_sent']} emails, "
                    f"deactivated {stats1['deactivated']} trackings"
                )
        else:
            frappe.logger("email_tracking_scheduler").error(f"❌ No-click trigger check failed: {result1.get('error')}")
            combined_result["success"] = False

        if result2.get("success"):
            stats2 = result2.get("results", {})
            frappe.logger("email_tracking_scheduler").info(f"✅ Pool email tracking check completed: {stats2}")

            if stats2.get("deactivated_talents", 0) > 0:
                frappe.logger("email_tracking_scheduler").info(
                    f"🚫 Deactivated {stats2['deactivated_talents']} talents from {stats2['checked_pools']} pools, "
                    f"sent {stats2['follow_up_emails']} follow-up emails"
                )
        else:
            frappe.logger("email_tracking_scheduler").error(f"❌ Pool email tracking check failed: {result2.get('error')}")
            combined_result["success"] = False

        return combined_result

    except Exception as e:
        frappe.logger("email_tracking_scheduler").error(f"❌ Scheduler error: {str(e)}")
        frappe.log_error(f"Email tracking scheduler error: {str(e)}", "Email Tracking Scheduler")
        return {"success": False, "error": str(e)}

@frappe.whitelist()
def manual_trigger_check():
    """
    Manual trigger for testing - can be called from frontend
    """
    return run_email_tracking_check()
