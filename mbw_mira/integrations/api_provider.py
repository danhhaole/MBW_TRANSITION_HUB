import frappe
import requests

class APIProvider:
    """
    APIProvider lấy API key/secret từ config (site_config.json hoặc hooks)
    không lưu thông tin nhạy cảm vào DocType.
    """

    def __init__(self):

        # Lấy config từ site_config hoặc frappe conf
        provider_config = frappe.get_conf()
        print(provider_config.get("ladipage_base_url"))
        if not provider_config:
            frappe.throw(f"No config found for provider ")

        self.base_url = provider_config.get("ladipage_base_url")
        self.api_key = provider_config.get("ladipage_api_key")
        self.api_secret = provider_config.get("ladipage_api_secret")
        self.extra_headers = provider_config.get("headers", {})

        if not self.base_url or not self.api_key or not self.api_secret:
            frappe.throw(f"Provider  must have base_url, api_key, api_secret in config")

    def _get_headers(self):
        headers = {
            "Authorization": f"token {self.api_key}:{self.api_secret}",
            "Content-Type": "application/json"
        }
        headers.update(self.extra_headers)
        return headers

    def _make_url(self, endpoint):
        base = self.base_url.rstrip("/")
        endpoint = endpoint.lstrip("/")
        return f"{base}/api/method/{endpoint}"

    def get(self, endpoint, params=None):
        res = requests.get(self._make_url(endpoint), headers=self._get_headers(), params=params)
        self._check_response(res)
        return res.json()

    def post(self, endpoint, data=None, timeout=30):
        url = self._make_url(endpoint)
        frappe.logger().info(f"POST request to: {url}")
        frappe.logger().info(f"POST data: {data}")
        
        try:
            res = requests.post(url, headers=self._get_headers(), json=data, timeout=timeout)
            frappe.logger().info(f"POST response status: {res.status_code}")
            frappe.logger().info(f"POST response body: {res.text[:500]}")  # Log first 500 chars
            
            self._check_response(res)
            return res.json()
        except requests.exceptions.Timeout:
            frappe.logger().error(f"POST request timeout after {timeout}s to: {url}")
            frappe.throw(f"Request timeout after {timeout} seconds")
        except Exception as e:
            frappe.logger().error(f"POST request error: {str(e)}")
            raise

    def put(self, endpoint, data=None, timeout=30):
        url = self._make_url(endpoint)
        frappe.logger().info(f"PUT request to: {url}")
        frappe.logger().info(f"PUT data: {data}")
        
        try:
            res = requests.put(url, headers=self._get_headers(), json=data, timeout=timeout)
            frappe.logger().info(f"PUT response status: {res.status_code}")
            frappe.logger().info(f"PUT response body: {res.text[:500]}")  # Log first 500 chars
            
            self._check_response(res)
            return res.json()
        except requests.exceptions.Timeout:
            frappe.logger().error(f"PUT request timeout after {timeout}s to: {url}")
            frappe.throw(f"Request timeout after {timeout} seconds")
        except Exception as e:
            frappe.logger().error(f"PUT request error: {str(e)}")
            raise

    def delete(self, endpoint, data=None):
        res = requests.delete(self._make_url(endpoint), headers=self._get_headers(), json=data)
        self._check_response(res)
        return res.json()

    def _check_response(self, res):
        if not res.ok:
            frappe.throw(f"API call failed: {res.status_code} - {res.text}")
