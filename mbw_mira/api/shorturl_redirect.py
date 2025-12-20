import frappe
from frappe import _
import logging

# Get a logger instance
log = logging.getLogger(__name__)

@frappe.whitelist(allow_guest=True)
def redirect_short_url():
    """
    Xử lý redirect từ short URL sang long URL
    Hỗ trợ format: /short.x.y
    """
    try:
        log.warning("--- SHORT URL REDIRECT TRIGGERED ---")
        path = frappe.request.path
        log.warning(f"Request path received: {path}")

        if '/short.' in path:
            parts = path.split('/short.')
            if len(parts) > 1:
                raw_code = parts[1]
                short_code = raw_code.replace('.', '')
                log.warning(f"Extracted short_code: {short_code}")

                short_url_doc = frappe.db.get_value(
                    "Mira Short URL",
                    {"short_code": short_code},
                    ["long_url"],
                    as_dict=True
                )

                if short_url_doc and short_url_doc.long_url:
                    log.warning(f"SUCCESS: Found long_url: {short_url_doc.long_url}")
                    frappe.local.response["type"] = "redirect"
                    frappe.local.response["location"] = short_url_doc.long_url
                    return
                else:
                    log.error(f"ERROR: Short code '{short_code}' not found in database.")
        else:
            log.error(f"ERROR: Path '{path}' does not contain '/short.'.")

        # Fallback to 404
        frappe.local.response.http_status_code = 404
        return "<h1>404 - Short URL not found</h1>"

    except Exception as e:
        log.error(f"CRITICAL ERROR in redirect_short_url: {str(e)}", exc_info=True)
        frappe.log_error(f"Short URL redirect error: {str(e)}")
        frappe.local.response.http_status_code = 500
        return "<h1>500 - Internal Server Error</h1>"
