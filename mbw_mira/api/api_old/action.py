import frappe
import json
from frappe.utils import cstr, cint, flt, getdate, nowdate, get_datetime, now
from frappe import _
from .common import get_list_data, get_form_data, save_doc, delete_doc, get_filter_options


@frappe.whitelist()
def get_actions_paginated(
    page=1,
    limit=12,
    search="",
    status="",
    candidate_campaign_id="",
    campaign_step="",
    assignee_id="",
    order_by="scheduled_at desc"
):
    """
    Get paginated actions using common list data function
    """
    try:
        # Calculate start position
        start = (cint(page) - 1) * cint(limit)
        
        # Build filters
        filters = {}
        if status:
            filters["status"] = status
        if candidate_campaign_id:
            filters["candidate_campaign_id"] = candidate_campaign_id
        if campaign_step:
            filters["campaign_step"] = campaign_step
        if assignee_id:
            filters["assignee_id"] = assignee_id
        
        # Build search conditions
        search_conditions = []
        if search:
            search_conditions = [
                {"candidate_campaign_id": ["like", f"%{search}%"]},
                {"campaign_step": ["like", f"%{search}%"]},
                {"status": ["like", f"%{search}%"]},
                {"assignee_id": ["like", f"%{search}%"]}
            ]
        
        if search_conditions:
            filters["search_text"] = search_conditions
        
        # Fields to fetch
        fields = [
            "name", "candidate_campaign_id", "campaign_step", "status", 
            "scheduled_at", "executed_at", "result", "assignee_id",
            "modified", "creation"
        ]
        
        # Get data using common function
        result = get_list_data(
            doctype="Action",
            filters=filters,
            order_by=order_by,
            page_length=limit,
            start=start,
            fields=fields
        )
        
        if result.get("success"):
            # Enrich data with related details
            enriched_data = []
            for item in result["data"]:
                # Get candidate campaign details
                candidate_campaign = frappe.get_doc("CandidateCampaign", item.get("candidate_campaign_id"))
                
                # Get candidate details
                candidate = frappe.get_doc("Candidate", candidate_campaign.candidate_id)
                
                # Get campaign details
                campaign = frappe.get_doc("Campaign", candidate_campaign.campaign_id)
                
                # Get campaign step details
                campaign_step = frappe.get_doc("CampaignStep", item.get("campaign_step"))
                
                # Get assignee details
                assignee = None
                if item.get("assignee_id"):
                    assignee = frappe.get_doc("User", item.get("assignee_id"))
                
                item.update({
                    "candidate_name": candidate.full_name,
                    "candidate_email": candidate.email,
                    "campaign_name": campaign.campaign_name,
                    "campaign_step_name": campaign_step.campaign_step_name,
                    "action_type": campaign_step.action_type,
                    "step_order": campaign_step.step_order,
                    "assignee_name": assignee.full_name if assignee else None,
                    "assignee_email": assignee.email if assignee else None
                })
                enriched_data.append(item)
            
            return {
                "success": True,
                "data": enriched_data,
                "pagination": result["pagination"]
            }
        else:
            return {
                "success": False,
                "error": result.get("error", "Unknown error"),
                "data": [],
                "pagination": {
                    "page": 1,
                    "limit": limit,
                    "total": 0,
                    "pages": 0,
                    "has_next": False,
                    "has_prev": False,
                    "showing_from": 0,
                    "showing_to": 0
                }
            }
        
    except Exception as e:
        frappe.log_error(f"Error in get_actions_paginated: {str(e)}")
        return {
            "success": False,
            "error": str(e),
            "data": [],
            "pagination": {
                "page": 1,
                "limit": limit,
                "total": 0,
                "pages": 0,
                "has_next": False,
                "has_prev": False,
                "showing_from": 0,
                "showing_to": 0
            }
        }


@frappe.whitelist()
def get_action_by_name(name):
    """
    Get action details by name
    """
    try:
        return get_form_data("Action", name)
    except Exception as e:
        frappe.log_error(f"Error in get_action_by_name: {str(e)}")
        return {"success": False, "error": str(e)}


@frappe.whitelist()
def create_action(data):
    """
    Create new action
    """
    try:
        # Validate required fields
        if not data.get("candidate_campaign_id"):
            return {"success": False, "error": "Candidate Campaign is required"}
        if not data.get("campaign_step"):
            return {"success": False, "error": "Campaign Step is required"}
        
        # Set default values
        data["status"] = data.get("status", "SCHEDULED")
        if not data.get("scheduled_at"):
            data["scheduled_at"] = now()
        
        return save_doc("Action", data)
    except Exception as e:
        frappe.log_error(f"Error in create_action: {str(e)}")
        return {"success": False, "error": str(e)}


