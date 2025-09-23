import frappe
import requests
import json

@frappe.whitelist()
def debug_socialhub_api():
    """Debug SocialHub API calls"""
    try:
        print("=== DEBUG SOCIALHUB API ===")
        
        # Get connection details
        connections = frappe.get_all(
            "External Connection",
            filters={"active_status": 1, "platform_type": "Facebook"},
            fields=["name", "platform_type", "connection_status", "user_email", "tenant_name"]
        )
        
        if not connections:
            return {"status": "error", "message": "No Facebook connections found"}
        
        conn = connections[0]
        print(f"Testing with connection: {conn.name}")
        print(f"  - User email: {conn.user_email}")
        print(f"  - Tenant name: {conn.tenant_name}")
        
        # Test SocialHub Facebook API
        socialhub_host = frappe.conf.get("socialhub") or "https://socialhub.mbwcloud.com"
        print(f"  - SocialHub host: {socialhub_host}")
        
        # Test get_page_list API
        fb_url = f"{socialhub_host}/api/method/mbw_socialhub.api.facebook.get_page_list"
        params = {
            "tenant_name": conn.tenant_name,
            "email": conn.user_email
        }
        
        print(f"\n1. Testing Facebook get_page_list API:")
        print(f"  URL: {fb_url}")
        print(f"  Params: {params}")
        
        try:
            response = requests.get(fb_url, params=params, timeout=30)
            print(f"  Status: {response.status_code}")
            print(f"  Response: {response.text[:500]}...")
            
            if response.status_code == 200:
                data = response.json()
                pages = data.get("message", [])
                print(f"  Pages found: {len(pages)}")
                for page in pages:
                    print(f"    - {page.get('page_name', 'Unknown')} (ID: {page.get('external_page_id', 'Unknown')})")
            else:
                print(f"  Error: {response.text}")
                
        except Exception as e:
            print(f"  Request error: {e}")
        
        # Test other SocialHub APIs
        print(f"\n2. Testing other SocialHub APIs:")
        
        # Test connection status
        status_url = f"{socialhub_host}/api/method/mbw_socialhub.api.facebook.test_connection"
        try:
            status_response = requests.get(status_url, params=params, timeout=10)
            print(f"  Test connection: {status_response.status_code} - {status_response.text[:200]}")
        except Exception as e:
            print(f"  Test connection error: {e}")
        
        print("\n=== END DEBUG ===")
        return {"status": "success", "message": "Debug completed"}
        
    except Exception as e:
        frappe.log_error(f"SocialHub debug error: {str(e)}")
        return {"status": "error", "message": str(e)}
