"""
Email Tracking API - Track email opens, clicks and trigger follow-up actions
"""

import frappe
from frappe.utils import nowdate, now_datetime, add_to_date, get_datetime
import json
from datetime import datetime, timedelta
from mbw_mira.utils.email import send_email

@frappe.whitelist(allow_guest=True)
def track_email_click(tracking_id, talent_id=None, campaign_id=None):
    """
    Track email click and update talent engagement

    Args:
        tracking_id: Unique tracking ID for the email
        talent_id: ID of the talent who clicked
        campaign_id: ID of the campaign
    """
    try:
        # Log the click
        frappe.logger("email_tracking").info(f"📧 Email click tracked: {tracking_id}, talent: {talent_id}, campaign: {campaign_id}")
        current_time = now_datetime()

        # Check if tracking record exists using SQL
        exists = frappe.db.sql("""
            SELECT name FROM `tabMira Email Tracking` WHERE name = %s
        """, (tracking_id,))

        if exists:
            # Update existing record using SQL
            frappe.db.sql("""
                UPDATE `tabMira Email Tracking`
                SET email_clicked = 1, email_clicked_on = %s, modified = %s, modified_by = %s
                WHERE name = %s
            """, (current_time, current_time, frappe.session.user, tracking_id))
        else:
            # Create new record using SQL (without docstatus column)
            frappe.db.sql("""
                INSERT INTO `tabMira Email Tracking`
                (name, creation, modified, modified_by, owner, idx,
                 talent_id, campaign_id, email_sent, email_sent_on,
                 email_clicked, email_clicked_on, is_active)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """, (
                tracking_id, current_time, current_time, frappe.session.user, frappe.session.user, 0,
                talent_id, campaign_id, 1, current_time,
                1, current_time, 1
            ))

        frappe.db.commit()

        return {"success": True, "message": "Click tracked successfully"}

    except Exception as e:
        frappe.logger("email_tracking").error(f"❌ Error tracking email click: {str(e)}")
        return {"success": False, "error": str(e)}

@frappe.whitelist()
def create_email_tracking(talent_id, campaign_id, email_subject, email_content):
    """
    Create email tracking record when email is sent
    Uses direct SQL to avoid DocType module issues

    Returns:
        dict: Tracking ID and tracking URL
    """
    try:
        # Generate unique tracking ID
        tracking_id = frappe.generate_hash(length=16)
        current_time = now_datetime()

        # Create tracking record using direct SQL
        # First ensure the table exists
        frappe.db.sql("""
            CREATE TABLE IF NOT EXISTS `tabMira Email Tracking` (
                `name` VARCHAR(140) NOT NULL PRIMARY KEY,
                `creation` DATETIME(6),
                `modified` DATETIME(6),
                `modified_by` VARCHAR(140),
                `owner` VARCHAR(140),
                `docstatus` INT(1) NOT NULL DEFAULT 0,
                `idx` INT(8) NOT NULL DEFAULT 0,
                `talent_id` VARCHAR(140),
                `campaign_id` VARCHAR(140),
                `email_subject` VARCHAR(255),
                `email_content` LONGTEXT,
                `email_sent` INT(1) NOT NULL DEFAULT 0,
                `email_sent_on` DATETIME(6),
                `email_clicked` INT(1) NOT NULL DEFAULT 0,
                `email_clicked_on` DATETIME(6),
                `is_active` INT(1) NOT NULL DEFAULT 1,
                `deactivated_on` DATETIME(6),
                `deactivation_reason` VARCHAR(255),
                KEY `modified` (`modified`),
                KEY `talent_id` (`talent_id`),
                KEY `campaign_id` (`campaign_id`),
                KEY `email_sent_on` (`email_sent_on`)
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
        """)

        # Insert tracking record (without docstatus column)
        frappe.db.sql("""
            INSERT INTO `tabMira Email Tracking`
            (name, creation, modified, modified_by, owner, idx,
             talent_id, campaign_id, email_subject, email_content,
             email_sent, email_sent_on, email_clicked, is_active)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """, (
            tracking_id, current_time, current_time, frappe.session.user, frappe.session.user, 0,
            talent_id, campaign_id, email_subject, email_content,
            1, current_time, 0, 1
        ))
        frappe.db.commit()

        # Generate tracking URL
        site_url = frappe.utils.get_url()
        tracking_url = f"{site_url}/api/method/mbw_mira.api.email_tracking.track_email_click?tracking_id={tracking_id}&talent_id={talent_id}&campaign_id={campaign_id}"

        frappe.logger("email_tracking").info(f"📧 Email tracking created: {tracking_id} for talent: {talent_id}")

        return {
            "tracking_id": tracking_id,
            "tracking_url": tracking_url
        }

    except Exception as e:
        frappe.logger("email_tracking").error(f"❌ Error creating email tracking: {str(e)}")
        return {"error": str(e)}

