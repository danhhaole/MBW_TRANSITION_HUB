import datetime
import frappe
from frappe import _
from frappe.utils import now, add_days, get_datetime, now_datetime, get_url
import json
import secrets
import requests
from typing import Dict, List, Optional, Any
from urllib.parse import quote, urlparse, parse_qs, urlencode, urlunparse
import re
from mbw_mira.helpers.html_parse import convert_html_for_facebook
from mbw_mira.utils import make_signature

host = frappe.conf.get("socialhub") or "https://socialhub.mbwcloud.com"


@frappe.whitelist()
def get_connection_info(
    tenant_name=None, user_email=None, platform_type=None
) -> Dict[str, Any]:
    """
    Lấy thông tin kết nối của user

    Args:
        tenant_name: Tên tenant (optional)
        user_email: Email của user (optional)
        platform_type: Loại platform (optional)

    Returns:
        Dict chứa thông tin kết nối
    """
    try:
        # Build filters
        filters = {"active_status": 1}

        if tenant_name and tenant_name.strip():
            filters["tenant_name"] = tenant_name
        if user_email and user_email.strip():
            filters["user_email"] = user_email
        if platform_type and platform_type.strip():
            filters["platform_type"] = platform_type

        # Get connections
        connections = frappe.get_all(
            "Mira External Connection",
            filters=filters,
            fields=[
                "name",
                "platform_type",
                "connection_status",
                "primary_account_id",
                "last_connected_at",
                "success_rate",
                "total_api_calls",
                "successful_calls",
                "failed_calls",
                "last_activity",
                "tenant_name",
                "user_email",
                "full_name",
                "created_at",
                "api_key",
                "client_secret",
                "hook_url",
                "redirect_url",
            ],
        )

        result = []
        for conn in connections:
            # Get connected accounts
            accounts = frappe.get_all(
                "Mira External Connection Account",
                filters={"parent": conn.name, "is_active": 1},
                fields=[
                    "external_account_id",
                    "account_name",
                    "account_type",
                    "is_primary",
                    "follower_count",
                    "posts_count",
                    "profile_picture_url",
                    "connection_status",
                    "following_count",
                    "last_activity",
                    "permissions",
                    "scope_permissions",
                ],
            )

            conn_data = {
                "connection_id": conn.name,
                "platform_type": conn.platform_type,
                "connection_status": conn.connection_status,
                "primary_account_id": conn.primary_account_id,
                "tenant_name": conn.tenant_name,
                "user_email": conn.user_email,
                "full_name": conn.full_name,
                "statistics": {
                    "total_api_calls": conn.total_api_calls or 0,
                    "successful_calls": conn.successful_calls or 0,
                    "failed_calls": conn.failed_calls or 0,
                    "success_rate": conn.success_rate or 0,
                },
                "last_connected_at": conn.last_connected_at,
                "last_activity": conn.last_activity,
                "created_at": conn.created_at,
                "connected_accounts": accounts,
                "hook_url": conn.hook_url,
                "redirect_url": conn.redirect_url,
            }
            result.append(conn_data)

        return {"status": "success", "data": result, "total_connections": len(result)}

    except Exception as e:
        frappe.log_error(frappe.get_traceback(), "Get Connection Info Error")
        return {"status": "error", "message": str(e)}


@frappe.whitelist()
def get_all_accounts() -> List[Dict[str, Any]]:
    """
    Lấy tất cả accounts từ tất cả connections với thông tin parent connection
    
    Returns:
        List chứa thông tin tất cả accounts với parent_connection
    """
    try:
        # Get all active connections
        connections = frappe.get_all(
            "Mira External Connection",
            filters={"connection_status": "Connected"},
            fields=["name", "platform_type", "tenant_name"]
        )
        
        result = []
        for conn in connections:
            # Get accounts for this connection
            accounts = frappe.get_all(
                "Mira External Connection Account",
                filters={"parent": conn.name, "is_active": 1},
                fields=[
                    "name",
                    "external_account_id",
                    "account_name", 
                    "account_type",
                    "is_primary",
                    "connection_status",
                    "profile_picture_url",
                    "follower_count",
                    "following_count",
                    "posts_count",
                    "last_activity"
                ]
            )
            
            # Add parent connection info to each account
            for account in accounts:
                account["parent_connection"] = conn.name
                account["platform_type"] = conn.platform_type
                account["tenant_name"] = conn.tenant_name
                result.append(account)
        
        return result
        
    except Exception as e:
        frappe.log_error(frappe.get_traceback(), "Get All Accounts Error")
        return []


@frappe.whitelist()
def get_account_details(connection_id: str, account_id: str = None) -> Dict[str, Any]:
    """
    Lấy chi tiết tài khoản được kết nối

    Args:
        connection_id: ID của Mira External Connection
        account_id: ID của account cụ thể (optional)

    Returns:
        Dict chứa thông tin chi tiết account
    """
    try:
        # Verify connection exists
        connection_doc = frappe.get_doc("Mira External Connection", connection_id)
        if not connection_doc:
            return {"status": "error", "message": "Connection not found"}

        result = []
        for account in connection_doc.connected_accounts:
            if account_id and account.external_account_id != account_id:
                continue
            # Parse JSON fields safely
            account_metadata = {}
            if account.account_metadata:
                try:
                    account_metadata = (
                        json.loads(account.account_metadata)
                        if isinstance(account.account_metadata, str)
                        else account.account_metadata
                    )
                except (json.JSONDecodeError, TypeError):
                    account_metadata = {}

            account_data = {
                "external_account_id": account.external_account_id,
                "account_name": account.account_name,
                "account_type": account.account_type,
                "is_primary": account.is_primary,
                "is_active": account.is_active,
                "profile_picture_url": account.profile_picture_url,
                "follower_count": account.follower_count or 0,
                "following_count": account.following_count or 0,
                "posts_count": account.posts_count or 0,
                "connection_status": account.connection_status,
                "permissions": account.permissions,
                "scope_permissions": account.scope_permissions,
                "last_activity": account.last_activity,
                "token_expiry": account.token_expiry,
                "last_token_refresh": account.last_token_refresh,
                "account_metadata": account_metadata,
            }
            result.append(account_data)

        return {
            "status": "success",
            "data": result if not account_id else (result[0] if result else None),
            "total_accounts": len(result),
        }

    except Exception as e:
        frappe.log_error(frappe.get_traceback(), "Get Account Details Error")
        return {"status": "error", "message": str(e)}


from urllib.parse import urlencode, urlparse


def get_url_without_port():
    # Prefer explicit public base URL from config (works with Cloudflare tunnels)
    base = (
        frappe.conf.get("mbw_public_base_url")
        or frappe.conf.get("public_base_url")
        or None
    )
    if base:
        parsed = urlparse(base)
        return f"{parsed.scheme}://{parsed.hostname}"
    # Fallback to site URL without port
    url = get_url()
    parsed = urlparse(url)
    return f"{parsed.scheme}://{parsed.hostname}"


@frappe.whitelist()
def create_connection(
    platform_type: str,
    user_email: str,
    full_name: str,
    hook_url: str = None,
    redirect_url: str = None,
    **kwargs,
) -> Dict[str, Any]:
    """
    Tạo kết nối mới với platform bên ngoài

    Args:
        platform_type: Loại platform (Facebook, Zalo, etc.)
        tenant_name: Tên tenant
        user_email: Email của user
        full_name: Họ tên user
        hook_url: URL webhook (optional)
        redirect_url: URL redirect sau khi authorize (optional)
        **kwargs: Các tham số bổ sung

    Returns:
        Dict chứa thông tin kết nối được tạo
    """
    tenant_name = get_url_without_port()
    try:
        # Check if connection already exists
        existing = frappe.db.exists(
            "Mira External Connection",
            {
                "platform_type": platform_type,
                "tenant_name": tenant_name,
                "user_email": user_email,
                "active_status": 1,
            },
        )

        if existing:
            return {
                "status": "error",
                "message": f"Active connection already exists for {platform_type}",
                "connection_id": existing,
            }

        # Generate secret token
        secret_token = secrets.token_urlsafe(32)
        print("get_url_without_port>>>>>>>>>>>>>>>>>>>>:", get_url_without_port())
        hook_url = f"{get_url_without_port()}/api/method/mbw_mira.api.external_connections.handle_webhook"
        # hook_url = f"http://localhost:8008/api/method/mbw_mira.api.external_connections.handle_webhook"
        print("hook_url>>>>>>>>>>>>>>>>>>:", hook_url)
        redirect_url = f"{get_url_without_port()}/mbw_mira/connectors"
        # Create Mira External Connection document
        connection_doc = frappe.get_doc(
            {
                "doctype": "Mira External Connection",
                "platform_type": platform_type,
                "tenant_name": tenant_name,
                "user_email": user_email,
                "full_name": full_name,
                "hook_url": hook_url or "",
                "redirect_url": redirect_url or "",
                "secret_token": secret_token,
                "connection_status": "Pending",
                "active_status": 1,
                "auto_reconnect": 1,
                "sync_frequency": "Every 15 minutes",
                "max_retries": 3,
                "retry_count": 0,
                "total_api_calls": 0,
                "successful_calls": 0,
                "failed_calls": 0,
                "total_webhooks": 0,
                "created_at": now(),
                "updated_at": now(),
                "connected_by": frappe.session.user,
            }
        )

        # Set additional fields from kwargs
        allowed_fields = [
            "client_id",
            "client_secret",
            "api_key",
            "sync_settings",
            "permissions_config",
            "connection_notes",
        ]
        for key, value in kwargs.items():
            if key in allowed_fields and hasattr(connection_doc, key):
                setattr(connection_doc, key, value)

        connection_doc.insert()

        # Get platform-specific login URL
        login_url = _get_platform_login_url(platform_type, connection_doc)

        if login_url:
            connection_doc.login_url = login_url
            connection_doc.save()

        # Log the creation
        _create_connection_log(
            connection_doc.name,
            "System",
            "connection_created",
            platform_type,
            status="Success",
            notes=f"Connection created for {user_email}",
        )

        return {
            "status": "success",
            "message": "Connection created successfully",
            "data": {
                "connection_id": connection_doc.name,
                "secret_token": secret_token,
                "login_url": login_url,
                "platform_type": platform_type,
                "connection_status": "Pending",
            },
        }

    except Exception as e:
        frappe.log_error(frappe.get_traceback(), "Create Connection Error")
        return {"status": "error", "message": str(e)}


