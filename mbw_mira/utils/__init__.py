import re
import frappe
import hmac
import hashlib
import json
from rapidfuzz import fuzz
from frappe.utils import now_datetime
from mbw_mira.mbw_mira.doctype.mira_interaction.mira_interaction import (
    create_mira_interaction,
)
from urllib.parse import quote, unquote, urlencode
import ipaddress
import csv

#Send email chạy trigger 
def send_email_job(task_id, action):
    from mbw_mira.utils.email import send_email

    """
    Gửi email cho ứng viên, hỗ trợ cả message raw hoặc template.
    """

    # Lấy thông tin candidate
    task = frappe.get_doc("Mira Task", task_id)
    talentprofiles = frappe.get_cached_doc("Mira Talent", task.related_talent)

    logger = frappe.logger("campaign")
    if not talentprofiles.email:
        frappe.throw("Talent does not have an email.")
    # Nếu ứng viên đã unsubcrible
    if talentprofiles.email_opt_out:
        logger.error("Talent unsubcrible")
        return
    # Nếu email không tồn tại
    if talentprofiles.email_id_invalid:
        logger.error("Talent Email Invalid")
        return
    social = action
    context = (talentprofiles, social, task)

    condition = {}
    if hasattr(action, "action_parameters"):
        condition = json.loads(action.action_parameters)
    temp = condition
    
    # Get email content and render with template
    # Priority: template_content (full HTML) > email_content > block_content
    email_content = temp.get("template_content") or temp.get("email_content") or temp.get("block_content") or ""
    message = render_template(email_content, context)
    
    # IMPORTANT: Inject CSS into email content before sending
    # Try to get CSS from multiple sources
    css_content = temp.get("css_content") or ""
    
    # If no CSS in action_parameters, try to get from Mira Campaign Social if available
    if not css_content and hasattr(action, "campaign_social_id"):
        try:
            campaign_social = frappe.get_doc("Mira Campaign Social", action.campaign_social_id)
            if hasattr(campaign_social, "css_content") and campaign_social.css_content:
                css_content = campaign_social.css_content
                logger.info(f"[EMAIL] Got CSS from Mira Campaign Social: {len(css_content)} chars")
        except Exception as e:
            logger.warning(f"[EMAIL] Could not get CSS from campaign_social: {e}")
    
    if css_content and message:
        # Remove existing <style> tags from message to avoid duplicates
        message = re.sub(r'<style[^>]*>[\s\S]*?</style>', '', message, flags=re.IGNORECASE)
        
        # Inject CSS at the beginning of HTML (before <body> or at the start)
        # Check if message already has <html> or <body> tags
        if '<html>' in message.lower() or '<body>' in message.lower():
            # Insert CSS into <head> if exists, otherwise before <body>
            if '<head>' in message.lower():
                message = re.sub(r'<head[^>]*>', f'<head>\\n<style>{css_content}</style>', message, flags=re.IGNORECASE)
            elif '<body>' in message.lower():
                message = re.sub(r'<body[^>]*>', f'<head>\\n<style>{css_content}</style>\\n</head>\\n<body>', message, flags=re.IGNORECASE)
            else:
                message = f"<style>{css_content}</style>{message}"
        else:
            # No HTML structure, just inject CSS at the beginning
            message = f"<style>{css_content}</style>{message}"
        logger.info(f"[EMAIL] Injected CSS into email content, CSS length: {len(css_content)}")
    elif not css_content:
        logger.warning(f"[EMAIL] No CSS content found for task {task_id}, email will be sent without CSS")
    
    # Ensure base64 images and image URLs are preserved
    # Replace localhost image URLs with production domain
    message = re.sub(r'src="http://localhost[^"]*"', lambda m: m.group(0).replace('localhost:8080', 'hireos.fastwork.vn').replace('localhost:8000', 'hireos.fastwork.vn'), message)
    message = re.sub(r'src="http://127\.0\.0\.1[^"]*"', lambda m: m.group(0).replace('127.0.0.1:8080', 'hireos.fastwork.vn').replace('127.0.0.1:8000', 'hireos.fastwork.vn'), message)
    
    subject = "Thông báo"
    if condition and temp.get("email_subject"):
        subject = render_template(temp.get("email_subject"), context)
    talent_email = talentprofiles.email
    template = None
    template_args = None
    sender = temp.get("sender_account")
    if not talent_email:
        logger.error("[EMAIL ERROR] Missing candidate_email")
        return

    if not subject:
        logger.error(f"[EMAIL ERROR] Missing subject for {talent_email}")
        return

    if not message:
        logger.error(
            f"[EMAIL ERROR] Neither message nor template provided for {talent_email}"
        )
        return

    task.executed_at = now_datetime()
    try:
        result = send_email(
            recipients=[talent_email],
            subject=subject,
            content=message if not template else None,
            template=template,
            template_args=template_args,
            sender=sender
        )

        if result:
            task.status = "EXECUTED"
            task.execution_result = {
                "status": "Success",
                "message": f"[EMAIL] Sent to {talentprofiles.name} — task: {task.name}",
            }
            create_mira_interaction(
                {
                    "talent_id": talentprofiles.name,
                    "interaction_type": "EMAIL_SENT",
                    "source_action": action.name,
                }
            )
        else:
            task.status = "FAILED"
            task.execution_result = {
                "error": f"[EMAIL] Error Sent to {talent_email} — step: {task.name}",
                "traceback": frappe.get_traceback(),
            }
        task.save(ignore_permissions=True)
        frappe.db.commit()
    except Exception as e:
        frappe.log_error(frappe.get_traceback(), "[EMAIL ERROR] send_email_job")
        task.status = "FAILED"
        task.execution_result = {"error": str(e), "traceback": frappe.get_traceback()}
        task.save(ignore_permissions=True)
        frappe.db.commit()
        raise