@frappe.whitelist()
def update_action(name, data):
    """
    Update existing action
    """
    try:
        # Validate required fields
        if not data.get("candidate_campaign_id"):
            return {"success": False, "error": "Candidate Campaign is required"}
        if not data.get("campaign_step"):
            return {"success": False, "error": "Campaign Step is required"}
        
        return save_doc("Action", data, name)
    except Exception as e:
        frappe.log_error(f"Error in update_action: {str(e)}")
        return {"success": False, "error": str(e)}


@frappe.whitelist()
def delete_action(name):
    """
    Delete action
    """
    try:
        return delete_doc("Action", name)
    except Exception as e:
        frappe.log_error(f"Error in delete_action: {str(e)}")
        return {"success": False, "error": str(e)}


@frappe.whitelist()
def get_action_stats():
    """
    Get action statistics
    """
    try:
        total_actions = frappe.db.count("Action")
        
        # Count by status
        status_stats = frappe.db.sql("""
            SELECT status, COUNT(*) as count
            FROM `tabAction`
            GROUP BY status
        """, as_dict=True)
        
        # Count by action type (from campaign step)
        action_type_stats = frappe.db.sql("""
            SELECT cs.action_type, COUNT(*) as count
            FROM `tabAction` a
            LEFT JOIN `tabCampaignStep` cs ON a.campaign_step = cs.name
            GROUP BY cs.action_type
        """, as_dict=True)
        
        # Overdue actions
        overdue_actions = frappe.db.sql("""
            SELECT COUNT(*) as count
            FROM `tabAction`
            WHERE status IN ('SCHEDULED', 'PENDING_MANUAL') 
            AND scheduled_at < NOW()
        """, as_dict=True)
        
        # Recent executions
        recent_executions = frappe.db.sql("""
            SELECT a.name, cc.candidate_id, c.full_name, cs.campaign_step_name, 
                   a.executed_at, a.status
            FROM `tabAction` a
            LEFT JOIN `tabCandidateCampaign` cc ON a.candidate_campaign_id = cc.name
            LEFT JOIN `tabCandidate` c ON cc.candidate_id = c.name
            LEFT JOIN `tabCampaignStep` cs ON a.campaign_step = cs.name
            WHERE a.status = 'EXECUTED'
            ORDER BY a.executed_at DESC
            LIMIT 5
        """, as_dict=True)
        
        return {
            "success": True,
            "total_actions": total_actions,
            "status_stats": status_stats,
            "action_type_stats": action_type_stats,
            "overdue_actions": overdue_actions[0]["count"] if overdue_actions else 0,
            "recent_executions": recent_executions
        }
    except Exception as e:
        frappe.log_error(f"Error in get_action_stats: {str(e)}")
        return {"success": False, "error": str(e)}


@frappe.whitelist()
def search_actions(query, limit=10):
    """
    Search actions for autocomplete
    """
    try:
        if not query:
            return []
        
        results = frappe.db.sql("""
            SELECT a.name, cc.candidate_id, c.full_name, cs.campaign_step_name,
                   a.status, a.scheduled_at, a.executed_at
            FROM `tabAction` a
            LEFT JOIN `tabCandidateCampaign` cc ON a.candidate_campaign_id = cc.name
            LEFT JOIN `tabCandidate` c ON cc.candidate_id = c.name
            LEFT JOIN `tabCampaignStep` cs ON a.campaign_step = cs.name
            WHERE c.full_name LIKE %(query)s
            OR cs.campaign_step_name LIKE %(query)s
            OR a.status LIKE %(query)s
            ORDER BY a.scheduled_at DESC
            LIMIT %(limit)s
        """, {
            "query": f"%{query}%",
            "limit": limit
        }, as_dict=True)
        
        return results
    except Exception as e:
        frappe.log_error(f"Error in search_actions: {str(e)}")
        return []


@frappe.whitelist()
def get_action_filter_options():
    """
    Get filter options for actions
    """
    try:
        options = {}
        
        # Status options
        status_result = get_filter_options("Action", "status")
        if status_result.get("success"):
            options["status"] = status_result["options"]
        
        # Candidate Campaign options
        cc_result = get_filter_options("Action", "candidate_campaign_id")
        if cc_result.get("success"):
            options["candidate_campaign_id"] = cc_result["options"]
        
        # Campaign Step options
        cs_result = get_filter_options("Action", "campaign_step")
        if cs_result.get("success"):
            options["campaign_step"] = cs_result["options"]
        
        # Assignee options
        assignee_result = get_filter_options("Action", "assignee_id")
        if assignee_result.get("success"):
            options["assignee_id"] = assignee_result["options"]
            
        return {"success": True, "options": options}
    except Exception as e:
        frappe.log_error(f"Error in get_action_filter_options: {str(e)}")
        return {"success": False, "error": str(e)}


