# services/nurturing_collector_worker.py

import frappe
from frappe.utils import now_datetime

def process_nurturing_campaign(campaign_id: str):
    """
    Worker dùng để xử lý chiến dịch NURTURING:
    - Tìm tất cả ứng viên thuộc segment của campaign
    - Kiểm tra nếu ứng viên chưa có CandidateCampaign thì tạo mới
    """
    campaign = frappe.get_doc("Campaign", campaign_id)
    segment = campaign.get("target_segment")

    if not segment:
        frappe.logger().info(f"[Nurturing] Campaign {campaign_id} has no segment defined.")
        return

    # Tìm tất cả ứng viên thuộc segment
    candidates = get_candidates_by_segment(segment)

    for candidate in candidates:
        # Kiểm tra nếu ứng viên đã được enroll trong campaign này
        exists = frappe.db.exists("CandidateCampaign", {
            "candidate": candidate["name"],
            "campaign": campaign_id
        })

        if not exists:
            # Tạo mới CandidateCampaign
            frappe.get_doc({
                "doctype": "CandidateCampaign",
                "candidate": candidate["name"],
                "campaign": campaign_id,
                "status": "ACTIVE",
                "enrolled_at": now_datetime(),
                "current_step_order": 1,
                "next_action_at": now_datetime()
            }).insert(ignore_permissions=True)

            frappe.logger().info(f"[Nurturing] Enrolled candidate {candidate['name']} to campaign {campaign_id}")


def get_candidates_by_segment(segment_id: str) -> list:
    """
    Hàm phụ trợ để lấy danh sách ứng viên thuộc segment
    Giả định Candidate có field 'segment' (hoặc tạo bảng phụ nếu cần nâng cao)
    """
    return frappe.get_all("Candidate", filters={"segment": segment_id}, fields=["name"])
