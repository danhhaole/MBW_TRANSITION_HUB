import frappe
import json
from mbw_mira.campaign import background_jobs

@frappe.whitelist()
def create_candidate_segment():
    """
    API: tạo CandidateSegment trực tiếp (synchronous).
    """
    data = json.loads(frappe.request.data)
    if not data:
        frappe.throw("Data require")
    background_jobs.add_candidate_to_talentsegment(data)
    
    return {
        "status": "queued",
        "message": "CandidateSegment creation has been queued."
    }

@frappe.whitelist()
def complete_manual_action():
    data = json.loads(frappe.request.data)
    if not data:
        frappe.throw("Data require")
    action_id = data.get("action_id")
    if not action_id:
        frappe.throw("action_id require")
    note = data.get("note",None)
    user = data.get("user",None)
    background_jobs.complete_manual(action_id,note,user)
    return {
        "status": "queued",
        "message": "CandidateSegment creation has been queued."
    }

@frappe.whitelist(allow_guest=False)
def create_campaign_with_steps_bg():
    """
    Nhận dữ liệu từ request và đẩy xử lý vào background.
    { 
        campaign_name
        description
        target_segment
        owner_id
        start_date
        end_date
        status
        steps :[
                step_name,
                step_order
                action_type
                delay_in_days
                template
                action_config
            ]
    }
    """
    data = frappe.request.get_json()
    if not data:
        frappe.throw(frappe._("No JSON payload found in request"))

    # enqueue job
    background_jobs.process_campaign_with_steps(data)

    return {
        "status": "queued",
        "message": frappe._("Campaign creation has been scheduled. You will be notified when it's done.")
    }
# API Module for MBW Mira 

# API modules
from . import campaign
from . import candidate 