@frappe.whitelist()
def check_no_click_triggers():
    """
    Check for talents who haven't clicked emails within specified timeframe
    and trigger follow-up actions (for testing: 5 minutes, production: configurable days)
    """
    try:
        frappe.logger("email_tracking").info("🔍 Starting no-click trigger check...")

        results = {
            "checked": 0,
            "triggered": 0,
            "deactivated": 0,
            "emails_sent": 0,
            "details": []
        }

        # Get all active campaigns with ON_NO_EMAIL_CLICK triggers
        campaigns = frappe.get_all(
            "Mira Campaign",
            filters={"status": "ACTIVE"},
            fields=["name", "campaign_name", "target_pool"]
        )

        for campaign in campaigns:
            # Get flows for this campaign with ON_NO_EMAIL_CLICK triggers
            flows = frappe.get_all(
                "Mira Flow",
                filters={"campaign_id": campaign.name, "status": "Active"},
                fields=["name"]
            )

            for flow in flows:
                flow_doc = frappe.get_doc("Mira Flow", flow.name)

                # Check for ON_NO_EMAIL_CLICK triggers
                if hasattr(flow_doc, 'trigger_id') and flow_doc.trigger_id:
                    for trigger in flow_doc.trigger_id:
                        if trigger.trigger_type == "ON_NO_EMAIL_CLICK":
                            # Parse trigger conditions to get timeout
                            try:
                                conditions = json.loads(trigger.conditions) if trigger.conditions else {}
                                days_without_click = conditions.get("days_without_click", 5)

                                # For testing: convert days to minutes (5 days = 5 minutes)
                                timeout_minutes = days_without_click

                                frappe.logger("email_tracking").info(f"🕐 Checking trigger with {timeout_minutes} minute timeout")

                                # Calculate cutoff time
                                cutoff_time = add_to_date(now_datetime(), minutes=-timeout_minutes)

                                # Find talents with emails sent before cutoff who haven't clicked
                                no_click_talents = frappe.db.sql("""
                                    SELECT DISTINCT t.name, t.full_name, t.email, et.name as tracking_id,
                                           et.email_sent_on, et.email_subject
                                    FROM `tabMira Email Tracking` et
                                    INNER JOIN `tabMira Talent` t ON t.name = et.talent_id
                                    WHERE et.campaign_id = %s
                                    AND et.email_sent = 1
                                    AND et.email_clicked = 0
                                    AND et.is_active = 1
                                    AND et.email_sent_on <= %s
                                """, (campaign.name, cutoff_time), as_dict=True)

                                results["checked"] += len(no_click_talents)

                                for talent_data in no_click_talents:
                                    try:
                                        # Execute trigger actions
                                        for action in flow_doc.action_id:
                                            if action.action_type == "EMAIL":
                                                # Send follow-up email
                                                params = json.loads(action.action_parameters) if action.action_parameters else {}
                                                subject = params.get("email_subject", "Follow-up: Please check our previous email")
                                                content = params.get("email_content", f"""
Hi {talent_data.full_name},

We noticed you haven't had a chance to check our previous email: "{talent_data.email_subject}"

We wanted to follow up and see if you're still interested in our opportunities.

If you're no longer interested, please let us know and we'll respect your preferences.

Best regards,
MOBIWORK Team
""")

                                                # Send follow-up email
                                                send_result = send_email(
                                                    recipients=[talent_data.email],
                                                    subject=subject,
                                                    content=content,
                                                    as_html=False
                                                )

                                                if send_result:
                                                    results["emails_sent"] += 1
                                                    frappe.logger("email_tracking").info(f"📧 Follow-up email sent to {talent_data.email}")

                                            elif action.action_type == "STOP_TRACKING":
                                                # Deactivate talent tracking
                                                tracking_doc = frappe.get_doc("Mira Email Tracking", talent_data.tracking_id)
                                                tracking_doc.is_active = 0
                                                tracking_doc.deactivated_on = now_datetime()
                                                tracking_doc.deactivation_reason = "No email click after timeout"
                                                tracking_doc.save(ignore_permissions=True)

                                                results["deactivated"] += 1
                                                frappe.logger("email_tracking").info(f"🚫 Deactivated tracking for {talent_data.email}")

                                        results["triggered"] += 1
                                        results["details"].append({
                                            "talent": talent_data.full_name,
                                            "email": talent_data.email,
                                            "sent_on": talent_data.email_sent_on,
                                            "subject": talent_data.email_subject
                                        })

                                    except Exception as action_error:
                                        frappe.logger("email_tracking").error(f"❌ Error executing action for {talent_data.email}: {str(action_error)}")

                            except Exception as trigger_error:
                                frappe.logger("email_tracking").error(f"❌ Error processing trigger: {str(trigger_error)}")

        frappe.db.commit()

        frappe.logger("email_tracking").info(f"✅ No-click check completed: {results}")

        return {
            "success": True,
            "results": results
        }

    except Exception as e:
        frappe.logger("email_tracking").error(f"❌ Error in no-click trigger check: {str(e)}")
        return {"success": False, "error": str(e)}

