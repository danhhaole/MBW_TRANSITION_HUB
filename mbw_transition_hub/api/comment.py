from collections.abc import Iterable

import frappe
from frappe import _
from bs4 import BeautifulSoup
from frappe.desk.form.utils import add_comment as frappe_add_comment


def extract_mentions(html):
    if not html:
        return []
    soup = BeautifulSoup(html, "html.parser")
    mentions = []
    for d in soup.find_all("span", attrs={"data-type": "mention"}):
        mentions.append(
            frappe._dict(full_name=d.get("data-label"), email=d.get("data-id"))
        )
    return mentions


def handle_comment_refetch_resource(doc, _method=None):
    try:
        reference_name = getattr(doc, "reference_name", None)
        if not reference_name:
            return

        reference_doctype = getattr(doc, "reference_doctype", None)
        if not reference_doctype:
            return

        frappe.logger().info(
            "Publishing refetch_resource for Comment %s -> %s %s",
            getattr(doc, "name", None),
            getattr(doc, "reference_doctype", None),
            reference_name,
        )

        payload = {"cache_key": ["activity", reference_name]}

        frappe.publish_realtime(
            event="refetch_resource",
            message=payload,
            doctype=reference_doctype,
            docname=reference_name,
            after_commit=True,
        )
    except Exception as e:
        frappe.log_error(
            title="Error publishing refetch_resource for comment",
            message=str(e),
        )


@frappe.whitelist()
def add_attachments(name: str, attachments: Iterable[str | dict]) -> None:
    """Add attachments to the given Comment

    :param name: Comment name
    :param attachments: File names or dicts with keys "fname" and "fcontent"
    """
    # loop through attachments
    for a in attachments:
        if isinstance(a, str):
            attach = frappe.db.get_value("File", {"name": a}, ["file_url", "is_private"], as_dict=1)
            file_args = {
                "file_url": attach.file_url,
                "is_private": attach.is_private,
            }
        elif isinstance(a, dict) and "fcontent" in a and "fname" in a:
            # dict returned by frappe.attach_print()
            file_args = {
                "file_name": a["fname"],
                "content": a["fcontent"],
                "is_private": 1,
            }
        else:
            continue

        file_args.update(
            {
                "attached_to_doctype": "Comment",
                "attached_to_name": name,
                "folder": "Home/Attachments",
            }
        )

        _file = frappe.new_doc("File")
        _file.update(file_args)
        _file.save(ignore_permissions=True)

    try:
        comment_doc = frappe.get_doc("Comment", name)
        handle_comment_refetch_resource(comment_doc)
    except Exception as e:
        frappe.log_error(
            title="Error publishing refetch_resource after comment attachments",
            message=str(e),
        )               


