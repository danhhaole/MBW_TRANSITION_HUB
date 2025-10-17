import frappe
from frappe import _
from datetime import datetime, timedelta


@frappe.whitelist()
def get_dashboard_data():
    """
    API để lấy dữ liệu dashboard tổng quan
    """
    try:
        # Lấy user hiện tại
        current_user = frappe.session.user
        
        # Lấy tasks (actions) đang pending manual
        tasks = get_pending_tasks(current_user)
        
        # Lấy campaigns đang hoạt động
        active_campaigns = get_active_campaigns()
        
        # Lấy campaigns đã hoàn thành gần đây
        completed_campaigns = get_completed_campaigns()
        
        return {
            "tasks": tasks,
            "activeCampaigns": active_campaigns,
            "completedCampaigns": completed_campaigns
        }
        
    except Exception as e:
        frappe.log_error(f"Error in get_dashboard_data: {str(e)}")
        return {
            "tasks": [],
            "activeCampaigns": [],
            "completedCampaigns": []
        }


def get_pending_tasks(user_id):
    """
    Lấy danh sách tác vụ đang chờ thực hiện
    """
    try:
        # Query các Action có status PENDING_MANUAL
        actions = frappe.db.sql("""
            SELECT 
                a.name as id,
                cs.action_type as type,
                cs.campaign_step_name as title,
                c.full_name as candidate,
                camp.campaign_name as campaign,
                a.scheduled_at,
                CASE 
                    WHEN DATE(a.scheduled_at) = CURDATE() THEN 'Hôm nay'
                    WHEN DATE(a.scheduled_at) = DATE_ADD(CURDATE(), INTERVAL 1 DAY) THEN 'Ngày mai'
                    ELSE DATE_FORMAT(a.scheduled_at, '%d/%m')
                END as dueDate
            FROM `tabAction` a
            INNER JOIN `tabCampaignStep` cs ON a.campaign_step = cs.name
            INNER JOIN `tabCandidateCampaign` cc ON a.candidate_campaign_id = cc.name
            INNER JOIN `tabCandidate` c ON cc.candidate_id = c.name
            INNER JOIN `tabCampaign` camp ON cc.campaign_id = camp.name
            WHERE a.status = 'PENDING_MANUAL'
            AND (a.assignee_id = %(user_id)s OR a.assignee_id IS NULL)
            ORDER BY a.scheduled_at ASC
            LIMIT 10
        """, {"user_id": user_id}, as_dict=True)
        
        return actions or []
        
    except Exception as e:
        frappe.log_error(f"Error in get_pending_tasks: {str(e)}")
        return []


def get_active_campaigns():
    """
    Lấy danh sách campaigns đang hoạt động với thống kê
    """
    try:
        campaigns = frappe.db.sql("""
            SELECT 
                c.name as id,
                c.campaign_name as name,
                'active' as status
            FROM `tabCampaign` c
            WHERE c.status = 'ACTIVE'
            AND c.is_active = 1
            ORDER BY c.modified DESC
            LIMIT 5
        """, as_dict=True)
        
        # Tính thống kê cho từng campaign
        for campaign in campaigns:
            stats = get_campaign_stats(campaign.id)
            campaign.stats = stats
        
        return campaigns or []
        
    except Exception as e:
        frappe.log_error(f"Error in get_active_campaigns: {str(e)}")
        return []


def get_completed_campaigns():
    """
    Lấy danh sách campaigns đã hoàn thành gần đây
    """
    try:
        campaigns = frappe.db.sql("""
            SELECT 
                c.name as id,
                c.campaign_name as name,
                'completed' as status
            FROM `tabCampaign` c
            WHERE c.status IN ('ARCHIVED', 'COMPLETED')
            ORDER BY c.modified DESC
            LIMIT 5
        """, as_dict=True)
        
        # Tính số ứng viên mới cho từng campaign
        for campaign in campaigns:
            stats = get_campaign_stats(campaign.id)
            campaign.stats = stats
        
        return campaigns or []
        
    except Exception as e:
        frappe.log_error(f"Error in get_completed_campaigns: {str(e)}")
        return []


