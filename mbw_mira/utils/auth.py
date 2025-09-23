import frappe,random,hmac,time,hashlib,json
from functools import wraps
import json
import uuid
from frappe import _
from frappe.utils import now_datetime, nowdate, cint

def secure_api():
    def decorator(func):
        @frappe.whitelist(allow_guest=True)
        @wraps(func)
        def wrapper(*args, **kwargs):
            headers = frappe._dict({k.lower(): v for k, v in frappe.request.headers.items()})
            max_age_seconds=300  # 5 phút
            # 1. Lấy token từ header
            received_token = headers.get("x-authenication", "").replace("Bearer ", "").strip()
            expected_token = frappe.conf.get("api_token")
            print(expected_token)

            if not received_token or received_token != expected_token:
                frappe.throw("Invalid or missing token", frappe.AuthenticationError)

            # 2. Lấy và kiểm tra timestamp
            try:
                received_timestamp = int(headers.get("x-timestamp"))
            except (TypeError, ValueError):
                frappe.throw(f"Invalid or missing timestamp: {headers.get('x-timestamp')}")

            now = int(time.time())
            delta = abs(now - received_timestamp)

            # if delta > max_age_seconds:
            #     frappe.throw(f"Request expired (timestamp delta = {delta}s)")

            return func(*args, **kwargs)
        return wrapper
    return decorator

def secure_webhook(require_hmac=True, require_token=False):
    def decorator(func):
        @frappe.whitelist(allow_guest=True)  #
        @wraps(func)
        def wrapper(*args, **kwargs):
            headers = frappe._dict({k.lower(): v for k, v in frappe.request.headers.items()})
            
            # 1. HMAC signature (từ X-Signature)
            if require_hmac:
                secret = frappe.conf.get("webhook_secret", "default_secret")
                body = json.loads(frappe.request.data)
                payload_json = json.dumps({"name":body.get("name")})
                received_signature = headers.get("x-signature")

                if not received_signature:
                    frappe.throw("Missing HMAC signature")

                computed_signature = hmac.new(
                    key=secret.encode('utf-8'),
                    msg=payload_json.encode('utf-8'),
                    digestmod=hashlib.sha256
                ).hexdigest()

                if not hmac.compare_digest(computed_signature, received_signature):
                    frappe.throw("Invalid HMAC signature")

            # 2. Token header (Authorization: Bearer <token>)
            if require_token:
                expected_token = frappe.conf.get("api_token")
                received_token = headers.get("x-authorization", "").replace("Bearer ", "")

                if not received_token or received_token != expected_token:
                    frappe.throw("Invalid or missing token")

            return func(*args, **kwargs)
        return wrapper
    return decorator

def generate_api_token(user: str, application: str = None, doctype: str = None, actions: list = None, expires_in_days: int = 30):
    """Helper để tạo API Token mới"""
    token = str(uuid.uuid4())
    doc = frappe.get_doc({
        "doctype": "API Token",
        "user": user,
        "application": application,
        "doctype_name": doctype,
        "token": token,
        "expires_at": frappe.utils.add_days(now_datetime(), expires_in_days),
        "status": "Active"
    })
    doc.insert(ignore_permissions=True)

    # thêm action permissions
    if actions:
        for a in actions:
            doc.append("permissions", {"action": a})
        doc.save(ignore_permissions=True)

    return token

def require_api_token(doctype_name: str, action: str):
    """Decorator để xác thực API Token"""
    def wrapper(fn):
        def inner(*args, **kwargs):
            auth_header = frappe.get_request_header("Authorization")
            if not auth_header or not auth_header.startswith("Bearer "):
                frappe.throw(_("Missing or invalid Authorization header"), frappe.PermissionError)

            token_value = auth_header.split(" ")[1]

            token_doc = frappe.get_value("API Token", {"token": token_value, "status": "Active"}, ["name"], as_dict=True)
            if not token_doc:
                frappe.throw(_("Invalid or inactive token"), frappe.PermissionError)

            token = frappe.get_doc("API Token", token_doc.name)

            # expiry
            if token.expires_at and token.expires_at < now_datetime():
                frappe.throw(_("Token expired"), frappe.PermissionError)

            # rate limit check
            if cint(token.rate_limit) > 0:
                today = nowdate()
                cache_key = f"api_token_usage:{token.token}:{today}"
                usage = cint(frappe.cache().get(cache_key) or 0)
                if usage >= cint(token.rate_limit):
                    frappe.throw(_("API rate limit exceeded"), frappe.PermissionError)
                frappe.cache().set_value(cache_key, usage + 1, expires_in_sec=24*3600)

            # ip whitelist check
            whitelist = (token.ip_whitelist or "").splitlines()
            if whitelist:
                client_ip = frappe.local.request_ip
                if client_ip not in whitelist:
                    frappe.throw(_("IP not allowed"), frappe.PermissionError)

            # scope check
            if token.doctype_name and token.doctype_name != doctype_name:
                frappe.throw(_("Token not allowed for this Doctype"), frappe.PermissionError)

            allowed = [p.action for p in token.permissions]
            if action not in allowed:
                frappe.throw(_("Token not allowed for this action"), frappe.PermissionError)

            return fn(*args, **kwargs)
        return inner
    return wrapper