import frappe
from frappe.utils import now_datetime,add_days
from mbw_mira.api.external_connections import share_job_posting


def attraction_campaign(campaign_id):
    """
    Worker: Chạy campaign thu hút
    """
    campaign = frappe.get_doc("Mira Campaign", campaign_id)
    #Lấy Mira campaign social
    campaign_socials = frappe.get_all("Mira Campaign Social",filters={"campaign_id":campaign_id,"status":"Pending"},fields=["*"])
    if campaign_socials:
        for cps in campaign_socials:
            if cps and cps.external_connection:
                #Chạy post lên
                share_job_posting(cps.external_connection,campaign_id,cps.template_content, campaign.ladipage_url, cps.social_media_images)
            else:
                continue

def nurture_campaign(campaign_id):
    """
    Worker: Chạy campaign nuôi dưỡng
    """
    campaign = frappe.get_doc("Mira Campaign", campaign_id)
    #Lấy Mira campaign social
    campaign_socials = frappe.get_all("Mira Campaign Social",filters={"campaign_id":campaign_id,"status":"Pending"},fields=["*"])
    if campaign_socials:
        for cps in campaign_socials:
            if cps and cps.external_connection:
                #Chạy post lên
                share_job_posting(cps.external_connection,campaign_id,cps.template_content, campaign.ladipage_url, cps.social_media_images)
            else:
                continue



def recruitment_campaign(campaign_id):
    """
    Worker: Chạy campaign tuyển dụng
    """
    campaign = frappe.get_doc("Mira Campaign", campaign_id)
    #Lấy Mira campaign social
    campaign_socials = frappe.get_all("Mira Campaign Social",filters={"campaign_id":campaign_id,"status":"Pending"},fields=["*"])
    if campaign_socials:
        for cps in campaign_socials:
            if cps and cps.external_connection:
                #Chạy post lên
                share_job_posting(cps.external_connection,campaign_id,cps.template_content, campaign.ladipage_url, cps.social_media_images)
            else:
                continue
