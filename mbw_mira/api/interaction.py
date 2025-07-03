import frappe
from frappe import _
import json
from mbw_mira.campaign.controller import create_interaction
from mbw_mira.campaign.utils import verify_signature
from frappe.utils import now_datetime, add_days

@frappe.whitelist(allow_guest=True)
def track(candidate_id=None, action=None, type=None, url=None):
    if not candidate_id or not type:
        frappe.throw("Missing required parameters: candidate_id, type")

    # Ghi thêm thông tin User Agent, IP
    info = {
        "ip": frappe.local.request_ip,
        "user_agent": frappe.local.request.headers.get('User-Agent')
    }

    doc = frappe.get_doc({
        "doctype": "Interaction",
        "candidate_id": candidate_id,
        "interaction_type": type,
        "action": action,
        "url": url,
        "description": json.dumps(info)
    })
    doc.insert(ignore_permissions=True)
    frappe.db.commit()

    # 2. Flag Candidate Interaction last
    if frappe.db.exists("Candidate", candidate_id):
        frappe.db.set_value("Candidate", candidate_id, "last_interaction", now_datetime())
        frappe.db.commit()
        
    return {"status": "ok"}

@frappe.whitelist(allow_guest=True)
def click_redirect(candidate_id=None, action=None, url=None, sig=None):
    if not candidate_id or not url or not sig:
        frappe.throw("Missing required parameters")

    data_string = f"candidate_id={candidate_id}&action={action}&url={url}"
    if not verify_signature(data_string, sig):
        frappe.throw("Invalid signature")

    track(candidate_id=candidate_id, action=action, type="EMAIL_CLICKED", url=url)

    frappe.local.response["type"] = "redirect"
    frappe.local.response["location"] = url

@frappe.whitelist(allow_guest=True)
def tracking_pixel(candidate_id=None, action=None):
    track(candidate_id=candidate_id, action=action, type="EMAIL_OPENED")

    # Return transparent GIF
    frappe.local.response.filename = "pixel.gif"
    frappe.local.response.type = "image/gif"
    frappe.local.response.filecontent = (
        b"GIF89a\x01\x00\x01\x00\x80\x00\x00\x00\x00\x00"
        b"\xFF\xFF\xFF!\xF9\x04\x01\x00\x00\x00\x00,"
        b"\x00\x00\x00\x00\x01\x00\x01\x00\x00\x02\x02L\x01\x00;"
    )

@frappe.whitelist(allow_guest=True)
def unsubscribe(candidate_id=None, action=None, sig=None):
    if not candidate_id or not sig:
        frappe.throw("Missing parameters")

    data_string = f"candidate_id={candidate_id}&action={action or ''}"
    if not verify_signature(data_string, sig):
        frappe.throw("Invalid signature")

    # 1. Log Interaction
    frappe.get_doc({
        "doctype": "Interaction",
        "candidate_id": candidate_id,
        "action": action,
        "interaction_type": "EMAIL_UNSUBSCRIBED",
        "description": f"IP: {frappe.local.request_ip}, User-Agent: {frappe.local.request.headers.get('User-Agent')}"
    }).insert(ignore_permissions=True)

    # 2. Flag Candidate as Unsubscribed
    if frappe.db.exists("Candidate", candidate_id):
        frappe.db.set_value("Candidate", candidate_id, {"email_opt_out": 1,"last_interaction":now_datetime()})
        frappe.db.commit()

    # 3. Show confirmation page (Website context)
    html = """
    <html>
    <head><title>Unsubscribed</title></head>
    <body>
      <h2>You have been unsubscribed.</h2>
      <p>We're sorry to see you go.</p>
    </body>
    </html>
    """
    frappe.local.response.type = 'text/html'
    frappe.local.response.message = html
