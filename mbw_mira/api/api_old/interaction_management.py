import frappe
import json
from frappe.utils import cstr, cint, flt, getdate, nowdate, get_datetime, now
from frappe import _
from .common import get_list_data, get_form_data, save_doc, delete_doc, get_filter_options


@frappe.whitelist()
def get_interactions_paginated(
    page=1,
    limit=12,
    search="",
    candidate_id="",
    interaction_type="",
    action="",
    order_by="creation desc"
):
    """
    Get paginated interactions using common list data function
    """
    try:
        # Calculate start position
        start = (cint(page) - 1) * cint(limit)
        
        # Build filters
        filters = {}
        if candidate_id:
            filters["candidate_id"] = candidate_id
        if interaction_type:
            filters["interaction_type"] = interaction_type
        if action:
            filters["action"] = action
        
        # Build search conditions
        search_conditions = []
        if search:
            search_conditions = [
                {"candidate_id": ["like", f"%{search}%"]},
                {"interaction_type": ["like", f"%{search}%"]},
                {"description": ["like", f"%{search}%"]},
                {"url": ["like", f"%{search}%"]}
            ]
        
        if search_conditions:
            filters["search_text"] = search_conditions
        
        # Fields to fetch
        fields = [
            "name", "candidate_id", "interaction_type", "action", "url", 
            "description", "modified", "creation"
        ]
        
        # Get data using common function
        result = get_list_data(
            doctype="Interaction",
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
                # Get candidate details
                candidate = frappe.get_doc("Candidate", item.get("candidate_id"))
                
                # Get action details if available
                action_details = None
                if item.get("action"):
                    action_doc = frappe.get_doc("Action", item.get("action"))
                    campaign_step = frappe.get_doc("CampaignStep", action_doc.campaign_step)
                    action_details = {
                        "name": action_doc.name,
                        "campaign_step_name": campaign_step.campaign_step_name,
                        "action_type": campaign_step.action_type
                    }
                
                item.update({
                    "candidate_name": candidate.full_name,
                    "candidate_email": candidate.email,
                    "candidate_headline": candidate.headline,
                    "action_details": action_details
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
        frappe.log_error(f"Error in get_interactions_paginated: {str(e)}")
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
def get_interaction_by_name(name):
    """
    Get interaction details by name
    """
    try:
        return get_form_data("Interaction", name)
    except Exception as e:
        frappe.log_error(f"Error in get_interaction_by_name: {str(e)}")
        return {"success": False, "error": str(e)}


@frappe.whitelist()
def create_interaction(data):
    """
    Create new interaction
    """
    try:
        # Validate required fields
        if not data.get("candidate_id"):
            return {"success": False, "error": "Candidate is required"}
        if not data.get("interaction_type"):
            return {"success": False, "error": "Interaction type is required"}
        
        return save_doc("Interaction", data)
    except Exception as e:
        frappe.log_error(f"Error in create_interaction: {str(e)}")
        return {"success": False, "error": str(e)}


@frappe.whitelist()
def update_interaction(name, data):
    """
    Update existing interaction
    """
    try:
        # Validate required fields
        if not data.get("candidate_id"):
            return {"success": False, "error": "Candidate is required"}
        if not data.get("interaction_type"):
            return {"success": False, "error": "Interaction type is required"}
        
        return save_doc("Interaction", data, name)
    except Exception as e:
        frappe.log_error(f"Error in update_interaction: {str(e)}")
        return {"success": False, "error": str(e)}


@frappe.whitelist()
def delete_interaction(name):
    """
    Delete interaction
    """
    try:
        return delete_doc("Interaction", name)
    except Exception as e:
        frappe.log_error(f"Error in delete_interaction: {str(e)}")
        return {"success": False, "error": str(e)}


@frappe.whitelist()
def get_interaction_stats():
    """
    Get interaction statistics
    """
    try:
        total_interactions = frappe.db.count("Interaction")
        
        # Count by interaction type
        type_stats = frappe.db.sql("""
            SELECT interaction_type, COUNT(*) as count
            FROM `tabInteraction`
            GROUP BY interaction_type
            ORDER BY count DESC
        """, as_dict=True)
        
        # Count by candidate (top 10)
        candidate_stats = frappe.db.sql("""
            SELECT i.candidate_id, c.full_name, COUNT(*) as interaction_count
            FROM `tabInteraction` i
            LEFT JOIN `tabCandidate` c ON i.candidate_id = c.name
            GROUP BY i.candidate_id, c.full_name
            ORDER BY interaction_count DESC
            LIMIT 10
        """, as_dict=True)
        
        # Recent interactions
        recent_interactions = frappe.db.sql("""
            SELECT i.name, i.candidate_id, c.full_name, i.interaction_type, 
                   i.creation, i.description
            FROM `tabInteraction` i
            LEFT JOIN `tabCandidate` c ON i.candidate_id = c.name
            ORDER BY i.creation DESC
            LIMIT 10
        """, as_dict=True)
        
        # Interactions by day (last 7 days)
        daily_stats = frappe.db.sql("""
            SELECT DATE(creation) as date, COUNT(*) as count
            FROM `tabInteraction`
            WHERE creation >= DATE_SUB(NOW(), INTERVAL 7 DAY)
            GROUP BY DATE(creation)
            ORDER BY date DESC
        """, as_dict=True)
        
        return {
            "success": True,
            "total_interactions": total_interactions,
            "type_stats": type_stats,
            "candidate_stats": candidate_stats,
            "recent_interactions": recent_interactions,
            "daily_stats": daily_stats
        }
    except Exception as e:
        frappe.log_error(f"Error in get_interaction_stats: {str(e)}")
        return {"success": False, "error": str(e)}


@frappe.whitelist()
def search_interactions(query, limit=10):
    """
    Search interactions for autocomplete
    """
    try:
        if not query:
            return []
        
        results = frappe.db.sql("""
            SELECT i.name, i.candidate_id, c.full_name, i.interaction_type,
                   i.creation, i.description
            FROM `tabInteraction` i
            LEFT JOIN `tabCandidate` c ON i.candidate_id = c.name
            WHERE c.full_name LIKE %(query)s
            OR i.interaction_type LIKE %(query)s
            OR i.description LIKE %(query)s
            ORDER BY i.creation DESC
            LIMIT %(limit)s
        """, {
            "query": f"%{query}%",
            "limit": limit
        }, as_dict=True)
        
        return results
    except Exception as e:
        frappe.log_error(f"Error in search_interactions: {str(e)}")
        return []


@frappe.whitelist()
def get_interaction_filter_options():
    """
    Get filter options for interactions
    """
    try:
        options = {}
        
        # Interaction type options
        type_result = get_filter_options("Interaction", "interaction_type")
        if type_result.get("success"):
            options["interaction_type"] = type_result["options"]
        
        # Candidate options
        candidate_result = get_filter_options("Interaction", "candidate_id")
        if candidate_result.get("success"):
            options["candidate_id"] = candidate_result["options"]
        
        # Action options
        action_result = get_filter_options("Interaction", "action")
        if action_result.get("success"):
            options["action"] = action_result["options"]
            
        return {"success": True, "options": options}
    except Exception as e:
        frappe.log_error(f"Error in get_interaction_filter_options: {str(e)}")
        return {"success": False, "error": str(e)}


@frappe.whitelist()
def get_interactions_by_candidate(candidate_id, limit=100):
    """
    Get all interactions for a specific candidate
    """
    try:
        interactions = frappe.db.sql("""
            SELECT i.name, i.interaction_type, i.action, i.url, i.description,
                   i.creation, a.name as action_name, cs.campaign_step_name
            FROM `tabInteraction` i
            LEFT JOIN `tabAction` a ON i.action = a.name
            LEFT JOIN `tabCampaignStep` cs ON a.campaign_step = cs.name
            WHERE i.candidate_id = %(candidate_id)s
            ORDER BY i.creation DESC
            LIMIT %(limit)s
        """, {"candidate_id": candidate_id, "limit": limit}, as_dict=True)
        
        return {
            "success": True,
            "data": interactions
        }
    except Exception as e:
        frappe.log_error(f"Error in get_interactions_by_candidate: {str(e)}")
        return {"success": False, "error": str(e)}


@frappe.whitelist()
def get_candidate_engagement_score(candidate_id):
    """
    Calculate engagement score for a candidate based on interactions
    """
    try:
        # Define scoring weights for different interaction types
        interaction_weights = {
            "EMAIL_OPENED": 1,
            "EMAIL_CLICKED": 3,
            "EMAIL_REPLIED": 5,
            "PAGE_VISITED": 2,
            "FORM_SUBMITTED": 8,
            "DOWNLOAD_TRIGGERED": 4,
            "CHAT_STARTED": 6,
            "CHAT_COMPLETED": 10,
            "CALL_COMPLETED": 15,
            "APPLICATION_SUBMITTED": 20,
            "DOCUMENT_UPLOADED": 10,
            "TEST_COMPLETED": 12,
            "INTERVIEW_CONFIRMED": 15
        }
        
        interactions = frappe.db.sql("""
            SELECT interaction_type, COUNT(*) as count
            FROM `tabInteraction`
            WHERE candidate_id = %(candidate_id)s
            GROUP BY interaction_type
        """, {"candidate_id": candidate_id}, as_dict=True)
        
        total_score = 0
        interaction_breakdown = {}
        
        for interaction in interactions:
            interaction_type = interaction.interaction_type
            count = interaction.count
            weight = interaction_weights.get(interaction_type, 1)
            score = count * weight
            total_score += score
            
            interaction_breakdown[interaction_type] = {
                "count": count,
                "weight": weight,
                "score": score
            }
        
        return {
            "success": True,
            "data": {
                "total_score": total_score,
                "interaction_breakdown": interaction_breakdown,
                "total_interactions": sum(i.count for i in interactions)
            }
        }
    except Exception as e:
        frappe.log_error(f"Error in get_candidate_engagement_score: {str(e)}")
        return {"success": False, "error": str(e)}
