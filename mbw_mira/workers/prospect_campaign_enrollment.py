import frappe
from frappe.utils import now_datetime,add_days


def enroll_prospect_for_campaign(campaign_id):
    """
    Worker: tìm ứng viên từ Mira Prospect theo campaign và tạo Mira Talent Campaign.
    """
    mira_prospects = get_prospects_for_campaign(campaign_id)

    if not mira_prospects:
        return

    # tìm bước đầu tiên trong CampaignStep (nếu có)
    # first_step = get_first_campaign_step(campaign_id)

    count = 0
    try:
        
        if mira_prospects:
            for prospect in mira_prospects:
                create_prospect_campaign(campaign_id, prospect)
                count += 1
        frappe.publish_realtime('enroll_prospect_campaign', message={'campaign': campaign_id})
        return count
    except Exception as e:
        frappe.log_error(frappe.get_traceback())
        return count


def get_prospects_for_campaign(campaign_id):
    """
    Lấy Mira Prospect
    """
    mira_prospect = frappe.db.get_value("Campaign", campaign_id, "mira_prospect")
    return mira_prospect


def get_first_campaign_step(campaign_id):
    """
    Lấy bước đầu tiên (step_order nhỏ nhất) của CampaignStep
    """
    step = frappe.get_all(
        "CampaignStep",
        filters={"campaign": campaign_id},
        fields=["name", "step_order","delay_in_days"],
        order_by="step_order asc",
        limit=1,
    )
    
    return step[0] if step else None


def create_prospect_campaign(campaign_id, prospect):
    """
    Tạo mới Mira prospect Campaign, chỉ set current_step_order nếu có
    """
    try:
        next_action_at = add_days(now_datetime(), 0)
        if not check_exists(campaign_id,prospect):
            doc = frappe.get_doc(
                {
                    "doctype": "Mira Contact Campaign",
                    "campaign_id": campaign_id,
                    "prospect_id": prospect,
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

def check_exists(campaign_id,prospect_id):
    prospect_campaign_exists = frappe.db.exists("Mira Contact Campaign",{"campaign_id":campaign_id,"prospect_id":prospect_id})
    if prospect_campaign_exists:
        return True
    else:
        return False