#Sử dụng send email khi chạy campaign thông quan action
def send_email_action(talentprofile_id, action_id):
    from mbw_mira.utils.email import send_email

    """
    Gửi email cho ứng viên, hỗ trợ cả message raw hoặc template.
    """

    # Lấy thông tin candidate
    action = frappe.get_doc("Mira Action", action_id)
    social = frappe.get_doc("Mira Campaign Social",action.campaign_social)
    talentprofiles = frappe.get_doc("Mira Talent", talentprofile_id)

    logger = frappe.logger("campaign")
    if not talentprofiles.email:
        frappe.throw("Talent does not have an email.")
    # Nếu ứng viên đã unsubcrible
    if talentprofiles.email_opt_out:
        logger.error("Talent unsubcrible")
        return
    # Nếu email không tồn tại
    if talentprofiles.email_id_invalid:
        logger.error("Talent Email Invalid")
        return

    context = (talentprofiles, social, None)

    condition = {}
    if hasattr(social, "action_parameters"):
        condition = json.loads(social.action_parameters)
    temp = condition
    
    # Get email content - prioritize template_content (full HTML) > email_content
    email_content = temp.get("template_content") or temp.get("email_content") or ""
    message = render_template(email_content, context)
    
    # IMPORTANT: Inject CSS into email content before sending
    css_content = temp.get("css_content") or ""
    
    # If no CSS in action_parameters, try to get from Mira Campaign Social
    if not css_content and hasattr(social, "css_content") and social.css_content:
        css_content = social.css_content
        logger.info(f"[EMAIL] Got CSS from Mira Campaign Social: {len(css_content)} chars")
    
    if css_content and message:
        # Remove existing <style> tags from message to avoid duplicates
        message = re.sub(r'<style[^>]*>[\s\S]*?</style>', '', message, flags=re.IGNORECASE)
        
        # Inject CSS at the beginning of HTML (before <body> or at the start)
        # Check if message already has <html> or <body> tags
        if '<html>' in message.lower() or '<body>' in message.lower():
            # Insert CSS into <head> if exists, otherwise before <body>
            if '<head>' in message.lower():
                message = re.sub(r'<head[^>]*>', f'<head>\\n<style>{css_content}</style>', message, flags=re.IGNORECASE)
            elif '<body>' in message.lower():
                message = re.sub(r'<body[^>]*>', f'<head>\\n<style>{css_content}</style>\\n</head>\\n<body>', message, flags=re.IGNORECASE)
            else:
                message = f"<style>{css_content}</style>{message}"
        else:
            # No HTML structure, just inject CSS at the beginning
            message = f"<style>{css_content}</style>{message}"
        logger.info(f"[EMAIL] Injected CSS into email content, CSS length: {len(css_content)}")
    elif not css_content:
        logger.warning(f"[EMAIL] No CSS content found for action {action_id}, email will be sent without CSS")
    
    # Ensure base64 images and image URLs are preserved
    # Replace localhost image URLs with production domain
    message = re.sub(r'src="http://localhost[^"]*"', lambda m: m.group(0).replace('localhost:8080', 'hireos.fastwork.vn').replace('localhost:8000', 'hireos.fastwork.vn'), message)
    message = re.sub(r'src="http://127\.0\.0\.1[^"]*"', lambda m: m.group(0).replace('127.0.0.1:8080', 'hireos.fastwork.vn').replace('127.0.0.1:8000', 'hireos.fastwork.vn'), message)
    
    subject = "Thông báo"
    if condition and temp.get("email_subject"):
        subject = render_template(temp.get("email_subject"), context)
    talent_email = talentprofiles.email
    template = None
    template_args = None
    sender = temp.get("sender_account")
    if not talent_email:
        logger.error("[EMAIL ERROR] Missing candidate_email")
        return

    if not subject:
        logger.error(f"[EMAIL ERROR] Missing subject for {talent_email}")
        return

    if not message:
        logger.error(
            f"[EMAIL ERROR] Neither message nor template provided for {talent_email}"
        )
        return

    action.executed_at = now_datetime()
    
    # Log thông tin ban đầu
    logger.info(f"[EMAIL] ========== START send_email_action ==========")
    logger.info(f"[EMAIL] Action: {action.name}")
    logger.info(f"[EMAIL] Social: {social.name} (current status: {social.status})")
    logger.info(f"[EMAIL] Talent: {talentprofiles.name} ({talent_email})")
    logger.info(f"[EMAIL] Subject: {subject[:50]}")
    
    try:
        result = send_email(
            recipients=[talent_email],
            subject=subject,
            content=message if not template else None,
            template=template,
            template_args=template_args,
            sender=sender
        )
        
        logger.info(f"[EMAIL] send_email() returned: {result}")

        # Check Email Queue status thực tế sau khi gửi
        # Đợi một chút để Email Queue được tạo và process
        import time
        email_sent_successfully = False
        email_queue_status = None
        email_queues = []  # Khai báo biến bên ngoài vòng lặp
        latest_queue = None
        
        # Retry check Email Queue (tối đa 5 lần, mỗi lần đợi 2 giây)
        logger.info(f"[EMAIL] Starting Email Queue check (max 5 attempts, 2s delay each)")
        for attempt in range(5):
            logger.info(f"[EMAIL] --- Attempt {attempt + 1}/5: Waiting 2 seconds...")
            time.sleep(2)  # Đợi 2 giây để Email Queue được process
            
            # Tìm Email Queue record gần nhất - mở rộng filter để tìm chính xác hơn
            from frappe.utils import add_to_date
            # Tìm theo recipient và thời gian (không cần subject vì có thể bị encode)
            time_filter = add_to_date(frappe.utils.now_datetime(), minutes=-10)
            logger.info(f"[EMAIL] Searching Email Queue: recipient={talent_email}, creation > {time_filter}")
            
            # Lấy tất cả Email Queue records gần đây (chỉ lấy fields cơ bản)
            email_queues = frappe.get_all(
                "Email Queue",
                filters={
                    "creation": [">", time_filter]
                },
                fields=["name", "status", "modified", "error", "creation"],
                order_by="creation desc",
                limit=20
            )
            
            logger.info(f"[EMAIL] Found {len(email_queues)} Email Queue records (attempt {attempt + 1}, last 10 minutes)")
            
            # Filter trong Python code: check recipients và subject
            matching_queues = []
            for queue in email_queues:
                try:
                    # Load full doc để lấy recipients và subject
                    queue_doc = frappe.get_doc("Email Queue", queue.name)
                    queue_recipients = getattr(queue_doc, 'recipients', '') or ''
                    queue_subject = getattr(queue_doc, 'subject', '') or ''
                    
                    # Check recipient match
                    recipient_match = talent_email.lower() in queue_recipients.lower() if queue_recipients else False
                    # Check subject match (fuzzy)
                    subject_match = False
                    if subject and queue_subject:
                        subject_clean = subject[:50].lower().strip()
                        queue_subject_clean = queue_subject[:50].lower().strip()
                        subject_match = subject_clean in queue_subject_clean or queue_subject_clean in subject_clean
                    
                    if recipient_match and (subject_match or attempt >= 2):  # Sau 2 retries, chỉ cần recipient match
                        matching_queues.append({
                            **queue,
                            'recipients': queue_recipients
                        })
                except Exception as e:
                    logger.warning(f"[EMAIL]   Error loading queue {queue.name}: {e}")
                    continue
            
            logger.info(f"[EMAIL] Found {len(matching_queues)} matching Email Queue records (attempt {attempt + 1})")
            if matching_queues:
                for idx, q in enumerate(matching_queues[:3]):  # Log 3 records đầu
                    # Load subject từ doc
                    try:
                        q_doc = frappe.get_doc("Email Queue", q.name)
                        q_subject = getattr(q_doc, 'subject', '') or 'N/A'
                        logger.info(f"[EMAIL]   Queue {idx+1}: {q.name} | status={q.status} | subject={q_subject[:30]}")
                    except:
                        logger.info(f"[EMAIL]   Queue {idx+1}: {q.name} | status={q.status} | subject=N/A")
            
            if matching_queues:
                # Tìm queue phù hợp nhất (có subject tương tự hoặc gần nhất)
                for queue in matching_queues:
                    # Queue đã được filter theo recipient, chỉ cần check status
                    latest_queue = queue
                    email_queue_status = queue.status
                    # Load subject từ doc để log
                    try:
                        queue_doc_subject = frappe.get_doc("Email Queue", queue.name)
                        queue_subject_log = getattr(queue_doc_subject, 'subject', '') or 'N/A'
                    except:
                        queue_subject_log = 'N/A'
                    logger.info(f"[EMAIL] Email Queue {queue.name} status: {email_queue_status} (attempt {attempt + 1})")
                    logger.info(f"[EMAIL] Queue subject: {queue_subject_log[:50]}")
                    
                    if queue.status == "Sent":
                        email_sent_successfully = True
                        logger.info(f"[EMAIL] ✅ Email sent successfully - Queue: {queue.name}")
                        break
                    elif queue.status in ["Error", "Not Sent"]:
                        email_sent_successfully = False
                        logger.warning(f"[EMAIL] ❌ Email failed - Queue: {queue.name}, Status: {queue.status}")
                        break
                
                if latest_queue and latest_queue.status == "Sent":
                    break
                # Nếu status là "Queued" hoặc "Sending", tiếp tục retry
            else:
                logger.info(f"[EMAIL] No matching Email Queue found yet (attempt {attempt + 1}/5)")
        
        # Nếu vẫn chưa có kết quả, enqueue background job để check sau
        if not email_sent_successfully and email_queue_status not in ["Sent", "Error", "Not Sent"]:
            frappe.enqueue(
                "mbw_mira.api.campaign_social.check_email_queue_and_update_status",
                action_name=action.name,
                social_name=social.name,
                talent_email=talent_email,
                subject=subject,
                queue="short",
                job_name=f"check_email_queue_{action.name}"
            )
            logger.info(f"[EMAIL] Enqueued background job to check Email Queue later")
        
        # Fallback: nếu không tìm thấy Email Queue, dùng result từ send_email
        if email_queue_status is None:
            email_sent_successfully = result
            email_queue_status = "Not Found"
            logger.warning(f"[EMAIL] Email Queue not found, using send_email result: {result}")

        # Lấy thông tin Email Queue nếu có
        latest_queue_name = None
        if latest_queue:
            latest_queue_name = latest_queue.name
            if email_sent_successfully and latest_queue.modified:
                # Sử dụng modified từ Email Queue (thay vì sent_at vì sent_at không tồn tại)
                social.executed_at = latest_queue.modified
                social.share_at = latest_queue.modified
                logger.info(f"[EMAIL] Set executed_at from Email Queue: {latest_queue.modified}")
            elif email_sent_successfully:
                # Nếu không có sent_at, dùng now
                social.executed_at = now_datetime()
                social.share_at = now_datetime()
                logger.info(f"[EMAIL] Set executed_at to now: {now_datetime()}")
        
        logger.info(f"[EMAIL] ========== DECISION POINT ==========")
        logger.info(f"[EMAIL] email_sent_successfully: {email_sent_successfully}")
        logger.info(f"[EMAIL] email_queue_status: {email_queue_status}")
        logger.info(f"[EMAIL] latest_queue: {latest_queue.name if latest_queue else 'None'}")
        logger.info(f"[EMAIL] Current social.status: {social.status}")
        logger.info(f"[EMAIL] Current social.executed_at: {social.executed_at}")
        
        if email_sent_successfully:
            logger.info(f"[EMAIL] ✅ Setting status to Success...")
            action.status = "EXECUTED"
            social.status = "Success"
            # Đảm bảo executed_at và share_at được set
            if not social.executed_at:
                social.executed_at = now_datetime()
                logger.info(f"[EMAIL] Set executed_at to now: {social.executed_at}")
            if not social.share_at:
                social.share_at = now_datetime()
                logger.info(f"[EMAIL] Set share_at to now: {social.share_at}")
            
            logger.info(f"[EMAIL] ✅ Before save - social.status={social.status}, social.executed_at={social.executed_at}")
            
            action.execution_result = {
                "status": "Success",
                "message": f"[EMAIL] Sent to {talentprofiles.name} — task: {action.name}",
                "email_queue_status": email_queue_status,
                "email_queue_name": latest_queue_name
            }
            social.response_data = {
                "status": "Success",
                "message": f"[EMAIL] Sent to {talentprofiles.name} — task: {action.name}",
                "email_queue_status": email_queue_status,
                "email_queue_name": latest_queue_name
            }
            # Clear error message nếu có
            social.error_message = None
            create_mira_interaction(
                {
                    "talent_id": talentprofiles.name,
                    "interaction_type": "EMAIL_SENT",
                    "source_action": action.name,
                }
            )
            logger.info(f"[EMAIL] ✅ Prepared data for save - social.status={social.status}, social.executed_at={social.executed_at}")
        else:
            action.status = "FAILED"
            social.status = "Failed"
            error_msg = f"[EMAIL] Error Sent to {talent_email} — step: {action.name}"
            if latest_queue and latest_queue.error:
                error_msg += f" — Error: {latest_queue.error}"
            action.execution_result = {
                "error": error_msg,
                "email_queue_status": email_queue_status,
                "email_queue_name": latest_queue_name,
                "traceback": frappe.get_traceback(),
            }
            social.response_data = {
                "error": error_msg,
                "email_queue_status": email_queue_status,
                "email_queue_name": latest_queue_name,
                "traceback": frappe.get_traceback(),
            }
            if latest_queue and latest_queue.error:
                social.error_message = latest_queue.error
            logger.warning(f"[EMAIL] ❌ Updated Mira Campaign Social {social.name} to Failed")
        
        # Save và commit ngay lập tức để đảm bảo status được update
        logger.info(f"[EMAIL] ========== SAVING ==========")
        logger.info(f"[EMAIL] Before save - Action status: {action.status}")
        logger.info(f"[EMAIL] Before save - Social status: {social.status}")
        logger.info(f"[EMAIL] Before save - Social executed_at: {social.executed_at}")
        
        try:
            action.save(ignore_permissions=True)
            logger.info(f"[EMAIL] ✅ Action saved: {action.name} status={action.status}")
        except Exception as e:
            logger.error(f"[EMAIL] ❌ Error saving action: {e}")
            logger.error(f"[EMAIL] Traceback: {frappe.get_traceback()}")
        
        try:
            social.save(ignore_permissions=True)
            logger.info(f"[EMAIL] ✅ Social saved: {social.name} status={social.status}, executed_at={social.executed_at}")
        except Exception as e:
            logger.error(f"[EMAIL] ❌ Error saving social: {e}")
            logger.error(f"[EMAIL] Traceback: {frappe.get_traceback()}")
        
        try:
            frappe.db.commit()
            logger.info(f"[EMAIL] ✅ Database committed")
        except Exception as e:
            logger.error(f"[EMAIL] ❌ Error committing: {e}")
            logger.error(f"[EMAIL] Traceback: {frappe.get_traceback()}")
        
        # Verify sau khi save
        try:
            social_reload = frappe.get_doc("Mira Campaign Social", social.name)
            logger.info(f"[EMAIL] ========== VERIFICATION ==========")
            logger.info(f"[EMAIL] After save - Social status: {social_reload.status}")
            logger.info(f"[EMAIL] After save - Social executed_at: {social_reload.executed_at}")
            logger.info(f"[EMAIL] After save - Action status: {action.status}")
            logger.info(f"[EMAIL] ========== END send_email_action ==========")
        except Exception as e:
            logger.error(f"[EMAIL] ❌ Error verifying: {e}")
    except Exception as e:
        frappe.log_error(frappe.get_traceback(), "[EMAIL ERROR] send_email_job")
        action.status = "FAILED"
        social.status = "Failed"
        action.execution_result = {"error": str(e), "traceback": frappe.get_traceback()}
        social.response_data = {"error": str(e), "traceback": frappe.get_traceback()}
        action.save(ignore_permissions=True)
        social.save(ignore_permissions=True)
        frappe.db.commit()
        raise