@frappe.whitelist()
def update_connection(connection_id: str, **kwargs) -> Dict[str, Any]:
    """
    Cập nhật thông tin kết nối

    Args:
        connection_id: ID của Mira External Connection
        **kwargs: Các fields cần update

    Returns:
        Dict chứa kết quả update
    """
    try:
        # Get connection document
        connection_doc = frappe.get_doc("Mira External Connection", connection_id)

        # Track changes
        changes = {}
        updatable_fields = [
            "hook_url",
            "redirect_url",
            "active_status",
            "auto_reconnect",
            "sync_frequency",
            "max_retries",
            "connection_status",
            "access_token",
            "refresh_token",
            "token_expiry",
            "primary_account_id",
            "sync_settings",
            "permissions_config",
            "connection_notes",
            "client_id",
            "client_secret",
            "api_key",
        ]

        for key, value in kwargs.items():
            if key in updatable_fields and hasattr(connection_doc, key):
                old_value = getattr(connection_doc, key)
                if old_value != value:
                    changes[key] = {"old": old_value, "new": value}
                    setattr(connection_doc, key, value)

        if changes:
            connection_doc.updated_at = now()
            connection_doc.save()

            # Log the update
            _create_connection_log(
                connection_id,
                "System",
                "connection_updated",
                connection_doc.platform_type,
                status="Success",
                custom_data=json.dumps(changes),
                notes=f"Connection updated: {', '.join(changes.keys())}",
            )

            return {
                "status": "success",
                "message": "Connection updated successfully",
                "changes": changes,
            }
        else:
            return {"status": "info", "message": "No changes detected"}

    except frappe.DoesNotExistError:
        return {"status": "error", "message": "Connection not found"}
    except Exception as e:
        frappe.log_error(frappe.get_traceback(), "Update Connection Error")
        return {"status": "error", "message": str(e)}


@frappe.whitelist()
def disconnect_connection(connection_id: str, reason: str = "") -> Dict[str, Any]:
    """
    Ngắt kết nối với platform

    Args:
        connection_id: ID của Mira External Connection
        reason: Lý do ngắt kết nối

    Returns:
        Dict chứa kết quả disconnect
    """
    try:
        connection_doc = frappe.get_doc("Mira External Connection", connection_id)

        # Update connection status
        connection_doc.connection_status = "Disconnected"
        connection_doc.active_status = 0
        connection_doc.last_disconnected_at = now()
        connection_doc.updated_at = now()

        if reason:
            current_notes = connection_doc.connection_notes or ""
            connection_doc.connection_notes = (
                f"{current_notes}\nDisconnected: {reason}".strip()
            )

        connection_doc.save()

        # Deactivate all connected accounts in child table
        for account in connection_doc.connected_accounts:
            account.is_active = 0
            account.connection_status = "Revoked"

        connection_doc.save()

        # Call platform-specific disconnect if needed
        _platform_disconnect(connection_doc)

        # Log the disconnection
        _create_connection_log(
            connection_id,
            "System",
            "connection_disconnected",
            connection_doc.platform_type,
            status="Success",
            notes=(
                f"Connection disconnected. Reason: {reason}"
                if reason
                else "Connection disconnected"
            ),
        )

        return {"status": "success", "message": "Connection disconnected successfully"}

    except frappe.DoesNotExistError:
        return {"status": "error", "message": "Connection not found"}
    except Exception as e:
        frappe.log_error(frappe.get_traceback(), "Disconnect Connection Error")
        return {"status": "error", "message": str(e)}


@frappe.whitelist()
def sync_accounts(connection_id: str, force_sync: bool = False) -> Dict[str, Any]:
    """
    Đồng bộ danh sách accounts từ platform

    Args:
        connection_id: ID của Mira External Connection
        force_sync: Có force sync không

    Returns:
        Dict chứa kết quả sync
    """
    try:
        connection_doc = frappe.get_doc("Mira External Connection", connection_id)

        if connection_doc.connection_status != "Connected" and not force_sync:
            return {"status": "error", "message": "Connection is not active"}

        # Get accounts from platform
        accounts_data = _fetch_platform_accounts(connection_doc)

        if not accounts_data.get("success"):
            return {
                "status": "error",
                "message": accounts_data.get("message", "Failed to fetch accounts"),
            }

        accounts = accounts_data.get("accounts", [])

        # Sync accounts
        sync_result = {"created": 0, "updated": 0, "deactivated": 0}

        existing_account_ids = set()

        for account_data in accounts:
            account_id = account_data.get("external_account_id")
            if not account_id:
                continue

            existing_account_ids.add(account_id)

            # Check if account exists in child table
            existing_account = None
            for account in connection_doc.connected_accounts:
                if account.external_account_id == account_id:
                    existing_account = account
                    break

            if existing_account:
                # Update existing account in child table
                updated = False

                update_fields = [
                    "account_name",
                    "profile_picture_url",
                    "follower_count",
                    "posts_count",
                    "following_count",
                    "account_metadata",
                ]

                for field in update_fields:
                    if field in account_data:
                        new_value = account_data[field]
                        # Handle JSON fields
                        if field == "account_metadata" and isinstance(new_value, dict):
                            new_value = json.dumps(new_value)

                        if getattr(existing_account, field) != new_value:
                            setattr(existing_account, field, new_value)
                            updated = True

                if not existing_account.is_active:
                    existing_account.is_active = 1
                    existing_account.connection_status = "Active"
                    updated = True

                if updated:
                    existing_account.last_activity = now()
                    sync_result["updated"] += 1

            else:
                # Create new account in child table
                account_data_copy = account_data.copy()
                if "account_metadata" in account_data_copy and isinstance(
                    account_data_copy["account_metadata"], dict
                ):
                    account_data_copy["account_metadata"] = json.dumps(
                        account_data_copy["account_metadata"]
                    )

                # Add to child table
                connection_doc.append(
                    "connected_accounts",
                    {
                        "external_account_id": account_data_copy.get(
                            "external_account_id"
                        ),
                        "account_name": account_data_copy.get("account_name"),
                        "account_type": account_data_copy.get("account_type", "User"),
                        "is_primary": account_data_copy.get("is_primary", 0),
                        "is_active": 1,
                        "connection_status": "Active",
                        "profile_picture_url": account_data_copy.get(
                            "profile_picture_url"
                        ),
                        "follower_count": account_data_copy.get("follower_count", 0),
                        "following_count": account_data_copy.get("following_count", 0),
                        "posts_count": account_data_copy.get("posts_count", 0),
                        "account_metadata": account_data_copy.get("account_metadata"),
                        "permissions": account_data_copy.get("permissions"),
                        "scope_permissions": account_data_copy.get("scope_permissions"),
                        "last_activity": now(),
                    },
                )
                sync_result["created"] += 1

        # Deactivate accounts not returned from platform
        for account in connection_doc.connected_accounts:
            if (
                account.is_active
                and account.external_account_id not in existing_account_ids
            ):
                account.is_active = 0
                account.connection_status = "Deactivated"
                sync_result["deactivated"] += 1

        # Update connection
        connection_doc.last_sync_time = now()
        connection_doc.next_sync_time = _calculate_next_sync_time(
            connection_doc.sync_frequency
        )
        connection_doc.updated_at = now()
        connection_doc.save()

        # Log the sync
        _create_connection_log(
            connection_id,
            "Sync",
            "accounts_synced",
            connection_doc.platform_type,
            status="Success",
            custom_data=json.dumps(sync_result),
            notes=f"Synced {len(accounts)} accounts from platform",
        )

        return {
            "status": "success",
            "message": "Accounts synced successfully",
            "sync_result": sync_result,
            "total_accounts": len(accounts),
        }

    except Exception as e:
        frappe.log_error(frappe.get_traceback(), "Sync Accounts Error")
        return {"status": "error", "message": str(e)}


