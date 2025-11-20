import frappe
from frappe.utils import now_datetime, add_days,add_to_date

# Chạy campaign social được tạo ra
def run_campaign_social_facebook():
    """Lấy ra campaign social là facebook với các điều kiện
    đang hoạt động, platform là Facebook, thời gian post bài hoặc chạy campaign
    """
    now = now_datetime()
    #Lấy ra thời gian trong vòng 60s
    before_60s = add_to_date(now, seconds=-60)
    after_60s = add_to_date(now, seconds=60)
    campaign_social_facebooks = frappe.get_all(
        "Mira Campaign Social",
        {"is_active": 1, "platform": "Facebook", "status": "Pending","post_schedule_time":["between", [before_60s, after_60s]]},order_by="post_schedule_time asc"
    )
    if campaign_social_facebooks:
        for csf in campaign_social_facebooks:
            # Kiểm tra xem có thời gian post bài ko
            frappe.enqueue(
                "mbw_mira.workers.process_action.process_facebook_action",
                social=csf,
                campaign_id=csf.campaign_id,                
                queue="short"
            )

def run_campaign_social_zalo():
    """Lấy ra campaign social là facebook với các điều kiện
    đang hoạt động, platform là Facebook, thời gian post bài hoặc chạy campaign
    """
    now = now_datetime()
    #Lấy ra thời gian trong vòng 60s
    before_60s = add_to_date(now, seconds=-60)
    after_60s = add_to_date(now, seconds=60)
    campaign_social_zalo = frappe.get_all(
        "Mira Campaign Social",
        {"is_active": 1, "platform": "Zalo", "status": "Pending","post_schedule_time":["between", [before_60s, after_60s]]},order_by="post_schedule_time asc"
    )
    if campaign_social_zalo:
        for csf in campaign_social_zalo:
            # Kiểm tra xem có thời gian post bài ko
            frappe.enqueue(
                "mbw_mira.workers.process_action.process_facebook_action",
                social=csf,
                campaign_id=csf.campaign_id,                
                queue="short"
            )


def run_campaign_social_topcv():
    """Lấy ra campaign social là facebook với các điều kiện
    đang hoạt động, platform là Facebook, thời gian post bài hoặc chạy campaign
    """
    now = now_datetime()
    #Lấy ra thời gian trong vòng 60s
    before_60s = add_to_date(now, seconds=-60)
    after_60s = add_to_date(now, seconds=60)
    campaign_social_topcv = frappe.get_all(
        "Mira Campaign Social",
        {"is_active": 1, "platform": "TopCV", "status": "Pending","post_schedule_time":["between", [before_60s, after_60s]]},order_by="post_schedule_time asc"
    )
    if campaign_social_topcv:
        for csf in campaign_social_topcv:
            # Kiểm tra xem có thời gian post bài ko
            frappe.enqueue(
                "mbw_mira.workers.process_action.process_facebook_action",
                social=csf,
                campaign_id=csf.campaign_id,                
                queue="short"
            )

#Tạo talent campaign để sinh ra action gửi email đến từng talent
def run_campaign_social_email():
    """Lấy ra danh sách socail email tìm campaign lấy ra danh sách
    """
    now = now_datetime()
    #Lấy ra thời gian trong vòng 60s
    before_60s = add_to_date(now, seconds=-60)
    after_60s = add_to_date(now, seconds=60)
    campaign_social_email = frappe.get_all(
        "Mira Campaign Social",
        {"is_active": 1, "platform": "Email", "status": "Pending","post_schedule_time":["between", [before_60s, after_60s]]},order_by="post_schedule_time asc"
    )
    if campaign_social_email:
        for cpe in campaign_social_email:
            frappe.enqueue(
                "mbw_mira.workers.process_action.enroll_talent_campaign",
                social=cpe,          
                queue="short"
            )