def send_sms_job(talentprofile_id, action_id, step_id):
    try:
        talentprofiles = frappe.get_cached_doc("Mira Prospect", talentprofile_id)
        action = frappe.get_doc("Mira Action", action_id)
        step = frappe.get_cached_doc("Mira Campaign Step", step_id)
        # Gửi thật nếu có provider
        phone = talentprofiles.phone
        message = None
        talent_id = talentprofiles.name

        create_mira_interaction(
            {
                "talent_id": talent_id,
                "interaction_type": "SMS_SENT",
                "source_action": action.name,
            }
        )

        if not talentprofiles.phone:
            frappe.throw("Candidate does not have a phone number.")
        action.executed_at = now_datetime()
        action.status = "EXECUTED"
        action.result = {
            "status": "Success",
            "message": f"[EMAIL] Sent to {talentprofile_id} — step: {step} — candidate: {talentprofile_id}",
        }

        action.save(ignore_permissions=True)
        frappe.db.commit()
    except Exception as e:
        frappe.logger("campaign").error(f"[SMS ERROR] {phone} — {str(e)}")
        raise


def render_template(template_str, context):
    from urllib.parse import urlencode

    if not template_str:
        return "Xin chào bạn"

    talentprofiles, social, step = context

    # Base URL
    origin = frappe.request.headers.get("Origin")
    protocol = frappe.request.scheme
    host = frappe.request.host
    base_url = origin if origin else f"{protocol}://{host}"

    # Campaign
    campaign = frappe.get_doc("Mira Campaign", social.campaign_id)

    # =====================
    # Tracking Pixel
    # =====================
    pixel_params = {
        "talent_id": talentprofiles.name,
        "action": social.name,
        "url": campaign.ladipge_url,
        "utm_campaign": campaign.name,
        "utm_source": "email",
        "utm_medium": "email",
        "utm_term": campaign.tags,
    }

    sig = make_signature(pixel_params)
    pixel_query = urlencode({**pixel_params, "sig": sig})
    tracking_url = (
        f"{base_url}/api/method/mbw_mira.api.interaction.page_visited?{pixel_query}"
    )
    # Gửi vào context
    ctx = {
        "candidate_name": talentprofiles.full_name,
        "tracking_pixel_url": (
            f"{base_url}/api/method/mbw_mira.api.interaction.tracking_pixel?{pixel_query}"
        ),
        "unsubscribe_link": _create_unsubscribe_link(talentprofiles.name, campaign),
    }

    # =====================
    # Render raw HTML trước khi replace URL
    # =====================
    rendered_html = frappe.render_template(template_str, ctx)

    # =====================
    # Replace toàn bộ URL trong email bằng tracking link
    # =====================
    rendered_html = append_tracking_to_urls(
        content=rendered_html,
        tracking_url=tracking_url
    )

    return rendered_html

