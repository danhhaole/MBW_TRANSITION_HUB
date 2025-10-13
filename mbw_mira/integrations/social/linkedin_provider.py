import requests
import logging
from urllib3.util.retry import Retry
from requests.adapters import HTTPAdapter
import frappe
from frappe import _


class LinkedInProvider:
    """
    Provider kết nối tới LinkedIn API,
    dựa trên Mira Data Source (auth_method = OAuth2)
    """

    def __init__(self, source_name, timeout=10, max_retries=3, api_version="v2"):
        self.source_doc = frappe.get_doc("Mira Data Source", source_name)
        self.timeout = timeout
        self.max_retries = max_retries
        self.BASE_URL = f"https://api.linkedin.com/{api_version}/"

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

        self.logger.info("Connected to LinkedIn API")

    def disconnect(self):
        self.session.close()
        self.logger.info("Disconnected from LinkedIn")

    def is_token_expired(self):
        """
        Kiểm tra token hết hạn
        """
        if not self.source_doc.access_token or not self.source_doc.token_expires_at:
            return True
        from frappe.utils import now_datetime
        return now_datetime() >= self.source_doc.token_expires_at

    def refresh_access_token(self):
        """
        Refresh OAuth2 token từ LinkedIn
        """
        if not self.source_doc.refresh_token:
            frappe.throw(_("No refresh token available. Please re-authenticate with LinkedIn."))
        token_url = "https://www.linkedin.com/oauth/v2/accessToken"
        data = {
            "grant_type": "refresh_token",
            "refresh_token": self.source_doc.refresh_token,
            "client_id": self.source_doc.client_id,
            "client_secret": self.source_doc.client_secret
        }
        for attempt in range(self.max_retries):
            try:
                resp = self.session.post(token_url, data=data, timeout=self.timeout)
                resp.raise_for_status()
                token_data = resp.json()
                self.access_token = token_data.get("access_token")
                expires_in = int(token_data.get("expires_in", 3600))
                self.source_doc.access_token = self.access_token
                self.source_doc.token_expires_at = frappe.utils.add_seconds(frappe.utils.now_datetime(), expires_in)
                self.source_doc.save()
                frappe.db.commit()
                self.logger.info("Refreshed LinkedIn access_token")
                return
            except requests.exceptions.RequestException as e:
                self.logger.error(f"Attempt {attempt + 1} failed: {str(e)}")
                if attempt == self.max_retries - 1:
                    frappe.throw(_("Failed to refresh LinkedIn token after {0} attempts: {1}").format(self.max_retries, str(e)))

    # === Wrapper methods ===

    def get(self, path, params=None):
        self.logger.info(f"GET {path}")
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
        self.logger.info(f"POST {path}")
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

    def post_share(self, message, link=None, visibility="PUBLIC", author_urn=None):
        """
        Đăng bài viết (share) lên LinkedIn
        :param message: Nội dung bài đăng
        :param link: URL liên kết (nếu có, ví dụ: link ứng tuyển)
        :param visibility: Độ hiển thị (PUBLIC, CONNECTIONS)
        :param author_urn: URN của tác giả (person hoặc organization, mặc định lấy từ profile)
        """
        if not author_urn:
            profile = self.get_profile()
            author_urn = f"urn:li:person:{profile['id']}"

        payload = {
            "author": author_urn,
            "lifecycleState": "PUBLISHED",
            "specificContent": {
                "com.linkedin.ugc.ShareContent": {
                    "shareCommentary": {"text": message},
                    "shareMediaCategory": "NONE" if not link else "ARTICLE"
                }
            },
            "visibility": {"com.linkedin.ugc.MemberNetworkVisibility": visibility}
        }
        if link:
            payload["specificContent"]["com.linkedin.ugc.ShareContent"]["media"] = [
                {
                    "status": "READY",
                    "originalUrl": link
                }
            ]
        return self.post("ugcPosts", json=payload)