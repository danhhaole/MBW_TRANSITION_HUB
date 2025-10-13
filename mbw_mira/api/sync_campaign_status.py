import frappe

@frappe.whitelist()
def sync_campaign_status():
    """Đồng bộ status và is_active cho tất cả campaigns"""
    try:
        print("🔄 Bắt đầu đồng bộ status và is_active cho Campaign...")
        
        # Lấy tất cả campaigns
        campaigns = frappe.get_all(
            "Mira Campaign",
            fields=['name', 'status', 'is_active'],
            filters={}
        )
        
        updated_count = 0
        
        for campaign in campaigns:
            old_is_active = campaign.is_active
            new_is_active = 1 if campaign.status == "ACTIVE" else 0
            
            if old_is_active != new_is_active:
                frappe.db.set_value("Mira Campaign", campaign.name, 'is_active', new_is_active)
                updated_count += 1
                print(f"✅ Updated {campaign.name}: status={campaign.status}, is_active={old_is_active} -> {new_is_active}")
        
        frappe.db.commit()
        
        print(f"🎉 Hoàn thành! Đã cập nhật {updated_count}/{len(campaigns)} campaigns")
        
        # Hiển thị thống kê
        stats = frappe.db.sql("""
            SELECT status, is_active, COUNT(*) as count
            FROM `tabCampaign`
            GROUP BY status, is_active
            ORDER BY status, is_active
        """, as_dict=True)
        
        result = {
            "success": True,
            "message": f"Đã cập nhật {updated_count}/{len(campaigns)} campaigns",
            "updated_count": updated_count,
            "total_count": len(campaigns),
            "stats": stats
        }
        
        print("\n�� Thống kê hiện tại:")
        for stat in stats:
            print(f"  Status: {stat.status}, is_active: {stat.is_active} -> {stat.count} campaigns")
        
        return result
        
    except Exception as e:
        frappe.log_error(f"Error in sync_campaign_status: {str(e)}")
        return {
            "success": False,
            "message": f"Có lỗi xảy ra: {str(e)}"
        }
