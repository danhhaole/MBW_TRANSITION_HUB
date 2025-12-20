import frappe
from frappe import _

@frappe.whitelist(allow_guest=True)
def redirect_short_url():
    """
    Xử lý redirect từ short URL sang long URL
    Hỗ trợ format: /short.x.y
    """
    try:
        # Lấy path từ request
        path = frappe.request.path

        # Parse short code từ path /short.x.y
        if '/short.' in path:
            # Tách phần sau /short.
            parts = path.split('/short.')
            if len(parts) > 1:
                # Lấy x.y và ghép lại thành short_code
                code_parts = parts[1].split('.')
                if len(code_parts) >= 2:
                    short_code = code_parts[0] + code_parts[1]
                else:
                    short_code = code_parts[0]

                # Tìm long URL từ database
                short_url_doc = frappe.db.get_value(
                    "Mira Short URL",
                    {"short_code": short_code},
                    ["long_url", "name"],
                    as_dict=True
                )

                if short_url_doc and short_url_doc.long_url:
                    # Redirect về long URL
                    frappe.local.response["type"] = "redirect"
                    frappe.local.response["location"] = short_url_doc.long_url
                    return

        # Nếu không tìm thấy, trả về 404
        frappe.local.response.http_status_code = 404
        return "<h1>404 - Short URL not found</h1>"

    except Exception as e:
        frappe.log_error(f"Short URL redirect error: {str(e)}")
        frappe.local.response.http_status_code = 404
        return "<h1>404 - Error processing short URL</h1>"
