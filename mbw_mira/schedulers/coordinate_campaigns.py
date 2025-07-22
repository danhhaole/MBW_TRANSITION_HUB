import frappe
from datetime import date

def run():
    """
    Coordinate campaigns:
    - Activate campaigns that start today
    - Archive campaigns that ended
    - Pause campaigns if manually deactivated
    - Enqueue actions for ACTIVE campaigns
    """
    today = date.today()
    frappe.logger().info(f"[Coordinate Campaigns] Running at {today}")

    campaigns = frappe.get_all(
        "Campaign",
        fields=[
            "name", "campaign_name", "start_date", "end_date", 
            "is_active", "status"
        ]
    )

    for c in campaigns:
        updated = False

        # check is_active flag
        if not c.is_active and c.status != "PAUSED":
            frappe.db.set_value("Campaign", c.name, "status", "PAUSED")
            updated = True
            frappe.logger().info(f"Paused campaign: {c.campaign_name} (manually deactivated)")

        # check start_date
        elif c.is_active and c.start_date and c.start_date <= today:
            if c.status in ("DRAFT", "PAUSED"):
                frappe.db.set_value("Campaign", c.name, "status", "ACTIVE")
                updated = True
                frappe.logger().info(f"Activated campaign: {c.campaign_name}")

        # check end_date
        if c.end_date and c.end_date < today and c.status != "ARCHIVED":
            frappe.db.set_value("Campaign", c.name, "status", "ARCHIVED")
            updated = True
            frappe.logger().info(f"Archived campaign: {c.campaign_name} (ended)")


        if updated:
            frappe.db.commit()
    return True
