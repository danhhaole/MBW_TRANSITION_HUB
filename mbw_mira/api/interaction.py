import frappe
from frappe import _
import json
from mbw_mira.utils import verify_signature
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

    frappe.publish_realtime(
        event="interaction_created",
        message={
            "candidate_id": candidate_id,
            "interaction_type": type,
            "action": action
        },
        user=frappe.session.user
    )
    return {"status": "ok"}

@frappe.whitelist(allow_guest=True)
def click_redirect():
    candidate_id = frappe.form_dict.get("candidate_id")
    action = frappe.form_dict.get("action")
    url = frappe.form_dict.get("url")
    sig = frappe.form_dict.get("sig")

    if not candidate_id or not sig:
        frappe.throw("Missing required parameters")

    params = {
        "candidate_id": candidate_id,
        "action": action,
        "url":url
    }
    if not verify_signature(params, sig):
        frappe.throw("Invalid signature")

    track(candidate_id=candidate_id, action=action, type="EMAIL_CLICKED", url=url)

    frappe.local.response["type"] = "redirect"
    frappe.local.response["location"] = url


@frappe.whitelist(allow_guest=True)
def tracking_pixel():
    candidate_id = frappe.form_dict.get("candidate_id")
    action = frappe.form_dict.get("action")

    track(candidate_id=candidate_id, action=action, type="EMAIL_OPENED")

    # Return transparent GIF
    frappe.local.response.type = "binary"
    frappe.local.response.filename = "pixel.gif"
    frappe.local.response.filecontent = (
        b"GIF89a\x01\x00\x01\x00\x80\x00\x00\x00\x00\x00"
        b"\xFF\xFF\xFF!\xF9\x04\x01\x00\x00\x00\x00,"
        b"\x00\x00\x00\x00\x01\x00\x01\x00\x00\x02\x02L\x01\x00;"
    )

    # ensure headers is a dict
    if frappe.local.response.get("headers") is None:
        frappe.local.response["headers"] = {}

    frappe.local.response["headers"]["Content-Type"] = "image/gif"


@frappe.whitelist(allow_guest=True)
def unsubscribe():
    candidate_id = frappe.form_dict.get("candidate_id")
    action = frappe.form_dict.get("action")
    sig = frappe.form_dict.get("sig")
    url =  frappe.form_dict.get("url")

    if not candidate_id or not sig:
        frappe.throw("Missing parameters")

    params = {
        "candidate_id": candidate_id,
        "action": action,
        "url":url
    }
    if not verify_signature(params, sig):
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
        frappe.db.set_value(
            "Candidate",
            candidate_id,
            {
                "email_opt_out": 1,
                "last_interaction": now_datetime()
            }
        )
        frappe.db.commit()
        
    frappe.publish_realtime(
        event="interaction_created",
        message={
            "candidate_id": candidate_id,
            "interaction_type": "EMAIL_UNSUBSCRIBED",
            "action": action
        },
        user=frappe.session.user
    )
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

