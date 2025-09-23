import frappe
import requests
import json

@frappe.whitelist()
def check_facebook_connection_status():
    """Kiểm tra trạng thái kết nối Facebook và hướng dẫn fix"""
    try:
        print("=== FACEBOOK CONNECTION STATUS CHECK ===")
        
        # Lấy connection hiện tại
        connections = frappe.get_all(
            "External Connection",
            filters={"active_status": 1, "platform_type": "Facebook"},
            fields=["name", "tenant_name", "user_email", "connection_status", "login_url"]
        )
        
        if not connections:
            return {"status": "error", "message": "No Facebook connections found"}
        
        conn = connections[0]
        print(f"Connection: {conn.name}")
        print(f"Status: {conn.connection_status}")
        print(f"User: {conn.user_email}")
        print(f"Tenant: {conn.tenant_name}")
        
        # Kiểm tra SocialHub API
        socialhub_host = frappe.conf.get("socialhub") or "https://socialhub.mbwcloud.com"
        
        # 1. Test get_page_list
        print("\n1. Testing get_page_list API...")
        fb_url = f"{socialhub_host}/api/method/mbw_socialhub.api.facebook.get_page_list"
        params = {
            "tenant_name": conn.tenant_name,
            "email": conn.user_email
        }
        
        try:
            response = requests.get(fb_url, params=params, timeout=10)
            data = response.json()
            pages = data.get("message", [])
            print(f"   Status: {response.status_code}")
            print(f"   Pages found: {len(pages)}")
            
            if pages:
                print("   ✅ Facebook pages are connected!")
                for page in pages:
                    print(f"     - {page.get('page_name', 'Unknown')} (ID: {page.get('external_page_id', 'Unknown')})")
            else:
                print("   ❌ No Facebook pages connected")
                
        except Exception as e:
            print(f"   Error: {e}")
        
        # 2. Test get_facebook_login_url
        print("\n2. Testing get_facebook_login_url API...")
        login_url_api = f"{socialhub_host}/api/method/mbw_socialhub.api.facebook.get_facebook_login_url"
        
        try:
            login_response = requests.get(login_url_api, params={
                "tenant_name": conn.tenant_name,
                "user_email": conn.user_email,
                "full_name": "Admin User",
                "hook_url": conn.tenant_name + "/api/method/mbw_mira.api.external_connections.handle_webhook",
                "redirect_url": conn.tenant_name + "/mbw_mira/connectors"
            }, timeout=10)
            
            login_data = login_response.json()
            login_url = login_data.get("message", {}).get("login_url")
            
            print(f"   Status: {login_response.status_code}")
            if login_url:
                print(f"   ✅ Login URL generated: {login_url}")
            else:
                print(f"   ❌ No login URL: {login_data}")
                
        except Exception as e:
            print(f"   Error: {e}")
        
        # 3. Hướng dẫn fix
        print("\n3. SOLUTION STEPS:")
        print("   To fix this issue, you need to:")
        print("   1. Go to SocialHub dashboard")
        print("   2. Login with email: admin@example.com")
        print("   3. Connect Facebook account")
        print("   4. Select Facebook pages to connect")
        print("   5. Grant necessary permissions:")
        print("      - pages_manage_posts")
        print("      - pages_read_engagement") 
        print("      - pages_show_list")
        print("   6. Complete the OAuth flow")
        print("   7. Then run sync again")
        
        # 4. Tạo login URL mới nếu cần
        if conn.login_url:
            print(f"\n4. Current login URL: {conn.login_url}")
        else:
            print("\n4. No login URL found. Creating new one...")
            try:
                new_login_url = frappe.call("mbw_mira.api.external_connections._get_facebook_login_url", 
                                          frappe.get_doc("External Connection", conn.name))
                if new_login_url:
                    frappe.db.set_value("External Connection", conn.name, "login_url", new_login_url)
                    frappe.db.commit()
                    print(f"   New login URL: {new_login_url}")
                else:
                    print("   Failed to generate login URL")
            except Exception as e:
                print(f"   Error generating login URL: {e}")
        
        print("\n=== END CHECK ===")
        return {"status": "success", "message": "Check completed"}
        
    except Exception as e:
        frappe.log_error(f"Facebook connection check error: {str(e)}")
        return {"status": "error", "message": str(e)}

@frappe.whitelist()
def force_sync_facebook_accounts():
    """Force sync Facebook accounts"""
    try:
        connections = frappe.get_all(
            "External Connection",
            filters={"active_status": 1, "platform_type": "Facebook"},
            fields=["name"]
        )
        
        if not connections:
            return {"status": "error", "message": "No Facebook connections found"}
        
        conn = connections[0]
        print(f"Force syncing accounts for: {conn.name}")
        
        result = frappe.call("mbw_mira.api.external_connections.sync_accounts", 
                           connection_id=conn.name, 
                           force_sync=True)
        
        print(f"Sync result: {result}")
        return result
        
    except Exception as e:
        frappe.log_error(f"Force sync error: {str(e)}")
        return {"status": "error", "message": str(e)}
