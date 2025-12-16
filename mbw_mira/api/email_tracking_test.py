"""
Email Tracking Test API - For testing the no-click trigger functionality
"""

import frappe
from frappe.utils import now_datetime, add_to_date
from mbw_mira.api.email_tracking import create_email_tracking, check_no_click_triggers
from mbw_mira.utils.email import send_email
import json

@frappe.whitelist()
def test_send_tracked_email_to_pool(target_pool, subject="Test Email", content="This is a test email for tracking"):
    """
    Send test emails with tracking to all talents in a pool (segment-pool or talent-pool)

    Args:
        target_pool: Pool name to send emails to
        subject: Email subject
        content: Email content
    """
    try:
        frappe.logger("email_tracking_test").info(f"📧 Sending test emails to pool: {target_pool}")

        results = {
            "success": True,
            "sent_count": 0,
            "failed_count": 0,
            "tracking_ids": [],
            "details": []
        }

        # Get talents from the pool using Mira Talent Pool table
        talents = []

        frappe.logger("email_tracking_test").info(f"🔍 Looking for talents in pool: {target_pool}")

        # Check if Mira Talent Pool doctype exists and get talents by segment_id
        if frappe.db.exists("DocType", "Mira Talent Pool"):
            pool_talents = frappe.db.sql("""
                SELECT DISTINCT t.name, t.full_name, t.email, t.current_status
                FROM `tabMira Talent` t
                INNER JOIN `tabMira Talent Pool` tp ON tp.talent_id = t.name
                WHERE tp.segment_id = %s
                LIMIT 10
            """, (target_pool,), as_dict=True)
            talents.extend(pool_talents)
            frappe.logger("email_tracking_test").info(f"📋 Found {len(pool_talents)} talents in pool via Mira Talent Pool")

        # If no talents found, return error instead of using fake test data
        if not talents:
            frappe.logger("email_tracking_test").warning(f"⚠️ No talents found in pool: {target_pool}")
            return {
                "success": False,
                "error": f"No talents found in pool '{target_pool}'. Please check the pool has talents assigned.",
                "sent_count": 0,
                "failed_count": 0
            }

        # Send emails to talents
        for talent in talents:
            try:
                frappe.logger("email_tracking_test").info(f"📤 Attempting to send email to: {talent.email} (Talent: {talent.name})")

                # Create email tracking - use None for campaign_id in test mode
                # since we don't have a real campaign
                tracking_result = create_email_tracking(
                    talent_id=talent.name,
                    campaign_id=None,  # Optional - no real campaign for testing
                    email_subject=subject,
                    email_content=content
                )

                if tracking_result.get("error"):
                    frappe.logger("email_tracking_test").error(f"❌ Failed to create tracking: {tracking_result.get('error')}")
                    results["failed_count"] += 1
                    results["details"].append({"error": f"Tracking creation failed for {talent.email}: {tracking_result.get('error')}"})
                    continue

                frappe.logger("email_tracking_test").info(f"✅ Tracking created: {tracking_result.get('tracking_id')}")

                # Add tracking link to content
                tracking_url = tracking_result["tracking_url"]
                final_content = f"""{content}

---
📧 Test Email Tracking for Pool: {target_pool}
Talent: {talent.full_name}
Click here to simulate email engagement: {tracking_url}

This is a test email for the no-click trigger functionality.
If you don't click the link above within 5 minutes, a follow-up email will be sent automatically.
"""

                # Send email
                frappe.logger("email_tracking_test").info(f"📧 Sending email to {talent.email}...")
                try:
                    send_result = send_email(
                        recipients=[talent.email],
                        subject=f"[TEST-{target_pool}] {subject}",
                        content=final_content,
                        as_html=False
                    )
                    frappe.logger("email_tracking_test").info(f"📧 send_email result: {send_result}")
                except Exception as send_error:
                    frappe.logger("email_tracking_test").error(f"❌ send_email exception: {str(send_error)}")
                    send_result = None

                if send_result:
                    results["sent_count"] += 1
                    results["tracking_ids"].append(tracking_result["tracking_id"])
                    results["details"].append({
                        "talent_name": talent.full_name,
                        "email": talent.email,
                        "tracking_id": tracking_result["tracking_id"],
                        "tracking_url": tracking_url
                    })
                    frappe.logger("email_tracking_test").info(f"✅ Test email sent to {talent.email} with tracking ID: {tracking_result['tracking_id']}")
                else:
                    results["failed_count"] += 1
                    results["details"].append({"error": f"Email send failed for {talent.email}"})
                    frappe.logger("email_tracking_test").error(f"❌ Email send failed for {talent.email}")

            except Exception as talent_error:
                frappe.logger("email_tracking_test").error(f"❌ Error sending to {talent.email}: {str(talent_error)}")
                results["failed_count"] += 1

        results["message"] = f"Sent {results['sent_count']} test emails to pool '{target_pool}'. Check for follow-ups in 5 minutes if not clicked."

        return results

    except Exception as e:
        frappe.logger("email_tracking_test").error(f"❌ Error sending test emails to pool: {str(e)}")
        return {"success": False, "error": str(e)}