@frappe.whitelist()
def retry_connection(connection_id):
    """Retry a pending or failed connection"""
    try:
        connection_doc = frappe.get_doc("Mira External Connection", connection_id)
        if connection_doc.connection_status not in ["Pending", "Failed"]:
            return {
                "status": "error",
                "message": f"Cannot retry connection with status: {connection_doc.connection_status}",
            }
        # Move back to Pending until webhook confirms
        connection_doc.connection_status = "Pending"
        connection_doc.error_message = None
        connection_doc.last_sync = None
        connection_doc.save()

        login_url = _get_platform_login_url(
            connection_doc.platform_type, connection_doc
        )

        if login_url:
            return {
                "status": "success",
                "message": "Connection retry initiated successfully",
                "data": {
                    "login_url": login_url,
                    "connection_id": connection_doc.name,
                    "platform_type": connection_doc.platform_type,
                },
            }
        else:
            return {
                "status": "success",
                "message": f"Retry initiated for {connection_doc.platform_type}",
                "data": {
                    "connection_id": connection_doc.name,
                    "platform_type": connection_doc.platform_type,
                },
            }

    except frappe.DoesNotExistError:
        return {"status": "error", "message": "Connection not found"}
    except Exception as e:
        frappe.log_error(f"Error retrying connection {connection_id}: {str(e)}")
        return {"status": "error", "message": f"Failed to retry connection: {str(e)}"}


# Job Sharing Functions


@frappe.whitelist()
def share_job_posting(
    connection_id: str,
    campaign_id: str,
    ladipage_url:str,
    image_url:str,
    message: str,
    schedule_type: str = "now",
    scheduled_time: str = None,
    
    **kwargs,
) -> Dict[str, Any]:
    """
    Share job posting to external platform
    """
    try:
        # Validate connection
        connection = frappe.get_doc("Mira External Connection", connection_id)
        if connection.connection_status != "Connected":
            return {"status": "error", "message": "Connection is not active"}

        # Get job details
        # if not frappe.db.exists("Mira Job Opening", job_id):
        #     return {"status": "error", "message": "Job not found"}
        if message:
            message = convert_html_for_facebook(message)
        # job = frappe.get_doc("Mira Job Opening", job_id)
        share_data = json.dumps(kwargs)
        # Create sharing record
        share_doc = frappe.get_doc(
            {
                "doctype": "Mira Job Share Log",
                "campaign": campaign_id,
                "connection": connection_id,
                "platform_type": connection.platform_type,
                "message": message,
                "ladipage_url":ladipage_url,                
                "image_url":image_url,
                "schedule_type": schedule_type,
                "scheduled_time": (
                    get_datetime(scheduled_time) if scheduled_time else None
                ),
                "status": "Pending" if schedule_type == "later" else "Processing",
                "share_data": share_data,
                "retry_count": 0,
                "created_by": frappe.session.user,
            }
        )

        share_doc.insert(ignore_permissions=True)

        if schedule_type == "now":
            # Process immediately
            result = _process_job_share(share_doc)
            return {
                "status": "success" if result.get("success") else "error",
                "message": result.get(
                    "message",
                    (
                        "Job shared successfully"
                        if result.get("success")
                        else "Failed to share job"
                    ),
                ),
                "share_id": share_doc.name,
                "external_url": result.get("post_url"),
                "external_post_id": result.get("post_id"),
            }
        else:
            # Schedule for later
            frappe.enqueue(
                _process_scheduled_share,
                queue="short",
                timeout=12000,
                share_id=share_doc.name,
                eta=get_datetime(scheduled_time),
            )
            return {
                "status": "success",
                "share_id": share_doc.name,
                "message": "Job share scheduled successfully",
            }

    except Exception as e:
        frappe.log_error(f"Error sharing job: {str(e)}")
        return {"status": "error", "message": f"Failed to share job posting: {str(e)}"}


@frappe.whitelist()
def get_job_sharing_history(
    job_id: str, connection_id: str = None, platform_type: str = None
) -> List[Dict]:
    """
    Get sharing history for a specific job
    """
    try:
        filters = {"job": job_id}

        if connection_id:
            filters["connection"] = connection_id
        if platform_type and platform_type.strip():
            filters["platform_type"] = platform_type

        shares = frappe.get_list(
            "Mira Job Share Log",
            filters=filters,
            fields=[
                "name",
                "connection",
                "platform_type",
                "message",
                "status",
                "shared_at",
                "scheduled_time",
                "external_post_id",
                "external_url",
                "ladipage_url",
                "error_message",
                "retry_count",
                "engagement_data",
                "target_page_name",
                "modified",
                "created_by",
                "job_title",
            ],
            order_by="modified desc",
        )

        # Format engagement data
        for share in shares:
            if share.engagement_data:
                try:
                    share["engagement"] = json.loads(share.engagement_data)
                except (json.JSONDecodeError, TypeError):
                    share["engagement"] = {}
            else:
                share["engagement"] = {}

        return shares

    except Exception as e:
        frappe.log_error(f"Error getting sharing history: {str(e)}")
        return []


@frappe.whitelist()
def retry_share(share_id: str) -> Dict[str, Any]:
    """
    Retry a failed share
    """
    try:
        share_doc = frappe.get_doc("Mira Job Share Log", share_id)

        if share_doc.status not in ["Failed", "Error"]:
            return {"status": "error", "message": "Only failed shares can be retried"}

        # Reset status and increment retry count
        share_doc.status = "Processing"
        share_doc.retry_count = (share_doc.retry_count or 0) + 1
        share_doc.error_message = ""
        share_doc.save(ignore_permissions=True)

        # Process the share
        result = _process_job_share(share_doc)
        return {
            "status": "success" if result.get("success") else "error",
            "message": result.get(
                "message",
                (
                    "Share retried successfully"
                    if result.get("success")
                    else "Retry failed"
                ),
            ),
        }

    except Exception as e:
        frappe.log_error(f"Error retrying share: {str(e)}")
        return {"status": "error", "message": f"Failed to retry share: {str(e)}"}


# Helper Functions


def _get_platform_login_url(platform_type: str, connection_doc) -> Optional[str]:
    """Generate platform-specific login URL"""
    try:
        if platform_type == "Facebook":
            return _get_facebook_login_url(connection_doc)
        elif platform_type == "Zalo":
            return _get_zalo_login_url(connection_doc)
        elif platform_type == "TopCV":
            return _get_topcv_login_url(connection_doc)
        return None
    except Exception as e:
        frappe.log_error(f"Error getting login URL for {platform_type}: {str(e)}")
        return None


def _get_facebook_login_url(connection_doc) -> str:
    """Get Facebook login URL"""

    params = {
        "tenant_name": connection_doc.tenant_name,
        "user_email": connection_doc.user_email,
        "full_name": connection_doc.full_name,
        "hook_url": connection_doc.hook_url,
        "redirect_url": connection_doc.redirect_url,
    }

    try:
        response = requests.get(
            f"{host}/api/method/mbw_socialhub.api.facebook.get_facebook_login_url",
            params=params,
            timeout=1200,
        )

        if response.status_code == 200:
            data = response.json()
            print("_get_facebook_login_url>>>>>>>>>>>>>>>>>>>>>:",data)
            return data.get("message", {}).get("login_url")
    except requests.RequestException as e:
        frappe.log_error(f"Facebook login URL request failed: {str(e)}")

    return None


def _get_zalo_login_url(connection_doc) -> str:
    """Get Zalo login URL"""

    params = {
        "tenant_name": connection_doc.tenant_name,
        "user_email": connection_doc.user_email,
        "full_name": connection_doc.full_name,
        "hook_url": connection_doc.hook_url,
        "redirect_url": connection_doc.redirect_url,
    }

    try:
        response = requests.get(
            f"{host}/api/method/mbw_socialhub.api.zalo.get_zalo_login_url",
            params=params,
            timeout=1200,
        )

        if response.status_code == 200:
            data = response.json()
            return data.get("message", {}).get("login_url")
    except requests.RequestException as e:
        frappe.log_error(f"Zalo login URL request failed: {str(e)}")

    return None


def _fetch_platform_accounts(connection_doc) -> Dict[str, Any]:
    """Fetch accounts from platform"""

    try:
        if connection_doc.platform_type == "Facebook":
            return _fetch_facebook_accounts(connection_doc)
        elif connection_doc.platform_type == "Zalo":
            return _fetch_zalo_accounts(connection_doc)
        elif connection_doc.platform_type == "TopCV":
            return _fetch_topcv_accounts(connection_doc)
        return {"success": False, "message": "Unsupported platform"}
    except Exception as e:
        return {"success": False, "message": str(e)}


