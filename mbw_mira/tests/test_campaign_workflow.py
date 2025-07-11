import frappe
import unittest
from frappe.utils import now_datetime, add_days
from mbw_mira.campaign import controller, manual_task_handler
from frappe.tests.utils import FrappeTestCase


class TestCampaignWorkflow(FrappeTestCase):

    def setUp(self):
        # Tạo Campaign
        self.campaign = frappe.get_doc({
            "doctype": "Campaign",
            "campaign_name": "Test Campaign"
        }).insert(ignore_permissions=True)

        # Step 1: Gửi Email ngay
        self.step1 = frappe.get_doc({
            "doctype": "CampaignStep",
            "campaign": self.campaign.name,
            "step_order": 1,
            "action_type": "SEND_EMAIL",
            "delay_in_days": 0,
            "template": "Hello {{ candidate_name }}, welcome!"
        }).insert(ignore_permissions=True)

        # Step 2: MANUAL_TASK sau 2 ngày
        self.step2 = frappe.get_doc({
            "doctype": "CampaignStep",
            "campaign": self.campaign.name,
            "step_order": 2,
            "action_type": "MANUAL_TASK",
            "delay_in_days": 2,
            "template": "Please review profile manually."
        }).insert(ignore_permissions=True)

        # Candidate
        self.candidate = frappe.get_doc({
            "doctype": "Candidate",
            "full_name": "Nguyễn Văn A",
            "email": "vana@example.com",
            "phone": "0909123456"
        }).insert(ignore_permissions=True)

        # CandidateCampaign
        self.cc = frappe.get_doc({
            "doctype": "CandidateCampaign",
            "candidate_id": self.candidate.name,
            "campaign_id": self.campaign.name,
            "status": "ACTIVE",
            "current_step_order": 1,
            "next_action_at": now_datetime()
        }).insert(ignore_permissions=True)

    def test_campaign_email_to_manual_task_flow(self):
        # Handle step 1

        action_1 = frappe.get_all("Action", filters={
            "candidate_campaign_id": self.cc.name,
            "campaign_step": self.step1.name
        }, fields=["name", "status"])
        self.assertTrue(action_1)
        self.assertEqual(action_1[0]["status"], "SCHEDULED")

        # Simulate execution
        a1 = frappe.get_doc("Action", action_1[0]["name"])
        self.assertEqual(a1.status, "EXECUTED")

        # Process result → chuyển sang step 2
        cc = frappe.get_doc("CandidateCampaign", self.cc.name)
        self.assertEqual(cc.current_step_order, 2)

        # Trigger step 2 (manual task)
        action_2 = frappe.get_doc("Action", {
            "candidate_campaign_id": self.cc.name,
            "campaign_step": self.step2.name
        })
        self.assertEqual(action_2.status, "PENDING_MANUAL")

        # Simulate manual completion
        action_2.reload()
        self.assertEqual(action_2.status, "EXECUTED")

        # Process result → không còn step tiếp theo → campaign completed
        cc.reload()
        self.assertEqual(cc.status, "COMPLETED")
        self.assertIsNone(cc.next_action_at)

    def tearDown(self):
        # Xóa dữ liệu để đảm bảo clean
        for doctype in [
            "Action", "CandidateCampaign", "CampaignStep", "Candidate", "Campaign"
        ]:
            frappe.db.delete(doctype)
