"""
Birthday API - API endpoints cho birthday reminder system từ talent pools
"""

import frappe
from frappe.utils import nowdate
from mbw_mira.schedulers.birthday_scheduler import run_daily_birthday_check, run_migration_birthday_check, get_birthday_dashboard_stats

@frappe.whitelist()
def trigger_birthday_check(migration_run=False):
    """
    API endpoint để trigger birthday check manually từ Campaign Management

    Args:
        migration_run (bool): True nếu đây là migration run
    """
    try:
        result = run_daily_birthday_check(migration_run=migration_run)

        if result.get("success"):
            return {
                "status": "success",
                "message": f"Birthday check completed. Found {result['birthday_found']} birthdays, sent {result['emails_sent']} emails.",
                "data": result
            }
        else:
            return {
                "status": "error",
                "message": f"Birthday check failed: {result.get('error', 'Unknown error')}",
                "data": result
            }

    except Exception as e:
        frappe.log_error(f"Error in trigger_birthday_check: {str(e)}", "Birthday API")
        return {
            "status": "error",
            "message": f"API error: {str(e)}"
        }

@frappe.whitelist()
def get_birthday_stats_for_campaign():
    """
    Lấy thống kê birthday cho Campaign Management dashboard
    """
    try:
        stats = get_birthday_dashboard_stats()

        # Format for frontend display
        return {
            "status": "success",
            "data": {
                "today": {
                    "talents_checked": stats["today"]["total_talents_checked"],
                    "birthdays_found": stats["today"]["birthday_talents_found"],
                    "emails_sent": stats["today"]["emails_sent_successfully"],
                    "emails_failed": stats["today"]["emails_failed"],
                    "status": stats["today"]["status"]
                },
                "monthly": {
                    "total_talents": stats["last_30_days"]["total_checked"],
                    "total_birthdays": stats["last_30_days"]["total_birthdays"],
                    "total_emails_sent": stats["last_30_days"]["total_sent"],
                    "success_rate": stats["last_30_days"]["success_rate"],
                    "total_runs": stats["last_30_days"]["total_runs"]
                }
            }
        }

    except Exception as e:
        frappe.log_error(f"Error in get_birthday_stats_for_campaign: {str(e)}", "Birthday API")
        return {
            "status": "error",
            "message": f"Failed to get stats: {str(e)}"
        }

@frappe.whitelist()
def get_talent_pools_with_birthdays():
    """
    Lấy danh sách talent pools có ứng viên sinh nhật hôm nay
    """
    try:
        pools = frappe.db.sql("""
            SELECT tp.segment_id as pool_name,
                   COUNT(DISTINCT t.name) as birthday_count,
                   GROUP_CONCAT(DISTINCT t.full_name SEPARATOR ', ') as talent_names
            FROM `tabMira Talent` t
            INNER JOIN `tabMira Talent Pool` tp ON tp.talent_id = t.name
            WHERE t.date_of_birth IS NOT NULL
            AND t.email IS NOT NULL
            AND t.email != ''
            AND (t.email_opt_out = 0 OR t.email_opt_out IS NULL)
            AND MONTH(t.date_of_birth) = MONTH(CURDATE())
            AND DAY(t.date_of_birth) = DAY(CURDATE())
            GROUP BY tp.segment_id
            ORDER BY birthday_count DESC
        """, as_dict=True)

        return {
            "status": "success",
            "data": pools
        }

    except Exception as e:
        frappe.log_error(f"Error in get_talent_pools_with_birthdays: {str(e)}", "Birthday API")
        return {
            "status": "error",
            "message": f"Failed to get pools: {str(e)}"
        }

@frappe.whitelist()
def get_pool_birthday_details(pool_name):
    """
    Lấy chi tiết ứng viên sinh nhật trong một pool

    Args:
        pool_name (str): Tên của talent pool
    """
    try:
        talents = frappe.db.sql("""
            SELECT t.name, t.full_name, t.email, t.date_of_birth
            FROM `tabMira Talent` t
            INNER JOIN `tabMira Talent Pool` tp ON tp.talent_id = t.name
            WHERE tp.segment_id = %s
            AND t.date_of_birth IS NOT NULL
            AND t.email IS NOT NULL
            AND t.email != ''
            AND (t.email_opt_out = 0 OR t.email_opt_out IS NULL)
            AND MONTH(t.date_of_birth) = MONTH(CURDATE())
            AND DAY(t.date_of_birth) = DAY(CURDATE())
        """, (pool_name,), as_dict=True)

        return {
            "status": "success",
            "data": {
                "pool_name": pool_name,
                "birthday_talents": talents,
                "count": len(talents)
            }
        }

    except Exception as e:
        frappe.log_error(f"Error in get_pool_birthday_details: {str(e)}", "Birthday API")
        return {
            "status": "error",
            "message": f"Failed to get pool details: {str(e)}"
        }

@frappe.whitelist()
def run_birthday_test():
    """Chạy full test birthday system"""
    try:
        from mbw_mira.utils.birthday_test import run_birthday_test
        result = run_birthday_test()
        return {
            "status": "success",
            "data": result
        }
    except Exception as e:
        frappe.log_error(f"Error in run_birthday_test: {str(e)}", "Birthday API")
        return {
            "status": "error",
            "message": f"Test failed: {str(e)}"
        }

@frappe.whitelist()
def test_birthday_data():
    """Test birthday data"""
    try:
        from mbw_mira.utils.birthday_test import test_birthday_data
        result = test_birthday_data()
        return {
            "status": "success",
            "data": result
        }
    except Exception as e:
        frappe.log_error(f"Error in test_birthday_data: {str(e)}", "Birthday API")
        return {
            "status": "error",
            "message": f"Data test failed: {str(e)}"
        }

@frappe.whitelist()
def test_email_sending(test_email=None):
    """Test email sending"""
    try:
        from mbw_mira.utils.birthday_test import test_email_sending
        result = test_email_sending(test_email)
        return {
            "status": "success",
            "data": result
        }
    except Exception as e:
        frappe.log_error(f"Error in test_email_sending: {str(e)}", "Birthday API")
        return {
            "status": "error",
            "message": f"Email test failed: {str(e)}"
        }