@frappe.whitelist()
def test_send_tracked_email(talent_email, campaign_id, subject="Test Email", content="This is a test email for tracking"):
    """
    Send a test email with tracking for testing purposes (legacy function)
    """
    try:
        # Find talent by email
        talent = frappe.db.get_value("Mira Talent", {"email": talent_email}, ["name", "full_name"], as_dict=True)
        if not talent:
            return {"success": False, "error": f"Talent with email {talent_email} not found"}

        # Create email tracking
        tracking_result = create_email_tracking(
            talent_id=talent.name,
            campaign_id=campaign_id,
            email_subject=subject,
            email_content=content
        )

        if tracking_result.get("error"):
            return {"success": False, "error": tracking_result["error"]}

        # Add tracking link to content
        tracking_url = tracking_result["tracking_url"]
        final_content = f"""{content}

---
📧 Test Email Tracking
Click here to simulate email engagement: {tracking_url}

This is a test email for the no-click trigger functionality.
If you don't click the link above within 5 minutes, a follow-up email will be sent automatically.
"""

        # Send email
        send_result = send_email(
            recipients=[talent_email],
            subject=f"[TEST] {subject}",
            content=final_content,
            as_html=False
        )

        frappe.logger("email_tracking_test").info(f"📧 Test email sent to {talent_email} with tracking ID: {tracking_result['tracking_id']}")

        return {
            "success": True,
            "tracking_id": tracking_result["tracking_id"],
            "tracking_url": tracking_url,
            "talent_name": talent.full_name,
            "message": f"Test email sent to {talent_email}. Check for follow-up in 5 minutes if not clicked."
        }

    except Exception as e:
        frappe.logger("email_tracking_test").error(f"❌ Error sending test email: {str(e)}")
        return {"success": False, "error": str(e)}

@frappe.whitelist()
def test_no_click_trigger_now():
    """
    Manually trigger the no-click check for immediate testing
    """
    try:
        frappe.logger("email_tracking_test").info("🧪 Manual no-click trigger test started")

        result = check_no_click_triggers()

        frappe.logger("email_tracking_test").info(f"🧪 Manual test completed: {result}")

        return result

    except Exception as e:
        frappe.logger("email_tracking_test").error(f"❌ Error in manual test: {str(e)}")
        return {"success": False, "error": str(e)}

@frappe.whitelist()
def create_test_campaign_with_trigger(campaign_name="Test No-Click Campaign", target_pool=None):
    """
    Create a test campaign with ON_NO_EMAIL_CLICK trigger for testing
    """
    try:
        # Create test campaign
        campaign = frappe.get_doc({
            "doctype": "Mira Campaign",
            "campaign_name": campaign_name,
            "type": "NURTURING",
            "status": "ACTIVE",
            "target_pool": target_pool,
            "description": "Test campaign for no-click trigger functionality"
        })
        campaign.insert(ignore_permissions=True)

        # Create test flow with ON_NO_EMAIL_CLICK trigger
        flow = frappe.get_doc({
            "doctype": "Mira Flow",
            "flow_name": f"Test Flow - {campaign_name}",
            "campaign_id": campaign.name,
            "status": "Active",
            "trigger_id": [
                {
                    "trigger_type": "ON_NO_EMAIL_CLICK",
                    "conditions": json.dumps({
                        "days_without_click": 5  # 5 minutes for testing
                    }, indent=2),
                    "status": "active"
                }
            ],
            "action_id": [
                {
                    "action_type": "EMAIL",
                    "action_parameters": json.dumps({
                        "email_subject": "Follow-up: We missed you!",
                        "email_content": """Hi there!

We noticed you haven't clicked on our previous email yet.

We wanted to follow up and see if you're still interested in our opportunities.

If you're no longer interested, please let us know and we'll respect your preferences.

Best regards,
MOBIWORK Team"""
                    }, indent=2),
                    "delay_minutes": 0
                },
                {
                    "action_type": "STOP_TRACKING",
                    "action_parameters": json.dumps({
                        "stop_reason": "No email engagement after timeout"
                    }, indent=2),
                    "delay_minutes": 0
                }
            ]
        })
        flow.insert(ignore_permissions=True)

        frappe.logger("email_tracking_test").info(f"🧪 Test campaign created: {campaign.name} with flow: {flow.name}")

        return {
            "success": True,
            "campaign_id": campaign.name,
            "flow_id": flow.name,
            "message": f"Test campaign '{campaign_name}' created with no-click trigger (5 minute timeout)"
        }

    except Exception as e:
        frappe.logger("email_tracking_test").error(f"❌ Error creating test campaign: {str(e)}")
        return {"success": False, "error": str(e)}

@frappe.whitelist()
def get_tracking_logs(limit=50):
    """
    Get recent email tracking logs for debugging
    """
    try:
        # Get recent tracking records
        tracking_records = frappe.get_all(
            "Mira Email Tracking",
            fields=["name", "talent_id", "campaign_id", "email_subject", "email_sent_on",
                   "email_clicked", "email_clicked_on", "is_active", "deactivated_on", "deactivation_reason"],
            order_by="creation desc",
            limit=limit
        )

        # Get talent names
        for record in tracking_records:
            if record.talent_id:
                talent = frappe.db.get_value("Mira Talent", record.talent_id, ["full_name", "email"], as_dict=True)
                if talent:
                    record["talent_name"] = talent.full_name
                    record["talent_email"] = talent.email

        return {
            "success": True,
            "records": tracking_records,
            "count": len(tracking_records)
        }

    except Exception as e:
        frappe.logger("email_tracking_test").error(f"❌ Error getting tracking logs: {str(e)}")
        return {"success": False, "error": str(e)}
