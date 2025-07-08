import frappe
from frappe.utils import now_datetime, add_days

# | Trạng thái `CandidateCampaign` | Kết quả mong đợi                    |
# | ------------------------------ | ----------------------------------- |
# | `ACTIVE`                       | Cho phép thực thi bình thường       |
# | `PAUSED`                       | Dừng xử lý → skip queue / retry sau |
# | `CANCELLED`                    | Bỏ qua hoàn toàn, không retry       |
# | `COMPLETED`                    | Không xử lý nữa (vì đã xong)        |


def handle_step(candidate_campaign_id: str):
    cc = frappe.get_doc("CandidateCampaign", candidate_campaign_id)
    if cc.status != "ACTIVE":
        frappe.logger("campaign").info(
            f"[SKIP] Campaign {cc.name} is {cc.status}. No action created."
        )
        return
    print(cc)
    step = frappe.get_doc(
        "CampaignStep",
        {"campaign": cc.campaign_id, "step_order": cc.current_step_order},
    )

    status_action = (
        "SCHEDULED"
        if step.action_type in ["SEND_EMAIL", "SEND_SMS", "SEND_NOTIFICATION"]
        else "PENDING_MANUAL"
    )
    exists_action = frappe.db.get_value("Action",{"candidate_campaign_id":cc.name,"campaign_step":step.name})
    if not exists_action:
        action = frappe.get_doc(
            {
                "doctype": "Action",
                "candidate_campaign_id": cc.name,
                "campaign_step": step.name,
                "status": status_action,
                "scheduled_at": now_datetime(),
            }
        ).insert(ignore_permissions=True)

        # Nếu status là Scheduled thì chạy tự động
        if status_action == "SCHEDULED":
            frappe.enqueue(
                "mbw_mira.campaign.background_jobs.execute_action",
                job_name="execute_action",
                action_id=action.name,
                queue="short",
            )


# Process campaign tạo candidate segment
def handle_campaign():
    from mbw_mira.services import candidate_service

    frappe.logger("campaign").info(f"handle_campaign")
    candidate_service.handle_candidate_segment()


# Process CandidateCampaign xử lý logic
def handle_candidate_campaign():
    from mbw_mira.services import candidate_service

    candidate_service.handle_candidate_campaign()


def execute_action_logic(action_id: str):
    action = frappe.get_doc("Action", action_id)
    cc = frappe.get_doc("CandidateCampaign", action.candidate_campaign_id)
    if cc.status != "ACTIVE":
        frappe.logger("campaign").info(
            f"[SKIP] Execute ignored for action {action.name} — Campaign is {cc.status}"
        )
        return

    candidate = frappe.get_doc("Candidate", cc.candidate_id)
    step = frappe.get_doc("CampaignStep", action.campaign_step)

    try:
        result = None
        if step.action_type == "SEND_EMAIL":
            result = send_email_to_candidate(candidate, action, step)
            create_interaction(
                candidate_id=candidate.name,
                interaction_type="EMAIL_SENT",
                source_action=action.name,
            )
        elif step.action_type == "SEND_SMS":
            result = send_sms_to_candidate(candidate, action, step)
            create_interaction(
                candidate_id=candidate.name,
                interaction_type="SMS_SENT",
                source_action=action.name,
            )

        action.status = "EXECUTED"
        action.executed_at = now_datetime()
        action.result = result or {}
        action.save()

        frappe.enqueue(
            "mbw_mira.campaign.background_jobs.step_executed",
            action_id=action.name,
            queue="short",
            job_name="step_executed",
        )

    except Exception as e:
        action.status = "FAILED"
        action.result = {"error": str(e), "traceback": frappe.get_traceback()}
        action.save()
        frappe.logger("campaign").error(
            f"[ERROR] Action {action.name} failed:\n{frappe.get_traceback()}"
        )
        raise


def process_step_result(action_id: str):
    action = frappe.get_doc("Action", action_id)
    cc = frappe.get_doc("CandidateCampaign", action.candidate_campaign_id)
    if cc.status != "ACTIVE":
        frappe.logger("campaign").info(
            f"[SKIP] Step result ignored — campaign {cc.name} is {cc.status}"
        )
        return

    current_order = cc.current_step_order
    next_step = frappe.get_all(
        "CampaignStep",
        filters={"campaign": cc.campaign_id, "step_order": current_order + 1},
        fields=["name", "step_order", "delay_in_days"],
        limit=1,
    )

    if not next_step:
        cc.status = "COMPLETED"
        cc.next_action_at = None
    else:
        step_info = next_step[0]
        cc.current_step_order = step_info.step_order
        cc.next_action_at = add_days(now_datetime(), step_info.delay_in_days or 0)

    cc.save()


def send_email_to_candidate(candidate, action,step):
    if not candidate.email:
        frappe.throw("Candidate does not have an email.")
    # Nếu ứng viên đã unsubcrible
    if candidate.email_opt_out:
        frappe.logger("campain").error("Candidate unsubcrible")
        return

    subject = "Thông báo từ chiến dịch"
    context = (candidate,action,step)
    message = render_template(step.template, context)

    frappe.enqueue(
        "mbw_mira.campaign.notification_jobs.send_email_job",
        queue="short",
        job_name="send_email_job",
        candidate_email=candidate.email,
        subject=subject,
        message=message,
        campaign_step=step.name,
        candidate_id=candidate.name,
    )
    return {"queued_email": candidate.email, "subject": subject}


def send_sms_to_candidate(candidate,action, step):
    if not candidate.phone:
        frappe.throw("Candidate does not have a phone number.")

    if candidate.email_opt_out:
        frappe.logger("campain").error("Candidate unsubcrible")
        return
    context = (candidate,action, step)
    message = render_template(step.template, context)

    frappe.enqueue(
        "mbw_mira.campaign.notification_jobs.send_sms_job",
        queue="short",
        job_name="send_sms_job",
        phone=candidate.phone,
        message=message,
        campaign_step=step.name,
        candidate_id=candidate.name,
    )
    return {"queued_sms": candidate.phone, "message": message}


def render_template(template_str, context):
    from mbw_mira.campaign.utils import make_signature
    from urllib.parse import urlencode
    from frappe.utils import get_url
    if not template_str:
        return "Xin chào bạn"
    candidate,action, step = context
    base_url = get_url()
    params = {
        "candidate_id": candidate.name,
        "action": action.name,
        "url": f"{base_url}/mbw_mira"
    }

    context_parse ={
        "candidate_name":candidate.full_name
        }
    
    sig = make_signature(params)

    # dùng urllib để encode query string
    query = urlencode({**params, "sig": sig})

    
    context_parse["tracking_pixel_url"] = (
        f"{base_url}/api/method/mbw_mira.api.interaction.tracking_pixel?{query}"
    )
    context_parse["tracking_link"] = (
        f"{base_url}/api/method/mbw_mira.api.interaction.click_redirect?{query}"
    )
    context_parse['url_link'] = (
        f"{base_url}/api/method/mbw_mira.api.interaction.unsubscribe?{query}"
    )

    return frappe.render_template(template_str, context_parse)


def create_interaction(
    candidate_id: str,
    interaction_type: str,
    source_action: str = None,
    url: str = None,
    description: str = None,
):
    frappe.get_doc(
        {
            "doctype": "Interaction",
            "candidate_id": candidate_id,
            "interaction_type": interaction_type,
            "action": source_action,
            "url": url,
            "description": description,
        }
    ).insert(ignore_permissions=True)
