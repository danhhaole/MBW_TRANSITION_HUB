import frappe
from frappe.utils import now
import email
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
import os
import boto3
from frappe.query_builder import DocType, Query


def send_email(
    recipients,
    subject,
    template=None,
    template_args=None,
    content=None,
    sender=None,
    cc=None,
    bcc=None,
    reply_to=None,
    attachments=None,
    text_message=None,
    as_html=True,
    debug=True,
    inline_css=True
):
    print("!!! send_email function called !!!")
    """
    Unified send email utility:
    - Use Frappe Email Account if configured
    - Else fallback to AWS SES
    - Logs all emails to Email Log
    """
    print(f"\n===== EMAIL SEND DEBUG START =====")
    print(f"Recipients: {recipients}")
    print(f"Subject: {subject}")
    print(f"Template: {template}")
    print(f"Content length: {len(content) if content else 0}")
    print(f"Content type: {'HTML' if as_html and content and ('<' in content and '>' in content) else 'Plain Text'}")
    print(f"Sender: {sender}")
    print(f"CC: {cc}")
    print(f"BCC: {bcc}")
    print(f"Reply To: {reply_to}")
    print(f"=====================================")
    print("DEBUG: About to check recipients...")
    if not recipients:
        print("DEBUG: No recipients found, throwing error...")
        frappe.throw("Recipients are required")
    print("DEBUG: Recipients check passed")
    if not (template or content):
        print("DEBUG: No template or content found, throwing error...")
        frappe.throw("Either template name or raw content must be provided")
    print("DEBUG: Template/content check passed")

    print("DEBUG: Skipping normalize_emails and prepare_attachments for debugging...")
    # Skip these functions temporarily to isolate the issue
    prepared_attachments = []
    print("DEBUG: Email preparation complete (simplified)")

    # Default sender
    senderemail = ''
    print("DEBUG: About to check for email account...")
    try:
        email_account = sender_email()
        print(f"DEBUG: Email account check result: {email_account}")
    except Exception as e:
        print(f"DEBUG: Error checking email account: {e}")
        email_account = None

    if email_account:
        senderemail = email_account.email_id
        print(f"DEBUG: Using sender email: {senderemail}")
        print(f"DEBUG: Email account enabled: {email_account.enabled}")
    else:
        print("DEBUG: No email account found!")

    if not sender:
        sender = senderemail or frappe.get_system_settings('mail_sender_name') or 'Notifications'
        print(f"DEBUG: Final sender: {sender}")

    print("DEBUG: About to enter try block for email sending...")
    if template:
        print("DEBUG: Processing template...")
        content = render_template(template, template_args)
        if not text_message:
            text_message = frappe.utils.strip_html(content)
        print("DEBUG: Template processed")
    status = "Success"
    error = None
    print("DEBUG: Status and error initialized")

    try:
        print(f"\nDEBUG: Attempting to send email...")
        print(f"DEBUG: senderemail exists: {bool(senderemail)}")
        print(f"DEBUG: as_html: {as_html}")
        print(f"DEBUG: content exists: {bool(content)}")

        if senderemail:
            print("DEBUG: Using Frappe email account...")
            # Use Frappe with HTML support
            if as_html and content:
                print("DEBUG: Sending HTML email via Frappe...")
                print(f"DEBUG: About to call frappe.sendmail with HTML content...")
                print(f"DEBUG: Content preview: {content[:100]}...")
                # Send as HTML email using 'message' parameter to preserve HTML formatting
                # 'content' parameter goes through template processing which can strip formatting
                # 'message' parameter sends raw HTML as-is
                result = frappe.sendmail(
                    recipients=recipients,
                    subject=subject,
                    sender=senderemail,
                    message=content,  # Use 'message' instead of 'content' to preserve HTML
                    now=True
                )
                print(f"DEBUG: frappe.sendmail returned: {result}")
                # Verify immediate delivery
                try:
                    queue_name = getattr(result, "name", None) or str(result)
                    if queue_name:
                        import time
                        for _ in range(5):  # wait up to ~5 seconds (5*1s)
                            q_status = frappe.db.get_value('Email Queue', queue_name, 'status')
                            if q_status == 'Sent':
                                print(f"DEBUG: EmailQueue {queue_name} status=Sent ✅")
                                break
                            elif q_status in ('Error', 'Cancelled'):
                                raise Exception(f"EmailQueue {queue_name} status={q_status}")
                            time.sleep(1)
                        else:
                            raise Exception(f"EmailQueue {queue_name} not sent within timeout")
                except Exception as verify_err:
                    print(f"DEBUG: Verification failed: {verify_err}")
                    raise
                print("DEBUG: HTML email sent via Frappe successfully!")
            else:
                print("DEBUG: Sending plain text email via Frappe...")
                # Send as plain text
                frappe.sendmail(
                    recipients=recipients,
                    subject=subject,
                    sender=senderemail,
                    message=text_message or content,
                    now=True
                )
                print("DEBUG: Plain text email sent via Frappe successfully!")
            status = "Success"
            frappe.logger().info(f"Email sent via Frappe to {recipients}")
        else:
            print("DEBUG: No email account, falling back to AWS SES...")
            # Fallback to AWS SES with HTML support
            sendmail_via_ses(
                recipients=recipients,
                subject=subject,
                message=content,
                text_message=text_message if text_message else (frappe.utils.strip_html(content) if content else None),
                debug=debug
            )
            print("DEBUG: Email sent via SES successfully!")
            status = "Fallback"
            frappe.logger().info(f"Email sent via AWS SES to {recipients}")

    except Exception as e:
        status = "Failed"
        error = str(e)
        print(f"DEBUG: Email sending failed with error: {error}")
        print(f"DEBUG: Error type: {type(e).__name__}")
        import traceback
        print(f"DEBUG: Traceback: {traceback.format_exc()}")
        frappe.log_error(frappe.get_traceback(), "send_email Failed")
        raise

    finally:
        print(f"DEBUG: Email sending completed with status: {status}")
        # Process email queue to send immediately
        process_email_queue()
        # Check email queue after sending
        check_email_queue()
        # Always log to Email Log
        log_email_transaction(
            subject=subject,
            sender=senderemail or sender,
            recipients=recipients,
            cc=cc,
            bcc=bcc,
            reply_to=reply_to,
            content=content,
            attachments=[a.get("fname") for a in prepared_attachments],
            status=status,
            error=error
        )
        print(f"DEBUG: Email transaction logged")
        print(f"===== EMAIL SEND DEBUG END =====\n")
        return status in ["Success", "Fallback"]

