#Kiểm tra các actions đang pending quá lâu, gửi thông báo nhắc nhở cho người được giao (assigned_to).
import frappe

#Quét talent trong talent pool không có tương tác sau 30 ngày từ khi tạo
def scan_talent_pool_interaction_cold():
    #lấy Danh sách segment đang active
    segments = frappe.get_all("Mira Segment",{"is_active":1})
    
    if segments:
        for seg in segments:
            frappe.enqueue(
                "mbw_mira.mbw_mira.doctype.mira_talent_pool.mira_talent_pool.cleanup_inactive_talent_pool",
                pool_id=seg.name,                
                queue="short"
            )
            
            