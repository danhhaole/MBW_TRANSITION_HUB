import frappe
from frappe.website.utils import clear_cache
from frappe import _
from mbw_mira.campaign.controller import create_interaction

def open_tracker(action_id):
    action = frappe.get_doc("Action", action_id)
    cc = frappe.get_doc("CandidateCampaign", action.candidate_campaign_id)
    create_interaction(
        candidate_id=cc.candidate_id,
        interaction_type="EMAIL_OPENED",
        source_action=action.name
    )
    # Trả về ảnh trắng (1x1 pixel)
    from flask import send_file
    return send_file("public/images/transparent.png", mimetype='image/png')

def click_tracker(action_id):
    redirect = frappe.form_dict.get("redirect")
    action = frappe.get_doc("Action", action_id)
    cc = frappe.get_doc("CandidateCampaign", action.candidate_campaign_id)

    create_interaction(
        candidate_id=cc.candidate_id,
        interaction_type="EMAIL_CLICKED",
        source_action=action.name,
        url=redirect
    )

    from werkzeug.utils import redirect as werkzeug_redirect
    return werkzeug_redirect(redirect or "https://yourdomain.com/")