def _fetch_facebook_accounts(connection_doc) -> Dict[str, Any]:
    """Fetch Facebook pages and user account"""

    params = {
        "tenant_name": connection_doc.tenant_name,
        "email": connection_doc.user_email,
    }

    try:
        response = requests.get(
            f"{host}/api/method/mbw_socialhub.api.facebook.get_page_list",
            params=params,
            timeout=1200,
        )
        
        print("response>>>>>>>>>>>>>>>>>>:",response)

        if response.status_code == 200:
            data = response.json()
            pages = data.get("message", [])

            accounts = []
            
            # Add pages to accounts
            for page in pages:
                accounts.append(
                    {
                        "external_account_id": page.get("external_page_id"),
                        "account_name": page.get("page_name"),
                        "account_type": "Page",
                        "account_metadata": page.get("metadata", {}),
                        "follower_count": page.get("follower_count", 0),
                        "posts_count": page.get("posts_count", 0),
                    }
                )

            # If no pages, try to get user account info
            if not pages:
                try:
                    user_response = requests.get(
                        f"{host}/api/method/mbw_socialhub.api.facebook.get_user_account_by_email",
                        params=params,
                        timeout=1200,
                    )
                    
                    if user_response.status_code == 200:
                        user_data = user_response.json()
                        user_info = user_data.get("message", {})
                        
                        if user_info:
                            # Get profile picture URL
                            picture_url = ""
                            if user_info.get("picture") and isinstance(user_info.get("picture"), dict):
                                picture_data = user_info.get("picture", {}).get("data", {})
                                picture_url = picture_data.get("url", "")
                            
                            accounts.append(
                                {
                                    "external_account_id": user_info.get("email", connection_doc.user_email),
                                    "account_name": user_info.get("name", "Facebook User"),
                                    "account_type": "User",
                                    "account_metadata": {
                                        "email": user_info.get("email", ""),
                                        "picture": picture_url
                                    },
                                    "profile_picture_url": picture_url,
                                    "is_primary": True,
                                    "is_active": True,
                                    "follower_count": 0,
                                    "posts_count": 0,
                                }
                            )
                except requests.RequestException as e:
                    frappe.log_error(f"Facebook user account fetch failed: {str(e)}")

            return {"success": True, "accounts": accounts}
    except requests.RequestException as e:
        frappe.log_error(f"Facebook accounts fetch failed: {str(e)}")

    return {"success": False, "message": "Failed to fetch Facebook accounts"}


def _fetch_zalo_accounts(connection_doc) -> Dict[str, Any]:
    """Fetch Zalo OA info"""

    params = {
        "tenant_name": connection_doc.tenant_name,
        "user_email": connection_doc.user_email,
    }

    try:
        response = requests.get(
            f"{host}/api/method/mbw_socialhub.api.zalo.get_oa_info",
            params=params,
            timeout=1200,
        )

        if response.status_code == 200:
            data = response.json()
            oa_info = json.loads(data.get("message", {}))
            print("oa_info", oa_info)
            if oa_info.get("oa_id"):
                accounts = [
                    {
                        "external_account_id": oa_info.get("oa_id"),
                        "account_name": oa_info.get("name"),
                        "account_type": "OA",
                        "profile_picture_url": oa_info.get("avatar"),
                        "account_metadata": {"description": oa_info.get("description")},
                    }
                ]

                return {"success": True, "accounts": accounts}
    except requests.RequestException as e:
        frappe.log_error(f"Zalo accounts fetch failed: {str(e)}")

    return {"success": False, "message": "Failed to fetch Zalo OA info"}


def _platform_disconnect(connection_doc):
    """Handle platform-specific disconnect logic"""
    try:
        if connection_doc.platform_type == "Facebook":
            _disconnect_facebook(connection_doc)
        elif connection_doc.platform_type == "Zalo":
            _disconnect_zalo(connection_doc)
        elif connection_doc.platform_type == "TopCV":
            _disconnect_topcv(connection_doc)
    except Exception as e:
        frappe.log_error(f"Platform disconnect error: {str(e)}")


def _disconnect_facebook(connection_doc):
    """Disconnect Facebook connection"""

    params = {
        "tenant_name": connection_doc.tenant_name,
        "user_email": connection_doc.user_email,
    }

    try:
        requests.get(
            f"{host}/api/method/mbw_socialhub.api.facebook.disconnected_account",
            params=params,
            timeout=1200,
        )
    except requests.RequestException as e:
        frappe.log_error(f"Facebook disconnect request failed: {str(e)}")


def _disconnect_zalo(connection_doc):
    """Disconnect Facebook connection"""

    params = {
        "tenant_name": connection_doc.tenant_name,
        "user_email": connection_doc.user_email,
    }

    try:
        requests.get(
            f"{host}/api/method/mbw_socialhub.api.zalo.disconnected_account",
            params=params,
            timeout=1200,
        )
    except requests.RequestException as e:
        frappe.log_error(f"Facebook disconnect request failed: {str(e)}")


def _calculate_next_sync_time(sync_frequency: str) -> str:
    """Calculate next sync time based on frequency"""
    frequency_map = {
        "Real-time": 0,
        "Every 5 minutes": 5,
        "Every 15 minutes": 15,
        "Every 30 minutes": 30,
        "Hourly": 60,
        "Daily": 1440,
    }

    minutes = frequency_map.get(sync_frequency, 15)
    if minutes == 0:
        return now()

    return add_days(now(), minutes / (24 * 60))


def _create_connection_log(
    connection_id: str,
    log_type: str,
    event_type: str,
    platform_name: str,
    status: str = "Success",
    **kwargs,
):
    """Create connection log entry"""
    try:
        # Check if Connection Log doctype exists
        if not frappe.db.exists("DocType", "Connection Log"):
            # Skip logging if doctype doesn't exist
            return

        # log_doc = frappe.get_doc({
        #     "doctype": "Connection Log",
        #     "external_connection": connection_id,
        #     "log_type": log_type,
        #     "event_type": event_type,
        #     "platform_name": platform_name,
        #     "status": status,
        #     "timestamp": now(),
        #     "created_by_system": 1,
        #     "created_at": now(),
        #     **kwargs
        # })
        # log_doc.insert()
    except Exception as e:
        frappe.log_error(f"Failed to create connection log: {str(e)}")


def _process_job_share(share_doc):
    """
    Internal function to process job sharing
    """
    try:
        connection = frappe.get_doc("Mira External Connection", share_doc.connection)
        # job = frappe.get_doc("Mira Job Opening", share_doc.job)

        # Parse share_data safely
        share_data = {}
        if share_doc.share_data:
            try:
                share_data = json.loads(share_doc.share_data)
            except (json.JSONDecodeError, TypeError):
                share_data = {}

        # Process based on platform type
        if connection.platform_type.lower() == "facebook":

            result = _share_to_facebook(connection, share_doc, share_data)

        elif connection.platform_type.lower() == "zalo":
            result = _share_to_zalo(connection, share_doc, share_data)
        elif connection.platform_type.lower() == "topcv":
            result = _share_to_topcv(connection, share_doc, share_data)
        else:
            result = {
                "success": False,
                "error": f"Unsupported platform type: {connection.platform_type}",
            }

        
        
        # Update share record with results
        share_doc.status = "Success" if result.get("success") else "Failed"
        share_doc.shared_at = now_datetime() if result.get("success") else None
        share_doc.external_post_id = result.get("post_id")
        share_doc.external_url = result.get("post_url")
        share_doc.target_page_name = result.get("target_page_name")

        if not result.get("success"):
            share_doc.error_message = result.get("error", "Unknown error")

        # Store response data
        if result.get("response_data"):
            share_doc.response_data = json.dumps(result.get("response_data"))

        share_doc.save(ignore_permissions=True)

        #Update social
        if share_data and hasattr(share_data,"social_id"):
            social = frappe.get_doc("Mira Campaign Social",share_data.social_id)
            social.status = share_doc.status
            social.response_data = share_doc.response_data
            social.error_message = share_doc.error_message
            social.share_at = share_doc.shared_at
            social.executed_at = now_datetime()
            social.save(ignore_permissions=True)

        # Update connection statistics
        _update_connection_stats(connection, result.get("success", False))

        return result

    except Exception as e:
        # Update share record with error
        share_doc.status = "Failed"
        share_doc.error_message = str(e)
        share_doc.save(ignore_permissions=True)

        frappe.log_error(f"Error processing job share: {str(e)}")
        return {"success": False, "error": str(e)}

from frappe.utils import get_url

