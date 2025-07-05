import frappe
from frappe.utils import now
import traceback

def log_to_view_log(method: str, status: str, error: str = None):
    """
    Ghi một log vào Scheduled Job Log (View Log)

    Args:
        method (str): tên phương thức hoặc mô tả, ví dụ: "my_app.tasks.do_something"
        status (str): "Success" hoặc "Failed"
        error (str): chuỗi lỗi (nếu có)
    """
    log = frappe.get_doc({
        "doctype": "Scheduled Job Log",
        "status": status,
        "method": method,
        "scheduled_at": now(),
        "error": error
    })
    log.insert(ignore_permissions=True)
