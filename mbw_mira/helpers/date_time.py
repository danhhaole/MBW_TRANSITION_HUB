from datetime import time, timedelta
import pytz
import frappe

def get_next_working_time(now=None, tz_name="Asia/Ho_Chi_Minh"):
    tz = pytz.timezone(tz_name)
    now = now or frappe.utils.now_datetime()
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

