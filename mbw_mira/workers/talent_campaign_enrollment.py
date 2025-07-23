import frappe
from frappe.utils import now_datetime,add_days


def enroll_talent_for_campaign(campaign_id):
    """
    Worker: tìm ứng viên từ TalentProfiles theo campaign và tạo TalentProfilesCampaign.
    """
    talent_profiles = get_talents_segment_for_campaign(campaign_id)

    if not talent_profiles:
        return

    # tìm bước đầu tiên trong CampaignStep (nếu có)
    first_step = get_first_campaign_step(campaign_id)

    count = 0
    try:
        
        if first_step and talent_profiles:
            for profile in talent_profiles:
                create_talent_campaign(campaign_id, profile, first_step)
                count += 1
        frappe.publish_realtime('enroll_talent_campaign', data={'campaign': campaign_id})
        return count
    except Exception as e:
        frappe.log_error(frappe.get_traceback())
        return count


def get_talents_segment_for_campaign(campaign_id):
    """
    Lấy danh talentSegment từ Campaign (TalentProfilesSegment)
    Lấy TalentProfiles từ talentsegment
    """
    talent_segment = frappe.db.get_value("Campaign", campaign_id, "target_segment")
    talent_profiles = frappe.get_all(
        "TalentProfilesSegment",
        filters={"segment_id": talent_segment},
        fields=["talent_id"],
    )

    return talent_profiles


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


def create_talent_campaign(campaign_id, profile, first_step):
    """
    Tạo mới TalentProfilesCampaign, chỉ set current_step_order nếu có
    """
    try:
        next_action_at = add_days(now_datetime(), first_step.get("delay_in_days") or 0)
        if not check_exists(campaign_id,profile.get("talent_id")):
            doc = frappe.get_doc(
                {
                    "doctype": "TalentProfilesCampaign",
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

def check_exists(campaign_id,talent_id):
    talent_campaign_exists = frappe.db.exists("TalentProfilesCampaign",{"campaign_id":campaign_id,"talent_id":talent_id})
    if talent_campaign_exists:
        return True
    else:
        return False