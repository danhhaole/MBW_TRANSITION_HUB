import requests
import logging
from urllib3.util.retry import Retry
from requests.adapters import HTTPAdapter
import frappe
from frappe import _

class FacebookProvider:
    """
    Provider kết nối tới Facebook Graph API
    dựa trên Mira Data Source (auth_method = OAuth2)
    """

    def __init__(self, source_name, timeout=20, max_retries=3, api_version="v23.0"):
        self.source_doc = frappe.get_doc("Mira Data Source", source_name)
        self.timeout = timeout
        self.max_retries = max_retries
        self.BASE_URL = f"https://graph.facebook.com/{api_version}/"

        self.session = requests.Session()
        retries = Retry(
            total=max_retries,
            backoff_factor=0.3,
            status_forcelist=(500, 502, 504),
            allowed_methods=["HEAD", "GET", "POST", "DELETE"]
        )
        adapter = HTTPAdapter(max_retries=retries)
        self.session.mount("https://", adapter)
        self.session.mount("http://", adapter)

        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.INFO)

        if self.source_doc.auth_method != "OAuth2":
            raise ValueError("FacebookProvider only supports OAuth2")

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

        self.logger.info("Connected to Facebook Graph API")

    def disconnect(self):
        self.session.close()
        self.logger.info("Disconnected from Facebook")

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
        Lấy long-lived token từ short-lived token
        """
        if not self.source_doc.access_token:
            frappe.throw(_("No access token available. Please re-authenticate with Facebook."))
        token_url = self.BASE_URL + "oauth/access_token"
        params = {
            "grant_type": "fb_exchange_token",
            "client_id": self.source_doc.client_id,
            "client_secret": self.source_doc.client_secret,
            "fb_exchange_token": self.source_doc.access_token
        }
        for attempt in range(self.max_retries):
            try:
                resp = self.session.get(token_url, params=params, timeout=self.timeout)
                resp.raise_for_status()
                token_data = resp.json()
                self.access_token = token_data.get("access_token")
                expires_in = int(token_data.get("expires_in", 60 * 60 * 24 * 60))  # default 60 days
                self.source_doc.access_token = self.access_token
                self.source_doc.token_expires_at = frappe.utils.add_seconds(frappe.utils.now_datetime(), expires_in)
                self.source_doc.save()
                frappe.db.commit()
                self.logger.info("🔄 Refreshed Facebook access_token")
                return
            except requests.exceptions.RequestException as e:
                self.logger.error(f"Attempt {attempt + 1} failed: {str(e)}")
                if attempt == self.max_retries - 1:
                    frappe.throw(_("Failed to refresh Facebook token after {0} attempts: {1}").format(self.max_retries, str(e)))

    # === Wrapper methods ===

    def get(self, path, params=None):
        self.logger.info(f"GET {path}")
        url = self.BASE_URL + path
        params = params or {}
        params["access_token"] = self.access_token
        resp = self.session.get(
            url,
            params=params,
            timeout=self.timeout
        )
        resp.raise_for_status()
        return resp.json()

    def post(self, path, data=None, json=None):
        self.logger.info(f"POST {path}")
        url = self.BASE_URL + path
        if data is None:
            data = {}
        data["access_token"] = self.access_token
        resp = self.session.post(
            url,
            data=data,
            json=json,
            timeout=self.timeout
        )
        resp.raise_for_status()
        return resp.json()

    # === Facebook specific ===

    def get_me(self):
        """
        Lấy profile của user
        """
        return self.get("me", params={"fields": "id,name,email"})

    def get_pages(self):
        """
        Lấy danh sách pages mà user quản lý
        """
        return self.get("me/accounts")

    def post_to_page(self, page_id, message):
        """
        Đăng bài lên page
        """
        return self.post(f"{page_id}/feed", data={"message": message})

    def post_to_feed(self, target_id, message, link=None, picture=None):
        """
        Đăng bài lên News Feed của tài khoản cá nhân hoặc fanpage
        :param target_id: ID của tài khoản cá nhân ('me') hoặc fanpage
        :param message: Nội dung bài đăng
        :param link: URL liên kết (nếu có, ví dụ: link ứng tuyển)
        :param picture: URL hình ảnh (nếu có)
        """
        data = {"message": message}
        if link:
            data["link"] = link
        if picture:
            data["picture"] = picture
        return self.post(f"{target_id}/feed", data=data)