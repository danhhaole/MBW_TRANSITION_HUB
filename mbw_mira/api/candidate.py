import frappe
import json
from frappe.utils import cstr, cint, flt, getdate, nowdate, get_datetime
from frappe import _
from .common import get_list_data, get_form_data, save_doc, delete_doc, get_filter_options


@frappe.whitelist()
def get_candidates_paginated(
    page=1,
    limit=12,
    search="",
    status="",
    source="",
    skills="",
    order_by="modified desc"
):
    """
    Get paginated candidates using common list data function
    """
    try:
        # Calculate start position
        start = (cint(page) - 1) * cint(limit)
        
        # Build filters
        filters = {}
        if status:
            filters["status"] = status
        if source:
            filters["source"] = source
        
        # Build search conditions
        search_conditions = []
        if search:
            search_conditions = [
                {"full_name": ["like", f"%{search}%"]},
                {"email": ["like", f"%{search}%"]},
                {"headline": ["like", f"%{search}%"]},
                {"skills": ["like", f"%{search}%"]}
            ]
        
        # Add skills filter
        if skills:
            if isinstance(skills, str):
                skills = json.loads(skills) if skills.startswith('[') else [skills]
            for skill in skills:
                search_conditions.append({"skills": ["like", f"%{skill}%"]})
        
        if search_conditions:
            filters["search_text"] = search_conditions
        
        # Fields to fetch
        fields = [
            "name", "full_name", "email", "phone", "headline", "source", 
            "skills", "status", "cv_original_url", "ai_summary", 
            "profile_data", "email_opt_out", "modified", "creation"
        ]
        
        # Get data using common function
        result = get_list_data(
            doctype="Candidate",
            filters=filters,
            order_by=order_by,
            page_length=limit,
            start=start,
            fields=fields
        )
        
        if result.get("success"):
            return {
                "success": True,
                "candidates": result["data"],
                "pagination": result["pagination"]
            }
        else:
            return {
                "success": False,
                "error": result.get("error", "Unknown error"),
                "candidates": [],
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
        frappe.log_error(f"Error in get_candidates_paginated: {str(e)}")
        return {
            "success": False,
            "error": str(e),
            "candidates": [],
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
def get_candidate_stats():
    """
    Get candidate statistics
    """
    try:
        total = frappe.db.count("Candidate")
        
        # Count by status
        new_count = frappe.db.count("Candidate", {"status": "New"})
        nurturing_count = frappe.db.count("Candidate", {"status": "Nurturing"})
        qualified_count = frappe.db.count("Candidate", {"status": "Qualified"})
        
        # Recently active (modified in last 7 days)
        from frappe.utils import add_days
        week_ago = add_days(nowdate(), -7)
        recent_count = frappe.db.count("Candidate", {"modified": [">", week_ago]})
        
        return {
            "success": True,
            "stats": {
                "total": total,
                "new": new_count,
                "nurturing": nurturing_count,
                "qualified": qualified_count,
                "recent": recent_count
            }
        }
        
    except Exception as e:
        frappe.log_error(f"Error in get_candidate_stats: {str(e)}")
        return {
            "success": False,
            "error": str(e)
        }


@frappe.whitelist()
def search_candidates(query="", limit=10):
    """
    Quick search candidates for autocomplete
    """
    try:
        if not query:
            return {"success": True, "candidates": []}
        
        candidates = frappe.get_list(
            "Candidate",
            fields=["name", "full_name", "email", "headline"],
            filters=[
                ["full_name", "like", f"%{query}%"],
                ["email", "like", f"%{query}%"],
                ["headline", "like", f"%{query}%"]
            ],
            limit=limit,
            order_by="full_name asc"
        )
        
        return {"success": True, "candidates": candidates}
        
    except Exception as e:
        frappe.log_error(f"Error in search_candidates: {str(e)}")
        return {"success": False, "error": str(e)}


@frappe.whitelist()
def get_candidate_by_name(name):
    """
    Get candidate details by name using common form data function
    """
    try:
        result = get_form_data("Candidate", name)
        if result.get("success"):
            candidate = result["data"]
            
            # Process skills if it's JSON string
            if candidate.get("skills") and isinstance(candidate["skills"], str):
                try:
                    candidate["skills"] = json.loads(candidate["skills"])
                except:
                    candidate["skills"] = candidate["skills"].split(",") if candidate["skills"] else []
            
            # Process profile_data if it's JSON string
            if candidate.get("profile_data") and isinstance(candidate["profile_data"], str):
                try:
                    candidate["profile_data"] = json.loads(candidate["profile_data"])
                except:
                    pass
            
            return {"success": True, "candidate": candidate}
        else:
            return {"success": False, "error": result.get("error", "Candidate not found")}
        
    except Exception as e:
        frappe.log_error(f"Error in get_candidate_by_name: {str(e)}")
        return {"success": False, "error": str(e)}


@frappe.whitelist()
def create_candidate(data):
    """
    Create new candidate using common save function
    """
    try:
        if isinstance(data, str):
            data = json.loads(data)
        
        # Process skills array to JSON string
        if "skills" in data and isinstance(data["skills"], list):
            data["skills"] = json.dumps(data["skills"])
        
        # Process profile_data to JSON string
        if "profile_data" in data and not isinstance(data["profile_data"], str):
            data["profile_data"] = json.dumps(data["profile_data"])
        
        result = save_doc("Candidate", data)
        
        if result.get("success"):
            candidate = result["data"]
            
            # Process skills back to array for response
            if candidate.get("skills") and isinstance(candidate["skills"], str):
                try:
                    candidate["skills"] = json.loads(candidate["skills"])
                except:
                    candidate["skills"] = candidate["skills"].split(",") if candidate["skills"] else []
            
            return {"success": True, "candidate": candidate, "message": result["message"]}
        else:
            return result
        
    except Exception as e:
        frappe.log_error(f"Error in create_candidate: {str(e)}")
        return {"success": False, "error": str(e)}


@frappe.whitelist()
def update_candidate(name, data):
    """
    Update candidate using common save function
    """
    try:
        if isinstance(data, str):
            data = json.loads(data)
        
        # Process skills array to JSON string
        if "skills" in data and isinstance(data["skills"], list):
            data["skills"] = json.dumps(data["skills"])
        
        # Process profile_data to JSON string
        if "profile_data" in data and not isinstance(data["profile_data"], str):
            data["profile_data"] = json.dumps(data["profile_data"])
        
        result = save_doc("Candidate", data, name)
        
        if result.get("success"):
            candidate = result["data"]
            
            # Process skills back to array for response
            if candidate.get("skills") and isinstance(candidate["skills"], str):
                try:
                    candidate["skills"] = json.loads(candidate["skills"])
                except:
                    candidate["skills"] = candidate["skills"].split(",") if candidate["skills"] else []
            
            return {"success": True, "candidate": candidate, "message": result["message"]}
        else:
            return result
        
    except Exception as e:
        frappe.log_error(f"Error in update_candidate: {str(e)}")
        return {"success": False, "error": str(e)}


@frappe.whitelist()
def delete_candidate(name):
    """
    Delete candidate using common delete function
    """
    try:
        result = delete_doc("Candidate", name)
        return result
        
    except Exception as e:
        frappe.log_error(f"Error in delete_candidate: {str(e)}")
        return {"success": False, "error": str(e)}


@frappe.whitelist()
def get_candidate_filter_options():
    """
    Get filter options for candidates
    """
    try:
        # Get status options
        status_result = get_filter_options("Candidate", "status")
        status_options = status_result.get("options", []) if status_result.get("success") else []
        
        # Get source options
        source_result = get_filter_options("Candidate", "source")
        source_options = source_result.get("options", []) if source_result.get("success") else []
        
        # Get unique skills
        candidates = frappe.get_all("Candidate", fields=["skills"], filters={"skills": ["!=", ""]})
        all_skills = []
        for candidate in candidates:
            if candidate.skills:
                try:
                    if candidate.skills.startswith('['):
                        skills = json.loads(candidate.skills)
                    else:
                        skills = candidate.skills.split(',')
                    all_skills.extend([skill.strip() for skill in skills if skill.strip()])
                except:
                    continue
        
        unique_skills = list(set(all_skills))
        skills_options = [{"label": skill, "value": skill} for skill in sorted(unique_skills)]
        
        return {
            "success": True,
            "options": {
                "status": status_options,
                "source": source_options,
                "skills": skills_options
            }
        }
        
    except Exception as e:
        frappe.log_error(f"Error in get_candidate_filter_options: {str(e)}")
        return {
            "success": False,
            "error": str(e),
            "options": {
                "status": [],
                "source": [],
                "skills": []
            }
        } 