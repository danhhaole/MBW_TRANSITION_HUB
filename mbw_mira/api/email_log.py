import frappe
import json
from frappe.utils import cstr, cint, flt, getdate, nowdate, get_datetime, now
from frappe import _
from .common import get_list_data, get_form_data, save_doc, delete_doc, get_filter_options


@frappe.whitelist()
def get_email_logs_paginated(
    page=1,
    limit=12,
    search="",
    status="",
    sender="",
    order_by="creation desc"
):
    """
    Get paginated email logs using common list data function
    """
    try:
        # Calculate start position
        start = (cint(page) - 1) * cint(limit)
        
        # Build filters
        filters = {}
        if status:
            filters["status"] = status
        if sender:
            filters["sender"] = sender
        
        # Build search conditions
        search_conditions = []
        if search:
            search_conditions = [
                {"subject": ["like", f"%{search}%"]},
                {"recipients": ["like", f"%{search}%"]},
                {"sender": ["like", f"%{search}%"]},
                {"content": ["like", f"%{search}%"]}
            ]
        
        if search_conditions:
            filters["search_text"] = search_conditions
        
        # Fields to fetch
        fields = [
            "name", "subject", "recipients", "cc", "bcc", "sender", 
            "content", "attachments", "status", "error", "modified", "creation"
        ]
        
        # Get data using common function
        result = get_list_data(
            doctype="EmailLog",
            filters=filters,
            order_by=order_by,
            page_length=limit,
            start=start,
            fields=fields
        )
        
        if result.get("success"):
            # Process data for display
            for item in result["data"]:
                # Count recipients
                recipients_list = []
                if item.get("recipients"):
                    recipients_list.extend(item.get("recipients").split(","))
                if item.get("cc"):
                    recipients_list.extend(item.get("cc").split(","))
                if item.get("bcc"):
                    recipients_list.extend(item.get("bcc").split(","))
                
                item["recipient_count"] = len([r.strip() for r in recipients_list if r.strip()])
                
                # Truncate content for list view
                if item.get("content") and len(item["content"]) > 200:
                    item["content_preview"] = item["content"][:200] + "..."
                else:
                    item["content_preview"] = item.get("content", "")
                
                # Parse attachments if JSON
                if item.get("attachments"):
                    try:
                        attachments = json.loads(item["attachments"])
                        item["attachment_count"] = len(attachments) if isinstance(attachments, list) else 0
                    except:
                        item["attachment_count"] = 0
                else:
                    item["attachment_count"] = 0
            
            return {
                "success": True,
                "data": result["data"],
                "pagination": result["pagination"]
            }
        else:
            return {
                "success": False,
                "error": result.get("error", "Unknown error"),
                "data": [],
                "pagination": {
                    "page": 1,
                    "limit": limit,
                    "total": 0,
                    "pages": 0,
                    "has_next": False,
                    "has_prev": False,
                    "showing_from": 0,
                    "showing_to": 0
                }
            }
        
    except Exception as e:
        frappe.log_error(f"Error in get_email_logs_paginated: {str(e)}")
        return {
            "success": False,
            "error": str(e),
            "data": [],
            "pagination": {
                "page": 1,
                "limit": limit,
                "total": 0,
                "pages": 0,
                "has_next": False,
                "has_prev": False,
                "showing_from": 0,
                "showing_to": 0
            }
        }


@frappe.whitelist()
def get_email_log_by_name(name):
    """
    Get email log details by name
    """
    try:
        return get_form_data("EmailLog", name)
    except Exception as e:
        frappe.log_error(f"Error in get_email_log_by_name: {str(e)}")
        return {"success": False, "error": str(e)}


@frappe.whitelist()
def create_email_log(data):
    """
    Create new email log
    """
    try:
        # Validate required fields
        if not data.get("subject"):
            return {"success": False, "error": "Subject is required"}
        if not data.get("recipients"):
            return {"success": False, "error": "Recipients are required"}
        if not data.get("sender"):
            return {"success": False, "error": "Sender is required"}
        
        # Set default status
        if not data.get("status"):
            data["status"] = "PENDING"
        
        return save_doc("EmailLog", data)
    except Exception as e:
        frappe.log_error(f"Error in create_email_log: {str(e)}")
        return {"success": False, "error": str(e)}


@frappe.whitelist()
def update_email_log(name, data):
    """
    Update existing email log
    """
    try:
        # Validate required fields
        if not data.get("subject"):
            return {"success": False, "error": "Subject is required"}
        if not data.get("recipients"):
            return {"success": False, "error": "Recipients are required"}
        if not data.get("sender"):
            return {"success": False, "error": "Sender is required"}
        
        return save_doc("EmailLog", data, name)
    except Exception as e:
        frappe.log_error(f"Error in update_email_log: {str(e)}")
        return {"success": False, "error": str(e)}


