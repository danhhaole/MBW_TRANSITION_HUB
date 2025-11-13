import frappe
from frappe.utils import now_datetime,add_days,add_to_date
from mbw_mira.api.external_connections import share_job_posting
from mbw_mira.utils import _normalize_condition

def attraction_campaign(campaign_id):
    """
    Worker: Chạy campaign thu hút
    Chiến dịch thu hút chỉ gửi qua kênh socaial
    """
    campaign = frappe.get_doc("Mira Campaign", campaign_id)
    now = now_datetime()
    before_60s = add_to_date(now, seconds=-60)
    after_60s = add_to_date(now, seconds=60)
    #Lấy Mira campaign social
    campaign_socials = frappe.get_all("Mira Campaign Social",filters={"campaign_id":campaign_id,"status":"Pending"},fields=["*"])
    if campaign_socials:
        for cps in campaign_socials:
            if cps and cps.external_connection:
                #Kiểm tra nếu social thì gọi share
                if cps.platform in  ['Facebook','Zalo', 'TopCV']:
                    if cps.post_schedule_time:#Kiểm tra thời gian post nếu cầu hình delay
                        if cps.post_schedule_time >=before_60s and cps.post_schedule_time <= after_60s:
                            share_job_posting(cps.external_connection,campaign_id,campaign.ladipage_url, cps.social_media_images,cps.template_content)
                    else:
                        share_job_posting(cps.external_connection,campaign_id,campaign.ladipage_url, cps.social_media_images,cps.template_content)
                    
            else:
                continue

def nurture_campaign(campaign_id):
    """
    Worker: Chạy campaign nuôi dưỡng
    Chiến dịch nuôi dưỡng sẽ chỉ tiếp cận qua các kênh:Email, ZaloOA
    """
    campaign = frappe.get_doc("Mira Campaign", campaign_id)
    #Lấy Mira campaign social
    #Tạo talent campaign
    _enroll_talent_for_campaign(campaign)
    # campaign_socials = frappe.get_all("Mira Campaign Social",filters={"campaign_id":campaign_id,"status":"Pending"},fields=["*"])
    # if campaign_socials:
    #     for cps in campaign_socials:
    #         if cps and cps.external_connection:
    #             if cps.platform in  ['Zalo']:
    #                 share_job_posting(cps.external_connection,campaign_id,cps.template_content, campaign.ladipage_url, cps.social_media_images)
    #             else:
    #                 #Gửi email
    #                 pass
    #         else:
    #             continue



def recruitment_campaign(campaign_id):
    """
    Worker: Chạy campaign tuyển dụng
    Chiến dịch này chạy trên cả
    """
    now = now_datetime()
    before_60s = add_to_date(now, seconds=-60)
    after_60s = add_to_date(now, seconds=60)
    campaign = frappe.get_doc("Mira Campaign", campaign_id)

    #Chiến dịch này có kích hoạt gửi email
    _enroll_talent_for_campaign(campaign)
    
    #Lấy Mira campaign social
    campaign_socials = frappe.get_all("Mira Campaign Social",filters={"campaign_id":campaign_id,"status":"Pending"},fields=["*"])
    if campaign_socials:
        for cps in campaign_socials:
            if cps and cps.external_connection:
                #Kiểm tra nếu social thì gọi share
                if cps.platform in  ['Facebook','Zalo', 'TopCV']:
                    if cps.post_schedule_time:#Kiểm tra thời gian post nếu cầu hình delay
                        if cps.post_schedule_time >=before_60s and cps.post_schedule_time <= after_60s:
                            share_job_posting(cps.external_connection,campaign_id,campaign.ladipage_url, cps.social_media_images,cps.template_content)
                    else:
                        share_job_posting(cps.external_connection,campaign_id,campaign.ladipage_url, cps.social_media_images,cps.template_content)
            else:
                continue
                


def _enroll_talent_for_campaign(campaign):
    """
    Worker: tìm ứng viên từ Mira Talent theo campaign và tạo Mira Talent Campaign.
    """
    talent_profiles = _get_talents_segment_for_campaign(campaign)

    if not talent_profiles:
        return

    # tìm bước đầu tiên trong CampaignStep (nếu có)
    first_step = _get_first_campaign_step(campaign)

    count = 0
    try:
        
        if first_step and talent_profiles:
            for profile in talent_profiles:
                _create_talent_campaign(campaign, profile, first_step)
                count += 1
        #frappe.publish_realtime('enroll_talent_campaign', message={'campaign': campaign})
        return count
    except Exception as e:
        frappe.log_error(frappe.get_traceback())
        return count



def _get_talents_segment_for_campaign(campaign):
    """
    Lấy danh sách talent từ Campaign (Mira Talent Pool)
    Áp dụng segment_id + condition nâng cao nếu có.
    """
    base_filter = [["segment_id", "=", campaign.talent_pool]]

    # Kiểm tra condition
    if getattr(campaign, "condition", None):
        try:
            normalized_condition = _normalize_condition(campaign.condition)
            combined_filter = [base_filter[0], "and", normalized_condition]
        except Exception as e:
            frappe.log_error(f"Error parsing campaign condition: {str(e)}")
            combined_filter = base_filter
    else:
        combined_filter = base_filter

    # Lấy danh sách talent
    talent_profiles = frappe.get_all(
        "Mira Talent Pool",
        filters=combined_filter,
        fields=["talent_id"]
    )

    return talent_profiles


def _get_first_campaign_step(campaign):
    """
    Lấy bước đầu tiên (step_order nhỏ nhất) của CampaignStep
    """
    step = frappe.get_all(
        "Mira Campaign Social",
        filters={"campaign_id": campaign.name, "status":"Pending"},
        fields=["*"],
        order_by="post_schedule_time asc",
        limit=1,
    )
    
    return step[0] if step else None
    


def _create_talent_campaign(campaign, profile, first_step):
    """
    Tạo mới Mira Talent Campaign, chỉ set current_step_order nếu có
    """
    try:
        next_action_at = add_days(first_step.post_schedule_time, 0)
        if not _check_exists(campaign.name,profile.get("talent_id")):
            doc = frappe.get_doc(
                {
                    "doctype": "Mira Talent Campaign",
                    "campaign_id": campaign.name,
                    "talent_id": profile.get("talent_id"),
                    "campaign_social":first_step.name,
                    "status": "ACTIVE",
                    "enrolled_at": now_datetime(),
                    "current_step_order": 1,
                    "next_action_at": next_action_at,
                }
            )
            doc.insert(ignore_permissions=True)
            frappe.db.commit()
            return doc.name
        else:
            return None
    except Exception as e:
        #frappe.log_error(f"talent_profiles {e}")
        return None

def _check_exists(campaign_id,talent_id):
    talent_campaign_exists = frappe.db.exists("Mira Talent Campaign",{"campaign_id":campaign_id,"talent_id":talent_id})
    if talent_campaign_exists:
        return True
    else:
        return False