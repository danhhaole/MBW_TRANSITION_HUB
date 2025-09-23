import frappe
from frappe import _

@frappe.whitelist()
def debug_connections():
    """Debug connections and accounts"""
    try:
        print("=== DEBUG SOCIALHUB CONNECTION ===")
        
        # 1. Kiểm tra connections hiện tại
        print("\n1. Kiểm tra External Connections:")
        connections = frappe.get_all(
            "External Connection",
            filters={"active_status": 1},
            fields=["name", "platform_type", "connection_status", "user_email", "tenant_name"]
        )
        
        result = {
            "total_connections": len(connections),
            "connections": []
        }
        
        for conn in connections:
            print(f"  - {conn.name}: {conn.platform_type} - {conn.connection_status}")
            
            # Kiểm tra accounts
            accounts = frappe.get_all(
                "External Connection Account",
                filters={"parent": conn.name, "is_active": 1},
                fields=["external_account_id", "account_name", "account_type", "is_primary"]
            )
            print(f"    Accounts: {len(accounts)}")
            
            conn_data = {
                "name": conn.name,
                "platform_type": conn.platform_type,
                "connection_status": conn.connection_status,
                "user_email": conn.user_email,
                "tenant_name": conn.tenant_name,
                "accounts": accounts
            }
            result["connections"].append(conn_data)
            
            for acc in accounts:
                print(f"      - {acc.account_name} ({acc.account_type})")
        
        # 2. Test sync accounts cho connection đầu tiên
        if connections:
            conn = connections[0]
            print(f"\n2. Test sync accounts cho: {conn.name}")
            
            try:
                sync_result = frappe.call("mbw_mira.api.external_connections.sync_accounts", 
                                   connection_id=conn.name, 
                                   force_sync=True)
                print(f"  Sync result: {sync_result}")
                result["sync_test"] = sync_result
            except Exception as e:
                print(f"  Sync error: {e}")
                result["sync_error"] = str(e)
        
        print("\n=== END DEBUG ===")
        return {"status": "success", "data": result}
        
    except Exception as e:
        frappe.log_error(f"Debug error: {str(e)}")
        return {"status": "error", "message": str(e)}