@frappe.whitelist()
def delete_email_log(name):
    """
    Delete email log
    """
    try:
        return delete_doc("EmailLog", name)
    except Exception as e:
        frappe.log_error(f"Error in delete_email_log: {str(e)}")
        return {"success": False, "error": str(e)}


@frappe.whitelist()
def get_email_log_stats():
    """
    Get email log statistics
    """
    try:
        total_emails = frappe.db.count("EmailLog")
        
        # Count by status
        status_stats = frappe.db.sql("""
            SELECT status, COUNT(*) as count
            FROM `tabEmailLog`
            GROUP BY status
        """, as_dict=True)
        
        # Count by sender
        sender_stats = frappe.db.sql("""
            SELECT sender, COUNT(*) as count
            FROM `tabEmailLog`
            GROUP BY sender
            ORDER BY count DESC
            LIMIT 10
        """, as_dict=True)
        
        # Emails by day (last 7 days)
        daily_stats = frappe.db.sql("""
            SELECT DATE(creation) as date, COUNT(*) as count
            FROM `tabEmailLog`
            WHERE creation >= DATE_SUB(NOW(), INTERVAL 7 DAY)
            GROUP BY DATE(creation)
            ORDER BY date DESC
        """, as_dict=True)
        
        # Recent emails
        recent_emails = frappe.db.sql("""
            SELECT name, subject, recipients, sender, status, creation
            FROM `tabEmailLog`
            ORDER BY creation DESC
            LIMIT 10
        """, as_dict=True)
        
        # Success rate
        success_rate = frappe.db.sql("""
            SELECT 
                COUNT(*) as total,
                SUM(CASE WHEN status = 'SENT' THEN 1 ELSE 0 END) as sent,
                SUM(CASE WHEN status = 'FAILED' THEN 1 ELSE 0 END) as failed,
                SUM(CASE WHEN status = 'PENDING' THEN 1 ELSE 0 END) as pending
            FROM `tabEmailLog`
        """, as_dict=True)
        
        return {
            "success": True,
            "total_emails": total_emails,
            "status_stats": status_stats,
            "sender_stats": sender_stats,
            "daily_stats": daily_stats,
            "recent_emails": recent_emails,
            "success_rate": success_rate[0] if success_rate else {}
        }
    except Exception as e:
        frappe.log_error(f"Error in get_email_log_stats: {str(e)}")
        return {"success": False, "error": str(e)}


@frappe.whitelist()
def search_email_logs(query, limit=10):
    """
    Search email logs for autocomplete
    """
    try:
        if not query:
            return []
        
        results = frappe.db.sql("""
            SELECT name, subject, recipients, sender, status, creation
            FROM `tabEmailLog`
            WHERE subject LIKE %(query)s
            OR recipients LIKE %(query)s
            OR sender LIKE %(query)s
            ORDER BY creation DESC
            LIMIT %(limit)s
        """, {
            "query": f"%{query}%",
            "limit": limit
        }, as_dict=True)
        
        return results
    except Exception as e:
        frappe.log_error(f"Error in search_email_logs: {str(e)}")
        return []


@frappe.whitelist()
def get_email_log_filter_options():
    """
    Get filter options for email logs
    """
    try:
        return get_filter_options("EmailLog", [
            "status",
            "sender"
        ])
    except Exception as e:
        frappe.log_error(f"Error in get_email_log_filter_options: {str(e)}")
        return {"success": False, "error": str(e)}


@frappe.whitelist()
def get_email_logs_by_sender(sender, limit=100):
    """
    Get email logs by sender
    """
    try:
        logs = frappe.db.sql("""
            SELECT name, subject, recipients, cc, bcc, status, creation
            FROM `tabEmailLog`
            WHERE sender = %(sender)s
            ORDER BY creation DESC
            LIMIT %(limit)s
        """, {"sender": sender, "limit": limit}, as_dict=True)
        
        return {
            "success": True,
            "data": logs
        }
    except Exception as e:
        frappe.log_error(f"Error in get_email_logs_by_sender: {str(e)}")
        return {"success": False, "error": str(e)}


@frappe.whitelist()
def get_email_logs_by_recipient(recipient, limit=100):
    """
    Get email logs by recipient
    """
    try:
        logs = frappe.db.sql("""
            SELECT name, subject, sender, status, creation
            FROM `tabEmailLog`
            WHERE recipients LIKE %(recipient)s
            OR cc LIKE %(recipient)s
            OR bcc LIKE %(recipient)s
            ORDER BY creation DESC
            LIMIT %(limit)s
        """, {"recipient": f"%{recipient}%", "limit": limit}, as_dict=True)
        
        return {
            "success": True,
            "data": logs
        }
    except Exception as e:
        frappe.log_error(f"Error in get_email_logs_by_recipient: {str(e)}")
        return {"success": False, "error": str(e)}


