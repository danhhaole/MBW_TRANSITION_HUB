import frappe
from frappe import _
import json
from mbw_mira.utils import verify_signature
from frappe.utils import now_datetime, add_days

@frappe.whitelist(allow_guest=True)
def track(campaign_id =None, talent_id=None, action=None, type=None, url=None):
    # if not talent_id or not type:
    #     frappe.throw("Missing required parameters: talent_id, type")

    # Ghi thêm thông tin User Agent, IP
    info = {
        "ip": frappe.local.request_ip,
        "user_agent": frappe.local.request.headers.get('User-Agent')
    }

    doc = frappe.get_doc({
        "doctype": "Mira Interaction",
        "talent_id": talent_id,
        "campaign_id":campaign_id,
        "interaction_type": type,
        "action": action,
        "url": url,
        "description": json.dumps(info)
    })
    doc.insert(ignore_permissions=True)
    frappe.db.commit()

    # 2. Flag Candidate Mira Interaction last
    if frappe.db.exists("Mira Talent", talent_id):
        frappe.db.set_value("Mira Talent", talent_id, "last_interaction", now_datetime())
        frappe.db.commit()

    frappe.publish_realtime(
        event="interaction_created",
        message={
            "talent_id": talent_id,
            "interaction_type": type,
            "action": action
        },
        user=frappe.session.user
    )
    return {"status": "ok"}

@frappe.whitelist(allow_guest=True)
def click_redirect():
    campaign_id = frappe.form_dict.get("utm_campaign")
    talent_id = frappe.form_dict.get("talent_id") or ""
    action = frappe.form_dict.get("action")
    url = frappe.form_dict.get("url")
    sig = frappe.form_dict.get("sig")

    # if not talent_id or not sig:
    #     frappe.throw("Missing required parameters")

    params = {
        "campaign_id":campaign_id,
        "talent_id": talent_id,
        "action": action,
        "url":url
    }
    # if not verify_signature(params, sig):
    #     frappe.throw("Invalid signature")

    track(campaign_id=campaign_id, talent_id=talent_id, action=action, type="ON_LINK_CLICK", url=url)

    frappe.local.response["type"] = "redirect"
    frappe.local.response["location"] = url