def _get_base_url():
    # Nếu đang trong HTTP request → dùng request data
    if getattr(frappe, "request", None):
        try:
            origin = frappe.request.headers.get("Origin")
            if origin:
                return origin

            protocol = frappe.request.scheme
            host = frappe.request.host
            if protocol and host:
                return f"{protocol}://{host}"
        except Exception:
            pass

    # Nếu đang trong background job hoặc không có request → fallback an toàn
    return get_url()

def _create_tracking(campaign_id, source,social_id) -> str:
    # Lấy domain chính xác
    
    campaign = frappe.get_doc("Mira Campaign",campaign_id)
    params = {
        "campaign_id": campaign.name if hasattr(campaign, "name") else campaign,
        "talent_id": "",
        "action": social_id,
        "url": campaign.ladipage_url,
        "utm_campaign": campaign.name,
        "utm_source": source,
        "utm_medium": "social"
    }

    sig = make_signature(params)
    query = urlencode({**params, "sig": sig})

    return f"{_get_base_url()}/api/method/mbw_mira.api.interaction.page_visited?{query}"

def replace_urls_with_tracking(content, campaign_id, source,social_id):
    """
    Thay tất cả URL trong content bằng redirect URL:
    - Gói URL gốc vào param `url`
    - Thêm param `url_tracking` với tracking link
    - Không append 2 lần
    """
    url_regex = r"(https?://[^\s\"\'<>]+)"

    # Lấy tracking URL
    tracking_url = _create_tracking(campaign_id, source,social_id)
    encoded_tracking = quote(tracking_url, safe="")

    # URL redirect
    redirect_base = f"{_get_base_url()}/api/method/mbw_mira.api.interaction.click_redirect?url="

    def replace(match):
        original_url = match.group(0)

        # Nếu đã có param url_tracking rồi → bỏ qua
        if "url_tracking=" in original_url:
            return original_url

        # Encode URL gốc để làm param
        encoded_original = quote(original_url, safe="")

        # Trả về URL redirect đầy đủ
        return f"{redirect_base}{encoded_original}&url_tracking={encoded_tracking}"

    return re.sub(url_regex, replace, content)

def _share_to_facebook(connection, share_doc, share_data):
    """Share job to Facebook via SocialHub API"""
    try:
        # Get Facebook page ID from share_data or connection accounts
        page_id = share_data.get("target_page_id")
        
        url_image = share_doc.get("image_url")
        if url_image and "http" not in url_image:
            url_image = f"{get_url_without_port()}{url_image}"
        if not page_id:
            # Get first active Facebook page from child table
            facebook_account = None
            connection_obj = frappe.get_doc("Mira External Connection", connection.name)
            for account in connection_obj.connected_accounts:
                if account.is_active and account.account_type == "Page":
                    facebook_account = account.external_account_id
                    break
            page_id = facebook_account

        if not page_id:
            return {"success": False, "error": "No Facebook page selected or available"}

        # Prepare post content
        social_id = None
        if hasattr(share_data,"social_id") and share_data.social_id:
            social_id = share_data.social_id
        message = replace_urls_with_tracking(share_doc.message,share_doc.campaign,"facebook",social_id)
        # Prepare image URL if available

        # SocialHub API call

        socialhub_url = f"{host}/api/method/mbw_socialhub.api.facebook.publish_post"
        post_data = {
            "page_id": page_id,
            "tenant_name": connection.tenant_name,
            "email": connection.user_email,
            "message": message,
            "url_image": url_image,
        }

        response = requests.post(socialhub_url, json=post_data, timeout=12000)
        response_data = response.json()
        print("page_id", response_data)
        if (
            response.status_code == 200
            and response_data.get("message", {}).get("status") == "success"
        ):
            post_id = response_data.get("message", {}).get("post_id")

            # Get permalink URL
            try:
                permalink_response = requests.get(
                    f"{host}/api/method/mbw_socialhub.api.facebook.get_permalink_post",
                    params={"page_id": page_id, "post_id": post_id},
                    timeout=1200,
                )

                post_url = ""
                if permalink_response.status_code == 200:
                    permalink_data = permalink_response.json()
                    if permalink_data.get("message", {}).get("status") == "success":
                        post_url = (
                            permalink_data.get("message", {})
                            .get("data", {})
                            .get("permalink_url", "")
                        )
            except Exception:
                post_url = ""

            return {
                "success": True,
                "post_id": post_id,
                "post_url": post_url,
                "target_page_name": share_data.get("target_page_name", "Facebook Page"),
                "response_data": response_data,
            }
        else:
            error_msg = response_data.get("message", {}).get(
                "message", f"Facebook API error: HTTP {response.status_code}"
            )
            return {
                "success": False,
                "error": error_msg,
                "response_data": response_data,
            }

    except requests.RequestException as e:
        return {"success": False, "error": f"Request failed: {str(e)}"}
    except Exception as e:
        return {"success": False, "error": str(e)}


def _share_to_zalo(connection, share_doc, share_data):
    """Share job to Zalo OA via SocialHub API"""
    try:

        # Get Zalo OA ID
        page_id = share_data.get("oa_id")
        url_image = share_doc.get("image_url")
        if url_image and "http" not in url_image:
            url_image = f"{get_url_without_port()}{url_image}"
        if not page_id:
            # Get OA ID from connection child table
            connection_obj = frappe.get_doc("Mira External Connection", connection.name)
            for account in connection_obj.connected_accounts:
                if account.is_active and account.account_type == "OA":
                    page_id = account.external_account_id
                    break

        if not page_id:
            return {"success": False, "error": "No Zalo OA ID configured or available"}

        social_id = None
        if hasattr(share_data,"social_id") and share_data.social_id:
            social_id = share_data.social_id

        # Prepare image URL if available
        # photo_url = ""
        # if hasattr(job, 'image') and job.image:
        #     photo_url = f"{get_url_without_port()}{job.image}"

        # SocialHub API call for Zalo

        socialhub_url = f"{host}/api/method/mbw_socialhub.api.zalo.publish_post"

        # Truncate description for Zalo
        description = share_doc.message
        if len(description) > 200:
            description = description[:200] + "..."

        post_data = {
            "page_id": page_id,
            "tenant_name": connection.tenant_name,
            "email": connection.user_email,
            "title": "",
            "photo_url": url_image,
            "description": description,
            "content": f"{share_doc.message}",
        }

        post_data.content = replace_urls_with_tracking(post_data.content,share_doc.campaign,"zalo",social_id) or ''
        
        response = requests.post(socialhub_url, json=post_data, timeout=1000)

        if response.status_code == 200:
            response_data = response.json()
            post_id = response_data.get("message")

            if post_id:
                return {
                    "success": True,
                    "post_id": str(post_id),
                    "target_page_name": "Zalo OA",
                    "response_data": response_data,
                }
            else:
                return {
                    "success": False,
                    "error": "No post ID returned from Zalo API",
                    "response_data": response_data,
                }
        else:
            try:
                error_data = response.json()
                error_msg = error_data.get(
                    "message", f"Zalo API error: HTTP {response.status_code}"
                )
            except Exception as e:
                error_msg = f"Zalo API error: HTTP {response.status_code} {str(e)}"

            return {"success": False, "error": error_msg}

    except requests.RequestException as e:
        return {"success": False, "error": f"Request failed: {str(e)}"}
    except Exception as e:
        return {"success": False, "error": str(e)}


def _update_connection_stats(connection, success: bool):
    """Update connection statistics"""
    try:
        connection.total_api_calls = (connection.total_api_calls or 0) + 1

        if success:
            connection.successful_calls = (connection.successful_calls or 0) + 1
        else:
            connection.failed_calls = (connection.failed_calls or 0) + 1

        # Calculate success rate
        if connection.total_api_calls > 0:
            connection.success_rate = (
                connection.successful_calls / connection.total_api_calls
            ) * 100

        connection.last_api_call = now()
        connection.last_activity = now()
        connection.updated_at = now()
        connection.save(ignore_permissions=True)

    except Exception as e:
        frappe.log_error(f"Failed to update connection stats: {str(e)}")


def _process_scheduled_share(share_id):
    """Process scheduled share (called by background job)"""
    try:
        share_doc = frappe.get_doc("Mira Job Share Log", share_id)

        if share_doc.status != "Pending":
            return {"success": False, "error": "Share is not in pending status"}

        share_doc.status = "Processing"
        share_doc.save(ignore_permissions=True)

        result = _process_job_share(share_doc)
        return result

    except Exception as e:
        frappe.log_error(f"Error processing scheduled share: {str(e)}")
        return {"success": False, "error": str(e)}