def _create_email_tracking(talent_id, campaign, original_url, action="EMAIL_CLICK"):
    origin = frappe.request.headers.get("Origin")
    protocol = frappe.request.scheme
    host = frappe.request.host
    base_url = origin if origin else f"{protocol}://{host}"

    params = {
        "talent_id": talent_id,
        "action": action,
        "url": original_url,
        "utm_campaign": campaign.name,
        "utm_source": "email",
        "utm_medium": "email",
        "utm_term": campaign.tags
    }

    sig = make_signature(params)
    query = urlencode({**params, "sig": sig})

    return (
        f"{base_url}/api/method/mbw_mira.api.interaction.click_redirect?{query}"
    )

def _create_unsubscribe_link(talent_id, campaign):
    
    params = {
        "talent_id": talent_id,
        "campaign": campaign.name,
        "action": "EMAIL_UNSUBSCRIBED"
    }

    sig = make_signature(params)
    query = urlencode({**params, "sig": sig})

    return f"{_get_base_url()}/api/method/mbw_mira.api.interaction.unsubscribe?{query}"

from frappe.utils import get_url

def _get_base_url():
    # Nếu đang trong HTTP request → dùng request data
    if getattr(frappe, "request", None):
        try:
            origin = frappe.request.headers.get("Origin")
            if origin:
                return origin

            protocol = frappe.request.scheme
            host = frappe.request.host
            if protocol and host:
                return f"{protocol}://{host}"
        except Exception:
            pass

    # Nếu đang trong background job hoặc không có request → fallback an toàn
    return get_url()
