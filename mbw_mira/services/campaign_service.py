import frappe

def process_campaign_with_steps(data):
    """
    Thực hiện tạo Campaign & CampaignStep trong background.
    """
    campaign_name = data.get("campaign_name")
    description = data.get("description", "")
    target_segment = data.get("target_segment")
    owner_id = data.get("owner_id", frappe.session.user)
    start_date = data.get("start_date")
    end_date = data.get("end_date")
    status = data.get("status","DRAFT")
    steps = data.get("steps", [])

    if not campaign_name or not target_segment or not steps:
        frappe.log_error("Missing parameters in background job", "process_campaign_with_steps")
        return

    # tạo campaign
    campaign_doc = frappe.get_doc({
        "doctype": "Campaign",
        "campaign_name": campaign_name,
        "description": description,
        "target_segment": target_segment,
        "owner_id": owner_id,
        "start_date": start_date,
        "end_date": end_date,
        "is_active": 1,
        "status": status
    }).insert(ignore_permissions=True)

    campaign_id = campaign_doc.name
    created_steps = []

    for step in steps:
        doc = frappe.get_doc({
            "doctype": "CampaignStep",
            "campaign": campaign_id,
            "campaign_step_name": step.get('step_name'),
            "step_order": step.get("step_order"),
            "action_type": step.get("action_type"),
            "delay_in_days": step.get("delay_in_days", 0),
            "template": step.get("template"),
            "action_config": frappe.as_json(step.get("action_config", {}))
        }).insert(ignore_permissions=True)
        created_steps.append(doc.name)

    frappe.db.commit()

    # tuỳ chọn: gửi thông báo realtime hoặc email
    frappe.publish_realtime(
        event="campaign_created",
        message={
            "campaign": campaign_id,
            "steps": created_steps
        },
        user=owner_id
    )
