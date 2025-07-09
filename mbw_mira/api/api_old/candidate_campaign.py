import frappe
import json
from frappe.utils import cstr, cint, flt, getdate, nowdate, get_datetime, now
from frappe import _
from .common import get_list_data, get_form_data, save_doc, delete_doc, get_filter_options


@frappe.whitelist()
def get_candidate_campaigns_paginated(
    page=1,
    limit=12,
    search="",
    campaign_id="",
    candidate_id="",
    status="",
    order_by="enrolled_at desc"
):
    """
    Get paginated candidate campaigns using common list data function
    """
    try:
        # Calculate start position
        start = (cint(page) - 1) * cint(limit)
        
        # Build filters
        filters = {}
        if campaign_id:
            filters["campaign_id"] = campaign_id
        if candidate_id:
            filters["candidate_id"] = candidate_id
        if status:
            filters["status"] = status
        
        # Build search conditions
        search_conditions = []
        if search:
            search_conditions = [
                {"candidate_id": ["like", f"%{search}%"]},
                {"campaign_id": ["like", f"%{search}%"]},
                {"status": ["like", f"%{search}%"]}
            ]
        
        if search_conditions:
            filters["search_text"] = search_conditions
        
        # Fields to fetch
        fields = [
            "name", "campaign_id", "candidate_id", "status", "enrolled_at",
            "current_step_order", "next_action_at", "modified", "creation"
        ]
        
        # Get data using common function
        result = get_list_data(
            doctype="CandidateCampaign",
            filters=filters,
            order_by=order_by,
            page_length=limit,
            start=start,
            fields=fields
        )
        
        if result.get("success"):
            # Enrich data with candidate and campaign details
            enriched_data = []
            for item in result["data"]:
                # Get candidate details
                candidate = frappe.get_doc("Candidate", item.get("candidate_id"))
                campaign = frappe.get_doc("Campaign", item.get("campaign_id"))
                
                # Get current step details
                current_step = None
                if item.get("current_step_order"):
                    current_step = frappe.db.get_value(
                        "CampaignStep",
                        {
                            "campaign": item.get("campaign_id"),
                            "step_order": item.get("current_step_order")
                        },
                        ["name", "campaign_step_name", "action_type"],
                        as_dict=True
                    )
                
                item.update({
                    "candidate_name": candidate.full_name,
                    "candidate_email": candidate.email,
                    "candidate_headline": candidate.headline,
                    "campaign_name": campaign.campaign_name,
                    "campaign_type": campaign.type,
                    "campaign_status": campaign.status,
                    "current_step_name": current_step.get("campaign_step_name") if current_step else None,
                    "current_step_action_type": current_step.get("action_type") if current_step else None
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
        frappe.log_error(f"Error in get_candidate_campaigns_paginated: {str(e)}")
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
def get_candidate_campaign_by_name(name):
    """
    Get candidate campaign details by name
    """
    try:
        return get_form_data("CandidateCampaign", name)
    except Exception as e:
        frappe.log_error(f"Error in get_candidate_campaign_by_name: {str(e)}")
        return {"success": False, "error": str(e)}


@frappe.whitelist()
def create_candidate_campaign(data):
    """
    Create new candidate campaign
    """
    try:
        # Validate required fields
        if not data.get("candidate_id"):
            return {"success": False, "error": "Candidate is required"}
        if not data.get("campaign_id"):
            return {"success": False, "error": "Campaign is required"}
        
        # Check if relationship already exists
        exists = frappe.db.exists("CandidateCampaign", {
            "candidate_id": data.get("candidate_id"),
            "campaign_id": data.get("campaign_id")
        })
        
        if exists:
            return {"success": False, "error": "Candidate is already enrolled in this campaign"}
        
        # Set default values
        data["enrolled_at"] = now()
        data["status"] = data.get("status", "ACTIVE")
        data["current_step_order"] = 1
        
        # Set next action time based on first step
        first_step = frappe.db.get_value(
            "CampaignStep",
            {"campaign": data.get("campaign_id"), "step_order": 1},
            "delay_in_days"
        )
        
        if first_step:
            from frappe.utils import add_days
            data["next_action_at"] = add_days(now(), first_step or 0)
        
        return save_doc("CandidateCampaign", data)
    except Exception as e:
        frappe.log_error(f"Error in create_candidate_campaign: {str(e)}")
        return {"success": False, "error": str(e)}


@frappe.whitelist()
def update_candidate_campaign(name, data):
    """
    Update existing candidate campaign
    """
    try:
        # Validate required fields
        if not data.get("candidate_id"):
            return {"success": False, "error": "Candidate is required"}
        if not data.get("campaign_id"):
            return {"success": False, "error": "Campaign is required"}
        
        # Check if relationship already exists (excluding current record)
        exists = frappe.db.exists("CandidateCampaign", {
            "candidate_id": data.get("candidate_id"),
            "campaign_id": data.get("campaign_id"),
            "name": ["!=", name]
        })
        
        if exists:
            return {"success": False, "error": "Candidate is already enrolled in this campaign"}
        
        return save_doc("CandidateCampaign", data, name)
    except Exception as e:
        frappe.log_error(f"Error in update_candidate_campaign: {str(e)}")
        return {"success": False, "error": str(e)}


@frappe.whitelist()
def delete_candidate_campaign(name):
    """
    Delete candidate campaign
    """
    try:
        return delete_doc("CandidateCampaign", name)
    except Exception as e:
        frappe.log_error(f"Error in delete_candidate_campaign: {str(e)}")
        return {"success": False, "error": str(e)}


@frappe.whitelist()
def get_candidate_campaign_stats():
    """
    Get candidate campaign statistics
    """
    try:
        total_enrollments = frappe.db.count("CandidateCampaign")
        
        # Count by status
        status_stats = frappe.db.sql("""
            SELECT status, COUNT(*) as count
            FROM `tabCandidateCampaign`
            GROUP BY status
        """, as_dict=True)
        
        # Count by campaign
        campaign_stats = frappe.db.sql("""
            SELECT cc.campaign_id, c.campaign_name, COUNT(*) as enrollment_count
            FROM `tabCandidateCampaign` cc
            LEFT JOIN `tabCampaign` c ON cc.campaign_id = c.name
            GROUP BY cc.campaign_id, c.campaign_name
            ORDER BY enrollment_count DESC
            LIMIT 10
        """, as_dict=True)
        
        # Active campaigns with pending actions
        pending_actions = frappe.db.sql("""
            SELECT COUNT(*) as count
            FROM `tabCandidateCampaign`
            WHERE status = 'ACTIVE' AND next_action_at <= NOW()
        """, as_dict=True)
        
        return {
            "success": True,
            "total_enrollments": total_enrollments,
            "status_stats": status_stats,
            "campaign_stats": campaign_stats,
            "pending_actions": pending_actions[0]["count"] if pending_actions else 0
        }
    except Exception as e:
        frappe.log_error(f"Error in get_candidate_campaign_stats: {str(e)}")
        return {"success": False, "error": str(e)}


@frappe.whitelist()
def search_candidate_campaigns(query, limit=10):
    """
    Search candidate campaigns for autocomplete
    """
    try:
        if not query:
            return []
        
        results = frappe.db.sql("""
            SELECT cc.name, cc.candidate_id, c.full_name, cc.campaign_id, 
                   camp.campaign_name, cc.status, cc.enrolled_at
            FROM `tabCandidateCampaign` cc
            LEFT JOIN `tabCandidate` c ON cc.candidate_id = c.name
            LEFT JOIN `tabCampaign` camp ON cc.campaign_id = camp.name
            WHERE c.full_name LIKE %(query)s
            OR c.email LIKE %(query)s
            OR camp.campaign_name LIKE %(query)s
            ORDER BY cc.enrolled_at DESC
            LIMIT %(limit)s
        """, {
            "query": f"%{query}%",
            "limit": limit
        }, as_dict=True)
        
        return results
    except Exception as e:
        frappe.log_error(f"Error in search_candidate_campaigns: {str(e)}")
        return []


@frappe.whitelist()
def get_candidate_campaign_filter_options():
    """
    Get filter options for candidate campaigns
    """
    try:
        options = {}
        
        # Status options
        status_result = get_filter_options("CandidateCampaign", "status")
        if status_result.get("success"):
            options["status"] = status_result["options"]
        
        # Campaign options
        campaign_result = get_filter_options("CandidateCampaign", "campaign_id")
        if campaign_result.get("success"):
            options["campaign_id"] = campaign_result["options"]
        
        # Candidate options
        candidate_result = get_filter_options("CandidateCampaign", "candidate_id")
        if candidate_result.get("success"):
            options["candidate_id"] = candidate_result["options"]
            
        return {"success": True, "options": options}
    except Exception as e:
        frappe.log_error(f"Error in get_candidate_campaign_filter_options: {str(e)}")
        return {"success": False, "error": str(e)}


@frappe.whitelist()
def get_candidates_by_campaign(campaign_id):
    """
    Get all candidates enrolled in a specific campaign
    """
    try:
        candidates = frappe.db.sql("""
            SELECT cc.name, cc.candidate_id, c.full_name, c.email, c.headline,
                   cc.status, cc.enrolled_at, cc.current_step_order, cc.next_action_at
            FROM `tabCandidateCampaign` cc
            LEFT JOIN `tabCandidate` c ON cc.candidate_id = c.name
            WHERE cc.campaign_id = %(campaign_id)s
            ORDER BY cc.enrolled_at DESC
        """, {"campaign_id": campaign_id}, as_dict=True)
        
        return {
            "success": True,
            "data": candidates
        }
    except Exception as e:
        frappe.log_error(f"Error in get_candidates_by_campaign: {str(e)}")
        return {"success": False, "error": str(e)}


@frappe.whitelist()
def get_campaigns_by_candidate(candidate_id):
    """
    Get all campaigns for a specific candidate
    """
    try:
        campaigns = frappe.db.sql("""
            SELECT cc.name, cc.campaign_id, c.campaign_name, c.type, c.status as campaign_status,
                   cc.status, cc.enrolled_at, cc.current_step_order, cc.next_action_at
            FROM `tabCandidateCampaign` cc
            LEFT JOIN `tabCampaign` c ON cc.campaign_id = c.name
            WHERE cc.candidate_id = %(candidate_id)s
            ORDER BY cc.enrolled_at DESC
        """, {"candidate_id": candidate_id}, as_dict=True)
        
        return {
            "success": True,
            "data": campaigns
        }
    except Exception as e:
        frappe.log_error(f"Error in get_campaigns_by_candidate: {str(e)}")
        return {"success": False, "error": str(e)}


@frappe.whitelist()
def bulk_enroll_candidates(campaign_id, candidate_ids):
    """
    Enroll multiple candidates in a campaign
    """
    try:
        if isinstance(candidate_ids, str):
            candidate_ids = json.loads(candidate_ids)
        
        results = []
        for candidate_id in candidate_ids:
            # Check if relationship already exists
            exists = frappe.db.exists("CandidateCampaign", {
                "candidate_id": candidate_id,
                "campaign_id": campaign_id
            })
            
            if not exists:
                # Get first step delay
                first_step = frappe.db.get_value(
                    "CampaignStep",
                    {"campaign": campaign_id, "step_order": 1},
                    "delay_in_days"
                )
                
                doc = frappe.new_doc("CandidateCampaign")
                doc.candidate_id = candidate_id
                doc.campaign_id = campaign_id
                doc.enrolled_at = now()
                doc.status = "ACTIVE"
                doc.current_step_order = 1
                
                if first_step:
                    from frappe.utils import add_days
                    doc.next_action_at = add_days(now(), first_step or 0)
                
                doc.save()
                results.append({"candidate_id": candidate_id, "status": "enrolled"})
            else:
                results.append({"candidate_id": candidate_id, "status": "already_enrolled"})
        
        return {"success": True, "results": results}
    except Exception as e:
        frappe.log_error(f"Error in bulk_enroll_candidates: {str(e)}")
        return {"success": False, "error": str(e)}


@frappe.whitelist()
def advance_candidate_step(name):
    """
    Advance candidate to next step in campaign
    """
    try:
        doc = frappe.get_doc("CandidateCampaign", name)
        
        # Get next step
        next_step = frappe.db.get_value(
            "CampaignStep",
            {
                "campaign": doc.campaign_id,
                "step_order": doc.current_step_order + 1
            },
            ["step_order", "delay_in_days"],
            as_dict=True
        )
        
        if next_step:
            doc.current_step_order = next_step["step_order"]
            if next_step["delay_in_days"]:
                from frappe.utils import add_days
                doc.next_action_at = add_days(now(), next_step["delay_in_days"])
            doc.save()
            return {"success": True, "message": "Advanced to next step"}
        else:
            doc.status = "COMPLETED"
            doc.next_action_at = None
            doc.save()
            return {"success": True, "message": "Campaign completed"}
        
    except Exception as e:
        frappe.log_error(f"Error in advance_candidate_step: {str(e)}")
        return {"success": False, "error": str(e)}


@frappe.whitelist()
def pause_candidate_campaign(name):
    """
    Pause candidate campaign
    """
    try:
        doc = frappe.get_doc("CandidateCampaign", name)
        doc.status = "PAUSED"
        doc.save()
        return {"success": True, "message": "Campaign paused"}
    except Exception as e:
        frappe.log_error(f"Error in pause_candidate_campaign: {str(e)}")
        return {"success": False, "error": str(e)}


@frappe.whitelist()
def resume_candidate_campaign(name):
    """
    Resume candidate campaign
    """
    try:
        doc = frappe.get_doc("CandidateCampaign", name)
        doc.status = "ACTIVE"
        doc.save()
        return {"success": True, "message": "Campaign resumed"}
    except Exception as e:
        frappe.log_error(f"Error in resume_candidate_campaign: {str(e)}")
        return {"success": False, "error": str(e)}