@frappe.whitelist(allow_guest=True)
def tracking_pixel():
    campaign_id = frappe.form_dict.get("utm_campaign")
    talent_id = frappe.form_dict.get("talent_id")
    action = frappe.form_dict.get("action")

    track(campaign_id=campaign_id, talent_id=talent_id, action=action, type="EMAIL_OPENED")

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
def page_visited():
    campaign_id = frappe.form_dict.get("utm_campaign")
    talent_id = frappe.form_dict.get("talent_id") or None
    action = frappe.form_dict.get("action")
    sig = frappe.form_dict.get("sig")
    
    track(campaign_id=campaign_id,talent_id=talent_id, action=action, type="PAGE_VISITED")
    
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
    campaign_id = frappe.form_dict.get("utm_campaign")
    talent_id = frappe.form_dict.get("talent_id")
    action = frappe.form_dict.get("action")
    sig = frappe.form_dict.get("sig")
    url =  frappe.form_dict.get("url")

    if not talent_id or not sig or not talent_id:
        frappe.throw("Missing parameters")

    params = {
        "campaign_id":campaign_id,
        "talent_id": talent_id,
        "action": action,
        "url":url
    }
    if not verify_signature(params, sig):
        frappe.throw("Invalid signature")

    # 1. Log Mira Interaction
    frappe.get_doc({
        "doctype": "Mira Interaction",
        "campaign_id":campaign_id,
        "talent_id": talent_id,
        "action": action,
        "interaction_type": "EMAIL_UNSUBSCRIBED",
        "description": f"IP: {frappe.local.request_ip}, User-Agent: {frappe.local.request.headers.get('User-Agent')}"
    }).insert(ignore_permissions=True)

    # 2. Flag Candidate as Unsubscribed
    if talent_id and frappe.db.exists("Mira Talent", talent_id):
        frappe.db.set_value(
            "Mira Talent",
            talent_id,
            {
                "email_opt_out": 1,
                "last_interaction": now_datetime()
            }
        )
        frappe.db.commit()
        
    frappe.publish_realtime(
        event="interaction_created",
        message={
            "talent_id": talent_id,
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


@frappe.whitelist()
def get_talent_email_interactions(talent_id):
    """
    Lấy các interaction EMAIL_SENT, EMAIL_OPENED, ON_LINK_CLICK của talent
    kèm theo tên campaign và platform từ Mira Campaign Social
    """
    if not talent_id:
        frappe.throw(_("Talent ID is required"))
    
    # Kiểm tra talent có tồn tại không
    if not frappe.db.exists("Mira Talent", talent_id):
        frappe.throw(_("Talent not found"))
    
    # Query để lấy interactions với campaign name và platform
    interactions = frappe.db.sql("""
        SELECT 
            mi.name,
            mi.talent_id,
            mi.campaign_id,
            mi.interaction_type,
            mi.action,
            mi.url,
            mi.channel,
            mi.creation,
            mi.modified,
            mc.campaign_name,
            mcs.platform,
            mcs.social_page_name
        FROM 
            `tabMira Interaction` mi
        LEFT JOIN 
            `tabMira Campaign` mc ON mi.campaign_id = mc.name
        LEFT JOIN 
            `tabMira Campaign Social` mcs ON mc.name = mcs.campaign_id
        WHERE 
            mi.talent_id = %(talent_id)s
            AND mi.interaction_type IN ('EMAIL_SENT', 'EMAIL_OPENED', 'ON_LINK_CLICK')
        ORDER BY 
            mi.creation DESC
    """, {"talent_id": talent_id}, as_dict=True)
    
    return {
        "status": "success",
        "talent_id": talent_id,
        "total": len(interactions),
        "interactions": interactions
    }


@frappe.whitelist()
def get_interaction_counts(talent_id):
    """
    Đếm số lượng interactions theo type cho talent
    """
    if not talent_id:
        frappe.throw(_("Talent ID is required"))
    
    counts = frappe.db.sql("""
        SELECT 
            interaction_type,
            COUNT(*) as count
        FROM 
            `tabMira Interaction`
        WHERE 
            talent_id = %(talent_id)s
        GROUP BY 
            interaction_type
    """, {"talent_id": talent_id}, as_dict=True)
    
    # Chuyển đổi thành dict để dễ sử dụng
    result = {item['interaction_type']: item['count'] for item in counts}
    
    return {
        "status": "success",
        "talent_id": talent_id,
        "counts": result
    }


@frappe.whitelist()
def get_talent_activity_logs(talent_id, limit=50):
    """
    Lấy activity logs của talent từ Talent Activity Log
    """
    if not talent_id:
        frappe.throw(_("Talent ID is required"))
    
    # Kiểm tra talent có tồn tại không
    if not frappe.db.exists("Mira Talent", talent_id):
        frappe.throw(_("Talent not found"))
    
    # Query để lấy activity logs
    activities = frappe.db.sql("""
        SELECT 
            name,
            talent_id,
            activity_type,
            subject,
            description,
            campaign_id,
            interaction_id,
            recruiter_id,
            reference_doctype,
            reference_name,
            trigger_type,
            is_system_generated,
            score_change,
            source,
            meta_json,
            date,
            creation,
            modified,
            owner,
            modified_by
        FROM 
            `tabTalent Activity Log`
        WHERE 
            talent_id = %(talent_id)s
        ORDER BY 
            date DESC, creation DESC
        LIMIT %(limit)s
    """, {"talent_id": talent_id, "limit": limit}, as_dict=True)
    
    return {
        "status": "success",
        "talent_id": talent_id,
        "total": len(activities),
        "activities": activities
    }

