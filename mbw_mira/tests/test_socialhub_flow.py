import json
import types
import unittest
from unittest.mock import patch, MagicMock

import frappe

from mbw_mira.api import external_connections as ec


class TestSocialHubFlow(unittest.TestCase):
	def setUp(self):
		# Backup and set public base url for deterministic tests
		self._orig_conf = dict(getattr(frappe, 'conf', {}))
		frappe.conf["mbw_public_base_url"] = "https://example.trycloudflare.com"

	def tearDown(self):
		# Restore conf
		for k in list(frappe.conf.keys()):
			frappe.conf.pop(k, None)
		frappe.conf.update(self._orig_conf)

	def test_get_url_without_port_uses_conf(self):
		url = ec.get_url_without_port()
		self.assertEqual(url, "https://example.trycloudflare.com".rstrip('/'))

	@patch("mbw_mira.api.external_connections.requests.post")
	def test_get_topcv_login_url_returns_none_on_success(self, mock_post):
		mock_resp = MagicMock()
		mock_resp.status_code = 200
		mock_resp.json.return_value = {"status": "Success"}
		mock_post.return_value = mock_resp

		doc = types.SimpleNamespace(
			tenant_name="https://example.trycloudflare.com",
			api_key="api",
			client_secret="secret",
		)
		self.assertIsNone(ec._get_topcv_login_url(doc))

	@patch("mbw_mira.api.external_connections._get_platform_login_url")
	@patch("mbw_mira.api.external_connections.frappe.get_doc")
	def test_retry_connection_sets_pending(self, mock_get_doc, mock_get_login):
		connection = types.SimpleNamespace(
			name="EC-1",
			platform_type="TopCV",
			connection_status="Failed",
			error_message=None,
			last_sync=None,
			save=lambda *a, **k: None,
		)
		mock_get_doc.return_value = connection
		mock_get_login.return_value = None

		res = ec.retry_connection("EC-1")
		self.assertEqual(res.get("status"), "success")
		self.assertEqual(connection.connection_status, "Pending")

	def test_cancel_scheduled_share_success_and_guard(self):
		share = types.SimpleNamespace(
			status="Pending",
			scheduled_time=True,
			save=lambda *a, **k: None,
		)
		with patch("mbw_mira.api.external_connections.frappe.get_doc") as get_doc:
			get_doc.return_value = share
			res = ec.cancel_scheduled_share("SHARE-1")
			self.assertEqual(res.get("status"), "success")

		# Not pending -> error
		share2 = types.SimpleNamespace(
			status="Success",
			scheduled_time=True,
			save=lambda *a, **k: None,
		)
		with patch("mbw_mira.api.external_connections.frappe.get_doc") as get_doc2:
			get_doc2.return_value = share2
			res2 = ec.cancel_scheduled_share("SHARE-2")
			self.assertEqual(res2.get("status"), "error")

	def test_handle_webhook_login_success_triggers_sync(self):
		payload = {
			"user_email": "user@example.com",
			"platform_name": "Facebook",
			"event_type": "login_success",
			"access_token": "acc",
		}

		fake_request = types.SimpleNamespace(method="POST", data=json.dumps(payload))
		with patch.object(ec.frappe, 'request', fake_request):
			with patch("mbw_mira.api.external_connections.frappe.db.get_value") as gv, \
				 patch("mbw_mira.api.external_connections.frappe.db.set_value") as sv, \
				 patch("mbw_mira.api.external_connections.frappe.enqueue") as enq, \
				 patch("mbw_mira.api.external_connections._create_connection_log") as clog, \
				 patch("mbw_mira.api.external_connections.frappe.get_request_header", return_value="UA"):
				gv.return_value = "EC-LOGIN"
				res = ec.handle_webhook()
				self.assertEqual(res.get("status"), "success")
				enq.assert_called()  # sync_accounts scheduled


if __name__ == '__main__':
	unittest.main() 