# Webhook handler
@frappe.whitelist(allow_guest=True)
def handle_webhook():
    """Handle incoming webhooks from platforms"""
    try:
        # Get request data
        if frappe.request.method != "POST":
            frappe.response["http_status_code"] = 405
            return {"status": "error", "message": "Method not allowed"}

        data = {}
        if frappe.request.data:
            try:
                data = json.loads(frappe.request.data)
            except json.JSONDecodeError:
                frappe.response["http_status_code"] = 400
                return {"status": "error", "message": "Invalid JSON data"}

        user_email = data.get("user_email")
        platform_name = data.get("platform_name")
        event_type = data.get("event_type")

        if not all([user_email, platform_name, event_type]):
            frappe.response["http_status_code"] = 400
            return {"status": "error", "message": "Missing required fields"}

        # Find connection
        connection = frappe.db.get_value(
            "Mira External Connection",
            {
                "user_email": user_email,
                "platform_type": platform_name,
                "active_status": 1,
            },
            "name",
        )

        if not connection:
            frappe.response["http_status_code"] = 404
            return {"status": "error", "message": "Connection not found"}

        # Process webhook based on event type
        if event_type == "login_success":
            _handle_login_success(connection, data)
        elif event_type == "login_failed":
            _handle_login_failed(connection, data)
        elif event_type == "token_refresh":
            _handle_token_refresh(connection, data)

        # Update webhook statistics
        frappe.db.set_value(
            "Mira External Connection",
            connection,
            {
                "total_webhooks": frappe.db.get_value(
                    "Mira External Connection", connection, "total_webhooks"
                )
                + 1,
                "last_webhook_received": now(),
                "last_activity": now(),
            },
        )

        # Log webhook
        _create_connection_log(
            connection,
            "Webhook",
            event_type,
            platform_name,
            status="Success",
            webhook_event_type=event_type,
            webhook_payload=json.dumps(data),
            webhook_source_ip=frappe.local.request_ip or "",
            webhook_user_agent=frappe.get_request_header("User-Agent") or "",
        )

        return {"status": "success", "message": "Webhook processed"}

    except Exception as e:
        frappe.log_error(frappe.get_traceback(), "Webhook Handler Error")
        frappe.response["http_status_code"] = 500
        return {"status": "error", "message": "Internal server error"}


def _handle_login_success(connection_id: str, data: Dict):
    """Handle successful login webhook"""
    try:
        update_data = {
            "connection_status": "Connected",
            "last_connected_at": now(),
            "last_activity": now(),
            "retry_count": 0,
            "updated_at": now(),
        }

        # Update token information if provided
        if data.get("access_token"):
            update_data["access_token"] = data.get("access_token")
        if data.get("refresh_token"):
            update_data["refresh_token"] = data.get("refresh_token")
        if data.get("token_expiry"):
            update_data["token_expiry"] = data.get("token_expiry")

        frappe.db.set_value("Mira External Connection", connection_id, update_data)

        # Trigger account sync
        frappe.enqueue(
            sync_accounts,
            queue="short",
            timeout=120,
            connection_id=connection_id,
            force_sync=True,
        )

    except Exception as e:
        frappe.log_error(f"Error handling login success: {str(e)}")


def _handle_login_failed(connection_id: str, data: Dict):
    """Handle failed login webhook"""
    try:
        connection_doc = frappe.get_doc("Mira External Connection", connection_id)

        connection_doc.connection_status = "Failed"
        connection_doc.retry_count = (connection_doc.retry_count or 0) + 1

        # Add error message to notes
        error_msg = data.get("error_message", "Login failed")
        current_notes = connection_doc.connection_notes or ""
        connection_doc.connection_notes = (
            f"{current_notes}\nLogin failed: {error_msg}".strip()
        )

        if connection_doc.retry_count >= connection_doc.max_retries:
            connection_doc.active_status = 0

        connection_doc.updated_at = now()
        connection_doc.save()

    except Exception as e:
        frappe.log_error(f"Error handling login failure: {str(e)}")


def _handle_token_refresh(connection_id: str, data: Dict):
    """Handle token refresh webhook"""
    try:
        update_data = {"last_activity": now(), "updated_at": now()}

        if data.get("access_token"):
            update_data["access_token"] = data.get("access_token")
        if data.get("refresh_token"):
            update_data["refresh_token"] = data.get("refresh_token")
        if data.get("token_expiry"):
            update_data["token_expiry"] = data.get("token_expiry")

        frappe.db.set_value("Mira External Connection", connection_id, update_data)

    except Exception as e:
        frappe.log_error(f"Error handling token refresh: {str(e)}")


# Additional utility functions


@frappe.whitelist()
def get_platform_statistics(platform_type: str = None) -> Dict[str, Any]:
    """Get platform connection statistics"""
    try:
        filters = {}
        if platform_type and platform_type.strip():
            filters["platform_type"] = platform_type

        connections = frappe.get_all(
            "Mira External Connection",
            filters=filters,
            fields=["platform_type", "connection_status", "active_status"],
        )

        stats = {}
        for conn in connections:
            platform = conn.platform_type
            if platform not in stats:
                stats[platform] = {
                    "total": 0,
                    "active": 0,
                    "connected": 0,
                    "failed": 0,
                    "pending": 0,
                }

            stats[platform]["total"] += 1

            if conn.active_status:
                stats[platform]["active"] += 1

            if conn.connection_status == "Connected":
                stats[platform]["connected"] += 1
            elif conn.connection_status == "Failed":
                stats[platform]["failed"] += 1
            elif conn.connection_status == "Pending":
                stats[platform]["pending"] += 1

        return {"status": "success", "data": stats}

    except Exception as e:
        frappe.log_error(f"Error getting platform statistics: {str(e)}")
        return {"status": "error", "message": str(e)}


@frappe.whitelist()
def test_connection(connection_id: str) -> Dict[str, Any]:
    """Test a connection by making a simple API call"""
    try:
        connection_doc = frappe.get_doc("Mira External Connection", connection_id)

        if connection_doc.platform_type == "Facebook":
            result = _test_facebook_connection(connection_doc)
        elif connection_doc.platform_type == "Zalo":
            result = _test_zalo_connection(connection_doc)
        elif connection_doc.platform_type == "TopCV":
            result = _test_topcv_connection(connection_doc)
        else:
            result = {"success": False, "message": "Platform not supported for testing"}

        # Update connection status based on test result
        if result.get("success"):
            connection_doc.connection_status = "Connected"
            connection_doc.last_activity = now()
        else:
            connection_doc.connection_status = "Failed"

        connection_doc.updated_at = now()
        connection_doc.save()

        return result

    except Exception as e:
        frappe.log_error(f"Error testing connection: {str(e)}")
        return {"success": False, "message": str(e)}


def _test_facebook_connection(connection_doc) -> Dict[str, Any]:
    """Test Facebook connection"""
    try:
        # Quick reachability check for SocialHub host
        try:
            requests.get(host, timeout=5)
        except Exception:
            return {
                "success": False,
                "message": f"SocialHub host unreachable: {host}. Configure frappe.conf.socialhub or check network.",
            }

        response = requests.get(
            f"{host}/api/method/mbw_socialhub.api.facebook.test_connection",
            params={
                "tenant_name": connection_doc.tenant_name,
                "user_email": connection_doc.user_email,
            },
            timeout=10,
        )

        if response.status_code == 200:
            data = response.json()
            return {
                "success": True,
                "message": "Facebook connection is working",
                "data": data.get("message", {}),
            }
        else:
            return {
                "success": False,
                "message": f"Facebook connection test failed: HTTP {response.status_code}",
            }

    except requests.RequestException as e:
        return {
            "success": False,
            "message": f"Facebook connection test error: {str(e)} | Host: {host}",
        }
    except Exception as e:
        return {
            "success": False,
            "message": f"Facebook connection test error: {str(e)}",
        }


def _test_zalo_connection(connection_doc) -> Dict[str, Any]:
    """Test Zalo connection"""
    try:
        host = "https://socialhub.mbwcloud.com"

        response = requests.get(
            f"{host}/api/method/mbw_socialhub.api.zalo.test_connection",
            params={
                "tenant_name": connection_doc.tenant_name,
                "user_email": connection_doc.user_email,
            },
            timeout=1200,
        )

        if response.status_code == 200:
            data = response.json()
            return {
                "success": True,
                "message": "Zalo connection is working",
                "data": data.get("message", {}),
            }
        else:
            return {
                "success": False,
                "message": f"Zalo connection test failed: HTTP {response.status_code}",
            }

    except Exception as e:
        return {"success": False, "message": f"Zalo connection test error: {str(e)}"}


# Cập nhật các hàm TopCV trong file external_connections.py theo API SocialHub


def _get_topcv_login_url(connection_doc) -> Optional[str]:
    """Get TopCV login URL - via SocialHub connect API.
    For API key/secret flows, there might be no login URL, so return None on success.
    """
    try:
        base = host
        hook_url = f"{get_url_without_port()}/api/method/mbw_mira.api.external_connections.handle_webhook"
        connect_url = f"{base}/api/method/mbw_socialhub.api.topcv.connect"
        response = requests.post(
            connect_url,
            json={
                "tenant_name": connection_doc.tenant_name,
                "api_key": connection_doc.api_key,
                "secret_key": connection_doc.client_secret,
                "hook_url": hook_url,
            },
            timeout=1200,
        )
        if response.status_code == 200:
            data = response.json()
            # For TopCV, successful connect does not require user login; return None
            if data.get("status") == "Success":
                return None
        return None
    except Exception as e:
        frappe.log_error(f"TopCV login URL error: {str(e)}")
        return None


