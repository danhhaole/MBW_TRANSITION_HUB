import frappe
from frappe import _


@frappe.whitelist()
def search_emails(txt=None):
    """
    Tìm kiếm email từ các nguồn: User, Mira Talent, Mira Contact
    
    Args:
        txt (str): Text để tìm kiếm (tên hoặc email)
    
    Returns:
        list: Danh sách các tuple [full_name, email, name]
    """
    if not txt:
        return []
    
    txt = txt.strip().lower()
    if not txt:
        return []
    
    results = []
    seen_emails = set()  # Để tránh trùng lặp
    
    # 1. Tìm trong User (Frappe User)
    try:
        # Tìm kiếm với or_filters để tìm trong cả email và full_name
        users = frappe.get_all(
            "User",
            filters={
                "enabled": 1,
                "name": ["!=", "Guest"]
            },
            or_filters=[
                ["email", "like", f"%{txt}%"],
                ["full_name", "like", f"%{txt}%"],
                ["name", "like", f"%{txt}%"]
            ],
            fields=["name", "email", "full_name"],
            limit=50
        )
        
        for user in users:
            email = (user.get("email") or "").strip()
            full_name = (user.get("full_name") or "").strip()
            name = user.get("name", "")
            
            if not email:
                continue
            
            # Kiểm tra nếu email đã tồn tại
            if email.lower() in seen_emails:
                continue
            
            # Kiểm tra lại điều kiện tìm kiếm
            if (txt in email.lower() or 
                txt in full_name.lower() or 
                txt in name.lower()):
                results.append([full_name or name, email, name])
                seen_emails.add(email.lower())
    except Exception as e:
        frappe.log_error(f"Error searching users: {str(e)}", "search_emails")
    
    # 2. Tìm trong Mira Talent
    try:
        talents = frappe.get_all(
            "Mira Talent",
            filters={},
            or_filters=[
                ["email", "like", f"%{txt}%"],
                ["full_name", "like", f"%{txt}%"],
                ["name", "like", f"%{txt}%"]
            ],
            fields=["name", "email", "full_name"],
            limit=50
        )
        
        for talent in talents:
            email = (talent.get("email") or "").strip()
            full_name = (talent.get("full_name") or "").strip()
            name = talent.get("name", "")
            
            if not email:
                continue
            
            # Kiểm tra nếu email đã tồn tại
            if email.lower() in seen_emails:
                continue
            
            # Kiểm tra lại điều kiện tìm kiếm
            if (txt in email.lower() or 
                txt in full_name.lower() or 
                txt in name.lower()):
                results.append([full_name or name, email, name])
                seen_emails.add(email.lower())
    except Exception as e:
        frappe.log_error(f"Error searching Mira Talent: {str(e)}", "search_emails")
    
    # 3. Tìm trong Mira Contact (nếu doctype tồn tại)
    try:
        if frappe.db.exists("DocType", "Mira Contact"):
            contacts = frappe.get_all(
                "Mira Contact",
                filters={},
                or_filters=[
                    ["email", "like", f"%{txt}%"],
                    ["full_name", "like", f"%{txt}%"],
                    ["name", "like", f"%{txt}%"]
                ],
                fields=["name", "email", "full_name"],
                limit=50
            )
            
            for contact in contacts:
                email = (contact.get("email") or "").strip()
                full_name = (contact.get("full_name") or "").strip()
                name = contact.get("name", "")
                
                if not email:
                    continue
                
                # Kiểm tra nếu email đã tồn tại
                if email.lower() in seen_emails:
                    continue
                
                # Kiểm tra lại điều kiện tìm kiếm
                if (txt in email.lower() or 
                    txt in full_name.lower() or 
                    txt in name.lower()):
                    results.append([full_name or name, email, name])
                    seen_emails.add(email.lower())
    except Exception as e:
        frappe.log_error(f"Error searching Mira Contact: {str(e)}", "search_emails")
    
    # Sắp xếp kết quả theo full_name
    results.sort(key=lambda x: (x[0] or "").lower())
    
    # Giới hạn số lượng kết quả
    return results[:100]