@frappe.whitelist()
def retry_failed_email(name):
    """
    Retry sending a failed email
    """
    try:
        doc = frappe.get_doc("EmailLog", name)
        
        if doc.status != "FAILED":
            return {"success": False, "error": "Email is not in failed status"}
        
        # Reset status to pending for retry
        doc.status = "PENDING"
        doc.error = ""
        doc.save()
        
        # Here you would typically trigger the email sending process
        # For now, we'll just update the status
        
        return {"success": True, "message": "Email queued for retry"}
    except Exception as e:
        frappe.log_error(f"Error in retry_failed_email: {str(e)}")
        return {"success": False, "error": str(e)}


@frappe.whitelist()
def bulk_retry_failed_emails(email_ids):
    """
    Retry multiple failed emails
    """
    try:
        if isinstance(email_ids, str):
            email_ids = json.loads(email_ids)
        
        results = []
        for email_id in email_ids:
            doc = frappe.get_doc("EmailLog", email_id)
            
            if doc.status == "FAILED":
                doc.status = "PENDING"
                doc.error = ""
                doc.save()
                results.append({"email_id": email_id, "status": "queued"})
            else:
                results.append({"email_id": email_id, "status": "not_failed"})
        
        return {"success": True, "results": results}
    except Exception as e:
        frappe.log_error(f"Error in bulk_retry_failed_emails: {str(e)}")
        return {"success": False, "error": str(e)}


@frappe.whitelist()
def get_email_content(name):
    """
    Get full email content for preview
    """
    try:
        doc = frappe.get_doc("EmailLog", name)
        
        return {
            "success": True,
            "data": {
                "subject": doc.subject,
                "content": doc.content,
                "recipients": doc.recipients,
                "cc": doc.cc,
                "bcc": doc.bcc,
                "sender": doc.sender,
                "attachments": doc.attachments,
                "status": doc.status,
                "error": doc.error,
                "creation": doc.creation
            }
        }
    except Exception as e:
        frappe.log_error(f"Error in get_email_content: {str(e)}")
        return {"success": False, "error": str(e)}


@frappe.whitelist()
def get_email_delivery_report(start_date=None, end_date=None):
    """
    Get email delivery report for a date range
    """
    try:
        conditions = []
        params = {}
        
        if start_date:
            conditions.append("creation >= %(start_date)s")
            params["start_date"] = start_date
        
        if end_date:
            conditions.append("creation <= %(end_date)s")
            params["end_date"] = end_date
        
        where_clause = ""
        if conditions:
            where_clause = f"WHERE {' AND '.join(conditions)}"
        
        query = f"""
            SELECT 
                DATE(creation) as date,
                COUNT(*) as total_emails,
                SUM(CASE WHEN status = 'SENT' THEN 1 ELSE 0 END) as sent,
                SUM(CASE WHEN status = 'FAILED' THEN 1 ELSE 0 END) as failed,
                SUM(CASE WHEN status = 'PENDING' THEN 1 ELSE 0 END) as pending,
                ROUND(SUM(CASE WHEN status = 'SENT' THEN 1 ELSE 0 END) * 100.0 / COUNT(*), 2) as success_rate
            FROM `tabEmailLog`
            {where_clause}
            GROUP BY DATE(creation)
            ORDER BY date DESC
        """
        
        report = frappe.db.sql(query, params, as_dict=True)
        
        return {
            "success": True,
            "data": report
        }
    except Exception as e:
        frappe.log_error(f"Error in get_email_delivery_report: {str(e)}")
        return {"success": False, "error": str(e)}


@frappe.whitelist()
def log_email_sent(subject, recipients, sender, content, attachments=None):
    """
    Log a sent email
    """
    try:
        doc = frappe.new_doc("EmailLog")
        doc.subject = subject
        doc.recipients = recipients
        doc.sender = sender
        doc.content = content
        doc.status = "SENT"
        
        if attachments:
            doc.attachments = json.dumps(attachments)
        
        doc.save()
        
        return {"success": True, "name": doc.name}
    except Exception as e:
        frappe.log_error(f"Error in log_email_sent: {str(e)}")
        return {"success": False, "error": str(e)}


@frappe.whitelist()
def log_email_failed(subject, recipients, sender, content, error, attachments=None):
    """
    Log a failed email
    """
    try:
        doc = frappe.new_doc("EmailLog")
        doc.subject = subject
        doc.recipients = recipients
        doc.sender = sender
        doc.content = content
        doc.status = "FAILED"
        doc.error = error
        
        if attachments:
            doc.attachments = json.dumps(attachments)
        
        doc.save()
        
        return {"success": True, "name": doc.name}
    except Exception as e:
        frappe.log_error(f"Error in log_email_failed: {str(e)}")
        return {"success": False, "error": str(e)}
