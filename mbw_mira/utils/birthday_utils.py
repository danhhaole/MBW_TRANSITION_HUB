
import frappe
from frappe.utils import getdate, nowdate
from mbw_mira.utils.email import send_email

def check_birthday(talent_doc):
    """
    Check if the talent's birthday is today.

    Args:
        talent_doc (dict): Talent document (or dict) containing 'date_of_birth'

    Returns:
        bool: True if birthday is today.
    """
    dob = talent_doc.get("date_of_birth")
    if not dob:
        return False

    try:
        today = getdate(nowdate())
        dob_date = getdate(dob)

        # Chỉ cần so sánh tháng và ngày
        is_today = (dob_date.month == today.month and dob_date.day == today.day)
        return is_today

    except Exception as e:
        error_msg = f"Error checking birthday for talent {talent_doc.get('name', 'unknown')}: {str(e)}"
        frappe.log_error(error_msg)
        return False

def check_birthday_in_pool(pool_name):
    """
    Check if any talent in the pool has a birthday today.
    Returns: (bool, list_of_logs)
    """
    logs = [f"🔍 Checking birthday for pool: {pool_name}"]
    try:
        if frappe.db.exists("DocType", "Mira Talent Pool"):
            # Use SQL Join to ensure we get date_of_birth from Mira Talent
            talents = frappe.db.sql("""
                SELECT t.name, t.date_of_birth, t.email, t.full_name
                FROM `tabMira Talent` t
                INNER JOIN `tabMira Talent Pool` tp ON tp.talent_id = t.name
                WHERE tp.segment_id = %s
            """, (pool_name,), as_dict=True)
        else:
            talents = frappe.db.sql("SELECT name, date_of_birth, email FROM `tabMira Talent` WHERE date_of_birth IS NOT NULL", as_dict=True)

        logs.append(f"-------- BIRTHDAY CHECK START FOR POOL: {pool_name} --------")
        logs.append(f"Current date: {getdate(nowdate())}")
        logs.append(f"Total talents found in pool: {len(talents)}")

        has_match = False
        talents_with_dob_count = 0
        eligible_talents = []

        for t in talents:
            dob = t.get('date_of_birth')
            email = t.get('email')
            name = t.get('full_name') or t.get('name', 'Unknown')

            if dob:
                talents_with_dob_count += 1
                dob_date = getdate(dob)
                today = getdate(nowdate())
                is_today = (dob_date.month == today.month and
                           dob_date.day == today.day)

                log_entry = (f"  > Talent {name} (Email: {email}): "
                           f"DOB={dob} | Is today: {is_today}")
                logs.append(log_entry)

                if is_today:
                    has_match = True
                    eligible_talents.append(f"{name} ({email} - {dob})")

        logs.append(f"\n📊 Summary:")
        logs.append(f"- {talents_with_dob_count}/{len(talents)} talents have DOB set")

        if eligible_talents:
            logs.append("\n🎂 Eligible talents for birthday email:")
            for talent in eligible_talents:
                logs.append(f"  - {talent}")
            logs.append(f"\n✅ Total eligible: {len(eligible_talents)}")
        else:
            logs.append("\nℹ️ No talents have birthday today")

        logs.append("----------------------------------------------------------")

        # Log to error log for easier debugging
        if has_match:
            frappe.log_error(
                f"🎂 Found {len(eligible_talents)} talents with birthday today in pool {pool_name}"
            )

        return has_match, logs

    except Exception as e:
        error_msg = f"❌ Error checking birthday in pool {pool_name}: {str(e)}"
        frappe.log_error(error_msg, "Birthday Check Error")
        logs.append(error_msg)
        return False, logs
