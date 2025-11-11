"""
API endpoints for Mira External Connection
"""
import frappe
from frappe import _


@frappe.whitelist()
def get_facebook_pages():
    """
    Get all Facebook pages from Mira External Connection
    Returns list of connected Facebook pages with their details
    """
    try:
        # Get Facebook connection
        connections = frappe.get_all(
            "Mira External Connection",
            filters={
                "platform_type": "Facebook",
                "connection_status": "Connected",
                "active_status": 1
            },
            fields=["name", "tenant_name", "user_email", "primary_account_id"]
        )
        
        if not connections:
            return {
                "success": True,
                "data": [],
                "message": _("No Facebook connection found")
            }
        
        # Get all Facebook pages from connected accounts
        pages = []
        for conn in connections:
            # Get connected accounts (pages) for this connection
            accounts = frappe.get_all(
                "Mira External Connection Account",
                filters={
                    "parent": conn.name,
                    "parenttype": "Mira External Connection",
                    "account_type": "Page",
                    "is_active": 1
                },
                fields=[
                    "external_account_id",
                    "account_name",
                    "profile_picture_url",
                    "follower_count",
                    "connection_status"
                ]
            )
            
            for account in accounts:
                pages.append({
                    "page_id": account.external_account_id,
                    "page_name": account.account_name,
                    "profile_picture": account.profile_picture_url,
                    "follower_count": account.follower_count,
                    "connection_name": conn.name,
                    "connection_status": account.connection_status
                })
        
        return {
            "success": True,
            "data": pages,
            "message": _("Facebook pages loaded successfully")
        }
        
    except Exception as e:
        frappe.log_error(f"Error getting Facebook pages: {str(e)}")
        return {
            "success": False,
            "data": [],
            "message": str(e)
        }


@frappe.whitelist()
def get_zalo_oas():
    """
    Get all Zalo OAs from Mira External Connection
    Returns list of connected Zalo Official Accounts
    """
    try:
        # Get Zalo connection
        connections = frappe.get_all(
            "Mira External Connection",
            filters={
                "platform_type": "Zalo",
                "connection_status": "Connected",
                "active_status": 1
            },
            fields=["name", "tenant_name", "user_email"]
        )
        
        if not connections:
            return {
                "success": True,
                "data": [],
                "message": _("No Zalo connection found")
            }
        
        # Get all Zalo OAs from connected accounts
        oas = []
        for conn in connections:
            accounts = frappe.get_all(
                "Mira External Connection Account",
                filters={
                    "parent": conn.name,
                    "parenttype": "Mira External Connection",
                    "account_type": "OA",
                    "is_active": 1
                },
                fields=[
                    "external_account_id",
                    "account_name",
                    "profile_picture_url",
                    "follower_count",
                    "connection_status"
                ]
            )
            
            for account in accounts:
                oas.append({
                    "oa_id": account.external_account_id,
                    "oa_name": account.account_name,
                    "profile_picture": account.profile_picture_url,
                    "follower_count": account.follower_count,
                    "connection_name": conn.name,
                    "connection_status": account.connection_status
                })
        
        return {
            "success": True,
            "data": oas,
            "message": _("Zalo OAs loaded successfully")
        }
        
    except Exception as e:
        frappe.log_error(f"Error getting Zalo OAs: {str(e)}")
        return {
            "success": False,
            "data": [],
            "message": str(e)
        }
