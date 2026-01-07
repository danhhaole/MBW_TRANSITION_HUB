import frappe
import json


@frappe.whitelist()
def get_notifications(filters=None):
    """
    Get notifications from Notification Log doctype.
    Similar to mbw_ats.api.notifications.get_notifications
    """
    # Parse filters if it's a string
    if isinstance(filters, str):
        filters = json.loads(filters)
    
    if not filters:
        filters = {}
    
    # Get current user
    current_user = frappe.session.user
    
    # Try for_user first, then fallback to owner
    for_user_filters = {**filters, "for_user": current_user}
    notifications = frappe.get_all(
        "Notification Log",
        filters=for_user_filters,
        fields=["subject", "from_user", "link", "read", "name", "creation", "type", "document_type", "document_name"],
        order_by="creation desc",
    )
    
    # If no results with for_user, try with owner
    if not notifications:
        owner_filters = {**filters, "owner": current_user}
        # Remove for_user if it was in original filters
        owner_filters.pop("for_user", None)
        notifications = frappe.get_all(
            "Notification Log",
            filters=owner_filters,
            fields=["subject", "from_user", "link", "read", "name", "creation", "type", "document_type", "document_name"],
            order_by="creation desc",
        )

    for notification in notifications:
        if notification.from_user:
            from_user_details = frappe.db.get_value(
                "User", notification.from_user, ["full_name", "user_image"], as_dict=1
            )
            if from_user_details:
                notification.update(from_user_details)

    return notifications


@frappe.whitelist()
def mark_as_read(name):
    """
    Mark a notification as read.
    Similar to mbw_ats.api.notifications.mark_as_read
    """
    doc = frappe.get_doc("Notification Log", name)
    doc.read = 1
    doc.save(ignore_permissions=True)
    return {"success": True}


@frappe.whitelist()
def mark_all_as_read():
    """
    Mark all unread notifications as read for current user.
    Similar to mbw_ats.api.notifications.mark_all_as_read
    """
    current_user = frappe.session.user
    
    # Try for_user first
    notifications = frappe.get_all(
        "Notification Log", {"for_user": current_user, "read": 0}, pluck="name"
    )
    
    # If no results, try owner
    if not notifications:
        notifications = frappe.get_all(
            "Notification Log", {"owner": current_user, "read": 0}, pluck="name"
        )

    for notification in notifications:
        mark_as_read(notification)
    
    return {"success": True, "marked": len(notifications)}