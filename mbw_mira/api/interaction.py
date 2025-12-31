import urllib
import frappe
from frappe import _
import json
from mbw_mira.utils import verify_signature
from frappe.utils import now_datetime, add_days

@frappe.whitelist(allow_guest=True)
def track(campaign_id =None, talent_id=None,source=None,medium = None, action=None, type=None, url=None,ip_address=None):
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
        "utm_campaign":campaign_id,
        "utm_source":source,
        "utm_medium":medium,
        "chanel":source,
        "url": url,
        "ip_address":ip_address,
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
    encoded_url = frappe.form_dict.get("url") or ""
    tracking_sig = frappe.form_dict.get("url_tracking") or ""
    sig = frappe.form_dict.get("sig") or ""

    # Kiểm tra token/sig
    if sig and frappe.cache().get(f"used_sig:{sig}"):
        # Sig đã dùng → chỉ redirect
        frappe.local.response["type"] = "redirect"
        frappe.local.response["location"] = urllib.parse.unquote(encoded_url)
        return

    # Đánh dấu token đã dùng
    if sig:
        frappe.cache().set(f"used_sig:{sig}", True, expire=3600)  # hết hạn 1h

    # Decode URL gốc
    decoded_url = urllib.parse.unquote(encoded_url)
    decode_urltrack = urllib.parse.unquote(tracking_sig)
    # Parse query params
    parsed = urllib.parse.urlparse(decode_urltrack)
    query_params = urllib.parse.parse_qs(parsed.query)
    campaign_id = query_params.get("utm_campaign",[""])[0]
    source = query_params.get("utm_source",[""])[0]
    medium = query_params.get("utm_medium",[""])[0]
    print(query_params)
    talent_id = query_params.get("talent_id",[""])[0]
    action = query_params.get("action",[""])[0]
    ip_address = frappe.local.request_ip or ""
    # Ghi tracking chỉ 1 lần
    track(campaign_id=campaign_id, talent_id=talent_id,
          source=source, medium=medium,
          action=action, type="ON_LINK_CLICK",
          url=decoded_url,ip_address=ip_address)

    frappe.local.response["type"] = "redirect"
    frappe.local.response["location"] = decoded_url



@frappe.whitelist(allow_guest=True)
def tracking_pixel():
    encoded_url = frappe.form_dict.get("url") or ""
    tracking_sig = frappe.form_dict.get("url_tracking") or ""
    sig = frappe.form_dict.get("sig") or ""

    # Decode URL gốc
    decoded_url = urllib.parse.unquote(encoded_url)

    # Parse query params từ URL gốc
    parsed = urllib.parse.urlparse(decoded_url)
    query_params = urllib.parse.parse_qs(parsed.query)

    campaign_id = query_params.get("utm_campaign")
    source = query_params.get("utm_source")
    medium = query_params.get("utm_medium")

    talent_id = frappe.form_dict.get("talent_id") or ""
    action = frappe.form_dict.get("action") or ""
    ip_address = frappe.local.request_ip or ""
    # --- Track chỉ 1 lần dựa trên sig ---
    if sig and frappe.cache().get(f"used_sig:{sig}"):
        # Sig đã dùng → không track nữa
        pass
    else:
        if sig:
            frappe.cache().set(f"used_sig:{sig}", True, expire=3600)  # cache 1h
        
        # Gọi hàm track
        track(
            campaign_id=campaign_id,
            talent_id=talent_id,
            source=source,
            medium=medium,
            action=action,
            type="EMAIL_OPENED",
            url=decoded_url,
            ip_address = ip_address
        )

    # --- Trả về transparent 1x1 GIF ---
    gif_bytes = (
        b"GIF89a\x01\x00\x01\x00\x80\x00\x00\x00\x00\x00"
        b"\xFF\xFF\xFF!\xF9\x04\x01\x00\x00\x00\x00,"
        b"\x00\x00\x00\x00\x01\x00\x01\x00\x00\x02\x02L\x01\x00;"
    )

    frappe.local.response.type = "binary"
    frappe.local.response.filename = "pixel.gif"
    frappe.local.response.filecontent = gif_bytes

    # Headers chuẩn
    if frappe.local.response.get("headers") is None:
        frappe.local.response["headers"] = {}

    frappe.local.response["headers"]["Content-Type"] = "image/gif"
    frappe.local.response["headers"]["Cache-Control"] = "no-cache, no-store, must-revalidate"
    frappe.local.response["headers"]["Pragma"] = "no-cache"
    frappe.local.response["headers"]["Expires"] = "0"

