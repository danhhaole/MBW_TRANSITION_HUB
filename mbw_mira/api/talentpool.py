import frappe
import json
from frappe.utils import cstr, cint, flt, getdate, nowdate, get_datetime
from frappe import _
from .common import get_list_data, get_form_data, save_doc, delete_doc, get_filter_options


@frappe.whitelist()
def get_talent_pools_paginated(
    page=1,
    limit=12,
    search="",
    status="",
    source="",
    skills="",
    order_by="modified desc"
):
    """
    Get paginated talent pools using common list data function
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
                {"current_position": ["like", f"%{search}%"]},
                {"location": ["like", f"%{search}%"]},
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
        
        # Fields to fetch for TalentPool
        fields = [
            "name", "full_name", "email", "phone", "current_position", "location", 
            "experience_years", "source", "skills", "status", "campaign_id", 
            "segment_id", "synced_at", "notes", "modified", "creation"
        ]
        
        # Get data using common function
        result = get_list_data(
            doctype="TalentPool",
            filters=filters,
            order_by=order_by,
            page_length=limit,
            start=start,
            fields=fields
        )
        
        if result.get("success"):
            return {
                "success": True,
                "talent_pools": result["data"],
                "pagination": result["pagination"]
            }
        else:
            return {
                "success": False,
                "error": result.get("error", "Unknown error"),
                "talent_pools": [],
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
        frappe.log_error(f"Error in get_talent_pools_paginated: {str(e)}")
        return {
            "success": False,
            "error": str(e),
            "talent_pools": [],
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
def get_talent_pool_stats():
    """
    Get talent pool statistics
    """
    try:
        total = frappe.db.count("TalentPool")
        
        # Count by status
        active_count = frappe.db.count("TalentPool", {"status": "Active"})
        inactive_count = frappe.db.count("TalentPool", {"status": "Inactive"})
        
        # Recently active (modified in last 7 days)
        from frappe.utils import add_days
        week_ago = add_days(nowdate(), -7)
        recent_count = frappe.db.count("TalentPool", {"modified": [">", week_ago]})
        
        # Count by experience levels
        junior_count = frappe.db.count("TalentPool", {"experience_years": ["<", 3]})
        senior_count = frappe.db.count("TalentPool", {"experience_years": [">=", 5]})
        
        return {
            "success": True,
            "stats": {
                "total": total,
                "active": active_count,
                "inactive": inactive_count,
                "recent": recent_count,
                "junior": junior_count,
                "senior": senior_count
            }
        }
        
    except Exception as e:
        frappe.log_error(f"Error in get_talent_pool_stats: {str(e)}")
        return {
            "success": False,
            "error": str(e)
        }


@frappe.whitelist()
def search_talent_pools(query="", limit=10):
    """
    Quick search talent pools for autocomplete
    """
    try:
        if not query:
            return {"success": True, "talent_pools": []}
        
        talent_pools = frappe.get_list(
            "TalentPool",
            fields=["name", "full_name", "email", "current_position", "location"],
            filters=[
                ["full_name", "like", f"%{query}%"],
                ["email", "like", f"%{query}%"],
                ["current_position", "like", f"%{query}%"],
                ["location", "like", f"%{query}%"]
            ],
            limit=limit,
            order_by="full_name asc"
        )
        
        return {"success": True, "talent_pools": talent_pools}
        
    except Exception as e:
        frappe.log_error(f"Error in search_talent_pools: {str(e)}")
        return {"success": False, "error": str(e)}


@frappe.whitelist()
def get_talent_pool_by_name(name):
    """
    Get talent pool details by name using common form data function
    """
    try:
        result = get_form_data("TalentPool", name)
        if result.get("success"):
            talent_pool = result["data"]
            
            # Process skills if it's JSON string
            if talent_pool.get("skills") and isinstance(talent_pool["skills"], str):
                try:
                    talent_pool["skills"] = json.loads(talent_pool["skills"])
                except:
                    talent_pool["skills"] = talent_pool["skills"].split(",") if talent_pool["skills"] else []
            
            return {"success": True, "talent_pool": talent_pool}
        else:
            return {"success": False, "error": result.get("error", "Talent pool not found")}
        
    except Exception as e:
        frappe.log_error(f"Error in get_talent_pool_by_name: {str(e)}")
        return {"success": False, "error": str(e)}


@frappe.whitelist()
def create_talent_pool(data):
    """
    Create new talent pool using common save function
    """
    try:
        if isinstance(data, str):
            data = json.loads(data)
        
        # Process skills array to JSON string
        if "skills" in data and isinstance(data["skills"], list):
            data["skills"] = json.dumps(data["skills"])
        
        # Convert experience_years to float if provided
        if "experience_years" in data and data["experience_years"]:
            try:
                data["experience_years"] = flt(data["experience_years"])
            except:
                data["experience_years"] = 0
        
        result = save_doc("TalentPool", data)
        
        if result.get("success"):
            talent_pool = result["data"]
            
            # Process skills back to array for response
            if talent_pool.get("skills") and isinstance(talent_pool["skills"], str):
                try:
                    talent_pool["skills"] = json.loads(talent_pool["skills"])
                except:
                    talent_pool["skills"] = talent_pool["skills"].split(",") if talent_pool["skills"] else []
            
            return {"success": True, "talent_pool": talent_pool, "message": result["message"]}
        else:
            return result
        
    except Exception as e:
        frappe.log_error(f"Error in create_talent_pool: {str(e)}")
        return {"success": False, "error": str(e)}


@frappe.whitelist()
def update_talent_pool(name, data):
    """
    Update talent pool using common save function
    """
    try:
        if isinstance(data, str):
            data = json.loads(data)
        
        # Process skills array to JSON string
        if "skills" in data and isinstance(data["skills"], list):
            data["skills"] = json.dumps(data["skills"])
        
        # Convert experience_years to float if provided
        if "experience_years" in data and data["experience_years"]:
            try:
                data["experience_years"] = flt(data["experience_years"])
            except:
                data["experience_years"] = 0
        
        result = save_doc("TalentPool", data, name)
        
        if result.get("success"):
            talent_pool = result["data"]
            
            # Process skills back to array for response
            if talent_pool.get("skills") and isinstance(talent_pool["skills"], str):
                try:
                    talent_pool["skills"] = json.loads(talent_pool["skills"])
                except:
                    talent_pool["skills"] = talent_pool["skills"].split(",") if talent_pool["skills"] else []
            
            return {"success": True, "talent_pool": talent_pool, "message": result["message"]}
        else:
            return result
        
    except Exception as e:
        frappe.log_error(f"Error in update_talent_pool: {str(e)}")
        return {"success": False, "error": str(e)}


@frappe.whitelist()
def delete_talent_pool(name):
    """
    Delete talent pool using common delete function
    """
    try:
        result = delete_doc("TalentPool", name)
        return result
        
    except Exception as e:
        frappe.log_error(f"Error in delete_talent_pool: {str(e)}")
        return {"success": False, "error": str(e)}


@frappe.whitelist()
def get_talent_pool_filter_options():
    """
    Get filter options for talent pools
    """
    try:
        # Get status options from TalentPool doctype
        status_result = get_filter_options("TalentPool", "status")
        status_options = status_result.get("options", []) if status_result.get("success") else []
        
        # If no options from API, provide default status options
        if not status_options:
            status_options = [
                {"label": "Active", "value": "Active"},
                {"label": "Inactive", "value": "Inactive"}
            ]
        
        # Get source options
        source_result = get_filter_options("TalentPool", "source")
        source_options = source_result.get("options", []) if source_result.get("success") else []
        
        # If no options from API, provide default source options
        if not source_options:
            source_options = [
                {"label": "Manual", "value": "Manual"},
                {"label": "LinkedIn", "value": "LinkedIn"},
                {"label": "Website", "value": "Website"},
                {"label": "Referral", "value": "Referral"},
                {"label": "Job Board", "value": "Job Board"},
                {"label": "ATS Import", "value": "ATS Import"},
                {"label": "Email", "value": "Email"}
            ]
        
        # Get unique skills from talent pools
        talent_pools = frappe.get_all("TalentPool", fields=["skills"], filters={"skills": ["!=", ""]})
        all_skills = []
        for pool in talent_pools:
            if pool.skills:
                try:
                    if pool.skills.startswith('[') or pool.skills.startswith('{'):
                        skills = json.loads(pool.skills)
                        if isinstance(skills, list):
                            all_skills.extend([str(skill).strip() for skill in skills if skill])
                        elif isinstance(skills, dict):
                            all_skills.extend([str(v).strip() for v in skills.values() if v])
                    else:
                        skills = pool.skills.split(',')
                        all_skills.extend([skill.strip() for skill in skills if skill.strip()])
                except:
                    # Fallback for plain text skills
                    if ',' in pool.skills:
                        skills = pool.skills.split(',')
                    else:
                        skills = [pool.skills]
                    all_skills.extend([skill.strip() for skill in skills if skill.strip()])
        
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
        frappe.log_error(f"Error in get_talent_pool_filter_options: {str(e)}")
        return {
            "success": False,
            "error": str(e),
            "options": {
                "status": [],
                "source": [],
                "skills": []
            }
        }


# Legacy functions for backward compatibility - these will redirect to new TalentPool functions
@frappe.whitelist()
def get_candidates_paginated(*args, **kwargs):
    """Legacy function - redirects to get_talent_pools_paginated"""
    return get_talent_pools_paginated(*args, **kwargs)

@frappe.whitelist()
def get_candidate_stats():
    """Legacy function - redirects to get_talent_pool_stats"""
    return get_talent_pool_stats()

@frappe.whitelist()
def search_candidates(*args, **kwargs):
    """Legacy function - redirects to search_talent_pools"""
    return search_talent_pools(*args, **kwargs)

@frappe.whitelist()
def get_candidate_by_name(*args, **kwargs):
    """Legacy function - redirects to get_talent_pool_by_name"""
    return get_talent_pool_by_name(*args, **kwargs)

@frappe.whitelist()
def create_candidate(*args, **kwargs):
    """Legacy function - redirects to create_talent_pool"""
    return create_talent_pool(*args, **kwargs)

@frappe.whitelist()
def update_candidate(*args, **kwargs):
    """Legacy function - redirects to update_talent_pool"""
    return update_talent_pool(*args, **kwargs)

@frappe.whitelist()
def delete_candidate(*args, **kwargs):
    """Legacy function - redirects to delete_talent_pool"""
    return delete_talent_pool(*args, **kwargs)

@frappe.whitelist()
def get_candidate_filter_options():
    """Legacy function - redirects to get_talent_pool_filter_options"""
    return get_talent_pool_filter_options() 