import requests
import logging
from urllib3.util.retry import Retry
from requests.adapters import HTTPAdapter
import frappe


class TopCVProvider:
    """
    Provider kết nối TopCV API, dựa trên CandidateDataSource.
    Đã hỗ trợ:
    + BASE_URL = https://partner.topcv.vn
    + API Key + Secret
    + Context manager (with)
    + Retry, timeout, logging
    + /api/connect và /api/disconnect
    + get_jobs, get_candidates, post_job
    """

    BASE_URL = "https://partner.topcv.vn"

    def __init__(self, source_name, timeout=10, max_retries=3):
        """
        :param source_name: name của bản ghi CandidateDataSource
        :param timeout: timeout cho mỗi request (giây)
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
            allowed_methods=["HEAD", "GET", "POST", "DELETE"]
        )
        adapter = HTTPAdapter(max_retries=retries)
        self.session.mount("https://", adapter)
        self.session.mount("http://", adapter)

        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.INFO)

        self.api_key = None
        self.api_secret = None

    def __enter__(self):
        self.connect()
        self.connect_session()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.disconnect_session()
        self.disconnect()

    def connect(self):
        """
        Lấy API Key & Secret từ Doctype
        """
        if not self.source_doc.api_key or not self.source_doc.api_secret:
            raise ValueError("Missing API Key or API Secret for TopCV")
        self.api_key = self.source_doc.api_key
        self.api_secret = self.source_doc.api_secret
        self.logger.info("+ Loaded API Key & Secret for TopCV")

    def disconnect(self):
        self.session.close()
        self.logger.info("🔒 Disconnected HTTP session from TopCV")

    def _headers(self):
        return {
            "X-API-KEY": self.api_key,
            "X-API-SECRET": self.api_secret,
            "Content-Type": "application/json"
        }

    def get(self, path, params=None):
        """
        Wrapper GET request
        """
        self.logger.info(f"📄 GET {path}")
        url = f"{self.BASE_URL}/{path.lstrip('/')}"
        resp = self.session.get(
            url,
            headers=self._headers(),
            params=params,
            timeout=self.timeout
        )
        resp.raise_for_status()
        return resp.json()

    def post(self, path, json=None):
        """
        Wrapper POST request
        """
        self.logger.info(f"📄 POST {path}")
        url = f"{self.BASE_URL}/{path.lstrip('/')}"
        resp = self.session.post(
            url,
            headers=self._headers(),
            json=json,
            timeout=self.timeout
        )
        resp.raise_for_status()
        return resp.json()

    # === TopCV specific ===

    def connect_session(self):
        """
        Gọi /api/connect để báo bắt đầu phiên
        """
        self.logger.info("📡 Connecting session to TopCV")
        return self.post("api/connect")

    def disconnect_session(self):
        """
        Gọi /api/disconnect để báo kết thúc phiên
        """
        self.logger.info("📡 Disconnecting session from TopCV")
        return self.post("api/disconnect")

    def get_jobs(self):
        """
        Lấy danh sách job đã đăng
        """
        return self.get("jobs")

    def get_candidates(self, job_id=None):
        """
        Lấy danh sách ứng viên theo job
        """
        params = {}
        if job_id:
            params["job_id"] = job_id
        return self.get("candidates", params=params)

    def post_job(self, job_data):
        """
        Đăng một job mới
        """
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
