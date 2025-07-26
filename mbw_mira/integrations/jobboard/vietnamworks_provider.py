import requests
import logging
from urllib3.util.retry import Retry
from requests.adapters import HTTPAdapter
import frappe


class VietnamWorksProvider:
    """
    Provider kết nối VietnamWorks API, dựa trên CandidateDataSource.
    """

    BASE_URL = "https://api.vietnamworks.com/v1/"

    def __init__(self, source_name, timeout=10, max_retries=3):
        self.source_doc = frappe.get_doc("CandidateDataSource", source_name)
        self.timeout = timeout
        self.max_retries = max_retries

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

        self.access_token = None

    def __enter__(self):
        self.connect()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.disconnect()

    def connect(self):
        """
        Lấy & refresh access_token nếu cần
        """
        if self.is_token_expired():
            self.refresh_access_token()
        else:
            self.access_token = self.source_doc.access_token
        self.logger.info("Connected to VietnamWorks API")

    def disconnect(self):
        self.session.close()
        self.logger.info("Disconnected from VietnamWorks")

    def is_token_expired(self):
        if not self.source_doc.token_expires_at:
            return False
        from frappe.utils import now_datetime
        return now_datetime() >= self.source_doc.token_expires_at

    def refresh_access_token(self):
        """
        Refresh token
        """
        token_url = self.BASE_URL + "oauth2/token"
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
        from frappe.utils import now_datetime, add_seconds
        self.source_doc.access_token = self.access_token
        self.source_doc.token_expires_at = add_seconds(now_datetime(), int(token_data.get("expires_in", 3600)))
        self.source_doc.save()
        frappe.db.commit()
        self.logger.info("Refreshed VietnamWorks access_token")

    def _headers(self):
        return {
            "Authorization": f"Bearer {self.access_token}",
            "Content-Type": "application/json"
        }

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

    # === VietnamWorks specific ===

    def get_jobs(self):
        return self.get("jobs")

    def get_candidates(self, job_id=None):
        params = {}
        if job_id:
            params["job_id"] = job_id
        return self.get("candidates", params=params)

    def post_job(self, job_data):
        return self.post("jobs", json=job_data)


#Cách sử dụng
# from myapp.topcv_provider import TopCVProvider
# from myapp.vietnamworks_provider import VietnamWorksProvider

# source_name = "SOURCE-20250717-00004"

# with TopCVProvider(source_name) as topcv:
#     jobs = topcv.get_jobs()
#     print(jobs)

#     candidates = topcv.get_candidates()
#     print(candidates)

# with VietnamWorksProvider(source_name) as vw:
#     jobs = vw.get_jobs()
#     print(jobs)

#     candidates = vw.get_candidates()
#     print(candidates)