@frappe.whitelist()
def manual_trigger_email_tracking(campaign_id=None):
    """
    Manual trigger - ONLY checks existing emails and stops nurturing for no-click talents
    Does NOT send new emails - only deactivates talents who haven't clicked existing emails
    """
    try:
        frappe.logger("email_tracking").info(f"🔥 Manual trigger started - checking no-click emails for campaign: {campaign_id}")

        results = {
            "talents_checked": 0,
            "talents_deactivated": 0,
            "nurturing_stopped": 0,
            "details": []
        }

        # Only check existing emails that haven't been clicked (older than 1 minute)
        cutoff_time = add_to_date(now_datetime(), minutes=-1)

        # First, log ALL tracking records to debug
        all_records = frappe.db.sql("""
            SELECT et.name as tracking_id, et.talent_id, et.email_sent_on,
                   et.email_clicked, et.is_active, t.full_name, t.current_status
            FROM `tabMira Email Tracking` et
            INNER JOIN `tabMira Talent` t ON t.name = et.talent_id
            ORDER BY et.email_sent_on DESC
        """, as_dict=True)

        frappe.logger("email_tracking").info(f"🔍 ALL tracking records in database ({len(all_records)}):")
        for record in all_records:
            frappe.logger("email_tracking").info(f"  - {record.tracking_id}: {record.full_name} - sent: {record.email_sent_on}, clicked: {record.email_clicked}, active: {record.is_active}, status: {record.current_status}")

        # Build query based on campaign_id with detailed logging
        frappe.logger("email_tracking").info(f"🔍 Checking emails sent before: {cutoff_time}")

        if campaign_id:
            no_click_emails = frappe.db.sql("""
                SELECT et.name as tracking_id, et.talent_id, et.email_sent_on,
                       et.email_subject, et.campaign_id, t.full_name, t.email,
                       et.email_clicked, et.is_active, et.email_content
                FROM `tabMira Email Tracking` et
                INNER JOIN `tabMira Talent` t ON t.name = et.talent_id
                WHERE et.email_sent = 1
                AND et.email_clicked = 0
                AND et.is_active = 1
                AND et.email_sent_on <= %s
                AND (et.campaign_id = %s OR et.campaign_id IS NULL)
                AND t.current_status = 'Active'
                AND et.email_content LIKE '%tracking_id=%'
            """, (cutoff_time, campaign_id), as_dict=True)
        else:
            # Check all campaigns if no specific campaign_id
            no_click_emails = frappe.db.sql("""
                SELECT et.name as tracking_id, et.talent_id, et.email_sent_on,
                       et.email_subject, et.campaign_id, t.full_name, t.email,
                       et.email_clicked, et.is_active, et.email_content
                FROM `tabMira Email Tracking` et
                INNER JOIN `tabMira Talent` t ON t.name = et.talent_id
                WHERE et.email_sent = 1
                AND et.email_clicked = 0
                AND et.is_active = 1
                AND et.email_sent_on <= %s
                AND t.current_status = 'Active'
                AND et.email_content LIKE '%tracking_id=%'
            """, (cutoff_time,), as_dict=True)

        # Log all found emails for debugging
        frappe.logger("email_tracking").info(f"📋 Found {len(no_click_emails)} emails with tracking URLs to check:")
        for email in no_click_emails:
            has_tracking = "tracking_id=" in (email.email_content or "")
            frappe.logger("email_tracking").info(f"  - {email.tracking_id}: {email.full_name} ({email.email}) - sent: {email.email_sent_on}, clicked: {email.email_clicked}, active: {email.is_active}, has_tracking: {has_tracking}")

        # Also check how many emails WITHOUT tracking URLs exist
        all_emails_no_tracking = frappe.db.sql("""
            SELECT COUNT(*) as count FROM `tabMira Email Tracking` et
            WHERE et.email_sent = 1
            AND et.email_clicked = 0
            AND et.is_active = 1
            AND et.email_sent_on <= %s
            AND (et.email_content NOT LIKE '%tracking_id=%' OR et.email_content IS NULL)
        """, (cutoff_time,), as_dict=True)

        frappe.logger("email_tracking").info(f"📋 Found {all_emails_no_tracking[0].count} emails WITHOUT tracking URLs (notification emails) - these will be IGNORED")

        results["talents_checked"] = len(no_click_emails)

        # Group by talent to avoid duplicate processing
        talents_to_deactivate = {}
        for email_record in no_click_emails:
            talent_id = email_record.talent_id
            if talent_id not in talents_to_deactivate:
                talents_to_deactivate[talent_id] = {
                    "talent_name": email_record.full_name,
                    "email": email_record.email,
                    "tracking_records": []
                }
            talents_to_deactivate[talent_id]["tracking_records"].append(email_record)

        # Process each talent only once
        for talent_id, talent_data in talents_to_deactivate.items():
            try:
                # Log detailed info about this talent
                frappe.logger("email_tracking").info(f"🎯 Processing talent: {talent_data['talent_name']} ({talent_data['email']})")
                frappe.logger("email_tracking").info(f"   - Has {len(talent_data['tracking_records'])} unclicked emails")

                # Verify all emails are actually unclicked
                unclicked_count = 0
                for tracking_record in talent_data["tracking_records"]:
                    if tracking_record.email_clicked == 0:
                        unclicked_count += 1
                        frappe.logger("email_tracking").info(f"   - ✗ Email {tracking_record.tracking_id} NOT clicked (sent: {tracking_record.email_sent_on})")
                    else:
                        frappe.logger("email_tracking").info(f"   - ✓ Email {tracking_record.tracking_id} WAS clicked (sent: {tracking_record.email_sent_on})")

                # Only proceed if there are actually unclicked emails
                if unclicked_count > 0:
                    # Change talent status to Passive (stop nurturing)
                    talent = frappe.get_doc("Mira Talent", talent_id)
                    talent.current_status = "Passive"
                    talent.save(ignore_permissions=True)

                    # Deactivate all tracking records for this talent
                    for tracking_record in talent_data["tracking_records"]:
                        frappe.db.sql("""
                            UPDATE `tabMira Email Tracking`
                            SET is_active = 0, deactivated_on = %s,
                                deactivation_reason = %s, modified = %s, modified_by = %s
                            WHERE name = %s
                        """, (
                            now_datetime(),
                            "Nurturing stopped - No email click after 1 minute",
                            now_datetime(), frappe.session.user, tracking_record.tracking_id
                        ))

                    results["talents_deactivated"] += 1
                    results["nurturing_stopped"] += 1
                    results["details"].append({
                        "action": "nurturing_stopped",
                        "talent_name": talent_data["talent_name"],
                        "email": talent_data["email"],
                        "tracking_records_count": len(talent_data["tracking_records"]),
                        "unclicked_count": unclicked_count,
                        "stopped_at": now_datetime(),
                        "reason": f"No clicks on {unclicked_count} emails after 1+ minute"
                    })

                    frappe.logger("email_tracking").info(f"🚫 STOPPED nurturing for {talent_data['talent_name']} - {unclicked_count} unclicked emails")
                else:
                    frappe.logger("email_tracking").info(f"✅ SKIPPED {talent_data['talent_name']} - All emails were clicked")

            except Exception as e:
                frappe.logger("email_tracking").error(f"❌ Error stopping nurturing for talent {talent_id}: {str(e)}")

        frappe.db.commit()

        summary_message = f"Nurturing check completed: Checked {results['talents_checked']} emails, stopped nurturing for {results['nurturing_stopped']} talents"
        frappe.logger("email_tracking").info(f"✅ {summary_message}")

        # Notification emails disabled per user request
        frappe.logger("email_tracking").info(f"📧 Notification emails disabled - no emails sent to users")

        return {
            "success": True,
            "message": summary_message,
            "results": results
        }

    except Exception as e:
        frappe.logger("email_tracking").error(f"❌ Error in manual nurturing check: {str(e)}")
        return {"success": False, "error": str(e)}

