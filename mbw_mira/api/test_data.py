import frappe
from frappe import _


@frappe.whitelist()
def get_test_dashboard_data():
    """
    API để lấy dữ liệu test cho dashboard
    """
    return {
        "tasks": [
            {
                "id": "test_task_001",
                "type": "MANUAL_CALL",
                "title": "Gọi điện thoại",
                "candidate": "Nguyễn Văn An",
                "campaign": "Nuôi dưỡng React",
                "dueDate": "Hôm nay"
            },
            {
                "id": "test_task_002", 
                "type": "MANUAL_CALL",
                "title": "Gọi điện thoại",
                "candidate": "Trần Thị Bình",
                "campaign": "Thu hút Golang",
                "dueDate": "Ngày mai"
            },
            {
                "id": "test_task_003",
                "type": "MANUAL_TASK", 
                "title": "Review hồ sơ LinkedIn",
                "candidate": "Lê Hoàng Cường",
                "campaign": "Xây dựng thương hiệu Data Science",
                "dueDate": "28/06"
            }
        ],
        "activeCampaigns": [
            {
                "id": "camp_01",
                "name": "Nuôi dưỡng ứng viên React",
                "status": "active",
                "stats": {
                    "candidates": 150,
                    "openRate": 82,
                    "clickRate": 25,
                    "newApplicants": 4
                }
            },
            {
                "id": "camp_02", 
                "name": "Thu hút nhân tài Golang",
                "status": "active",
                "stats": {
                    "candidates": 45,
                    "openRate": 75,
                    "clickRate": 18,
                    "newApplicants": 1
                }
            }
        ],
        "completedCampaigns": [
            {
                "id": "camp_03",
                "name": "Xây dựng thương hiệu Employer",
                "status": "completed",
                "stats": {
                    "newApplicants": 0
                }
            },
            {
                "id": "camp_04",
                "name": "Giới thiệu bạn bè Q2", 
                "status": "completed",
                "stats": {
                    "newApplicants": 12
                }
            }
        ]
    }


@frappe.whitelist()
def test_update_task(taskId, outcome, notes, completedAt):
    """
    API test để cập nhật task
    """
    return {
        "success": True,
        "message": f"Task {taskId} updated with outcome: {outcome}"
    } 