@frappe.whitelist(allow_guest=True)
def page_visited():
    # Parse query params từ URL gốc
    sig = frappe.form_dict.get("sig") or ""
    campaign_id = frappe.form_dict.get("utm_campaign")
    source = frappe.form_dict.get("utm_source")
    medium = frappe.form_dict.get("utm_medium")

    talent_id = frappe.form_dict.get("talent_id")
    action = frappe.form_dict.get("action")
    ip_address = frappe.local.request_ip or ""
    # --- Track chỉ 1 lần dựa trên sig ---
    if sig and frappe.cache().get(f"used_sig:{sig}"):
        # Sig đã dùng → không track nữa
        pass
    else:
        # Đánh dấu sig đã dùng 1 lần
        if sig:
            frappe.cache().set(f"used_sig:{sig}", True, expire=3600)

        # Gọi hàm track
        track(
            campaign_id=campaign_id,
            talent_id=talent_id,
            source=source,
            medium=medium,
            action=action,
            type="PAGE_VISITED",
            url="",
            ip_address = ip_address
        )

    # --- Trả về response JSON success ---
    frappe.local.response.type = "json"
    frappe.local.response.data = {
        "status": "success",
        "message": "Page visited tracked",
        "url": ""
    }




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


@frappe.whitelist()
def get_campaign_stats(campaign_id):
    """
    Lấy thống kê tương tác cho một campaign từ Mira Interaction và Mira Action
    Trả về: sent, delivered, opened, clicked, unsubscribed, bounced, replied, failed
    """
    try:
        if not campaign_id:
            frappe.throw(_("Campaign ID is required"))
        
        # Kiểm tra campaign có tồn tại không
        if not frappe.db.exists("Mira Campaign", campaign_id):
            frappe.throw(_("Campaign not found"))
        
        # Lấy tất cả interactions của campaign này
        interactions = frappe.get_all(
            "Mira Interaction",
            filters={"campaign_id": campaign_id},
            fields=["interaction_type"],
            limit_page_length=0
        ) or []
        
        # Đếm số lượng theo interaction_type
        counts = {}
        for item in interactions:
            itype = item.get("interaction_type")
            if itype:
                counts[itype] = counts.get(itype, 0) + 1
        
        # Đếm số talent trong campaign (từ Mira Talent Campaign)
        try:
            total_talents = frappe.db.count("Mira Talent Campaign", {"campaign_id": campaign_id}) or 0
        except:
            total_talents = 0
        
        # Đếm số contact trong campaign (từ Mira Contact Campaign)
        try:
            total_contacts = frappe.db.count("Mira Contact Campaign", {"campaign_id": campaign_id}) or 0
        except:
            total_contacts = 0
        
        total_recipients = total_talents + total_contacts
        
        # Lấy danh sách talent_campaign_ids thuộc campaign này
        try:
            talent_campaigns = frappe.get_all(
                "Mira Talent Campaign",
                filters={"campaign_id": campaign_id},
                fields=["name"],
                limit_page_length=0
            ) or []
        except:
            talent_campaigns = []
        
        talent_campaign_ids = [tc.name for tc in talent_campaigns if tc.get("name")]
        
        # Đếm số actions theo status từ Mira Action
        action_status = {}
        if talent_campaign_ids:
            try:
                actions = frappe.get_all(
                    "Mira Action",
                    filters={"talent_campaign_id": ["in", talent_campaign_ids]},
                    fields=["status"],
                    limit_page_length=0
                ) or []
                for action in actions:
                    status = action.get("status")
                    if status:
                        action_status[status] = action_status.get(status, 0) + 1
            except:
                pass
        
        # Tính toán các metrics
        sent = counts.get('EMAIL_SENT', 0)
        delivered = counts.get('EMAIL_DELIVERED', 0)
        opened = counts.get('EMAIL_OPENED', 0)
        clicked = counts.get('ON_LINK_CLICK', 0)
        unsubscribed = counts.get('EMAIL_UNSUBSCRIBED', 0)
        bounced = counts.get('EMAIL_BOUNCED', 0)
        replied = counts.get('EMAIL_REPLIED', 0)
        failed = action_status.get('FAILED', 0)
        
        # Nếu không có sent, dùng total_recipients làm base
        base = sent if sent > 0 else total_recipients
        
        # Tính tỷ lệ phần trăm
        def calc_rate(count, base):
            if base == 0:
                return "0%"
            return f"{round((count / base) * 100, 1)}%"
        
        return {
            "status": "success",
            "campaign_id": campaign_id,
            "stats": {
                "sent": sent if sent > 0 else total_recipients,
                "delivered": delivered,
                "delivered_percent": calc_rate(delivered, base),
                "open_rate": calc_rate(opened, base),
                "open_count": opened,
                "click_rate": calc_rate(clicked, base),
                "click_count": clicked,
                "unsubscribe_rate": calc_rate(unsubscribed, base),
                "unsubscribe_count": unsubscribed,
                "bounce_rate": calc_rate(bounced, base),
                "bounce_count": bounced,
                "reply_rate": calc_rate(replied, base),
                "reply_count": replied,
                "error_rate": calc_rate(failed, base),
                "error_count": failed,
                "total_recipients": total_recipients,
                "total_talents": total_talents,
                "total_contacts": total_contacts
            },
            "raw_counts": counts,
            "action_status": action_status
        }
    except Exception as e:
        frappe.log_error(f"Error in get_campaign_stats: {str(e)}", "get_campaign_stats")
        return {
            "status": "error",
            "message": str(e),
            "stats": {
                "sent": 0,
                "delivered": 0,
                "delivered_percent": "0%",
                "open_rate": "0%",
                "open_count": 0,
                "click_rate": "0%",
                "click_count": 0,
                "unsubscribe_rate": "0%",
                "unsubscribe_count": 0,
                "bounce_rate": "0%",
                "bounce_count": 0,
                "reply_rate": "0%",
                "reply_count": 0,
                "error_rate": "0%",
                "error_count": 0,
                "total_recipients": 0,
                "total_talents": 0,
                "total_contacts": 0
            }
    }