@frappe.whitelist()
def check_test_email_tracking():
    """
    Check test emails (campaign_id = NULL) for no-click triggers
    """
    try:
        frappe.logger("email_tracking").info("🔍 Checking test email tracking...")

        results = {
            "checked": 0,
            "triggered": 0,
            "deactivated": 0,
            "emails_sent": 0,
            "details": []
        }

        # Find test emails that haven't been clicked in the last 5 minutes
        cutoff_time = add_to_date(now_datetime(), minutes=-5)

        no_click_emails = frappe.db.sql("""
            SELECT et.name as tracking_id, et.talent_id, et.email_sent_on, et.email_subject
            FROM `tabMira Email Tracking` et
            WHERE et.campaign_id IS NULL
            AND et.email_sent = 1
            AND et.email_clicked = 0
            AND et.is_active = 1
            AND et.email_sent_on <= %s
        """, (cutoff_time,), as_dict=True)

        results["checked"] = len(no_click_emails)

        for email_record in no_click_emails:
            try:
                # Get talent info
                talent = frappe.get_doc("Mira Talent", email_record.talent_id)

                if talent.current_status == "Active":
                    # Change talent status to Passive
                    talent.current_status = "Passive"
                    talent.save(ignore_permissions=True)

                    # Deactivate tracking record
                    frappe.db.sql("""
                        UPDATE `tabMira Email Tracking`
                        SET is_active = 0, deactivated_on = %s,
                            deactivation_reason = %s, modified = %s, modified_by = %s
                        WHERE name = %s
                    """, (
                        now_datetime(),
                        "Test email - No click after 5 minutes",
                        now_datetime(), frappe.session.user, email_record.tracking_id
                    ))

                    results["triggered"] += 1
                    results["deactivated"] += 1
                    results["details"].append({
                        "talent_name": talent.full_name,
                        "email": talent.email,
                        "tracking_id": email_record.tracking_id,
                        "deactivated_at": now_datetime()
                    })

                    frappe.logger("email_tracking").info(f"🚫 Deactivated talent {talent.full_name} - No test email click for 5+ minutes")

            except Exception as e:
                frappe.logger("email_tracking").error(f"❌ Error processing test email {email_record.tracking_id}: {str(e)}")

        frappe.db.commit()

        return {
            "success": True,
            "results": results
        }

    except Exception as e:
        frappe.logger("email_tracking").error(f"❌ Error checking test email tracking: {str(e)}")
        return {"success": False, "error": str(e)}

