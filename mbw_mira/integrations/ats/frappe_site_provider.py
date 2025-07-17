import frappe
import logging
from frappe.frappeclient import FrappeClient
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry


class FrappeSiteProvider:
    """
    Provider kết nối đến Frappe site khác hoặc ngay trong cùng site
    dựa trên Doctype CandidateDataSource.

    + same_site + ATS → dùng trực tiếp ORM của site hiện tại
    + API Key hoặc OAuth2 nếu khác site
    + tự refresh token nếu OAuth2
    + context manager
    + retry, timeout, logging
    + CRUD + sync_direction
    """

    def __init__(self, source_name, timeout=10, max_retries=3):
        self.source_doc = frappe.get_doc("CandidateDataSource", source_name)
        self.timeout = timeout
        self.max_retries = max_retries

        self.session = requests.Session()
        retries = Retry(
            total=max_retries,
            backoff_factor=0.3,
            status_forcelist=(500, 502, 504),
            allowed_methods=["HEAD", "GET", "POST", "PUT", "DELETE"]
        )
        adapter = HTTPAdapter(max_retries=retries)
        self.session.mount("https://", adapter)
        self.session.mount("http://", adapter)

        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.INFO)

        self.client = None
        self.auth_method = self.source_doc.auth_method or "API Key"
        self.sync_direction = self.source_doc.sync_direction or "Both"

        self._same_site_active = False

    def __enter__(self):
        self.connect()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.disconnect()

    def connect(self):
        """
        Khởi tạo kết nối (same_site DB hoặc remote API)
        """
        if getattr(self.source_doc, "same_site", 0) and self.source_doc.source_type == "ATS":
            if not frappe.local.site:
                raise RuntimeError("No active Frappe site context found. Cannot operate in same_site mode.")
            self._same_site_active = True
            self.logger.info("+ Same site & ATS: using current site context")
            return

        if getattr(self.source_doc, "same_site", 0) and self.source_doc.source_type != "ATS":
            self.logger.warning("⚠️ same_site is only valid with ATS; falling back to API")

        url = self.source_doc.api_base_url
        if not url:
            raise ValueError("api_base_url is required when not same_site")

        if self.auth_method == "API Key":
            api_key = self.source_doc.api_key
            api_secret =  self.source_doc.get_password("api_secret", raise_exception=False)
            print(api_key,api_secret)
            if not all([api_key, api_secret]):
                raise ValueError("Missing api_key or api_secret")
            self.client = FrappeClient(
                url=url,
                api_key=api_key,
                api_secret=api_secret
            )

        elif self.auth_method == "OAuth2":
            if self.is_token_expired():
                self.refresh_access_token()
            access_token = self.source_doc.access_token
            if not access_token:
                raise ValueError("Missing access_token")
            self.client = FrappeClient(
                url=url,
                access_token=access_token
            )
        else:
            raise ValueError(f"Unsupported auth_method: {self.auth_method}")

        self.logger.info(f"+ Connected to remote site {url} via {self.auth_method}")

    def disconnect(self):
        if self._same_site_active:
            self.logger.info("🔒 Same site mode: nothing to disconnect")
        else:
            self.session.close()
            self.logger.info("🔒 Disconnected HTTP session")

    def is_token_expired(self):
        if not self.source_doc.token_expires_at:
            return False
        from frappe.utils import now_datetime
        return now_datetime() >= self.source_doc.token_expires_at

    def refresh_access_token(self):
        """
        Refresh OAuth2 access token
        """
        url = self.source_doc.api_base_url + "/api/method/oauth2/token"
        data = {
            "grant_type": "refresh_token",
            "refresh_token": self.source_doc.refresh_token,
            "client_id": self.source_doc.client_id,
            "client_secret": self.source_doc.client_secret,
        }
        r = self.session.post(url, data=data, timeout=self.timeout)
        if not r.ok:
            raise RuntimeError(f"Failed to refresh token: {r.status_code} {r.text}")
        resp = r.json()
        self.source_doc.access_token = resp.get("access_token")
        self.source_doc.refresh_token = resp.get("refresh_token", self.source_doc.refresh_token)
        from frappe.utils import add_seconds, now_datetime
        self.source_doc.token_expires_at = add_seconds(now_datetime(), int(resp.get("expires_in", 3600)))
        self.source_doc.save()
        frappe.db.commit()
        self.logger.info("🔄 Refreshed OAuth2 access_token")

    # === CRUD & Call ===

    def get_list(self, doctype, **kwargs):
        self.logger.info(f"📄 get_list({doctype})")
        if self._same_site_active:
            return frappe.get_all(doctype, **kwargs)
        else:
            return self.client.get_list(doctype, **kwargs)

    def get_doc(self, doctype, name):
        self.logger.info(f"📄 get_doc({doctype}, {name})")
        if self._same_site_active:
            return frappe.get_doc(doctype, name).as_dict()
        else:
            return self.client.get_doc(doctype, name)

    def insert(self, doc):
        self.logger.info(f"📄 insert({doc.get('doctype')})")
        if self.sync_direction not in ("Push", "Both"):
            raise PermissionError("Sync direction does not allow Push")
        if self._same_site_active:
            d = frappe.get_doc(doc)
            d.insert()
            frappe.db.commit()
            return d.as_dict()
        else:
            return self.client.insert(doc)

    def update(self, doctype, name, doc):
        self.logger.info(f"📄 update({doctype}, {name})")
        if self.sync_direction not in ("Push", "Both"):
            raise PermissionError("Sync direction does not allow Push")
        if self._same_site_active:
            d = frappe.get_doc(doctype, name)
            d.update(doc)
            d.save()
            frappe.db.commit()
            return d.as_dict()
        else:
            return self.client.update(doctype, name, doc)

    def delete(self, doctype, name):
        self.logger.info(f"📄 delete({doctype}, {name})")
        if self.sync_direction not in ("Push", "Both"):
            raise PermissionError("Sync direction does not allow Push")
        if self._same_site_active:
            frappe.delete_doc(doctype, name)
            frappe.db.commit()
            return {"status": "deleted"}
        else:
            return self.client.delete(doctype, name)

    def call(self, method, params=None):
        self.logger.info(f"📄 call({method})")
        if self._same_site_active:
            return frappe.call(method, **(params or {}))
        else:
            return self.client.get_api(method, params=params)

#Cách dùng 
# from frappe_site_provider import FrappeSiteProvider

# source_name = "SOURCE-250717-00161"

# with FrappeSiteProvider(source_name) as provider:
#     # pull
#     if provider.sync_direction in ("Pull", "Both"):
#         users = provider.get_list("User", fields=["name", "email"])
#         print(users)

#     # push
#     if provider.sync_direction in ("Push", "Both"):
#         new_todo = provider.insert({
#             "doctype": "ToDo",
#             "description": "Inserted via FrappeSiteProvider",
#             "status": "Open"
#         })
#         print(new_todo)