@frappe.whitelist()
def get_campaign_link_clicks(campaign_id, limit=20):
    """
    Lấy danh sách các link được click trong campaign, group theo URL
    """
    if not campaign_id:
        frappe.throw(_("Campaign ID is required"))
    
    # Lấy tất cả interactions loại ON_LINK_CLICK có URL
    interactions = frappe.get_all(
        "Mira Interaction",
        filters={
            "campaign_id": campaign_id,
            "interaction_type": "ON_LINK_CLICK",
            "url": ["is", "set"]
        },
        fields=["url"],
        limit_page_length=0
    )
    
    # Group theo URL và đếm
    url_counts = {}
    for item in interactions:
        url = item.get("url")
        if url:
            url_counts[url] = url_counts.get(url, 0) + 1
    
    # Chuyển thành list và sort theo clicks giảm dần
    link_clicks = [{"url": url, "clicks": count} for url, count in url_counts.items()]
    link_clicks.sort(key=lambda x: x["clicks"], reverse=True)
    
    # Limit kết quả
    link_clicks = link_clicks[:int(limit)]
    
    return {
        "status": "success",
        "campaign_id": campaign_id,
        "total": len(link_clicks),
        "link_clicks": link_clicks
    }


@frappe.whitelist()
def get_campaign_top_talents(campaign_id, limit=10):
    """
    Lấy danh sách top talents có nhiều tương tác nhất trong campaign
    """
    if not campaign_id:
        frappe.throw(_("Campaign ID is required"))
    
    # Lấy tất cả interactions có talent_id
    interactions = frappe.get_all(
        "Mira Interaction",
        filters={
            "campaign_id": campaign_id,
            "talent_id": ["is", "set"]
        },
        fields=["talent_id", "interaction_type"],
        limit_page_length=0
    )
    
    # Group theo talent_id và đếm các loại interaction
    talent_stats = {}
    for item in interactions:
        talent_id = item.get("talent_id")
        itype = item.get("interaction_type")
        
        if talent_id not in talent_stats:
            talent_stats[talent_id] = {
                "talent_id": talent_id,
                "total_interactions": 0,
                "clicks": 0,
                "opens": 0,
                "replies": 0
            }
        
        talent_stats[talent_id]["total_interactions"] += 1
        
        if itype == "ON_LINK_CLICK":
            talent_stats[talent_id]["clicks"] += 1
        elif itype == "EMAIL_OPENED":
            talent_stats[talent_id]["opens"] += 1
        elif itype == "EMAIL_REPLIED":
            talent_stats[talent_id]["replies"] += 1
    
    # Lấy thông tin talent (full_name, email)
    talent_ids = list(talent_stats.keys())
    if talent_ids:
        talents = frappe.get_all(
            "Mira Talent",
            filters={"name": ["in", talent_ids]},
            fields=["name", "full_name", "email"],
            limit_page_length=0
        )
        talent_info = {t.name: t for t in talents}
        
        # Merge thông tin
        for talent_id, stats in talent_stats.items():
            info = talent_info.get(talent_id, {})
            stats["full_name"] = info.get("full_name", "")
            stats["email"] = info.get("email", "")
    
    # Chuyển thành list và sort
    top_talents = list(talent_stats.values())
    top_talents.sort(key=lambda x: (x["clicks"], x["opens"], x["total_interactions"]), reverse=True)
    
    # Limit kết quả
    top_talents = top_talents[:int(limit)]
    
    return {
        "status": "success",
        "campaign_id": campaign_id,
        "total": len(top_talents),
        "top_talents": top_talents
    }


