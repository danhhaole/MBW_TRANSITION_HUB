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


@frappe.whitelist()
def get_segment_top_skills(segment_id, limit=10):
    """
    Lấy top skills phổ biến nhất trong một segment
    
    Args:
        segment_id: ID của segment cần lấy thống kê
        limit: Số lượng skills trả về (mặc định 10, có thể từ 5-10)
    
    Returns:
        List các skills với tên và số lần xuất hiện
        Format: [{"name": "Python", "value": 15}, ...]
    """
    try:
        # Validate segment_id
        if not segment_id:
            frappe.throw(_("Segment ID is required"))
        
        # Kiểm tra segment có tồn tại không
        if not frappe.db.exists("Mira Segment", segment_id):
            frappe.throw(_("Segment not found"))
        
        # Convert limit to int và validate
        limit = int(limit)
        if limit < 5:
            limit = 5
        elif limit > 10:
            limit = 10
        
        # Lấy tất cả talents trong segment thông qua Mira Talent Pool
        talent_ids = frappe.db.sql("""
            SELECT talent_id
            FROM `tabMira Talent Pool`
            WHERE segment_id = %(segment_id)s
        """, {"segment_id": segment_id}, as_dict=True)
        
        if not talent_ids:
            return []
        
        # Lấy skills của tất cả talents
        talent_id_list = [t.talent_id for t in talent_ids]
        talents = frappe.db.sql("""
            SELECT skills
            FROM `tabMira Talent`
            WHERE name IN %(talent_ids)s
            AND skills IS NOT NULL
            AND skills != ''
        """, {"talent_ids": talent_id_list}, as_dict=True)
        
        # Đếm tần suất xuất hiện của từng skill
        skill_count = {}
        for talent in talents:
            if talent.skills:
                # Skills được lưu dưới dạng comma-separated string
                skills_list = [s.strip() for s in talent.skills.split(',')]
                for skill in skills_list:
                    if skill:  # Bỏ qua các string rỗng
                        skill_lower = skill.lower()  # Chuẩn hóa về lowercase để tránh trùng lặp
                        if skill_lower in skill_count:
                            skill_count[skill_lower] = {
                                "name": skill_count[skill_lower]["name"],
                                "value": skill_count[skill_lower]["value"] + 1
                            }
                        else:
                            skill_count[skill_lower] = {
                                "name": skill,  # Giữ nguyên format gốc của skill đầu tiên
                                "value": 1
                            }
        
        # Sắp xếp theo số lần xuất hiện giảm dần và lấy top N
        sorted_skills = sorted(
            skill_count.values(),
            key=lambda x: x["value"],
            reverse=True
        )[:limit]
        
        return sorted_skills
        
    except Exception as e:
        frappe.log_error(f"Error in get_segment_top_skills: {str(e)}")
        return []


@frappe.whitelist()
def get_segment_experience_distribution(segment_id):
    """
    Lấy phân bố kinh nghiệm của các talents trong một segment
    
    Args:
        segment_id: ID của segment cần lấy thống kê
    
    Returns:
        List phân bố kinh nghiệm theo nhóm
        Format: [
            {"name": "0-2 years", "value": 15},
            {"name": "3-5 years", "value": 28},
            ...
        ]
    """
    try:
        # Validate segment_id
        if not segment_id:
            frappe.throw(_("Segment ID is required"))
        
        # Kiểm tra segment có tồn tại không
        if not frappe.db.exists("Mira Segment", segment_id):
            frappe.throw(_("Segment not found"))
        
        # Lấy tất cả talents trong segment với số năm kinh nghiệm
        results = frappe.db.sql("""
            SELECT 
                COALESCE(t.total_years_of_experience, 0) as years
            FROM `tabMira Talent Pool` tp
            INNER JOIN `tabMira Talent` t ON tp.talent_id = t.name
            WHERE tp.segment_id = %(segment_id)s
        """, {"segment_id": segment_id}, as_dict=True)
        
        if not results:
            return []
        
        # Khởi tạo các nhóm kinh nghiệm
        experience_groups = {
            "0-2 years": 0,
            "3-5 years": 0,
            "6-10 years": 0,
            "11-15 years": 0,
            "15+ years": 0
        }
        
        # Phân loại talents vào các nhóm
        for result in results:
            years = result.years or 0
            
            if years <= 2:
                experience_groups["0-2 years"] += 1
            elif years <= 5:
                experience_groups["3-5 years"] += 1
            elif years <= 10:
                experience_groups["6-10 years"] += 1
            elif years <= 15:
                experience_groups["11-15 years"] += 1
            else:
                experience_groups["15+ years"] += 1
        
        # Chuyển đổi sang format output
        distribution = [
            {"name": "0-2 years", "value": experience_groups["0-2 years"]},
            {"name": "3-5 years", "value": experience_groups["3-5 years"]},
            {"name": "6-10 years", "value": experience_groups["6-10 years"]},
            {"name": "11-15 years", "value": experience_groups["11-15 years"]},
            {"name": "15+ years", "value": experience_groups["15+ years"]}
        ]
        
        return distribution
        
    except Exception as e:
        frappe.log_error(f"Error in get_segment_experience_distribution: {str(e)}")
        return []