@frappe.whitelist()
def get_actions_by_candidate_campaign(candidate_campaign_id):
    """
    Get all actions for a specific candidate campaign
    """
    try:
        actions = frappe.db.sql("""
            SELECT a.name, a.campaign_step, cs.campaign_step_name, cs.action_type,
                   a.status, a.scheduled_at, a.executed_at, a.result, a.assignee_id
            FROM `tabAction` a
            LEFT JOIN `tabCampaignStep` cs ON a.campaign_step = cs.name
            WHERE a.candidate_campaign_id = %(candidate_campaign_id)s
            ORDER BY cs.step_order, a.scheduled_at
        """, {"candidate_campaign_id": candidate_campaign_id}, as_dict=True)
        
        return {
            "success": True,
            "data": actions
        }
    except Exception as e:
        frappe.log_error(f"Error in get_actions_by_candidate_campaign: {str(e)}")
        return {"success": False, "error": str(e)}


@frappe.whitelist()
def get_actions_by_assignee(assignee_id):
    """
    Get all actions assigned to a specific user
    """
    try:
        actions = frappe.db.sql("""
            SELECT a.name, cc.candidate_id, c.full_name, cs.campaign_step_name,
                   cs.action_type, a.status, a.scheduled_at, a.executed_at
            FROM `tabAction` a
            LEFT JOIN `tabCandidateCampaign` cc ON a.candidate_campaign_id = cc.name
            LEFT JOIN `tabCandidate` c ON cc.candidate_id = c.name
            LEFT JOIN `tabCampaignStep` cs ON a.campaign_step = cs.name
            WHERE a.assignee_id = %(assignee_id)s
            ORDER BY a.scheduled_at DESC
        """, {"assignee_id": assignee_id}, as_dict=True)
        
        return {
            "success": True,
            "data": actions
        }
    except Exception as e:
        frappe.log_error(f"Error in get_actions_by_assignee: {str(e)}")
        return {"success": False, "error": str(e)}


@frappe.whitelist()
def execute_action(name, result_data=None):
    """
    Mark action as executed
    """
    try:
        doc = frappe.get_doc("Action", name)
        doc.status = "EXECUTED"
        doc.executed_at = now()
        
        if result_data:
            if isinstance(result_data, str):
                result_data = json.loads(result_data)
            doc.result = json.dumps(result_data)
        
        doc.save()
        return {"success": True, "message": "Action executed successfully"}
    except Exception as e:
        frappe.log_error(f"Error in execute_action: {str(e)}")
        return {"success": False, "error": str(e)}


@frappe.whitelist()
def skip_action(name, reason=None):
    """
    Skip action
    """
    try:
        doc = frappe.get_doc("Action", name)
        doc.status = "SKIPPED"
        doc.executed_at = now()
        
        if reason:
            doc.result = json.dumps({"reason": reason})
        
        doc.save()
        return {"success": True, "message": "Action skipped"}
    except Exception as e:
        frappe.log_error(f"Error in skip_action: {str(e)}")
        return {"success": False, "error": str(e)}


@frappe.whitelist()
def fail_action(name, error_message=None):
    """
    Mark action as failed
    """
    try:
        doc = frappe.get_doc("Action", name)
        doc.status = "FAILED"
        doc.executed_at = now()
        
        if error_message:
            doc.result = json.dumps({"error": error_message})
        
        doc.save()
        return {"success": True, "message": "Action marked as failed"}
    except Exception as e:
        frappe.log_error(f"Error in fail_action: {str(e)}")
        return {"success": False, "error": str(e)}


@frappe.whitelist()
def reschedule_action(name, new_scheduled_at):
    """
    Reschedule action
    """
    try:
        doc = frappe.get_doc("Action", name)
        doc.scheduled_at = new_scheduled_at
        doc.status = "SCHEDULED"
        doc.save()
        return {"success": True, "message": "Action rescheduled"}
    except Exception as e:
        frappe.log_error(f"Error in reschedule_action: {str(e)}")
        return {"success": False, "error": str(e)}


@frappe.whitelist()
def get_pending_actions(assignee_id=None, limit=50):
    """
    Get pending actions (for dashboard or task management)
    """
    try:
        conditions = ["a.status IN ('SCHEDULED', 'PENDING_MANUAL')"]
        params = {"limit": limit}
        
        if assignee_id:
            conditions.append("a.assignee_id = %(assignee_id)s")
            params["assignee_id"] = assignee_id
        
        query = f"""
            SELECT a.name, cc.candidate_id, c.full_name, cs.campaign_step_name,
                   cs.action_type, a.status, a.scheduled_at, a.assignee_id
            FROM `tabAction` a
            LEFT JOIN `tabCandidateCampaign` cc ON a.candidate_campaign_id = cc.name
            LEFT JOIN `tabCandidate` c ON cc.candidate_id = c.name
            LEFT JOIN `tabCampaignStep` cs ON a.campaign_step = cs.name
            WHERE {' AND '.join(conditions)}
            ORDER BY a.scheduled_at ASC
            LIMIT %(limit)s
        """
        
        actions = frappe.db.sql(query, params, as_dict=True)
        
        return {
            "success": True,
            "data": actions
        }
    except Exception as e:
        frappe.log_error(f"Error in get_pending_actions: {str(e)}")
        return {"success": False, "error": str(e)}
