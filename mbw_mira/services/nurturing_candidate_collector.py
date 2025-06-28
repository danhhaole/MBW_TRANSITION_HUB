# tự động đưa ứng viên vào chiến dịch NURTURING (Nuôi dưỡng ứng viên)
import frappe
from frappe.utils import now_datetime


class NurturingCandidateCollector:
    def __init__(self, campaign):
        self.campaign = campaign

    def collect(self):
        segment = self.campaign.get("target_segment")
        if not segment:
            frappe.logger().info(f"[NurturingCollector] Campaign {self.campaign.name} has no segment.")
            return

        # Giả sử mỗi ứng viên có field 'segment' để lọc
        candidates = frappe.get_all(
            "Candidate",
            filters={"segment": segment},
            fields=["name"]
        )

        for c in candidates:
            if not frappe.db.exists("CandidateCampaign", {
                "candidate": c.name,
                "campaign": self.campaign.name
            }):
                frappe.get_doc({
                    "doctype": "CandidateCampaign",
                    "candidate": c.name,
                    "campaign": self.campaign.name,
                    "status": "ACTIVE",
                    "enrolled_at": now_datetime(),
                    "current_step_order": 1,
                    "next_action_at": now_datetime()
                }).insert(ignore_permissions=True)

                frappe.logger().info(f"[NurturingCollector] Enrolled {c.name} to campaign {self.campaign.name}")
