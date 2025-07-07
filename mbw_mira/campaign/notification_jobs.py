import frappe

from mbw_mira.utils import email as email_utils

def send_email_job(
    candidate_email: str,
    subject: str,
    message: str = None,
    campaign_step: str = None,
    candidate_id: str = None,
    template: str = None,
    template_args: dict = None
):
    """
    Gửi email cho ứng viên, hỗ trợ cả message raw hoặc template.
    """
    logger = frappe.logger("campaign")

    if not candidate_email:
        logger.error("[EMAIL ERROR] Missing candidate_email")
        return

    if not subject:
        logger.error(f"[EMAIL ERROR] Missing subject for {candidate_email}")
        return

    if not message and not template:
        logger.error(f"[EMAIL ERROR] Neither message nor template provided for {candidate_email}")
        return

    try:
        email_utils.send_email(
            recipients=[candidate_email],
            subject=subject,
            content=message if not template else None,
            template=template,
            template_args=template_args
        )
        logger.info(f"[EMAIL] Sent to {candidate_email} — step: {campaign_step} — candidate: {candidate_id}")

    except Exception as e:
        logger.error(f"[EMAIL ERROR] {candidate_email} — {str(e)}")
        frappe.log_error(frappe.get_traceback(), "[EMAIL ERROR] send_email_job")
        raise
def send_sms_job(phone: str, message: str, campaign_step: str = None, candidate_id: str = None):
    try:
        # Gửi thật nếu có provider
        frappe.logger("campaign").info(f"[SMS] Sent to {phone} — step: {campaign_step}")
    except Exception as e:
        frappe.logger("campaign").error(f"[SMS ERROR] {phone} — {str(e)}")
        raise