def normalize_emails(emails):
    if not emails:
        return []
    if isinstance(emails, str):
        emails = [emails]
    return [
        e.strip()
        for e in emails
        if e and isinstance(e, str) and all(c not in e for c in [' ', '\n', '\r', '\t'])
    ]


def prepare_attachments(attachments):
    """
    Accept:
    - /files/ URLs
    - File paths
    - Dict with fname+content
    Returns frappe.sendmail-compatible list
    """
    result = []
    if not attachments:
        return result

    for item in attachments:
        if not item:
            continue
        if isinstance(item, dict) and 'fname' in item and 'content' in item:
            result.append(item)
        elif isinstance(item, str):
            if item.startswith("/files/"):
                result.append({"file_url": item})
            elif os.path.exists(item):
                with open(item, "rb") as f:
                    content = f.read()
                result.append({"fname": os.path.basename(item), "content": content})
            else:
                frappe.logger().warn(f"Attachment not found: {item}")
    return result


def render_template(template_name, context):
    if not template_name:
        return ""
    template = frappe.get_doc("Email Template", template_name)
    return frappe.render_template(template.response or "", context or {})

#Gửi email qua s3
def send_via_s3(recipients, subject, html_content, cc=None, bcc=None, attachments=None):
    frappe.logger().info(f"[S3 Fallback] Would send email to {recipients}")
    # Implement your S3, SES, Mailgun, etc. integration here
    pass
