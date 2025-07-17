import requests
import logging
from urllib3.util.retry import Retry
from requests.adapters import HTTPAdapter
import frappe


class LinkedInProvider:
    """
    Provider kết nối tới LinkedIn API,
    dựa trên CandidateDataSource (auth_method = OAuth2)
    """

    BASE_URL = "https://api.linkedin.com/v2/"

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

        if self.source_doc.auth_method != "OAuth2":
            raise ValueError("LinkedInProvider only supports OAuth2")

        self.access_token = None

    def __enter__(self):
        self.connect()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.disconnect()

    def connect(self):
        """
        Lấy access_token (refresh nếu cần)
        """
        if self.is_token_expired():
            self.refresh_access_token()
        else:
            self.access_token = self.source_doc.access_token

        self.logger.info("✅ Connected to LinkedIn API")

    def disconnect(self):
        self.session.close()
        self.logger.info("🔒 Disconnected from LinkedIn")

    def is_token_expired(self):
        """
        Kiểm tra token hết hạn
        """
        if not self.source_doc.token_expires_at:
            return False
        from frappe.utils import now_datetime
        return now_datetime() >= self.source_doc.token_expires_at

    def refresh_access_token(self):
        """
        Refresh OAuth2 token từ LinkedIn (nếu được cấp refresh_token)
        """
        token_url = "https://www.linkedin.com/oauth/v2/accessToken"
        data = {
            "grant_type": "refresh_token",
            "refresh_token": self.source_doc.refresh_token,
            "client_id": self.source_doc.client_id,
            "client_secret": self.source_doc.client_secret
        }
        resp = self.session.post(token_url, data=data, timeout=self.timeout)
        if not resp.ok:
            raise RuntimeError(f"Failed to refresh token: {resp.status_code} {resp.text}")
        token_data = resp.json()
        self.access_token = token_data.get("access_token")
        expires_in = int(token_data.get("expires_in", 3600))

        # update doc
        self.source_doc.access_token = self.access_token
        self.source_doc.token_expires_at = frappe.utils.add_seconds(frappe.utils.now_datetime(), expires_in)
        self.source_doc.save()
        frappe.db.commit()
        self.logger.info("🔄 Refreshed LinkedIn access_token")

    # === Wrapper methods ===

    def get(self, path, params=None):
        self.logger.info(f"📄 GET {path}")
        url = self.BASE_URL + path
        resp = self.session.get(
            url,
            headers=self._headers(),
            params=params,
            timeout=self.timeout
        )
        resp.raise_for_status()
        return resp.json()

    def post(self, path, json=None):
        self.logger.info(f"📄 POST {path}")
        url = self.BASE_URL + path
        resp = self.session.post(
            url,
            headers=self._headers(),
            json=json,
            timeout=self.timeout
        )
        resp.raise_for_status()
        return resp.json()

    def _headers(self):
        return {
            "Authorization": f"Bearer {self.access_token}",
            "X-Restli-Protocol-Version": "2.0.0"
        }

    # === LinkedIn specific ===

    def get_profile(self):
        """
        Lấy thông tin profile của current user
        """
        return self.get("me")

    def get_connections(self):
        """
        Lấy connections
        """
        return self.get("connections")

    def post_share(self, text):
        """
        Đăng bài viết (share)
        """
        urn = self.get_profile()["id"]
        payload = {
            "author": f"urn:li:person:{urn}",
            "lifecycleState": "PUBLISHED",
            "specificContent": {
                "com.linkedin.ugc.ShareContent": {
                    "shareCommentary": {"text": text},
                    "shareMediaCategory": "NONE"
                }
            },
            "visibility": {"com.linkedin.ugc.MemberNetworkVisibility": "PUBLIC"}
        }
        return self.post("ugcPosts", json=payload)


#Cách dùng
# from myapp.linkedin_provider import LinkedInProvider

# source_name = "SOURCE-20250717-00002"

# with LinkedInProvider(source_name) as linkedin:
#     profile = linkedin.get_profile()
#     print(profile)

#     linkedin.post_share("Hello from Frappe + LinkedInProvider 🚀")