@frappe.whitelist()
def check_pool_email_tracking_and_deactivate():
    """
    Check emails sent to segment-pools and talent-pools
    Automatically deactivate talents who haven't viewed emails for over 5 minutes when active
    """
    try:
        frappe.logger("email_tracking").info("🔍 Starting pool email tracking check and auto-deactivation...")

        results = {
            "checked_pools": 0,
            "checked_talents": 0,
            "deactivated_talents": 0,
            "follow_up_emails": 0,
            "details": []
        }

        # Get all active campaigns with target pools
        campaigns = frappe.get_all(
            "Mira Campaign",
            filters={"status": "ACTIVE", "target_pool": ["!=", ""]},
            fields=["name", "campaign_name", "target_pool", "type"]
        )

        for campaign in campaigns:
            if not campaign.target_pool:
                continue

            results["checked_pools"] += 1
            pool_name = campaign.target_pool

            frappe.logger("email_tracking").info(f"🎯 Checking pool: {pool_name} for campaign: {campaign.campaign_name}")

            # Get talents from the pool using Mira Talent Pool table
            pool_talents = []

            # Check if Mira Talent Pool doctype exists and get talents by segment_id
            if frappe.db.exists("DocType", "Mira Talent Pool"):
                talent_pool_members = frappe.db.sql("""
                    SELECT DISTINCT t.name, t.full_name, t.email, t.current_status
                    FROM `tabMira Talent` t
                    INNER JOIN `tabMira Talent Pool` tp ON tp.talent_id = t.name
                    WHERE tp.segment_id = %s
                """, (pool_name,), as_dict=True)
                pool_talents.extend(talent_pool_members)

            # Check email tracking for each talent in the pool
            for talent in pool_talents:
                results["checked_talents"] += 1

                # Find emails sent to this talent that haven't been clicked in the last 5 minutes
                cutoff_time = add_to_date(now_datetime(), minutes=-5)

                no_click_emails = frappe.db.sql("""
                    SELECT et.name as tracking_id, et.email_sent_on, et.email_subject,
                           et.campaign_id, et.is_active as tracking_active
                    FROM `tabMira Email Tracking` et
                    WHERE et.talent_id = %s
                    AND (et.campaign_id = %s OR et.campaign_id IS NULL)
                    AND et.email_sent = 1
                    AND et.email_clicked = 0
                    AND et.is_active = 1
                    AND et.email_sent_on <= %s
                """, (talent.name, campaign.name, cutoff_time), as_dict=True)

                if no_click_emails and talent.current_status == "Active":
                    try:
                        # Change talent status from Active to Passive (not interested in engagement)
                        talent_doc = frappe.get_doc("Mira Talent", talent.name)
                        talent_doc.current_status = "Passive"
                        talent_doc.save(ignore_permissions=True)

                        frappe.logger("email_tracking").info(f"📝 Changed talent {talent.full_name} status from Active to Passive")

                        # Deactivate email tracking records using SQL
                        for email_record in no_click_emails:
                            frappe.db.sql("""
                                UPDATE `tabMira Email Tracking`
                                SET is_active = 0, deactivated_on = %s,
                                    deactivation_reason = %s, modified = %s, modified_by = %s
                                WHERE name = %s
                            """, (
                                now_datetime(),
                                "Talent status changed to Passive - No click after 5 minutes",
                                now_datetime(), frappe.session.user, email_record.tracking_id
                            ))

                        # Send follow-up notification email
                        follow_up_content = f"""
Hi {talent.full_name},

We noticed you haven't engaged with our recent emails from the {campaign.campaign_name} campaign.

As per our policy, we have temporarily deactivated your profile to respect your preferences.

If you would like to re-engage with us, please contact our team.

Best regards,
MOBIWORK Team

---
Pool: {pool_name}
Campaign: {campaign.campaign_name}
Deactivated: {now_datetime()}
"""

                        send_result = send_email(
                            recipients=[talent.email],
                            subject=f"Profile Deactivated - {campaign.campaign_name}",
                            content=follow_up_content,
                            as_html=False
                        )

                        if send_result:
                            results["follow_up_emails"] += 1

                        results["deactivated_talents"] += 1
                        results["details"].append({
                            "talent_name": talent.full_name,
                            "email": talent.email,
                            "pool": pool_name,
                            "campaign": campaign.campaign_name,
                            "emails_count": len(no_click_emails),
                            "deactivated_at": now_datetime()
                        })

                        frappe.logger("email_tracking").info(f"🚫 Deactivated talent {talent.full_name} ({talent.email}) from pool {pool_name} - No email clicks for 5+ minutes")

                    except Exception as deactivation_error:
                        frappe.logger("email_tracking").error(f"❌ Error deactivating talent {talent.email}: {str(deactivation_error)}")

        frappe.db.commit()

        frappe.logger("email_tracking").info(f"✅ Pool email tracking check completed: {results}")

        return {
            "success": True,
            "results": results
        }

    except Exception as e:
        frappe.logger("email_tracking").error(f"❌ Error in pool email tracking check: {str(e)}")
        return {"success": False, "error": str(e)}

@frappe.whitelist()
def get_email_tracking_stats(campaign_id=None, talent_id=None):
    """
    Get email tracking statistics
    """
    try:
        filters = {}
        if campaign_id:
            filters["campaign_id"] = campaign_id
        if talent_id:
            filters["talent_id"] = talent_id

        # Get tracking records
        tracking_records = frappe.get_all(
            "Mira Email Tracking",
            filters=filters,
            fields=["name", "talent_id", "campaign_id", "email_sent", "email_clicked",
                   "email_sent_on", "email_clicked_on", "is_active"]
        )

        stats = {
            "total_sent": len([r for r in tracking_records if r.email_sent]),
            "total_clicked": len([r for r in tracking_records if r.email_clicked]),
            "click_rate": 0,
            "active_tracking": len([r for r in tracking_records if r.is_active]),
            "records": tracking_records
        }

        if stats["total_sent"] > 0:
            stats["click_rate"] = round((stats["total_clicked"] / stats["total_sent"]) * 100, 2)

        return stats

    except Exception as e:
        frappe.logger("email_tracking").error(f"❌ Error getting tracking stats: {str(e)}")
        return {"error": str(e)}