def _fetch_topcv_accounts(connection_doc) -> Dict[str, Any]:
    """Fetch TopCV connection info từ SocialHub"""
    try:
        host = "https://socialhub.mbwcloud.com/"

        # Check connection status từ SocialHub
        response = requests.post(
            f"{host}/api/method/mbw_socialhub.api.topcv.check_connection",
            json={
                "tenant_name": connection_doc.tenant_name,
                "api_key": connection_doc.api_key,
                "secret_key": connection_doc.client_secret,
            },
            timeout=1200,
        )

        if response.status_code == 200:
            data = response.json()

            if data.get("status") == "Success" and data.get("connected"):
                accounts = [
                    {
                        "external_account_id": connection_doc.tenant_name,
                        "account_name": f"TopCV - {connection_doc.tenant_name}",
                        "account_type": "Business",
                        "is_primary": True,
                        "account_metadata": {
                            "last_connected_at": data.get("last_connected_at"),
                            "platform": "TopCV Job Board",
                        },
                        "permissions": "job_posting,candidate_access,campaign_management",
                    }
                ]

                return {"success": True, "accounts": accounts}
            else:
                return {"success": False, "message": "TopCV not connected"}
        else:
            return {
                "success": False,
                "message": f"SocialHub API error: {response.status_code}",
            }

    except requests.RequestException as e:
        frappe.log_error(f"TopCV accounts fetch failed: {str(e)}")
        return {"success": False, "message": f"Request failed: {str(e)}"}
    except Exception as e:
        return {"success": False, "message": str(e)}


def _share_to_topcv(connection, job, share_doc, share_data):
    """Share job to TopCV thông qua SocialHub API"""
    try:

        # Kiểm tra kết nối trước khi post job
        check_response = requests.post(
            f"{host}/api/method/mbw_socialhub.api.topcv.check_connection",
            json={"tenant_name": connection.tenant_name},
            timeout=1200,
        )

        if check_response.status_code != 200:
            return {"success": False, "error": "Failed to check TopCV connection"}

        check_data = check_response.json()
        if not (check_data.get("status") == "Success" and check_data.get("connected")):
            return {"success": False, "error": "TopCV not connected"}

        # Chuẩn bị dữ liệu job theo format TopCV
        job_data = {
            "tenant_name": connection.tenant_name,
            "title": job.jo_public_title,
            "position_title": job.jo_public_title,
            "main_category": share_data.get("main_category", 1),  # Default IT
            "skills": share_data.get("skills", [1, 2]),  # Default skills
            "locations": share_data.get("locations", [1]),  # Default Hà Nội
            "salary_level": share_data.get("salary_level", 1),
            "job_type": share_data.get("job_type", 1),  # Full-time
            "employee_level": share_data.get("employee_level", 1),
            "experience": share_data.get("experience", "1-2 năm kinh nghiệm"),
            "quantity": (
                int(job.jo_number_of_positions) if job.jo_number_of_positions else 1
            ),
            "job_requirement": job.jo_description or share_doc.message,
            "job_benefit": job.jo_benefits
            or "Lương thưởng hấp dẫn, môi trường làm việc chuyên nghiệp",
            "deadline": (
                job.jo_deadline.strftime("%Y-%m-%d")
                if job.jo_deadline
                else (datetime.now() + datetime.timedelta(days=30)).strftime("%Y-%m-%d")
            ),
            "contact_email": (
                [job.jo_contact_email] if job.jo_contact_email else ["hr@company.com"]
            ),
            "contact_phone": job.jo_contact_phone or "0123456789",
            "contact_name": job.jo_contact_person or "HR Department",
            "publish_request_days": share_data.get("publish_request_days", 30),
            "job_tag_ids": share_data.get("job_tag_ids", []),
            "gender": share_data.get("gender", "Không yêu cầu"),
            "job_description": share_doc.message,
            "recruitment_campaign_id": share_data.get("recruitment_campaign_id", 0),
            "create_recruitment_campaign": share_data.get(
                "create_recruitment_campaign", 1
            ),
            "tenant_job_id": job.name,  # ID nội bộ
        }

        # Thêm salary info nếu có
        if job.jo_min_salary:
            job_data["salary_from"] = str(int(job.jo_min_salary))
        if job.jo_max_salary:
            job_data["salary_to"] = str(int(job.jo_max_salary))
        if job.jo_currency:
            job_data["salary_currency"] = job.jo_currency

        # Call SocialHub create job API
        response = requests.post(
            f"{host}/api/method/mbw_socialhub.api.topcv.create_job",
            json=job_data,
            timeout=120,
        )

        if response.status_code == 200:
            response_data = response.json()

            if response_data.get("status") == "Success":
                job_id = response_data.get("job_id")
                topcv_url = response_data.get(
                    "job_url", f"https://www.topcv.vn/viec-lam/{job_id}"
                )

                # Tự động publish job sau khi tạo thành công
                try:
                    publish_response = requests.post(
                        f"{host}/api/method/mbw_socialhub.api.topcv.publish_job",
                        json={"tenant_name": connection.tenant_name, "job_id": job_id},
                        timeout=12000,
                    )

                    publish_success = (
                        publish_response.status_code == 200
                        and publish_response.json().get("status") == "Success"
                    )
                except:
                    publish_success = False

                return {
                    "success": True,
                    "post_id": str(job_id),
                    "post_url": topcv_url,
                    "target_page_name": "TopCV Job Board",
                    "response_data": response_data,
                    "published": publish_success,
                }
            else:
                error_msg = response_data.get("message", "Unknown error from TopCV")
                return {
                    "success": False,
                    "error": error_msg,
                    "response_data": response_data,
                }
        else:
            return {
                "success": False,
                "error": f"SocialHub API error: HTTP {response.status_code}",
            }

    except requests.RequestException as e:
        return {"success": False, "error": f"Request failed: {str(e)}"}
    except Exception as e:
        return {"success": False, "error": str(e)}


def _test_topcv_connection(connection_doc) -> Dict[str, Any]:
    """Test TopCV connection thông qua SocialHub"""
    try:

        response = requests.post(
            f"{host}/api/method/mbw_socialhub.api.topcv.check_connection",
            json={"tenant_name": connection_doc.tenant_name},
            timeout=1200,
        )

        if response.status_code == 200:
            data = response.json()
            if data.get("status") == "Success":
                return {
                    "success": True,
                    "message": "TopCV connection is working",
                    "data": {
                        "connected": data.get("connected"),
                        "last_connected_at": data.get("last_connected_at"),
                        "tenant_name": connection_doc.tenant_name,
                    },
                }
            else:
                return {
                    "success": False,
                    "message": data.get("message", "TopCV connection failed"),
                }
        else:
            return {
                "success": False,
                "message": f"SocialHub API error: HTTP {response.status_code}",
            }

    except Exception as e:
        return {"success": False, "message": f"TopCV connection test error: {str(e)}"}


def _disconnect_topcv(connection_doc):
    """Disconnect TopCV connection thông qua SocialHub"""
    try:

        response = requests.post(
            f"{host}/api/method/mbw_socialhub.api.topcv.disconnect",
            json={
                "tenant_name": connection_doc.tenant_name,
                "api_key": connection_doc.api_key,
                "secret_key": connection_doc.client_secret,
            },
            timeout=1200,
        )

        if response.status_code == 200:
            data = response.json()
            if data.get("status") == "Success":
                frappe.log_error(
                    f"TopCV disconnected successfully for {connection_doc.tenant_name}"
                )

    except Exception as e:
        frappe.log_error(f"TopCV disconnect error: {str(e)}")


# TopCV specific API endpoints


@frappe.whitelist()
def get_topcv_metadata(connection_id: str, metadata_type: str) -> Dict[str, Any]:
    """Get TopCV metadata (categories, skills, cities, etc.)"""
    try:
        connection_doc = frappe.get_doc("Mira External Connection", connection_id)

        response = requests.get(
            f"{host}/api/method/mbw_socialhub.api.topcv.get_metadata",
            params={
                "tenant_name": connection_doc.tenant_name,
                "type": metadata_type,
                "token_key": connection_doc.secret_token,
            },
            timeout=1200,
        )

        if response.status_code == 200:
            data = response.json()

            if data.get("status") == "Success":
                return {
                    "status": "success",
                    "data": data.get("items", []),
                    "type": metadata_type,
                }
            else:
                return {
                    "status": "error",
                    "message": data.get("message", "Failed to get metadata"),
                }
        else:
            return {"status": "error", "message": f"API error: {response.status_code}"}

    except Exception as e:
        frappe.log_error(f"Error getting TopCV metadata: {str(e)}")
        return {"status": "error", "message": str(e)}


