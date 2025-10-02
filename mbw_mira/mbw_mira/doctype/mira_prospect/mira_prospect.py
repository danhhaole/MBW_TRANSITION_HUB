# Copyright (c) 2025, MBWCloud Co. and contributors
# For license information, please see license.txt

import json
import frappe
from frappe.model.document import Document
from frappe.utils import now_datetime,nowdate,cint
from mbw_mira.api.common import delete_doc, get_filter_options, get_form_data, get_list_data, save_doc


class MiraProspect(Document):
	
    def validate(self):
        # Check trùng talent_id,candidate_id
        self.validate_unique_prospect()

			
    def validate_unique_prospect(self):
        """
        Kiểm tra xem đã tồn tại Mira Prospect với cùng
        talent_id + candidate_id (ngoại trừ chính nó) hay chưa.
        """																												
        filters = {
            "email": self.email
        }

        existing = frappe.db.exists("Mira Prospect", filters)

        if existing and existing != self.name:
            frappe.throw(
            frappe._(
                "A Mira Prospect with Email <b>{0}</b> already exists: <a href='/app/Mira Prospect/{1}'>{1}</a>"
            ).format(self.email, existing),
            title=frappe._("Duplicate Mira Prospect"),
        )
    @staticmethod
    def create_mira_prospect(data: dict) ->str:
        if not data:
            frappe.throw(frappe._("Missing data for creating Mira Prospect"))

        doc = frappe.new_doc("Mira Prospect")

        # Map dữ liệu từ dict vào doc
        meta = frappe.get_meta("Mira Prospect")
        allowed_fields = [f.fieldname for f in meta.fields]

        for field, value in data.items():
            if field in allowed_fields:
                doc.set(field, value)

        # Insert vào DB
        doc.insert(ignore_permissions=True)
        frappe.db.commit()

        return doc.name
def create_mira_prospect_segment(self):
	#Tìm talentsegment theo title (position)
	segment = frappe.db.get_value("Mira Segment",{"title":self.position},"name")
	if segment:
		#Kiểm tra tồn tại profile trong segment chưa
		profile_segment_exists = frappe.db.exists("MiraProspectSegment",{"talent_id":self.name,"segment_id":segment})
		if not profile_segment_exists:
			doc = frappe.get_doc({
				"doctype":"MiraProspectSegment",
				"talent_id":self.name,
    			"segment_id":segment,
				"added_at": now_datetime(),
				"added_by": frappe.session.user
       		})
			doc.insert(ignore_permissions=True)
			frappe.db.commit()

		return True
#     "talent_id",
#   "segment_id",
#   "match_score",
#   "added_at",
#   "added_by"



