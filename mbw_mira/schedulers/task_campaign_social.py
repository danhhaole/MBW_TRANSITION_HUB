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
def run_campaign_social_email(sync_mode=False):
    """Lấy ra danh sách socail email tìm campaign lấy ra danh sách
    sync_mode: If True, run synchronously for testing (not via queue)
    """
    logger = frappe.logger("campaign_scheduler")
    now = now_datetime()
    #Lấy ra thời gian trong vòng 60s
    before_60s = add_to_date(now, seconds=-60)
    after_60s = add_to_date(now, seconds=60)
    
    print(f"\n{'='*80}")
    print(f"[SCHEDULER] run_campaign_social_email START")
    print(f"[SCHEDULER] Current time: {now}")
    print(f"[SCHEDULER] Checking campaigns between {before_60s} and {after_60s}")
    print(f"[SCHEDULER] Sync mode: {sync_mode}")
    print(f"{'='*80}\n")
    
    logger.info(f"[SCHEDULER] Checking Email campaigns between {before_60s} and {after_60s}")
    
    campaign_social_email = frappe.get_all(
        "Mira Campaign Social",
        {"is_active": 1, "platform": "Email", "status": "Pending","post_schedule_time":["between", [before_60s, after_60s]]},order_by="post_schedule_time asc"
    )
    
    print(f"[SCHEDULER] Found {len(campaign_social_email)} Email campaigns")
    logger.info(f"[SCHEDULER] Found {len(campaign_social_email)} Email campaigns")
    
    if campaign_social_email:
        for cpe in campaign_social_email:
            print(f"[SCHEDULER] Processing campaign: {cpe.name}")
            logger.info(f"[SCHEDULER] Processing campaign: {cpe.name}")
            
            if sync_mode:
                # Run synchronously for testing
                print(f"[SCHEDULER] Running synchronously (test mode)...")
                from mbw_mira.workers.process_action import enroll_talent_campaign
                count = enroll_talent_campaign(cpe)
                print(f"[SCHEDULER] Enrolled {count} talents")
                
                # Also process email actions immediately
                print(f"[SCHEDULER] Processing email actions...")
                from mbw_mira.schedulers.task_action import send_email_action_campaign
                send_email_action_campaign()
                print(f"[SCHEDULER] Email actions processed")
            else:
                # Normal mode: enqueue to worker
                print(f"[SCHEDULER] Enqueuing to worker queue...")
                frappe.enqueue(
                    "mbw_mira.workers.process_action.enroll_talent_campaign",
                    social=cpe,          
                    queue="short"
                )
                print(f"[SCHEDULER] Enqueued successfully")
    else:
        print("[SCHEDULER] No campaigns to process")
        logger.info("[SCHEDULER] No campaigns to process")
    
    print(f"\n{'='*80}")
    print(f"[SCHEDULER] run_campaign_social_email END")
    print(f"{'='*80}\n")
    
    return len(campaign_social_email)