@frappe.whitelist()
def connect_topcv(
    tenant_name: str,
    api_key: str,
    secret_key: str,
    hook_url: str,
    user_email: str = None,
    full_name: str = None,
) -> Dict[str, Any]:
    """Connect to TopCV thông qua SocialHub"""
    try:

        hook_url = f"{get_url_without_port()}/api/method/mbw_mira.api.external_connections.handle_webhook"
        # Call SocialHub connect API
        response = requests.post(
            f"{host}/api/method/mbw_socialhub.api.topcv.connect",
            json={
                "tenant_name": tenant_name,
                "api_key": api_key,
                "secret_key": secret_key,
                "hook_url": hook_url,
            },
            timeout=12000,
        )

        if response.status_code == 200:
            data = response.json()

            if data.get("status") == "Success":
                # Tìm hoặc tạo Mira External Connection
                connection = frappe.db.exists(
                    "Mira External Connection",
                    {
                        "platform_type": "TopCV",
                        "tenant_name": tenant_name,
                        "user_email": user_email or "",
                    },
                )

                if connection:
                    connection_doc = frappe.get_doc("Mira External Connection", connection)
                else:
                    connection_doc = frappe.get_doc(
                        {
                            "doctype": "Mira External Connection",
                            "platform_type": "TopCV",
                            "tenant_name": tenant_name,
                            "user_email": user_email or "",
                            "full_name": full_name or "",
                            "hook_url": hook_url,
                            "api_key": api_key,
                            "client_secret": secret_key,  # Store secret key
                            "active_status": 1,
                            "auto_reconnect": 1,
                            "sync_frequency": "Daily",
                            "created_by": frappe.session.user,
                        }
                    )
                    connection_doc.insert()

                # Update connection status
                connection_doc.secret_token = data.get("token_key")
                connection_doc.connection_status = "Connected"
                connection_doc.last_connected_at = now()
                connection_doc.updated_at = now()
                connection_doc.save()

                return {
                    "status": "success",
                    "message": "TopCV connected successfully",
                    "data": {
                        "connection_id": connection_doc.name,
                        "webhook_url": data.get("webhook_url"),
                        "webhook_secret": data.get("webhook_secret"),
                    },
                }
            else:
                return {
                    "status": "error",
                    "message": data.get("message", "Connection failed"),
                }
        else:
            return {
                "status": "error",
                "message": f"SocialHub API error: {response.status_code}",
            }

    except Exception as e:
        frappe.log_error(f"Error connecting TopCV: {str(e)}")
        return {"status": "error", "message": str(e)}


@frappe.whitelist()
def manage_topcv_job(
    connection_id: str,
    action: str,  # create, edit, publish, stop, detail
    job_data: Dict = None,
    job_id: str = None,
) -> Dict[str, Any]:
    """Manage TopCV jobs (create, edit, publish, stop, detail)"""
    try:
        connection_doc = frappe.get_doc("Mira External Connection", connection_id)

        # Determine API endpoint
        endpoint_map = {
            "create": "create_job",
            "edit": "edit_job",
            "publish": "publish_job",
            "stop": "stop_job",
            "detail": "detail_job",
        }

        if action not in endpoint_map:
            return {"status": "error", "message": f"Invalid action: {action}"}

        endpoint = f"{host}/api/method/mbw_socialhub.api.topcv.{endpoint_map[action]}"

        # Prepare request data
        request_data = {"tenant_name": connection_doc.tenant_name}

        if action in ["create", "edit"] and job_data:
            request_data.update(job_data)
        elif action in ["publish", "stop", "detail"] and job_id:
            request_data["job_id"] = int(job_id)
        else:
            return {
                "status": "error",
                "message": f"Missing required data for action: {action}",
            }

        # Call SocialHub API
        response = requests.post(endpoint, json=request_data, timeout=120)

        if response.status_code == 200:
            data = response.json()

            if data.get("status") == "Success":
                return {
                    "status": "success",
                    "message": f"Job {action} successful",
                    "data": data,
                }
            else:
                return {
                    "status": "error",
                    "message": data.get("message", f"Job {action} failed"),
                }
        else:
            return {"status": "error", "message": f"API error: {response.status_code}"}

    except Exception as e:
        frappe.log_error(f"Error managing TopCV job: {str(e)}")
        return {"status": "error", "message": str(e)}


# Update main functions để include TopCV với SocialHub pattern

# Trong hàm _get_platform_login_url, thêm:
# elif platform_type == "TopCV":
#     return _get_topcv_login_url(connection_doc)

# Trong hàm _fetch_platform_accounts, thêm:
# elif connection_doc.platform_type == "TopCV":
#     return _fetch_topcv_accounts(connection_doc)

# Trong hàm _process_job_share, thêm:
# elif connection.platform_type.lower() == "topcv":
#     result = _share_to_topcv(connection, job, share_doc, share_data)

# Trong hàm _platform_disconnect, thêm:
# elif connection_doc.platform_type == "TopCV":
#     _disconnect_topcv(connection_doc)

# Trong hàm test_connection, thêm:
# elif connection_doc.platform_type == "TopCV":
#     result = _test_topcv_connection(connection_doc)


@frappe.whitelist()
def cancel_scheduled_share(share_id: str) -> Dict[str, Any]:
    """Cancel a scheduled share that hasn't been processed yet"""
    try:
        share_doc = frappe.get_doc("Mira Job Share Log", share_id)
        if share_doc.status != "Pending" or not share_doc.scheduled_time:
            return {"status": "error", "message": "Only scheduled pending shares can be canceled"}
        share_doc.status = "Canceled"
        share_doc.save(ignore_permissions=True)
        return {"status": "success", "message": "Scheduled share canceled"}
    except frappe.DoesNotExistError:
        return {"status": "error", "message": "Share not found"}
    except Exception as e:
        frappe.log_error(f"Error canceling scheduled share: {str(e)}")
        return {"status": "error", "message": str(e)}


@frappe.whitelist()
def fix_connection_tenant_names(dry_run: int = 1) -> Dict[str, Any]:
    """Maintenance helper to fix tenant_name for existing connections.
    If previously set to a wrong base (e.g., socialhub), replace with current public base.
    dry_run=1 will only report; set to 0 to apply.
    """
    new_base = get_url_without_port()
    bad_prefixes = ["https://socialhub.mbwcloud.com"]
    updated = []
    to_fix = frappe.get_all(
        "Mira External Connection",
        filters={"active_status": 1},
        fields=["name", "tenant_name"],
    )
    for row in to_fix:
        if any(str(row.tenant_name or "").startswith(p) for p in bad_prefixes):
            if not dry_run:
                frappe.db.set_value("Mira External Connection", row.name, "tenant_name", new_base)
            updated.append({"name": row.name, "old": row.tenant_name, "new": new_base})
    return {"status": "success", "dry_run": int(dry_run), "updated": updated}


@frappe.whitelist()
def get_connected_data_sources(platform_type: str = None):
    """Return connected Mira External Connection records as data sources for wizard.
    Optional: filter by platform_type (e.g., 'Facebook', 'Zalo', 'TopCV').
    Output fields:
      - name: Mira External Connection name
      - source_name: human name for display
      - source_title: optional subtitle
      - description: optional
      - source_type: one of ['SocialNetwork', 'JobBoard', 'ATS'] mapped from platform_type
      - platform_type: original platform type
    """
    try:
        filters = {"connection_status": "Connected", "active_status": 1}
        if platform_type:
            filters["platform_type"] = platform_type

        connections = frappe.get_all(
            "Mira External Connection",
            filters=filters,
            fields=[
                "name",
                "platform_type",
                "tenant_name",
                "user_email",
                "full_name",
                "primary_account_id",
                "last_connected_at",
                "hook_url",
                "redirect_url",
            ],
            order_by="modified desc",
        )

        def map_source_type(pt: str) -> str:
            if not pt:
                return "DataSource"
            pt_l = pt.lower()
            if pt_l in ["facebook", "zalo", "instagram", "linkedin", "twitter"]:
                return "SocialNetwork"
            if pt_l in ["topcv", "jobboard", "indeed"]:
                return "JobBoard"
            if pt_l in ["ats", "greenhouse", "lever"]:
                return "ATS"
            return "DataSource"

        items = []
        for c in connections:
            items.append(
                {
                    "name": c.name,
                    "platform_type": c.platform_type,
                    "source_name": f"{c.platform_type} - {c.user_email or c.full_name or c.tenant_name}",
                    "source_title": c.tenant_name,
                    "description": _("Connected via SocialHub"),
                    "source_type": map_source_type(c.platform_type),
                }
            )

        return {"status": "success", "data": items}
    except Exception as e:
        frappe.log_error(frappe.get_traceback(), "Get Connected Data Sources Error")
        return {"status": "error", "message": str(e)}