@frappe.whitelist()
def notify_mentioned_users(comment_name: str, content: str, reference_doctype: str, reference_name: str) -> dict:
    """
    Gửi email thông báo cho các user được tag trong comment.

    Args:
        comment_name: Tên của Comment document
        content: Nội dung HTML của comment
        reference_doctype: DocType được comment (e.g., Mira Campaign)
        reference_name: Tên document được comment

    Returns:
        dict: Kết quả gửi email
    """

    mentions = extract_mentions(content)

    if not mentions:
        return {"success": True, "message": "No mentions found", "sent_to": []}

    # Deduplicate mentions by email
    unique_mentions = {}
    for m in mentions:
        if m.email not in unique_mentions:
            unique_mentions[m.email] = m
    
    mentions = list(unique_mentions.values())

    current_user = frappe.session.user
    current_user_name = frappe.get_cached_value(
        "User", current_user, "full_name") or current_user

    # Lấy thông tin document
    doc_title = reference_name
    if reference_doctype == "Mira Campaign":
        doc_title = frappe.get_cached_value(
            "Mira Campaign", reference_name, "campaign_name") or reference_name

    sent_to = []
    for mention in mentions:
        if mention.email == current_user:
            continue  # Không gửi cho chính mình

        try:
            subject = _("{0} mentioned you in a comment on {1}").format(
                current_user_name, doc_title
            )

            # Tạo URL dựa trên reference_doctype
            if reference_doctype == "Mira Campaign":
                notification_url = f"/campaign/{reference_name}#comments"
                email_url = f"/mbw_transition_hub/campaign/{reference_name}#comments"
            else:
                notification_url = f"/{reference_doctype.lower().replace('_', '-')}/{reference_name}#comments"
                email_url = f"/mbw_transition_hub/{reference_doctype.lower().replace('_', '-')}/{reference_name}#comments"

            # Kiểm tra có file đính kèm trong comment không
            attachments = frappe.get_all(
                "File",
                filters={
                    "attached_to_doctype": "Comment",
                    "attached_to_name": comment_name
                },
                fields=["file_name"]
            )

            attachment_text = ""
            if attachments:
                attachment_count = len(attachments)
                attachment_names = ", ".join(
                    [a.file_name for a in attachments[:3]])
                if attachment_count > 3:
                    attachment_names += f" và {attachment_count - 3} file khác"
                attachment_text = f"""
                <p style="color: #666; font-style: italic;">
                    <b>Bình luận</b> có {attachment_count} file đính kèm: {attachment_names}
                </p>
                """

            message = f"""
            <p><strong>{current_user_name}</strong> đã nhắc đến bạn trong một bình luận:</p>
            <blockquote style="border-left: 3px solid #ccc; padding-left: 10px; margin: 10px 0;">
                {content}
            </blockquote>
            {attachment_text}
            <p>
                <a href="{email_url}">
                    Xem chi tiết
                </a>
            </p>
            """

            # Check Rate Limit (10 minutes)
            cache_key = f"mention_email_cd:{mention.email}:{reference_doctype}:{reference_name}"
            if frappe.cache().get_value(cache_key):
                sent_to.append(f"{mention.email} (Rate Limit)")
            else:
                try:
                    frappe.get_doc({
                        "doctype": "Notification Log",
                        "type": "Mention",
                        "for_user": mention.email,
                        "from_user": current_user,
                        "subject": subject,
                        "document_type": reference_doctype,
                        "document_name": reference_name,
                        "link": notification_url,
                        "email_content": message,
                        "seen": 0,
                    }).insert(ignore_permissions=True)
                    frappe.cache().set_value(cache_key, 1, expires_in_sec=600)
                    sent_to.append(mention.email)
                except Exception as notification_error:
                    frappe.log_error(
                        title="Error creating notification log or sending email",
                        message=str(notification_error)
                    )
                    sent_to.append(
                        f"{mention.email} (Error: {str(notification_error)})")

        except Exception as e:
            frappe.log_error(
                title="Error sending mention notification",
                message=f"Failed to send to {mention.email}: {str(e)}"
            )
    
    return {"success": True, "sent_to": sent_to}


@frappe.whitelist()
def add_comment(reference_doctype, reference_name, content, comment_email, comment_by):
    """
    Wrapper API để add comment, bắn realtime và enqueue notification.
    """
    try:
        # Gọi API gốc của Frappe
        comment = frappe_add_comment(
            reference_doctype,
            reference_name,
            content,
            comment_email,
            comment_by
        )

        owner_name = frappe.get_cached_value("User", comment.owner, 'full_name') or comment.owner

        activity_data = {
            "name": comment.name,
            "owner": comment.owner,
            "owner_name": owner_name,
            "creation": comment.creation,
            "modified": comment.modified,
            "activity_type": "comment",
            "content": content,
            "reference_doctype": reference_doctype,
            "reference_name": reference_name,
            "data": {
                "type": "Comment",
                "content": content
            }
        }
        
        # Enqueue notification chạy ngầm
        frappe.enqueue(
            "mbw_transition_hub.api.comment.notify_mentioned_users",
            queue="short",
            comment_name=comment.name,
            content=content,
            reference_doctype=reference_doctype,
            reference_name=reference_name
        )

        # Publish Custom Event cho realtime UI
        frappe.publish_realtime(
            event="mbw_transition_hub:comment_added",
            message=activity_data,
            room=f"{reference_doctype}:{reference_name}",
            after_commit=True
        )

        return comment
    except Exception as e:
        frappe.log_error(title="Error adding comment via wrapper", message=str(e))
        raise e