@frappe.whitelist()
def get_segment_salary_alignment(segment_id):
    """
    Phân tích phân bố mức lương mong muốn của talents so với ngân sách segment
    
    Args:
        segment_id: ID của segment cần phân tích
    
    Returns:
        List phân bố salary alignment
        Format: [
            {"name": "In-Budget", "value": 58, "color": "#10B981"},
            {"name": "Slightly Over-Budget", "value": 28, "color": "#FBBF24"},
            {"name": "Under-Budget", "value": 14, "color": "#3B82F6"}
        ]
    """
    try:
        # Validate segment_id
        if not segment_id:
            frappe.throw(_("Segment ID is required"))
        
        # Kiểm tra segment có tồn tại không và lấy min/max budget
        segment = frappe.get_doc("Mira Segment", segment_id)
        if not segment:
            frappe.throw(_("Segment not found"))
        
        min_budget = segment.min_budget or 0
        max_budget = segment.max_budget or 0
        
        # Nếu segment không có budget range, trả về empty
        if min_budget <= 0 and max_budget <= 0:
            return []
        
        # Lấy expected_salary của tất cả talents trong segment
        results = frappe.db.sql("""
            SELECT 
                COALESCE(t.expected_salary, 0) as expected_salary
            FROM `tabMira Talent Pool` tp
            INNER JOIN `tabMira Talent` t ON tp.talent_id = t.name
            WHERE tp.segment_id = %(segment_id)s
            AND t.expected_salary IS NOT NULL
            AND t.expected_salary > 0
        """, {"segment_id": segment_id}, as_dict=True)
        
        if not results:
            return []
        
        # Khởi tạo các nhóm
        alignment_groups = {
            "In-Budget": 0,           # min_budget <= expected_salary <= max_budget
            "Slightly Over-Budget": 0, # expected_salary > max_budget
            "Under-Budget": 0          # expected_salary < min_budget
        }
        
        # Phân loại talents - so sánh với min/max budget
        for result in results:
            expected_salary = result.expected_salary or 0
            
            if expected_salary < min_budget:
                # Dưới min_budget -> Under-Budget
                alignment_groups["Under-Budget"] += 1
            elif expected_salary <= max_budget:
                # Trong khoảng min_budget đến max_budget -> In-Budget
                alignment_groups["In-Budget"] += 1
            else:
                # Trên max_budget -> Slightly Over-Budget
                alignment_groups["Slightly Over-Budget"] += 1
        
        # Tính tổng số talents để tính phần trăm
        total_talents = sum(alignment_groups.values())
        
        if total_talents == 0:
            return []
        
        # Chuyển đổi sang format output với phần trăm
        distribution = [
            {
                "name": "In-Budget",
                "value": round((alignment_groups["In-Budget"] / total_talents) * 100),
                "color": "#10B981",
                "count": alignment_groups["In-Budget"]
            },
            {
                "name": "Slightly Over-Budget",
                "value": round((alignment_groups["Slightly Over-Budget"] / total_talents) * 100),
                "color": "#FBBF24",
                "count": alignment_groups["Slightly Over-Budget"]
            },
            {
                "name": "Under-Budget",
                "value": round((alignment_groups["Under-Budget"] / total_talents) * 100),
                "color": "#3B82F6",
                "count": alignment_groups["Under-Budget"]
            }
        ]
        
        return distribution
        
    except Exception as e:
        frappe.log_error(f"Error in get_segment_salary_alignment: {str(e)}")
        return []