@frappe.whitelist()
def get_prospects_paginated(
    page=1,
    limit=12,
    search="",
    status="",
    source="",
    skills="",
    order_by="modified desc"
):
    """
    Get paginated talent profiles using common list data function
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
        
        # Fields to fetch for Mira Prospect
        fields = [
            "name", "full_name", "email", "phone", "avatar", "headline", 
            "source", "skills", "ai_summary", "status", "last_interaction", 
            "email_opt_out", "modified", "creation"
        ]
        
        # Get data using common function
        result = get_list_data(
            doctype="Mira Prospect",
            filters=filters,
            order_by=order_by,
            page_length=limit,
            start=start,
            fields=fields
        )
        
        if result.get("success"):
            return {
                "success": True,
                "talent_profiles": result["data"],
                "pagination": result["pagination"]
            }
        else:
            return {
                "success": False,
                "error": result.get("error", "Unknown error"),
                "talent_profiles": [],
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
        frappe.log_error(f"Error in get_talent_profiles_paginated: {str(e)}")
        return {
            "success": False,
            "error": str(e),
            "talent_profiles": [],
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
def get_talent_profile_stats():
    """
    Get talent profile statistics
    """
    try:
        total = frappe.db.count("Mira Prospect")
        
        # Count by status
        new_count = frappe.db.count("Mira Prospect", {"status": "NEW"})
        sourced_count = frappe.db.count("Mira Prospect", {"status": "SOURCED"})
        nurturing_count = frappe.db.count("Mira Prospect", {"status": "NURTURING"})
        engaged_count = frappe.db.count("Mira Prospect", {"status": "ENGAGED"})
        archived_count = frappe.db.count("Mira Prospect", {"status": "ARCHIVED"})
        
        # Recently active (modified in last 7 days)
        from frappe.utils import add_days
        week_ago = add_days(nowdate(), -7)
        recent_count = frappe.db.count("Mira Prospect", {"modified": [">", week_ago]})
        
        return {
            "success": True,
            "stats": {
                "total": total,
                "new": new_count,
                "sourced": sourced_count,
                "nurturing": nurturing_count,
                "engaged": engaged_count,
                "archived": archived_count,
                "recent": recent_count
            }
        }
        
    except Exception as e:
        frappe.log_error(f"Error in get_talent_profile_stats: {str(e)}")
        return {
            "success": False,
            "error": str(e)
        }


@frappe.whitelist()
def search_talent_profiles(query="", limit=10):
    """
    Quick search talent profiles for autocomplete
    """
    try:
        if not query:
            return {"success": True, "talent_profiles": []}
        
        talent_profiles = frappe.get_list(
            "Mira Prospect",
            fields=["name", "full_name", "email", "headline", "status"],
            filters=[
                ["full_name", "like", f"%{query}%"],
                ["email", "like", f"%{query}%"],
                ["headline", "like", f"%{query}%"]
            ],
            limit=limit,
            order_by="full_name asc"
        )
        
        return {"success": True, "talent_profiles": talent_profiles}
        
    except Exception as e:
        frappe.log_error(f"Error in search_talent_profiles: {str(e)}")
        return {"success": False, "error": str(e)}


@frappe.whitelist()
def get_talent_profile_by_name(name):
    """
    Get talent profile details by name using common form data function
    """
    try:
        result = get_form_data("Mira Prospect", name)
        if result.get("success"):
            talent_profile = result["data"]
            
            # Process skills if it's JSON string
            if talent_profile.get("skills") and isinstance(talent_profile["skills"], str):
                try:
                    talent_profile["skills"] = json.loads(talent_profile["skills"])
                except:
                    talent_profile["skills"] = talent_profile["skills"].split(",") if talent_profile["skills"] else []
            
            return {"success": True, "talent_profile": talent_profile}
        else:
            return {"success": False, "error": result.get("error", "Talent profile not found")}
        
    except Exception as e:
        frappe.log_error(f"Error in get_talent_profile_by_name: {str(e)}")
        return {"success": False, "error": str(e)}


@frappe.whitelist()
def create_talent_profile(data):
    """
    Create new talent profile using common save function
    """
    try:
        if isinstance(data, str):
            data = json.loads(data)
        
        # Process skills array to string if needed
        if "skills" in data and isinstance(data["skills"], list):
            data["skills"] = ", ".join(data["skills"])
        
        result = save_doc("Mira Prospect", data)
        
        if result.get("success"):
            talent_profile = result["data"]
            
            # Process skills back to array for response if needed
            if talent_profile.get("skills") and isinstance(talent_profile["skills"], str):
                if "," in talent_profile["skills"]:
                    talent_profile["skills"] = [s.strip() for s in talent_profile["skills"].split(",")]
            
            return {"success": True, "talent_profile": talent_profile, "message": result["message"]}
        else:
            return result
        
    except Exception as e:
        frappe.log_error(f"Error in create_talent_profile: {str(e)}")
        return {"success": False, "error": str(e)}


@frappe.whitelist()
def update_talent_profile(name, data):
    """
    Update talent profile using common save function
    """
    try:
        if isinstance(data, str):
            data = json.loads(data)
        
        # Process skills array to string if needed
        if "skills" in data and isinstance(data["skills"], list):
            data["skills"] = ", ".join(data["skills"])
        
        result = save_doc("Mira Prospect", data, name)
        
        if result.get("success"):
            talent_profile = result["data"]
            
            # Process skills back to array for response if needed
            if talent_profile.get("skills") and isinstance(talent_profile["skills"], str):
                if "," in talent_profile["skills"]:
                    talent_profile["skills"] = [s.strip() for s in talent_profile["skills"].split(",")]
            
            return {"success": True, "talent_profile": talent_profile, "message": result["message"]}
        else:
            return result
        
    except Exception as e:
        frappe.log_error(f"Error in update_talent_profile: {str(e)}")
        return {"success": False, "error": str(e)}


@frappe.whitelist()
def delete_talent_profile(name):
    """
    Delete talent profile using common delete function
    """
    try:
        result = delete_doc("Mira Prospect", name)
        return result
        
    except Exception as e:
        frappe.log_error(f"Error in delete_talent_profile: {str(e)}")
        return {"success": False, "error": str(e)}


@frappe.whitelist()
def get_talent_profile_filter_options():
    """
    Get filter options for talent profiles
    """
    try:
        # Get status options from Mira Prospect doctype
        status_result = get_filter_options("Mira Prospect", "status")
        status_options = status_result.get("options", []) if status_result.get("success") else []
        
        # If no options from API, provide default status options
        if not status_options:
            status_options = [
                {"label": "NEW", "value": "NEW"},
                {"label": "SOURCED", "value": "SOURCED"},
                {"label": "NURTURING", "value": "NURTURING"},
                {"label": "ENGAGED", "value": "ENGAGED"},
                {"label": "ARCHIVED", "value": "ARCHIVED"}
            ]
        
        # Get source options
        source_result = get_filter_options("Mira Prospect", "source")
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
        
        # Get unique skills from talent profiles
        talent_profiles = frappe.get_all("Mira Prospect", fields=["skills"], filters={"skills": ["!=", ""]})
        all_skills = []
        for profile in talent_profiles:
            if profile.skills:
                try:
                    if "," in profile.skills:
                        skills = profile.skills.split(',')
                    else:
                        skills = [profile.skills]
                    all_skills.extend([skill.strip() for skill in skills if skill.strip()])
                except:
                    # Fallback for plain text skills
                    all_skills.append(profile.skills.strip())
        
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
        frappe.log_error(f"Error in get_talent_profile_filter_options: {str(e)}")
        return {
            "success": False,
            "error": str(e),
            "options": {
                "status": [],
                "source": [],
                "skills": []
            }
        } 