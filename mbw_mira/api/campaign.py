import frappe
from frappe import _
import math

@frappe.whitelist()
def get_campaigns_paginated(page=1, limit=10, search="", status_filter="all", type_filter="all", active_filter="all", order_by="modified desc"):
    """
    API lấy danh sách campaigns với pagination đầy đủ
    
    Args:
        page (int): Trang hiện tại (1-based)
        limit (int): Số records mỗi trang
        search (str): Từ khóa tìm kiếm
        status_filter (str): Lọc theo status
        type_filter (str): Lọc theo type
        active_filter (str): Lọc theo is_active
        order_by (str): Sắp xếp
    
    Returns:
        dict: {
            data: [],
            pagination: {
                page: int,
                limit: int, 
                total: int,
                pages: int,
                has_next: bool,
                has_prev: bool
            }
        }
    """
    try:
        # Validate input
        page = max(1, int(page))
        limit = max(1, min(100, int(limit)))  # Giới hạn tối đa 100 records
        offset = (page - 1) * limit
        
        # Build filters
        filters = []
        
        # Search filter
        if search and search.strip():
            search_term = f"%{search.strip()}%"
            filters.append(["campaign_name", "like", search_term])
        
        # Status filter
        if status_filter and status_filter != "all":
            filters.append(["status", "=", status_filter])
        
        # Type filter  
        if type_filter and type_filter != "all":
            filters.append(["type", "=", type_filter])
        
        # Active filter
        if active_filter and active_filter != "all":
            is_active = 1 if active_filter == "active" else 0
            filters.append(["is_active", "=", is_active])
        
        # Fields to select
        fields = [
            'name', 
            'campaign_name', 
            'description', 
            'is_active', 
            'owner_id', 
            'start_date', 
            'end_date', 
            'type', 
            'status', 
            'target_segment',
            'owner', 
            'creation', 
            'modified'
        ]
        
        # Get total count (for pagination)
        total_count = frappe.db.count('Campaign', filters=filters)
        
        # Get paginated data
        campaigns = frappe.get_list(
            'Campaign',
            fields=fields,
            filters=filters,
            order_by=order_by,
            limit_start=offset,
            limit_page_length=limit
        )
        
        # Calculate pagination info
        total_pages = math.ceil(total_count / limit) if total_count > 0 else 1
        has_next = page < total_pages
        has_prev = page > 1
        
        # Format campaign data
        formatted_campaigns = []
        for campaign in campaigns:
            # Add display status for UI
            campaign['displayStatus'] = campaign.get('status', 'DRAFT')
            
            # Format dates
            if campaign.get('start_date'):
                campaign['start_date'] = str(campaign['start_date'])
            if campaign.get('end_date'):
                campaign['end_date'] = str(campaign['end_date'])
            
            # Add owner display name
            if campaign.get('owner_id'):
                try:
                    user_doc = frappe.get_doc('User', campaign['owner_id'])
                    campaign['owner_name'] = user_doc.get('full_name') or user_doc.get('first_name') or campaign['owner_id']
                except:
                    campaign['owner_name'] = campaign['owner_id']
            
            formatted_campaigns.append(campaign)
        
        return {
            "success": True,
            "data": formatted_campaigns,
            "pagination": {
                "page": page,
                "limit": limit,
                "total": total_count,
                "pages": total_pages,
                "has_next": has_next,
                "has_prev": has_prev,
                "showing_from": offset + 1 if total_count > 0 else 0,
                "showing_to": min(offset + limit, total_count),
                "filters_applied": {
                    "search": search,
                    "status_filter": status_filter,
                    "type_filter": type_filter,
                    "active_filter": active_filter
                }
            }
        }
        
    except Exception as e:
        frappe.log_error(f"Error in get_campaigns_paginated: {str(e)}")
        return {
            "success": False,
            "message": f"Có lỗi xảy ra: {str(e)}",
            "data": [],
            "pagination": {
                "page": 1,
                "limit": limit,
                "total": 0,
                "pages": 1,
                "has_next": False,
                "has_prev": False
            }
        }

@frappe.whitelist() 
def get_campaign_stats():
    """
    API lấy thống kê tổng quan campaigns
    """
    try:
        # Đếm theo status
        status_stats = frappe.db.sql("""
            SELECT status, COUNT(*) as count
            FROM `tabCampaign`
            GROUP BY status
        """, as_dict=True)
        
        # Đếm theo type
        type_stats = frappe.db.sql("""
            SELECT type, COUNT(*) as count
            FROM `tabCampaign`
            GROUP BY type
        """, as_dict=True)
        
        # Đếm active/inactive
        active_stats = frappe.db.sql("""
            SELECT is_active, COUNT(*) as count
            FROM `tabCampaign`
            GROUP BY is_active
        """, as_dict=True)
        
        # Tổng số campaigns
        total_campaigns = frappe.db.count('Campaign')
        
        return {
            "success": True,
            "data": {
                "total": total_campaigns,
                "by_status": {item['status']: item['count'] for item in status_stats},
                "by_type": {item['type']: item['count'] for item in type_stats},
                "by_active": {item['is_active']: item['count'] for item in active_stats}
            }
        }
        
    except Exception as e:
        frappe.log_error(f"Error in get_campaign_stats: {str(e)}")
        return {
            "success": False,
            "message": f"Có lỗi xảy ra: {str(e)}",
            "data": {}
        }

@frappe.whitelist()
def search_campaigns(query="", limit=10):
    """
    API tìm kiếm campaigns nhanh (autocomplete)
    """
    try:
        if not query or len(query.strip()) < 2:
            return {"success": True, "data": []}
        
        search_term = f"%{query.strip()}%"
        
        campaigns = frappe.get_list(
            'Campaign',
            fields=['name', 'campaign_name', 'status', 'type'],
            filters=[
                ['campaign_name', 'like', search_term]
            ],
            order_by='modified desc',
            limit_page_length=int(limit)
        )
        
        return {
            "success": True,
            "data": campaigns
        }
        
    except Exception as e:
        frappe.log_error(f"Error in search_campaigns: {str(e)}")
        return {
            "success": False,
            "message": f"Có lỗi xảy ra: {str(e)}",
            "data": []
        } 