@frappe.whitelist()
def get_segment_quality_source_analysis(segment_id):
    """
    Phân tích chất lượng nguồn tuyển dụng dựa trên internal_rating = 'A'
    
    Args:
        segment_id: ID của segment cần phân tích
    
    Returns:
        List phân tích chất lượng theo source
        Format: [
            {
                "name": "Referral",
                "value": 78,  // % talents có rating A
                "totalTalents": 45,  // Tổng số talents từ source này
                "color": "#10B981",
                "colorEnd": "#34D399"
            },
            ...
        ]
    """
    try:
        # Validate segment_id
        if not segment_id:
            frappe.throw(_("Segment ID is required"))
        
        # Kiểm tra segment có tồn tại không
        if not frappe.db.exists("Mira Segment", segment_id):
            frappe.throw(_("Segment not found"))
        
        # Lấy thống kê talents theo source và internal_rating
        results = frappe.db.sql("""
            SELECT 
                t.source,
                COUNT(*) as total_talents,
                SUM(CASE WHEN t.internal_rating = 'A' THEN 1 ELSE 0 END) as a_rated_talents
            FROM `tabMira Talent Pool` tp
            INNER JOIN `tabMira Talent` t ON tp.talent_id = t.name
            WHERE tp.segment_id = %(segment_id)s
            AND t.source IS NOT NULL
            AND t.source != ''
            GROUP BY t.source
            ORDER BY a_rated_talents DESC, total_talents DESC
        """, {"segment_id": segment_id}, as_dict=True)
        
        if not results:
            return []
        
        # Định nghĩa màu sắc cho từng source
        source_colors = {
            "Referral": {"color": "#10B981", "colorEnd": "#34D399"},
            "Headhunter": {"color": "#3B82F6", "colorEnd": "#60A5FA"},
            "LinkedIn": {"color": "#8B5CF6", "colorEnd": "#A78BFA"},
            "Facebook": {"color": "#EC4899", "colorEnd": "#F472B6"},
            "Zalo": {"color": "#06B6D4", "colorEnd": "#22D3EE"},
            "Manually": {"color": "#F59E0B", "colorEnd": "#FBBF24"},
            "Nurturing Interaction": {"color": "#14B8A6", "colorEnd": "#2DD4BF"},
            "MBW ATS": {"color": "#6366F1", "colorEnd": "#818CF8"},
            "Import Excel": {"color": "#EF4444", "colorEnd": "#F87171"},
            "Import CV": {"color": "#F97316", "colorEnd": "#FB923C"}
        }
        
        # Chuyển đổi sang format output
        quality_analysis = []
        for result in results:
            source = result.source
            total_talents = result.total_talents or 0
            a_rated_talents = result.a_rated_talents or 0
            
            # Tính phần trăm talents có rating A
            quality_percentage = round((a_rated_talents / total_talents * 100)) if total_talents > 0 else 0
            
            # Lấy màu sắc cho source, nếu không có thì dùng màu mặc định
            colors = source_colors.get(source, {"color": "#6B7280", "colorEnd": "#9CA3AF"})
            
            quality_analysis.append({
                "name": source,
                "value": quality_percentage,
                "totalTalents": total_talents,
                "aRatedTalents": a_rated_talents,
                "color": colors["color"],
                "colorEnd": colors["colorEnd"]
            })
        
        return quality_analysis
        
    except Exception as e:
        frappe.log_error(f"Error in get_segment_quality_source_analysis: {str(e)}")
        return []