@frappe.whitelist()
def get_campaign_filter_counts(campaign_id):
    """
    Lấy số lượng cho các filter buttons trong Campaign Detail (sent, delivered, opened, clicked, failed, bounced, spam)
    """
    try:
        if not campaign_id:
            frappe.throw(_("Campaign ID is required"))
        
        # Lấy danh sách talent_campaign_ids thuộc campaign này TRƯỚC để filter interactions
        try:
            talent_campaigns = frappe.get_all(
                "Mira Talent Campaign",
                filters={"campaign_id": campaign_id},
                fields=["name", "talent_id"],
                limit_page_length=0
            ) or []
        except:
            talent_campaigns = []
        
        # Lấy set các talent_id còn trong campaign
        active_talent_ids = set()
        for tc in talent_campaigns:
            if tc.get("talent_id"):
                active_talent_ids.add(tc.get("talent_id"))
        
        # Lấy tất cả interactions của campaign
        try:
            interactions = frappe.get_all(
                "Mira Interaction",
                filters={"campaign_id": campaign_id},
                fields=["interaction_type", "talent_id"],
                limit_page_length=0
            ) or []
        except:
            interactions = []
        
        # Đếm số unique talent_id theo interaction_type (CHỈ ĐẾM TALENTS CÒN TRONG CAMPAIGN)
        type_talents = {}
        for item in interactions:
            itype = item.get("interaction_type")
            talent_id = item.get("talent_id")
            # CHỈ ĐẾM nếu talent_id còn trong campaign
            if itype and talent_id and talent_id in active_talent_ids:
                if itype not in type_talents:
                    type_talents[itype] = set()
                type_talents[itype].add(talent_id)
        
        counts = {itype: len(talents) for itype, talents in type_talents.items()}
        
        talent_campaign_ids = [tc.name for tc in talent_campaigns if tc.get("name")]
        
        # Đếm số unique talent_id có action FAILED
        failed_talent_ids = set()
        if talent_campaign_ids:
            try:
                failed_actions = frappe.get_all(
                    "Mira Action",
                    filters={
                        "talent_campaign_id": ["in", talent_campaign_ids],
                        "status": "FAILED"
                    },
                    fields=["talent_campaign_id"],
                    limit_page_length=0
                ) or []
                
                # Map talent_campaign_id -> talent_id
                tc_to_talent = {tc.name: tc.talent_id for tc in talent_campaigns if tc.get("name") and tc.get("talent_id")}
                for action in failed_actions:
                    tc_id = action.get("talent_campaign_id")
                    if tc_id and tc_id in tc_to_talent:
                        failed_talent_ids.add(tc_to_talent[tc_id])
            except:
                pass
        
        # Tổng số talent/contact trong campaign
        try:
            total_talents = frappe.db.count("Mira Talent Campaign", {"campaign_id": campaign_id}) or 0
        except:
            total_talents = 0
        
        try:
            total_contacts = frappe.db.count("Mira Contact Campaign", {"campaign_id": campaign_id}) or 0
        except:
            total_contacts = 0
        
        return {
            "status": "success",
            "campaign_id": campaign_id,
            "filter_counts": {
                "sent": counts.get('EMAIL_SENT', 0) or (total_talents + total_contacts),
                "delivered": counts.get('EMAIL_DELIVERED', 0),
                "opened": counts.get('EMAIL_OPENED', 0),
                "clicked": counts.get('ON_LINK_CLICK', 0),
                "failed": len(failed_talent_ids),
                "bounced": counts.get('EMAIL_BOUNCED', 0),
                "spam": counts.get('EMAIL_SPAM', 0) or 0
            },
            "total_recipients": total_talents + total_contacts
        }
    except Exception as e:
        frappe.log_error(f"Error in get_campaign_filter_counts: {str(e)}", "get_campaign_filter_counts")
        return {
            "status": "error",
            "message": str(e),
            "filter_counts": {
                "sent": 0,
                "delivered": 0,
                "opened": 0,
                "clicked": 0,
                "failed": 0,
                "bounced": 0,
                "spam": 0
            },
            "total_recipients": 0
        }


@frappe.whitelist()
def get_campaign_interactions(campaign_id, limit=100):
    """
    Lấy danh sách interactions của campaign một cách an toàn
    """
    try:
        if not campaign_id:
            frappe.throw(_("Campaign ID is required"))
        
        # Kiểm tra campaign có tồn tại không
        if not frappe.db.exists("Mira Campaign", campaign_id):
            frappe.throw(_("Campaign not found"))
        
        # Sử dụng SQL query trực tiếp để tránh lỗi field
        interactions = frappe.db.sql("""
            SELECT 
                name,
                talent_id,
                campaign_id,
                interaction_type,
                action,
                url,
                description,
                creation,
                modified
            FROM 
                `tabMira Interaction`
            WHERE 
                campaign_id = %(campaign_id)s
            ORDER BY 
                creation DESC
            LIMIT %(limit)s
        """, {
            "campaign_id": campaign_id,
            "limit": int(limit)
        }, as_dict=True)
        
        return {
            "status": "success",
            "interactions": interactions or []
        }
    except Exception as e:
        frappe.log_error(f"Error in get_campaign_interactions: {str(e)}", "get_campaign_interactions")
        return {
            "status": "error",
            "message": str(e),
            "interactions": []
        }

