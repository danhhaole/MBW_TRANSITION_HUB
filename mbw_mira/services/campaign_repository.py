#lấy các campaign đang hoạt động
import frappe
class CampaignRepository:
    @staticmethod
    def get_active_campaigns():
        """
        Trả về danh sách các Campaign có status = 'ACTIVE'
        và type nằm trong ['NURTURING', 'ATTRACTION']
        """
        return frappe.get_all(
            "Campaign",
            filters={
                "status": "ACTIVE",
                "type": ["in", ["NURTURING", "ATTRACTION"]],
            },
            fields=["name", "type", "target_segment"]
        )
