from datetime import time, timedelta,datetime
import pytz
import frappe
from frappe.utils import now_datetime

def get_next_working_time(now=None, tz_name="Asia/Ho_Chi_Minh"):
    tz = pytz.timezone(tz_name)
    now = now or now_datetime()
    now = now.astimezone(tz)

    # Giờ hành chính
    WORK_START = time(8, 0)
    WORK_END = time(17, 0)

    # Nếu đang trong giờ làm việc -> dùng luôn
    if WORK_START <= now.time() <= WORK_END and now.weekday() < 5:
        return now

    # Nếu sau giờ làm -> chuyển sang 9h sáng hôm sau
    if now.time() > WORK_END or now.weekday() >= 5:
        next_day = now + timedelta(days=1)
        # Nếu rơi vào cuối tuần, đẩy đến thứ 2
        while next_day.weekday() >= 5:
            next_day += timedelta(days=1)
        return tz.localize(next_day.replace(hour=9, minute=0, second=0, microsecond=0))

    # Nếu trước giờ làm
    if now.time() < WORK_START:
        return tz.localize(now.replace(hour=9, minute=0, second=0, microsecond=0))

# Utility functions
def get_business_hours_schedule(timezone_str="Asia/Ho_Chi_Minh"):
	"""Get next business hours datetime"""
	try:
		tz = pytz.timezone(timezone_str)
		now_tz = datetime.now(tz)
		
		business_start = time(8, 0)
		business_end = time(17, 0)
		
		# If within business hours on weekday, return now
		if (now_tz.weekday() < 5 and 
		    business_start <= now_tz.time() <= business_end):
			return now_tz.replace(tzinfo=None)
		
		# Find next business day start time
		next_day = now_tz
		while True:
			if next_day.weekday() < 5:  # Monday-Friday
				next_schedule = next_day.replace(
					hour=business_start.hour,
					minute=business_start.minute,
					second=0,
					microsecond=0
				)
				if next_schedule > now_tz:
					return next_schedule.replace(tzinfo=None)
			next_day = next_day + timedelta(days=1)
			
	except Exception as e:
		frappe.log_error(f"Business hours schedule error: {str(e)}")
		return now_datetime()


def get_user_timezone_string():
	"""Get user timezone string or default"""
	try:
		user_tz = frappe.db.get_value("User", frappe.session.user, "time_zone")
		if user_tz:
			return user_tz
		
		system_tz = frappe.db.get_single_value("System Settings", "time_zone")
		if system_tz:
			return system_tz
			
		return "Asia/Ho_Chi_Minh"
	except Exception:
		return "Asia/Ho_Chi_Minh"
