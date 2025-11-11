import frappe
from datetime import datetime

#Task quét chiến dich thu hút để post bài
def run_attraction_campaign():
    """
    Scan ACTIVE campaigns and enqueue tasks.
    """
    today = datetime.now()
    campaigns = frappe.get_all(
        "Mira Campaign",
        filters={
            # "is_active": 1,
            "status": "ACTIVE",
            "start_date": ("<=", today),
            # "scheduled_at": (">=", today),
            "type":"ATTRACTION"
        },
        fields=["name", "campaign_name"]
    )
    
    for c in campaigns:
        frappe.enqueue(
            "mbw_mira.workers.task_campaign.attraction_campaign",
            campaign_id=c.name,
            job_name=c.name,
            queue="default",
            
        )
    return True

#Task quét chiến dịch nuôi dưỡng để đăng bài
def run_nurture_campaign():
    """
    Scan ACTIVE campaigns and enqueue tasks.
    """
    today = datetime.now()
    campaigns = frappe.get_all(
        "Mira Campaign",
        filters={
            # "is_active": 1,
            "status": "ACTIVE",
            "start_date": ("<=", today),
            # "scheduled_at": (">=", today),
            "type":"NURTURE"
        },
        fields=["name", "campaign_name"]
    )

    for c in campaigns:
        frappe.enqueue(
            "mbw_mira.workers.task_campaign.nurture_campaign",
            campaign_id=c.name,
            job_name=c.name,
            queue="default",
            
        )
    return True

#Task quét chiến dịch tuyển dụng để đăng bài
def run_recruitment_campaign():
    """
    Scan ACTIVE campaigns and enqueue tasks.
    """
    today = datetime.now()
    campaigns = frappe.get_all(
        "Mira Campaign",
        filters={
            # "is_active": 1,
            "status": "ACTIVE",
            "start_date": ("<=", today),
            # "scheduled_at": (">=", today),
            "type":"RECRUITMENT"
        },
        fields=["name", "campaign_name"]
    )

    for c in campaigns:
        frappe.enqueue(
            "mbw_mira.workers.task_campaign.recruitment_campaign",
            campaign_id=c.name,
            job_name=c.name,
            queue="default",
            
        )
    return True

