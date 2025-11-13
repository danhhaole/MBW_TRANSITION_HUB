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
    campaign_socials = frappe.get_all("Mira Campaign Social",filters={"campaign_id":campaign_id,"status":"Pending"},fields=["*"])
    if campaign_socials:
        for cps in campaign_socials:
            if cps and cps.external_connection:
                if cps.platform in  ['Zalo']:
                    share_job_posting(cps.external_connection,campaign_id,cps.template_content, campaign.ladipage_url, cps.social_media_images)
                else:
                    #Gửi email
                    pass
            else:
                continue



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
