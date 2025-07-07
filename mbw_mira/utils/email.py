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
    text_message=None
):
    """
    Unified send email utility:
    - Use Frappe Email Account if configured
    - Else fallback to AWS SES
    - Logs all emails to Email Log
    """
    if not recipients:
        frappe.throw("Recipients are required")
    if not (template or content):
        frappe.throw("Either template name or raw content must be provided")

    # Normalize
    recipients = normalize_emails(recipients)
    cc = normalize_emails(cc)
    bcc = normalize_emails(bcc)
    reply_to = normalize_emails(reply_to)
    prepared_attachments = prepare_attachments(attachments)
    
    # Default sender
    senderemail= ''
    if sender_email():
        senderemail = sender_email().email_id
    if template:
        content = render_template(template, template_args)
        if not text_message:
            text_message = frappe.utils.strip_html(content)
    status = "Success"
    error = None

    try:
        if senderemail:
            # Use Frappe
            frappe.sendmail(
                recipients=recipients,
                subject=subject,
                sender=senderemail,
                cc=cc,
                bcc=bcc,
                reply_to=reply_to,
                attachments=prepared_attachments,
                content=content,
                delayed=False
            )
            frappe.logger().info(f"Email sent via Frappe to {recipients}")
        else:
            # Fallback to AWS SES
            status = "Fallback"
            sendmail_via_ses(
                recipients=recipients,
                subject=subject,
                message=content
            )
            frappe.logger().info(f"Email sent via AWS SES to {recipients}")

    except Exception as e:
        status = "Failed"
        error = str(e)
        frappe.log_error(frappe.get_traceback(), "send_email Failed")
        raise

    finally:
        # Always log to Email Log
        log_email_transaction(
            subject=subject,
            sender=sender_email or sender,
            recipients=recipients,
            cc=cc,
            bcc=bcc,
            reply_to=reply_to,
            content=content,
            attachments=[a.get("fname") for a in prepared_attachments],
            status=status,
            error=error
        )

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
def sendmail_via_ses(recipients, subject, message):
    try:
        sender = (frappe.conf.get("aws_sender") or "no-reply@mbwcloud.com").strip()
        region = frappe.conf.get("aws_region") or "us-east-1"
        aws_access_key_id = frappe.conf.get("aws_access_key_id")
        aws_secret_access_key = frappe.conf.get("aws_secret_access_key")
        
        client = boto3.client(
            'ses',
            region_name=region,
            aws_access_key_id=aws_access_key_id,
            aws_secret_access_key=aws_secret_access_key
        )

        if isinstance(recipients, str):
            recipients = [recipients]
        
        # Clean email addresses
        recipients = [r.strip() for r in recipients if r and isinstance(r, str) and r.strip()]

        # Check for invalid email addresses
        for r in recipients + [sender]:
            if any(c in r for c in [' ', '\n', '\r', '\t']):
                raise ValueError(f"Invalid email address detected: {repr(r)}")

        if client:
            response = client.send_email(
                Source=sender,
                Destination={'ToAddresses': recipients},
                Message={
                    'Subject': {'Data': subject, 'Charset': 'UTF-8'},
                    'Body': {
                        'Html': {'Data': message, 'Charset': 'UTF-8'},
                        'Text': {'Data': frappe.utils.strip_html(message), 'Charset': 'UTF-8'}
                    }
                }
            )
            return response
        else:
            return None

    except Exception as e:
        frappe.log_error(frappe.get_traceback(), "SES Email Sending Failed")

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
            "doctype": "EmailLog",
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
