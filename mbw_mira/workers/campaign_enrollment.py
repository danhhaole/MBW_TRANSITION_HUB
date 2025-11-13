import frappe
from frappe.utils import now_datetime,add_days
from mbw_mira.api.external_connections import share_job_posting


def attraction_campaign(campaign_id):
    """
    Worker: Chạy campaign thu hút
    Chiến dịch thu hút chỉ gửi qua kênh socaial
    """
    campaign = frappe.get_doc("Mira Campaign", campaign_id)
    #Lấy Mira campaign social
    campaign_socials = frappe.get_all("Mira Campaign Social",filters={"campaign_id":campaign_id,"status":"Pending"},fields=["*"])
    if campaign_socials:
        for cps in campaign_socials:
            if cps and cps.external_connection:
                #Kiểm tra nếu social thì gọi share
                if cps.platform in  ['Facebook','Zalo', 'TopCV']:
                    share_job_posting(cps.external_connection,campaign_id,cps.template_content, campaign.ladipage_url, cps.social_media_images)
                    
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
    campaign = frappe.get_doc("Mira Campaign", campaign_id)
    #Lấy Mira campaign social
    campaign_socials = frappe.get_all("Mira Campaign Social",filters={"campaign_id":campaign_id,"status":"Pending"},fields=["*"])
    if campaign_socials:
        for cps in campaign_socials:
            if cps and cps.external_connection:
                if cps.platform in  ['Facebook','Zalo', 'TopCV']:
                    share_job_posting(cps.external_connection,campaign_id,cps.template_content, campaign.ladipage_url, cps.social_media_images)
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
        frappe.publish_realtime('enroll_talent_campaign', message={'campaign': campaign})
        return count
    except Exception as e:
        frappe.log_error(frappe.get_traceback())
        return count



def _get_talents_segment_for_campaign(campaign_id):
    """
    Lấy danh talentSegment từ Campaign (Mira Talent Pool)
    Lấy Mira Prospect từ talentsegment
    """
    target_pool = frappe.db.get_value("Mira Campaign", campaign_id, "target_pool")
    talent_profiles = frappe.get_all(
        "Mira Talent Pool",
        filters={"segment_id": target_pool},
        fields=["talent_id"],
    )

    return talent_profiles


def _get_first_campaign_step(campaign_id):
    """
    Lấy bước đầu tiên (step_order nhỏ nhất) của CampaignStep
    """
    # step = frappe.get_all(
    #     "Mira Campaign Step",
    #     filters={"campaign": campaign_id},
    #     fields=["name", "step_order","delay_in_days"],
    #     order_by="step_order asc",
    #     limit=1,
    # )
    
    # return step[0] if step else None
    


def _create_talent_campaign(campaign_id, profile, first_step):
    """
    Tạo mới Mira Talent Campaign, chỉ set current_step_order nếu có
    """
    try:
        next_action_at = add_days(now_datetime(), first_step.get("delay_in_days") or 0)
        if not _check_exists(campaign_id,profile.get("talent_id")):
            doc = frappe.get_doc(
                {
                    "doctype": "Mira Talent Campaign",
                    "campaign_id": campaign_id,
                    "talent_id": profile.get("talent_id"),
                    "status": "ACTIVE",
                    "enrolled_at": now_datetime(),
                    "current_step_order": first_step.get("step_order")  or 1,
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