import frappe
import logging
from frappe.frappeclient import FrappeClient
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry


class FrappeSiteProvider:
    """
    Provider để kết nối tới một Frappe site khác
    dựa trên thông tin trong Doctype CandidateDataSource.
    Hỗ trợ:
        API Key / Secret
        OAuth2
        Retry, Timeout
        Logging
        Context manager
    """

    def __init__(self, source_name, timeout=10, max_retries=3):
        """
        :param source_name: name của CandidateDataSource
        :param timeout: timeout mỗi request (giây)
        :param max_retries: số lần retry nếu lỗi tạm thời
        """
        self.source_doc = frappe.get_doc("CandidateDataSource", source_name)
        self.timeout = timeout
        self.max_retries = max_retries

        self.session = requests.Session()
        retries = Retry(
            total=max_retries,
            backoff_factor=0.3,
            status_forcelist=(500, 502, 504),
            allowed_methods=["HEAD", "GET", "POST", "PUT", "DELETE", "OPTIONS"]
        )
        adapter = HTTPAdapter(max_retries=retries)
        self.session.mount("https://", adapter)
        self.session.mount("http://", adapter)

        self.client = None
        self.auth_method = self.source_doc.auth_method or "API Key"
        self.sync_direction = self.source_doc.sync_direction or "Both"

        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.INFO)

    def __enter__(self):
        self.connect()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.disconnect()

    def connect(self):
        """
        Khởi tạo kết nối.
        """
        url = self.source_doc.api_base_url

        if self.auth_method == "API Key":
            api_key = self.source_doc.api_key
            api_secret = self.source_doc.api_secret
            if not all([url, api_key, api_secret]):
                raise ValueError("Missing api_base_url, api_key, or api_secret")
            self.client = FrappeClient(
                url=url,
                api_key=api_key,
                api_secret=api_secret,
                session=self.session,
                timeout=self.timeout
            )

        elif self.auth_method == "OAuth2":
            # tự gọi token endpoint nếu cần
            if self.is_token_expired():
                self.refresh_access_token()
            access_token = self.source_doc.access_token
            self.client = FrappeClient(
                url=url,
                access_token=access_token,
                session=self.session,
                timeout=self.timeout
            )
        else:
            raise ValueError(f"Unsupported auth_method: {self.auth_method}")

        self.logger.info(f"Connected to site {url} via {self.auth_method}")

    def disconnect(self):
        """
        Cleanup.
        """
        self.session.close()
        self.logger.info("🔒 Disconnected from remote site")

    def is_token_expired(self):
        """
        Kiểm tra token hết hạn (nếu có trường token_expires_at)
        """
        if not self.source_doc.token_expires_at:
            return False
        from frappe.utils import now_datetime
        return now_datetime() >= self.source_doc.token_expires_at

    def refresh_access_token(self):
        """
        Lấy lại access_token qua refresh_token (giả sử site hỗ trợ OAuth2 chuẩn)
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
        self.source_doc.token_expires_at = frappe.utils.add_seconds(frappe.utils.now_datetime(), int(resp.get("expires_in", 3600)))
        self.source_doc.save()
        frappe.db.commit()
        self.logger.info("🔄 Refreshed OAuth2 access_token")

    # === Wrapper methods ===

    def get_list(self, doctype, **kwargs):
        self.logger.info(f"📄 get_list({doctype})")
        return self.client.get_list(doctype, **kwargs)

    def get_doc(self, doctype, name):
        self.logger.info(f"📄 get_doc({doctype}, {name})")
        return self.client.get_doc(doctype, name)

    def insert(self, doc):
        self.logger.info(f"📄 insert({doc.get('doctype')})")
        if self.sync_direction in ("Push", "Both"):
            return self.client.insert(doc)
        else:
            raise PermissionError("Sync direction does not allow Push")

    def update(self, doctype, name, doc):
        self.logger.info(f"📄 update({doctype}, {name})")
        if self.sync_direction in ("Push", "Both"):
            return self.client.update(doctype, name, doc)
        else:
            raise PermissionError("Sync direction does not allow Push")

    def delete(self, doctype, name):
        self.logger.info(f"📄 delete({doctype}, {name})")
        if self.sync_direction in ("Push", "Both"):
            return self.client.delete(doctype, name)
        else:
            raise PermissionError("Sync direction does not allow Push")

    def call(self, method, params=None):
        self.logger.info(f"📄 call({method})")
        return self.client.get_api(method, params=params)

#Cáchs sử dụng
# from myapp.frappe_site_provider import FrappeSiteProvider

# source_name = "SOURCE-20250717-00001"

# with FrappeSiteProvider(source_name) as provider:
#     # pull data
#     if provider.sync_direction in ("Pull", "Both"):
#         users = provider.get_list("User", fields=["name", "email"])
#         print(users)

#     # push data
#     if provider.sync_direction in ("Push", "Both"):
#         new_doc = provider.insert({
#             "doctype": "ToDo",
#             "description": "Created via Provider",
#             "status": "Open"
#         })
#         print(new_doc)