def append_tracking_to_urls(content, tracking_url):
    """
    Thay tất cả URL trong content bằng redirect URL:
    - Gói URL gốc vào param `url`
    - Thêm param `url_tracking` với tracking link
    - Không thay đổi URL nếu đã có tracking
    """
    url_regex = r"(https?://[^\s\"\'<>]+)"

    # Encode tracking URL
    encoded_tracking = quote(tracking_url, safe="")

    # URL redirect
    redirect_base = f"{_get_base_url()}/api/method/mbw_mira.api.interaction.click_redirect?url="

    def replace(match):
        original_url = match.group(0)

        # Nếu đã có tracking → bỏ qua
        if "url_tracking=" in original_url:
            return original_url

        # Encode URL gốc để làm param
        encoded_original = quote(original_url, safe="")

        # Trả về URL redirect đầy đủ
        return f"{redirect_base}{encoded_original}&url_tracking={encoded_tracking}"

    return re.sub(url_regex, replace, content)



def make_signature(data) -> str:
    # data = f"candidate_id={candidate_id}&action={action}&url={url}"
    SECRET_KEY = (
        frappe.conf.get("tracking_secret_key")
        or "email_track_aff07b5a10af788e14e6fedb38ce39d9"
    )
    return hmac.new(
        SECRET_KEY.encode(), json.dumps(data).encode(), hashlib.sha256
    ).hexdigest()


def verify_signature(data, sig):
    expected = make_signature(data)
    return hmac.compare_digest(expected, sig)


