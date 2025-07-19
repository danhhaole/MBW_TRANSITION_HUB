import frappe
from frappe.utils import now_datetime


def enroll_talent_for_campaign(campaign_id):
    """
    Worker: tìm ứng viên từ TalentPool theo campaign và tạo TalentProfilesCampaign.
    """

    frappe.logger().info(f"[Worker] Enrolling from TalentPool for campaign: {campaign_id}")

    talents = get_talents_for_campaign(campaign_id)

    if not talents:
        frappe.logger().info(f"No talents found in TalentPool for campaign {campaign_id}")
        return

    # tìm bước đầu tiên trong CampaignStep (nếu có)
    first_step = get_first_campaign_step(campaign_id)

    count = 0
    for talent in talents:
        if not already_enrolled(campaign_id, talent.name):
            create_talent_campaign(campaign_id, talent, first_step)
            count += 1

    frappe.logger().info(f"[Worker] Created {count} TalentProfilesCampaign(s) for campaign {campaign_id}")


def get_talents_for_campaign(campaign_id):
    """
    Lấy danh sách bản ghi TalentPool theo campaign_id
    """
    return frappe.get_all(
        "TalentPool",
        filters={"campaign_id": campaign_id},
        fields=["name", "segment_id", "full_name", "email"]
    )


def already_enrolled(campaign_id, talent_id):
    """
    Kiểm tra đã có TalentProfilesCampaign chưa.
    """
    return frappe.db.exists(
        "TalentProfilesCampaign",
        {"campaign_id": campaign_id, "talent_id": talent_id}
    )


def get_first_campaign_step(campaign_id):
    """
    Lấy bước đầu tiên (step_order nhỏ nhất) của CampaignStep
    """
    step = frappe.get_all(
        "CampaignStep",
        filters={"campaign": campaign_id},
        fields=["name", "step_order"],
        order_by="step_order asc",
        limit=1
    )
    return step[0] if step else None


def create_talent_campaign(campaign_id, talent, first_step):
    """
    Tạo mới TalentProfilesCampaign, chỉ set current_step_order nếu có
    """
    doc = frappe.get_doc({
        "doctype": "TalentProfilesCampaign",
        "campaign_id": campaign_id,
        "talent_id": talent.name,
        "status": "ACTIVE",
        "enrolled_at": now_datetime(),
        "current_step_order": first_step["step_order"] if first_step else 0,
        "next_action_at": None
    })
    doc.insert(ignore_permissions=True)
    frappe.db.commit()

    frappe.logger().info(
        f"✨ Created TalentProfilesCampaign: {talent.full_name} → step_order: {first_step['step_order'] if first_step else 0}"
    )