def sendmail_via_ses(recipients, subject, message, text_message=None, debug=False):
    print(f"\n===== SES DEBUG START =====")
    print(f"DEBUG: SES recipients: {recipients}")
    print(f"DEBUG: SES subject: {subject}")
    print(f"DEBUG: SES message length: {len(message) if message else 0}")
    print(f"DEBUG: SES text_message length: {len(text_message) if text_message else 0}")
    try:
        sender = (frappe.conf.get("aws_sender") or "no-reply@mbwcloud.com").strip()
        region = frappe.conf.get("aws_region") or "us-east-1"
        aws_access_key_id = frappe.conf.get("aws_access_key_id")
        aws_secret_access_key = frappe.conf.get("aws_secret_access_key")

        print(f"DEBUG: SES sender: {sender}")
        print(f"DEBUG: SES region: {region}")
        print(f"DEBUG: SES access key configured: {bool(aws_access_key_id)}")
        print(f"DEBUG: SES secret key configured: {bool(aws_secret_access_key)}")

        client = boto3.client(
            'ses',
            region_name=region,
            aws_access_key_id=aws_access_key_id,
            aws_secret_access_key=aws_secret_access_key
        )
        print("DEBUG: SES client created successfully")

        if isinstance(recipients, str):
            recipients = [recipients]

        # Clean email addresses
        recipients = [r.strip() for r in recipients if r and isinstance(r, str) and r.strip()]

        # Check for invalid email addresses
        for r in recipients + [sender]:
            if any(c in r for c in [' ', '\n', '\r', '\t']):
                raise ValueError(f"Invalid email address detected: {repr(r)}")

        if client:
            print("DEBUG: Preparing SES message...")
            # Prepare message body
            message_body = {}

            # Add HTML part if message contains HTML
            if message and ('<' in message and '>' in message):
                message_body['Html'] = {'Data': message, 'Charset': 'UTF-8'}
                print("DEBUG: Added HTML part to SES message")

            # Add text part
            text_content = text_message or (frappe.utils.strip_html(message) if message else None)
            if text_content:
                message_body['Text'] = {'Data': text_content, 'Charset': 'UTF-8'}
                print("DEBUG: Added text part to SES message")

            print(f"DEBUG: Sending email via SES to {len(recipients)} recipients...")
            response = client.send_email(
                Source=sender,
                Destination={'ToAddresses': recipients},
                Message={
                    'Subject': {'Data': subject, 'Charset': 'UTF-8'},
                    'Body': message_body
                }
            )
            print(f"DEBUG: SES response: {response}")
            print("DEBUG: Email sent via SES successfully!")
            return response
        else:
            print("DEBUG: SES client is None!")
            return None

    except Exception as e:
        print(f"DEBUG: SES sending failed with error: {str(e)}")
        print(f"DEBUG: Error type: {type(e).__name__}")
        import traceback
        print(f"DEBUG: SES traceback: {traceback.format_exc()}")
        frappe.log_error(frappe.get_traceback(), "SES Email Sending Failed")
        print("===== SES DEBUG END =====\n")
        raise

def process_email_queue():
    """Process the email queue immediately"""
    print("\n===== PROCESSING EMAIL QUEUE =====")
    try:
        # Try different approaches to process the queue
        try:
            from frappe.email.queue import flush
            flush()
            print("DEBUG: Email queue flushed successfully!")
        except ImportError:
            try:
                # Alternative method - trigger send queued emails
                from frappe.email.doctype.email_queue.email_queue import send_unsent_emails
                send_unsent_emails()
                print("DEBUG: Email queue processed via send_unsent_emails!")
            except ImportError:
                # Last resort - directly call the sending function
                from frappe.utils.background_jobs import enqueue
                enqueue("frappe.email.queue.send_queued_emails", queue="short")
                print("DEBUG: Email queue processing enqueued!")
    except Exception as e:
        print(f"DEBUG: Error processing email queue: {e}")
        import traceback
        print(f"DEBUG: Traceback: {traceback.format_exc()}")
    print("===== EMAIL QUEUE PROCESSING END =====\n")