# Tìm candidate khớp với talentsegment
def find_candidates_fuzzy(
    criteria=None, segment_name=None, min_score=55, disenroll=False
):
    """
    Tìm các ứng viên có mức độ khớp >= min_score (0–100) theo fuzzy matching
    giữa candidate và talent_segment conditions.
    """
    try:
        # Convert min_score to float
        min_score = float(min_score) if float(min_score) >= 0 else 55.0
        
        # --- Load conditions và budget từ segment ---
        conditions = []
        segment_min_budget = None
        segment_max_budget = None
        
        if segment_name:
            segment_data = frappe.db.get_value(
                "Mira Segment", 
                segment_name, 
                ["criteria", "min_budget", "max_budget"],
                as_dict=True
            )
            
            if segment_data:
                # Parse conditions
                conditions_str = segment_data.get("criteria")
                if conditions_str:
                    try:
                        conditions = json.loads(conditions_str or "[]")
                    except Exception as e:
                        frappe.log_error(f"Lỗi khi đọc conditions JSON: {e}")
                        return []
                
                # Get budget range
                segment_min_budget = segment_data.get("min_budget")
                segment_max_budget = segment_data.get("max_budget")

        if not conditions or len(conditions) == 0:
            frappe.throw(f"Không tìm thấy điều kiện trong segment '{segment_name}'")

        # --- Parse conditions thành criteria ---
        criteria_skills = []
        criteria_tags = []
        criteria_filters = {}
        conjunction = "and"  # Default conjunction (and/or)

        print(f"\n=== PARSING CONDITIONS ===")
        print(f"Total conditions: {len(conditions)}")

        for condition in conditions:
            # Check for conjunction ("and" or "or")
            if isinstance(condition, str) and condition.lower() in ["and", "or"]:
                conjunction = condition.lower()
                print(f"  → Conjunction: {conjunction.upper()}")
                continue
            
            if not isinstance(condition, list) or len(condition) < 3:
                continue

            field, operator, value = condition[0], condition[1], condition[2]
            print(f"Condition: {field} {operator} {value}")

            # Parse skills
            if field == "skills" and value:
                if isinstance(value, str):
                    criteria_skills = [
                        unquote(s.strip().lower())
                        for s in value.split(",")
                        if s.strip()
                    ]
                elif isinstance(value, list):
                    criteria_skills = [
                        unquote(s.strip().lower()) for s in value if s.strip()
                    ]
                print(f"  → Parsed skills: {criteria_skills}")

            # Parse tags
            elif field == "tags" and value:
                if isinstance(value, str):
                    criteria_tags = [
                        unquote(s.strip().lower())
                        for s in value.split(",")
                        if s.strip()
                    ]
                elif isinstance(value, list):
                    criteria_tags = [
                        unquote(s.strip().lower()) for s in value if s.strip()
                    ]
                print(f"  → Parsed tags: {criteria_tags}")

            # Parse other fields
            else:
                criteria_filters[field] = {"operator": operator, "value": value}
                print(f"  → Added filter: {field} {operator} {value}")

        print(f"\n=== CRITERIA SUMMARY ===")
        print(f"Skills: {criteria_skills}")
        print(f"Tags: {criteria_tags}")
        print(f"Filters: {criteria_filters}")
        print(f"Conjunction: {conjunction.upper()}")
        
        # Count total number of conditions (for single vs multiple condition logic)
        total_conditions = 0
        if criteria_skills:
            total_conditions += 1  # skills counts as 1 condition
        if criteria_tags:
            total_conditions += 1  # tags counts as 1 condition
        total_conditions += len(criteria_filters)  # each filter is 1 condition
        
        print(f"Total conditions count: {total_conditions}")

        if not criteria_skills and not criteria_tags and not criteria_filters:
            frappe.throw(
                f"Không tìm thấy tiêu chí hợp lệ trong segment '{segment_name}'"
            )

        # --Lấy danh sách talent trong talent pool
        if disenroll:
            talent_profiles = frappe.db.get_all(
                "Mira Talent Pool",
                filters={"segment_id": segment_name},
                fields=[
                    "*",
                    "talent_id.full_name",
                    "talent_id.email",
                    "talent_id.phone",
                    "talent_id.skills",
                    "talent_id.tags",
                    "talent_id.source",
                    "talent_id.desired_role",
                    "talent_id.current_city",
                    "talent_id.crm_status",
                    "talent_id.total_years_of_experience",
                    "talent_id.availability_date",
                    "talent_id.internal_rating",
                    "talent_id.soft_skills",
                    "talent_id.cultural_fit",
                    "talent_id.expected_salary",
                ],
            )  # , "enroll_type":"Automatic"
        else:
            # --- Lấy danh sách ứng viên ---
            talent_profiles = frappe.get_all(
                "Mira Talent",
                # filters={"status": "NEW"},
                fields=["*"],  # This includes expected_salary
            )

        results = []
        print("+++++++++++++++++++++", talent_profiles, segment_name)
        print(f"\n=== PROCESSING {len(talent_profiles)} CANDIDATES ===")

        for idx, c in enumerate(talent_profiles):
            talent_skills = c.get("skills")
            talent_tags = c.get("tags")
            talent_source = c.get("source")
            candidate_skills = []
            candidate_tags = []

            print(f"\n--- Candidate {idx + 1}: {c.get('full_name')} ---")

            # Chuyển skills thành list nếu là chuỗi
            if talent_skills:
                if isinstance(talent_skills, str):
                    # Try to parse as JSON first (in case it's stored as string like "['skill1', 'skill2']")
                    try:
                        # Replace single quotes with double quotes for valid JSON
                        json_str = talent_skills.replace("'", '"')
                        parsed = json.loads(json_str)
                        if isinstance(parsed, list):
                            candidate_skills = [
                                unquote(str(s).strip().lower()) for s in parsed if s
                            ]
                        else:
                            candidate_skills = [
                                unquote(s.strip().lower())
                                for s in talent_skills.split(",")
                                if s.strip()
                            ]
                    except Exception as e:
                        print(
                            f"  Error parsing skills JSON: {e}, trying comma-separated"
                        )
                        # Not JSON, treat as comma-separated
                        candidate_skills = [
                            unquote(s.strip().lower())
                            for s in talent_skills.split(",")
                            if s.strip()
                        ]
                elif isinstance(talent_skills, list):
                    # Clean each skill - remove brackets and quotes
                    cleaned_skills = []
                    for s in talent_skills:
                        if s:
                            # Remove leading/trailing brackets and quotes: "['linux'" -> "linux"
                            cleaned = str(s).strip().strip("[]'\"").strip()
                            if cleaned:
                                cleaned_skills.append(unquote(cleaned.lower()))
                    candidate_skills = cleaned_skills
                print(f"Candidate skills: {candidate_skills}")

            if talent_tags:
                if isinstance(talent_tags, str):
                    # Try to parse as JSON first
                    try:
                        # Replace single quotes with double quotes for valid JSON
                        json_str = talent_tags.replace("'", '"')
                        parsed = json.loads(json_str)
                        if isinstance(parsed, list):
                            candidate_tags = [
                                unquote(str(s).strip().lower()) for s in parsed if s
                            ]
                        else:
                            candidate_tags = [
                                unquote(s.strip().lower())
                                for s in talent_tags.split(",")
                                if s.strip()
                            ]
                    except Exception as e:
                        print(f"  Error parsing tags JSON: {e}, trying comma-separated")
                        # Not JSON, treat as comma-separated
                        candidate_tags = [
                            unquote(s.strip().lower())
                            for s in talent_tags.split(",")
                            if s.strip()
                        ]
                elif isinstance(talent_tags, list):
                    # Clean each tag - remove brackets and quotes
                    cleaned_tags = []
                    for t in talent_tags:
                        if t:
                            # Remove leading/trailing brackets and quotes
                            cleaned = str(t).strip().strip("[]'\"").strip()
                            if cleaned:
                                cleaned_tags.append(unquote(cleaned.lower()))
                    candidate_tags = cleaned_tags
                print(f"Candidate tags: {candidate_tags}")

            # --- Tính điểm matching ---
            # Logic mới: 
            # - Nếu chỉ có 1 condition: match 1 trong nhiều giá trị → 100 điểm
            # - Nếu có nhiều conditions: tính điểm theo tỷ lệ match của từng condition
            
            condition_scores = []  # List of scores for each condition
            score_breakdown = []
            
            # Calculate skills score
            if criteria_skills:
                print(f"Checking skills...")
                # Count how many criteria skills the talent has
                matched_skills = 0
                for crit_skill in criteria_skills:
                    # Check exact match (case-insensitive)
                    is_matched = any(
                        crit_skill.lower() == cand_skill.lower() 
                        for cand_skill in candidate_skills
                    )
                    if is_matched:
                        matched_skills += 1
                        print(f"  Skill '{crit_skill}' → MATCHED")
                    else:
                        # Try fuzzy match with high threshold (>= 85)
                        best_fuzzy = max(
                            [fuzz.token_sort_ratio(crit_skill, cand_skill) for cand_skill in candidate_skills],
                            default=0
                        )
                        if best_fuzzy >= 85:
                            matched_skills += 1
                            print(f"  Skill '{crit_skill}' → FUZZY MATCHED ({best_fuzzy}%)")
                        else:
                            print(f"  Skill '{crit_skill}' → NOT MATCHED")
                
                # Calculate skill score for this condition
                if total_conditions == 1:
                    # Single condition: match any 1 skill → 100 points
                    skill_score = 100 if matched_skills >= 1 else 0
                    print(f"  Single condition mode: matched {matched_skills}/{len(criteria_skills)} → {skill_score} points")
                else:
                    # Multiple conditions: score based on match ratio
                    skill_score = round((matched_skills / len(criteria_skills)) * 100)
                    print(f"  Multiple conditions mode: matched {matched_skills}/{len(criteria_skills)} → {skill_score} points")
                
                condition_scores.append(skill_score)
                score_breakdown.append(f"Skills: {matched_skills}/{len(criteria_skills)} matched → {skill_score}")

            # Calculate tags score
            if criteria_tags:
                print(f"Checking tags...")
                # Count how many criteria tags the talent has
                matched_tags = 0
                for criteria_tag in criteria_tags:
                    # Check exact match (case-insensitive)
                    is_matched = any(
                        criteria_tag.lower() == cand_tag.lower() 
                        for cand_tag in candidate_tags
                    )
                    if is_matched:
                        matched_tags += 1
                        print(f"  Tag '{criteria_tag}' → MATCHED")
                    else:
                        # Try fuzzy match with high threshold (>= 85)
                        best_fuzzy = max(
                            [fuzz.token_sort_ratio(criteria_tag, cand_tag) for cand_tag in candidate_tags],
                            default=0
                        )
                        if best_fuzzy >= 85:
                            matched_tags += 1
                            print(f"  Tag '{criteria_tag}' → FUZZY MATCHED ({best_fuzzy}%)")
                        else:
                            print(f"  Tag '{criteria_tag}' → NOT MATCHED")
                
                # Calculate tag score for this condition
                if total_conditions == 1:
                    # Single condition: match any 1 tag → 100 points
                    tag_score = 100 if matched_tags >= 1 else 0
                    print(f"  Single condition mode: matched {matched_tags}/{len(criteria_tags)} → {tag_score} points")
                else:
                    # Multiple conditions: score based on match ratio
                    tag_score = round((matched_tags / len(criteria_tags)) * 100)
                    print(f"  Multiple conditions mode: matched {matched_tags}/{len(criteria_tags)} → {tag_score} points")
                
                condition_scores.append(tag_score)
                score_breakdown.append(f"Tags: {matched_tags}/{len(criteria_tags)} matched → {tag_score}")

            # Check other filters (each filter is a separate condition)
            if criteria_filters:
                print(f"Checking filters...")
                for field, filter_data in criteria_filters.items():
                    operator = filter_data.get("operator")
                    value = filter_data.get("value")
                    talent_value = c.get(field)

                    filter_score = 0
                    if not talent_value:
                        print(f"  Filter '{field}': No value in candidate → 0 points")
                    else:
                        # Simple matching
                        matched = False
                        if operator in ["==", "equals"]:
                            if str(talent_value).lower() == str(value).lower():
                                filter_score = 100
                                matched = True
                        elif operator in ["like", "contains"]:
                            if str(value).lower() in str(talent_value).lower():
                                filter_score = 100
                                matched = True
                        
                        print(f"  Filter '{field}' {operator} '{value}' → {'MATCH (100)' if matched else 'NO MATCH (0)'}")
                    
                    condition_scores.append(filter_score)
                    score_breakdown.append(f"Filter '{field}': {filter_score}")

            # Check salary/budget matching (as a separate condition)
            if segment_min_budget is not None or segment_max_budget is not None:
                talent_expected_salary = c.get("expected_salary")
                salary_score = 0
                
                print(f"Checking salary/budget matching...")
                print(f"  Segment budget range: {segment_min_budget} - {segment_max_budget}")
                print(f"  Talent expected salary: {talent_expected_salary}")
                
                if talent_expected_salary:
                    try:
                        expected_salary = float(talent_expected_salary)
                        min_budget = float(segment_min_budget) if segment_min_budget else 0
                        max_budget = float(segment_max_budget) if segment_max_budget else float('inf')
                        
                        # Perfect match: expected salary within budget range
                        if min_budget <= expected_salary <= max_budget:
                            salary_score = 100
                            print(f"  ✓ PERFECT MATCH: Salary within budget range → 100 points")
                        
                        # Partial match: calculate proximity score
                        else:
                            # If salary is below min_budget
                            if expected_salary < min_budget:
                                diff_percent = ((min_budget - expected_salary) / min_budget) * 100
                                if diff_percent <= 20:
                                    salary_score = round(100 - (diff_percent * 2.5))
                                    print(f"  ~ PARTIAL MATCH: {diff_percent:.1f}% below min → {salary_score} points")
                                else:
                                    salary_score = 0
                                    print(f"  ✗ TOO LOW: {diff_percent:.1f}% below min → 0 points")
                            
                            # If salary is above max_budget
                            elif expected_salary > max_budget:
                                diff_percent = ((expected_salary - max_budget) / max_budget) * 100
                                if diff_percent <= 20:
                                    salary_score = round(100 - (diff_percent * 2.5))
                                    print(f"  ~ PARTIAL MATCH: {diff_percent:.1f}% above max → {salary_score} points")
                                else:
                                    salary_score = 0
                                    print(f"  ✗ TOO HIGH: {diff_percent:.1f}% above max → 0 points")
                        
                    except (ValueError, TypeError) as e:
                        print(f"  Error parsing salary values: {e}")
                        salary_score = 0
                else:
                    print(f"  No expected salary data → 0 points")
                
                condition_scores.append(salary_score)
                score_breakdown.append(f"Salary: {salary_score}")

            # Calculate final score based on conjunction (AND/OR)
            if len(condition_scores) == 0:
                print(f"No conditions matched, skipping candidate")
                continue

            if conjunction == "or":
                # OR logic: if ANY condition matches (score > 0), give 100 points
                # Otherwise, take the max score
                if any(score > 0 for score in condition_scores):
                    avg_score = 100
                else:
                    avg_score = 0
                print(f"\n=== SCORE CALCULATION (OR mode) ===")
                print(f"Condition scores: {condition_scores}")
                print(f"Any match found: {any(score > 0 for score in condition_scores)} → {avg_score}")
            else:
                # AND logic: average of all condition scores
                avg_score = round(sum(condition_scores) / len(condition_scores))
                print(f"\n=== SCORE CALCULATION (AND mode) ===")
                print(f"Condition scores: {condition_scores}")
                print(f"Average: ({' + '.join(map(str, condition_scores))}) / {len(condition_scores)} = {avg_score}")
            
            print(f"Min score required: {min_score}")
            print(f"Result: {'✓ PASS' if avg_score >= min_score else '✗ FAIL'}")

            if avg_score >= min_score:
                results.append(
                    {
                        "name": c.name,
                        "email": c.email,
                        "full_name": c.full_name,
                        "skills": candidate_skills,
                        "tags": candidate_tags,
                        "criteria_skills": criteria_skills,
                        "criteria_tags": criteria_tags,
                        "score": avg_score,  # Already rounded integer
                        "score_breakdown": score_breakdown,
                    }
                )

        # Sắp xếp theo điểm giảm dần
        results.sort(key=lambda x: x["score"], reverse=True)

        print(f"\n=== FINAL RESULTS ===")
        print(f"Total candidates matched: {len(results)}")
        for r in results[:5]:  # Show top 5
            print(f"  {r['full_name']}: {r['score']}")

        return results

    except Exception as e:
        print(f"\n=== ERROR ===")
        print(f"Exception: {str(e)}")
        import traceback

        traceback.print_exc()
        return []