@frappe.whitelist()
def get_segment_dashboard_data(segment_id):
    """
    API tổng hợp để lấy tất cả dữ liệu dashboard cho một segment
    Gọi một lần thay vì gọi nhiều API riêng lẻ
    
    Args:
        segment_id: ID của segment cần lấy dashboard data
    
    Returns:
        Dict chứa tất cả dữ liệu dashboard:
        {
            "skills": [...],
            "experience": [...],
            "salary_alignment": [...],
            "quality_source": [...],
            "talents_requiring_update": [...]
        }
    """
    try:
        # Validate segment_id
        if not segment_id:
            frappe.throw(_("Segment ID is required"))
        
        # Kiểm tra segment có tồn tại không
        if not frappe.db.exists("Mira Segment", segment_id):
            frappe.throw(_("Segment not found"))
        
        # Gọi song song tất cả các hàm lấy dữ liệu
        # Python không hỗ trợ async/await trong Frappe, nhưng các query này đã được tối ưu
        
        skills_data = get_segment_top_skills(segment_id, limit=8)
        experience_data = get_segment_experience_distribution(segment_id)
        salary_alignment_data = get_segment_salary_alignment(segment_id)
        quality_source_data = get_segment_quality_source_analysis(segment_id)
        talents_requiring_update_data = get_segment_talents_requiring_update(segment_id)
        recruitment_priority_data = get_recruitment_priority_matrix_data(segment_id)
        
        return {
            "skills": skills_data,
            "experience": experience_data,
            "salary_alignment": salary_alignment_data,
            "quality_source": quality_source_data,
            "talents_requiring_update": talents_requiring_update_data,
            "recruitment_priority": recruitment_priority_data
        }
        
    except Exception as e:
        frappe.log_error(f"Error in get_segment_dashboard_data: {str(e)}")
        # Trả về dữ liệu rỗng thay vì throw error để UI không bị crash
        return {
            "skills": [],
            "experience": [],
            "salary_alignment": [],
            "quality_source": [],
            "talents_requiring_update": [],
            "recruitment_priority": []
        }


@frappe.whitelist()
def get_recruitment_priority_matrix_data(segment_ids=None):
    """
    Lấy dữ liệu cho Recruitment Priority Bubble Chart
    
    Args:
        segment_ids: List ID của các segments cần lấy dữ liệu (optional)
                    Nếu không truyền thì lấy tất cả segments active
    
    Returns:
        List dữ liệu bubble chart:
        Format: [
            {
                "value": [engagement_timeline, readiness_index, talent_count],
                "name": "segment_name",
                "readinessLabel": "High/Medium/Low",
                "timelineLabel": "X days",
                "color": "#color"
            },
            ...
        ]
    """
    try:
        # Parse segment_ids nếu được truyền vào
        if segment_ids:
            if isinstance(segment_ids, str):
                # Nếu là string đơn lẻ, chuyển thành list
                if segment_ids.startswith('[') and segment_ids.endswith(']'):
                    import json
                    segment_ids = json.loads(segment_ids)
                else:
                    # String đơn lẻ, chuyển thành list
                    segment_ids = [segment_ids]
            elif not isinstance(segment_ids, list):
                # Nếu không phải string hoặc list, chuyển thành list
                segment_ids = [segment_ids]
        
        # Query để lấy dữ liệu aggregate từ các bảng liên quan
        segment_filter = ""
        params = {}
        
        if segment_ids and len(segment_ids) > 0:
            segment_filter = "AND s.name IN %(segment_ids)s"
            params["segment_ids"] = segment_ids
        
        # Query chính để lấy dữ liệu từ tất cả các bảng liên quan
        results = frappe.db.sql(f"""
            SELECT 
                s.name as segment_id,
                s.title as segment_name,
                COUNT(DISTINCT tp.talent_id) as talent_count,
                AVG(COALESCE(es.engagement_timeline, 0)) as avg_engagement_timeline,
                AVG(
                    CASE 
                        WHEN es.readiness_level = 'High' THEN 2
                        WHEN es.readiness_level = 'Medium' THEN 1
                        WHEN es.readiness_level = 'Low' THEN 0
                        ELSE 0
                    END
                ) as avg_readiness_score,
                AVG(COALESCE(es.total_score, 0)) as avg_engagement_score,
                -- Tính readiness level dominant
                SUM(CASE WHEN es.readiness_level = 'High' THEN 1 ELSE 0 END) as high_count,
                SUM(CASE WHEN es.readiness_level = 'Medium' THEN 1 ELSE 0 END) as medium_count,
                SUM(CASE WHEN es.readiness_level = 'Low' THEN 1 ELSE 0 END) as low_count
            FROM `tabMira Segment` s
            LEFT JOIN `tabMira Talent Pool` tp ON s.name = tp.segment_id
            LEFT JOIN `tabMira Talent` t ON tp.talent_id = t.name
            LEFT JOIN `tabMira Engagement Summary` es ON t.name = es.talent_id
            WHERE s.is_active = 1
            {segment_filter}
            GROUP BY s.name, s.title
            HAVING talent_count > 0
            ORDER BY talent_count DESC
        """, params, as_dict=True)
        
        if not results:
            return []
        
        # Định nghĩa màu sắc cho từng mức readiness
        readiness_colors = {
            "High": "#10B981",    # Green
            "Medium": "#F59E0B",  # Orange
            "Low": "#EF4444"      # Red
        }
        
        # Chuyển đổi dữ liệu sang format bubble chart
        bubble_data = []
        
        for result in results:
            # Tính toán các giá trị
            talent_count = result.talent_count or 0
            avg_timeline = round(result.avg_engagement_timeline or 0)
            avg_readiness_score = result.avg_readiness_score or 0
            
            # Xác định readiness level dominant
            high_count = result.high_count or 0
            medium_count = result.medium_count or 0
            low_count = result.low_count or 0
            
            # Tìm level có số lượng cao nhất
            if high_count >= medium_count and high_count >= low_count:
                readiness_label = "High"
                readiness_index = 2
            elif medium_count >= low_count:
                readiness_label = "Medium"
                readiness_index = 1
            else:
                readiness_label = "Low"
                readiness_index = 0
            
            # Đảm bảo timeline không vượt quá 90 ngày (theo component)
            timeline_display = min(avg_timeline, 90)
            
            # Format timeline label
            timeline_label = f"{timeline_display} days" if timeline_display > 0 else "No data"
            
            bubble_data.append({
                "value": [timeline_display, readiness_index, talent_count],
                "name": result.segment_name or f"Segment {result.segment_id}",
                "readinessLabel": readiness_label,
                "timelineLabel": timeline_label,
                "color": readiness_colors.get(readiness_label, "#6B7280"),
                "segmentId": result.segment_id,
                "talentCount": talent_count,
                "avgEngagementScore": round(result.avg_engagement_score or 0, 1)
            })
        
        return bubble_data
        
    except Exception as e:
        frappe.log_error(f"Error in get_recruitment_priority_matrix_data: {str(e)}")
        return []


