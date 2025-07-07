import frappe

def send_email_job(candidate_email: str, subject: str, message: str, campaign_step: str = None, candidate_id: str = None):
    from mbw_mira.utils import email
    try:
        email.send_email(recipients=[candidate_email], subject=subject, message=message)
        frappe.logger("campaign").info(f"[EMAIL] Sent to {candidate_email} — step: {campaign_step}")
    except Exception as e:
        frappe.logger("campaign").error(f"[EMAIL ERROR] {candidate_email} — {str(e)}")
        raise

def send_sms_job(phone: str, message: str, campaign_step: str = None, candidate_id: str = None):
    try:
        # Gửi thật nếu có provider
        frappe.logger("campaign").info(f"[SMS] Sent to {phone} — step: {campaign_step}")
    except Exception as e:
        frappe.logger("campaign").error(f"[SMS ERROR] {phone} — {str(e)}")
        raise