def render_merge_tags(html: str, context: dict) -> str:
    import re

    def replacer(match):
        tag = match.group(1).strip()
        return context.get(tag, f"{{{{ {tag} }}}}")  # nếu không có thì giữ nguyên

    return re.sub(r"\{\{\s*(.*?)\s*\}\}", replacer, html)



def _normalize_condition(cond):
    OPERATOR_MAP = {
        "==": "=",
        "!=": "!=",
        ">": ">",
        "<": "<",
        ">=": ">=",
        "<=": "<="
    }
    """
    Chuyển condition từ campaign sang dạng filters Frappe.
    Hỗ trợ AND/OR lồng nhau.
    Ví dụ:
        [["tags","==","Webinar"],"and",["skills","==","Python"]]
    """
    if isinstance(cond, str):
        # parse JSON string
        cond = json.loads(cond)

    if not isinstance(cond, list):
        frappe.throw(f"Invalid condition format: {cond}")

    # Nếu list có 3 phần: [left, 'and/or', right]
    if len(cond) == 3 and cond[1].lower() in ("and", "or"):
        left = _normalize_condition(cond[0])
        op = cond[1].lower()
        right = _normalize_condition(cond[2])
        return [left, op, right]

    # Nếu là điều kiện đơn: [field, operator, value]
    if len(cond) == 3:
        field, operator, value = cond
        operator = OPERATOR_MAP.get(operator, operator)
        return [field, operator, value]

    frappe.throw(f"Invalid condition format: {cond}")

