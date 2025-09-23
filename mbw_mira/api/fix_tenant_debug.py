import frappe
import requests
import json

@frappe.whitelist()
def test_different_tenant_names():
    """Test với các tenant_name khác nhau để tìm ra tenant_name đúng"""
    try:
        print("=== TEST DIFFERENT TENANT NAMES ===")
        
        # Lấy connection hiện tại
        connections = frappe.get_all(
            "External Connection",
            filters={"active_status": 1, "platform_type": "Facebook"},
            fields=["name", "tenant_name", "user_email"]
        )
        
        if not connections:
            return {"status": "error", "message": "No Facebook connections found"}
        
        conn = connections[0]
        print(f"Current connection: {conn.name}")
        print(f"Current tenant_name: {conn.tenant_name}")
        print(f"User email: {conn.user_email}")
        
        # Các tenant_name có thể thử
        test_tenants = [
            conn.tenant_name,  # Hiện tại
            "http://localhost:8000",  # Local
            "https://localhost:8000",  # Local HTTPS
            "http://127.0.0.1:8000",  # Local IP
            "https://127.0.0.1:8000",  # Local IP HTTPS
            "localhost",  # Chỉ hostname
            "127.0.0.1",  # Chỉ IP
            "mbw.ts",  # Site name
            "https://mbw.ts",  # Site name với HTTPS
        ]
        
        socialhub_host = frappe.conf.get("socialhub") or "https://socialhub.mbwcloud.com"
        fb_url = f"{socialhub_host}/api/method/mbw_socialhub.api.facebook.get_page_list"
        
        results = []
        
        for tenant in test_tenants:
            print(f"\nTesting tenant: {tenant}")
            
            params = {
                "tenant_name": tenant,
                "email": conn.user_email
            }
            
            try:
                response = requests.get(fb_url, params=params, timeout=10)
                data = response.json()
                pages = data.get("message", [])
                
                result = {
                    "tenant_name": tenant,
                    "status_code": response.status_code,
                    "pages_count": len(pages),
                    "pages": pages[:3] if pages else []  # Chỉ lấy 3 pages đầu
                }
                results.append(result)
                
                print(f"  Status: {response.status_code}, Pages: {len(pages)}")
                if pages:
                    print(f"  Sample pages: {[p.get('page_name', 'Unknown') for p in pages[:3]]}")
                    
            except Exception as e:
                print(f"  Error: {e}")
                results.append({
                    "tenant_name": tenant,
                    "error": str(e)
                })
        
        # Tìm tenant_name có pages
        working_tenants = [r for r in results if r.get("pages_count", 0) > 0]
        
        if working_tenants:
            print(f"\n✅ Found {len(working_tenants)} working tenant(s):")
            for tenant in working_tenants:
                print(f"  - {tenant['tenant_name']}: {tenant['pages_count']} pages")
            
            # Cập nhật connection với tenant_name đầu tiên có pages
            best_tenant = working_tenants[0]
            print(f"\nUpdating connection to use: {best_tenant['tenant_name']}")
            
            frappe.db.set_value("External Connection", conn.name, "tenant_name", best_tenant['tenant_name'])
            frappe.db.commit()
            
            # Test sync lại
            print("Testing sync after update...")
            sync_result = frappe.call("mbw_mira.api.external_connections.sync_accounts", 
                                   connection_id=conn.name, 
                                   force_sync=True)
            print(f"Sync result: {sync_result}")
            
        else:
            print("\n❌ No working tenant found. Possible issues:")
            print("1. Facebook pages not connected on SocialHub")
            print("2. Wrong user email")
            print("3. SocialHub configuration issue")
        
        print("\n=== END TEST ===")
        return {"status": "success", "results": results, "working_tenants": working_tenants}
        
    except Exception as e:
        frappe.log_error(f"Tenant debug error: {str(e)}")
        return {"status": "error", "message": str(e)}