def test_simple_email():
    """Simple test email function to isolate the issue"""
    print("\n===== SIMPLE EMAIL TEST =====")
    try:
        print("DEBUG: Starting simple email test...")

        # Test basic Frappe sendmail
        result = frappe.sendmail(
            recipients=['leduchoanh2k@gmail.com'],
            subject='Test Email - Simple',
            message='This is a test email to debug the sending issue.',
            delayed=False
        )
        print(f"DEBUG: Simple email result: {result}")
        print("DEBUG: Simple email test completed successfully!")

    except Exception as e:
        print(f"DEBUG: Simple email test failed: {e}")
        import traceback
        print(f"DEBUG: Traceback: {traceback.format_exc()}")

    print("===== SIMPLE EMAIL TEST END =====\n")

def check_email_queue():
    """Check the status of the email queue"""
    print("\n===== EMAIL QUEUE CHECK =====")
    try:
        # Check email queue using correct API
        try:
            queued_emails = frappe.db.get_all('Email Queue',
                                             fields=['name', 'recipients', 'subject', 'status', 'creation'],
                                             order_by='creation desc',
                                             limit=10)
            print(f"DEBUG: Found {len(queued_emails)} queued emails")

            for email in queued_emails:
                print(f"DEBUG: Queued email - To: {email.recipients}, Subject: {email.subject}, Status: {email.status}")

        except Exception as e:
            print(f"DEBUG: Error checking Email Queue: {e}")

        # Check email log
        email_logs = frappe.db.get_all('Email Log',
                                     fields=['recipient', 'subject', 'status', 'creation'],
                                     order_by='creation desc',
                                     limit=5)
        print(f"DEBUG: Found {len(email_logs)} recent email logs")
        for log in email_logs:
            print(f"DEBUG: Email Log - To: {log.recipient}, Subject: {log.subject}, Status: {log.status}, Time: {log.creation}")

    except Exception as e:
        print(f"DEBUG: Error checking email queue: {e}")
    print("===== EMAIL QUEUE CHECK END =====\n")

#Hàm log gửi email
def log_email_transaction(
    subject,
    sender,
    recipients,
    cc,
    bcc,
    reply_to,
    content,
    attachments,
    status,
    error=None
):
    try:
        frappe.get_doc({
            "doctype": "Mira Email Log",
            "subject": subject,
            "sender": sender,
            "recipients": ", ".join(recipients) if recipients else "",
            "cc": ", ".join(cc) if cc else "",
            "bcc": ", ".join(bcc) if bcc else "",
            "reply_to": ", ".join(reply_to) if reply_to else "",
            "content": content,
            "attachments": ", ".join(attachments) if attachments else "",
            "status": status,
            "error": error or "",
            "creation": now()
        }).insert(ignore_permissions=True)
        frappe.db.commit()
    except Exception as e:
        frappe.logger().error(f"Failed to write Email Log: {e}")

def query_get_one(q: Query) -> dict:
    r = q.run(as_dict=True)

    if len(r) != 1:
        return

    return r.pop()


def default_outgoing_email_account():
    QBEmailAccount = DocType("Email Account")

    r = (
        frappe.qb.from_(QBEmailAccount)
        .select(QBEmailAccount.star)
        .where(QBEmailAccount.default_outgoing == 1)
        .limit(1)
    )

    return query_get_one(r)


def default_ats_outgoing_email_account():
    QBEmailAccount = DocType("Email Account")
    QBImapFolder = DocType("IMAP Folder")

    r = (
        frappe.qb.from_(QBEmailAccount)
        .select(QBEmailAccount.star)
        .where(QBEmailAccount.default_outgoing == 1)
        .inner_join(QBImapFolder)
        .on(QBImapFolder.parent == QBEmailAccount.name)
        .where(QBImapFolder.append_to == "MBW_ATS")
        .limit(1)
    )

    return query_get_one(r)

def sender_email():
        """
        Find an email to use as sender. Fall back through multiple choices

        :return: `Email Account`
        """
        if email_account := default_ats_outgoing_email_account():
            return email_account

        if email_account := default_outgoing_email_account():
            return email_account


#======================================BACKGROUND============================