def convert_po_to_csv(po_path, csv_path):
    import polib

    po = polib.pofile(po_path)
    with open(csv_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        for entry in po:
            if entry.msgid:
                writer.writerow([entry.msgid, entry.msgstr])


# def translate_po_file(input_po_path, output_po_path):
#     from deep_translator import GoogleTranslator
#     import polib
#     # Load file .po gốc
#     po = polib.pofile(input_po_path)
#     # Dịch từng msgid nếu msgstr rỗng
#     for entry in po:
#         if entry.msgid and not entry.msgstr:
#             try:
#                 translated = GoogleTranslator(source='en', target='vi').translate(entry.msgid)
#                 entry.msgstr = translated
#             except Exception as e:
#                 print(f"Lỗi dịch '{entry.msgid}': {e}")
#                 entry.msgstr = ""  # fallback

#     # Ghi ra file mới
#     po.save(output_po_path)
#     print(f"Đã dịch và lưu: {output_po_path}")


def get_real_ip():
    req = frappe.local.request
    ip = (
        req.headers.get("X-Forwarded-For")
        or req.headers.get("X-Real-IP")
        or req.remote_addr
    )
    # Lấy IP đầu tiên nếu có chuỗi danh sách
    if "," in ip:
        ip = ip.split(",")[0].strip()
    try:
        ipaddress.ip_address(ip)
    except ValueError:
        ip = "0.0.0.0"
    return ip