@frappe.whitelist()
def get_segment_talents_requiring_update(segment_id):
    """
    Lấy danh sách talents cần cập nhật (không tương tác quá 6 tháng)
    
    Args:
        segment_id: ID của segment cần lấy danh sách
    
    Returns:
        List talents cần re-engagement
        Format: [
            {
                "name": "Nguyen Van A",
                "title": "Senior Data Scientist",
                "lastInteraction": "2023-12-15",
                "daysSince": 328,
                "status": "Passive",
                "source": "LinkedIn"
            },
            ...
        ]
    """
    try:
        # Validate segment_id
        if not segment_id:
            frappe.throw(_("Segment ID is required"))
        
        # Kiểm tra segment có tồn tại không
        if not frappe.db.exists("Mira Segment", segment_id):
            frappe.throw(_("Segment not found"))
        
        # Tính ngày 6 tháng trước
        six_months_ago = datetime.now() - timedelta(days=180)
        
        # Lấy danh sách talents cần cập nhật
        # Logic: last_interaction_date < six_months_ago nghĩa là tương tác lần cuối > 6 tháng trước
        results = frappe.db.sql("""
            SELECT 
                t.name as talent_id,
                t.full_name as name,
                t.email as title,
                t.last_interaction_date as lastInteraction,
                DATEDIFF(CURDATE(), t.last_interaction_date) as daysSince,
                t.current_status as status,
                t.source
            FROM `tabMira Talent Pool` tp
            INNER JOIN `tabMira Talent` t ON tp.talent_id = t.name
            WHERE tp.segment_id = %(segment_id)s
            AND t.last_interaction_date IS NOT NULL
            AND t.last_interaction_date < %(six_months_ago)s
            AND (t.current_status IS NULL OR t.current_status != 'Not Interested')
            ORDER BY t.last_interaction_date ASC
            LIMIT 50
        """, {
            "segment_id": segment_id,
            "six_months_ago": six_months_ago.date()
        }, as_dict=True)
        
        if not results:
            return []
        
        # Format dữ liệu trả về
        talents_requiring_update = []
        for result in results:
            talents_requiring_update.append({
                "talentId": result.talent_id,
                "name": result.name,
                "title": result.title,
                "lastInteraction": result.lastInteraction.strftime('%Y-%m-%d') if result.lastInteraction else None,
                "daysSince": result.daysSince or 0,
                "status": result.status,
                "source": result.source
            })
        
        return talents_requiring_update
        
    except Exception as e:
        frappe.log_error(f"Error in get_segment_talents_requiring_update: {str(e)}")
        return [] 