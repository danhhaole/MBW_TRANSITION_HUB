import frappe
from frappe.utils import now_datetime
from mbw_mira.workers.create_action_for_talent import create_action_for_talent_campaign


def run():
    """
    Quét Mira Talent Campaign ACTIVE đến hạn và enqueue worker tạo Action.
    """
    now = now_datetime()

    campaigns = frappe.get_all(
        "Mira Talent Campaign",
        filters={
            "status": "ACTIVE",
            "next_action_at": ("<=", now)
        },
        fields=["name", "campaign_id", "current_step_order", "next_action_at"]
    )

    for tc in campaigns:
        create_action_for_talent_campaign(tc.name)
        frappe.enqueue(
            "mbw_mira.workers.create_action_for_talent.create_action_for_talent_campaign",
            talent_campaign_id=tc.name,
            job_name=tc.name,
            queue="default"
        )

    return True