def get_campaign_stats(campaign_id):
    """
    Tính toán thống kê cho một campaign
    """
    try:
        # Số ứng viên trong campaign
        candidate_count = frappe.db.count("CandidateCampaign", {
            "campaign_id": campaign_id,
            "status": "ACTIVE"
        })
        
        # Tính tỷ lệ mở email (interaction EMAIL_OPENED)
        opened_emails = frappe.db.sql("""
            SELECT COUNT(DISTINCT cc.candidate_id) as count
            FROM `tabCandidateCampaign` cc
            INNER JOIN `tabInteraction` i ON cc.candidate_id = i.candidate_id
            INNER JOIN `tabAction` a ON i.action = a.name
            WHERE cc.campaign_id = %(campaign_id)s
            AND i.interaction_type = 'EMAIL_OPENED'
        """, {"campaign_id": campaign_id}, as_dict=True)
        
        opened_count = opened_emails[0].count if opened_emails else 0
        
        # Tính tỷ lệ nhấp (interaction EMAIL_CLICKED)
        clicked_emails = frappe.db.sql("""
            SELECT COUNT(DISTINCT cc.candidate_id) as count
            FROM `tabCandidateCampaign` cc
            INNER JOIN `tabInteraction` i ON cc.candidate_id = i.candidate_id
            INNER JOIN `tabAction` a ON i.action = a.name
            WHERE cc.campaign_id = %(campaign_id)s
            AND i.interaction_type = 'EMAIL_CLICKED'
        """, {"campaign_id": campaign_id}, as_dict=True)
        
        clicked_count = clicked_emails[0].count if clicked_emails else 0
        
        # Số ứng tuyển mới (trong 30 ngày qua)
        thirty_days_ago = datetime.now() - timedelta(days=30)
        new_applicants = frappe.db.sql("""
            SELECT COUNT(DISTINCT cc.candidate_id) as count
            FROM `tabCandidateCampaign` cc
            INNER JOIN `tabInteraction` i ON cc.candidate_id = i.candidate_id
            WHERE cc.campaign_id = %(campaign_id)s
            AND i.interaction_type = 'APPLICATION_SUBMITTED'
            AND i.creation >= %(since_date)s
        """, {
            "campaign_id": campaign_id,
            "since_date": thirty_days_ago
        }, as_dict=True)
        
        applicants_count = new_applicants[0].count if new_applicants else 0
        
        # Tính tỷ lệ phần trăm
        open_rate = round((opened_count / candidate_count * 100), 0) if candidate_count > 0 else 0
        click_rate = round((clicked_count / candidate_count * 100), 0) if candidate_count > 0 else 0
        
        return {
            "candidates": candidate_count,
            "openRate": int(open_rate),
            "clickRate": int(click_rate),
            "newApplicants": applicants_count
        }
        
    except Exception as e:
        frappe.log_error(f"Error in get_campaign_stats: {str(e)}")
        return {
            "candidates": 0,
            "openRate": 0,
            "clickRate": 0,
            "newApplicants": 0
        }


@frappe.whitelist()
def update_task(taskId, outcome, notes, completedAt):
    """
    Cập nhật trạng thái tác vụ
    """
    try:
        if not taskId:
            frappe.throw(_("Task ID is required"))
        
        # Lấy action document
        action = frappe.get_doc("Mira Action", taskId)
        
        if not action:
            frappe.throw(_("Task not found"))
        
        # Cập nhật trạng thái
        action.status = "EXECUTED"
        action.executed_at = completedAt or datetime.now()
        
        # Lưu kết quả vào field result (JSON)
        result_data = {
            "outcome": outcome,
            "notes": notes,
            "completed_by": frappe.session.user,
            "completed_at": completedAt or datetime.now().isoformat()
        }
        
        action.result = result_data
        action.save()
        
        # Commit transaction
        frappe.db.commit()
        
        return {
            "success": True,
            "message": _("Task updated successfully")
        }
        
    except Exception as e:
        frappe.log_error(f"Error in update_task: {str(e)}")
        frappe.throw(_("Failed to update task: {0}").format(str(e))) 