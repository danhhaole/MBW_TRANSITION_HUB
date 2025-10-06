# Copyright (c) 2025, MBWCloud Co. and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe.utils import cstr, cint, flt, getdate, nowdate, get_datetime
from mbw_mira.api.common import get_filter_options, get_form_data, get_list_data

class MiraTalent(Document):
    
    def before_insert(self):
        #Trước khi tạo talent thì tạo prospect
        if not self.prospect:
            prospect_data = {
                "first_name": self.full_name.split(" ")[0] if self.full_name else None,
                "last_name": " ".join(self.full_name.split(" ")[1:]) if self.full_name and len(self.full_name.split(" ")) > 1 else None,
                "full_name": self.full_name,
                "gender": self.gender,
                "date_of_birth": self.date_of_birth,
                "email": self.cemail,
                "phone_number": self.phone,
                "linkedin_profile": self.linkedin_profile,
                "facebook_profile": self.facebook_profile,
                "zalo_profile": self.zalo_profile,
                "current_location": self.current_location,
                "preferred_location": self.preferred_location,
                "skills": self.skills,
                "experience_years": self.experience_years,
                "source": self.source,
                "resume": self.resume,
                "notes": self.notes
            }

            # Gọi hàm create_mira_prospect đã có sẵn
            contact = frappe.new_doc("Mira Contact")
            contact_name = contact.create_mira_contact(prospect_data)

            # Gán lại vào Talent
            self.contact_id = contact_name



@frappe.whitelist()
def get_candidate_pools_paginated(
    page=1,
    limit=12,
    search="",
    status="",
    order_by="modified desc"
):
    """
    Get paginated candidate pools - READ ONLY
    """
    try:
        # Calculate start position
        start = (cint(page) - 1) * cint(limit)
        
        # Build filters
        filters = {}
        if status:
            filters["status"] = status
        
        # Build search conditions
        search_conditions = []
        if search:
            search_conditions = [
                {"applicant_id": ["like", f"%{search}%"]},
                {"status": ["like", f"%{search}%"]},
                {"interview_feedback": ["like", f"%{search}%"]},
                {"notes": ["like", f"%{search}%"]}
            ]
        
        if search_conditions:
            filters["search_text"] = search_conditions
        
        # Fields to fetch for Mira Talent
        fields = [
            "*"
        ]
        
        # Get data using common function
        result = get_list_data(
            doctype="Mira Talent",
            filters=filters,
            order_by=order_by,
            page_length=limit,
            start=start,
            fields=fields
        )
        
        if result.get("success"):
            # Enhance data with applicant details
            candidate_pools = result["data"]
            for pool in candidate_pools:
                if pool.get("applicant_id"):
                    try:
                        applicant = frappe.get_doc("ApplicantPool", pool["applicant_id"])
                        pool["applicant_name"] = applicant.get("full_name", "")
                        pool["applicant_email"] = applicant.get("email", "")
                        pool["applicant_phone"] = applicant.get("phone", "")
                        pool["applicant_position"] = applicant.get("current_position", "")
                    except:
                        pool["applicant_name"] = pool["applicant_id"]
                        pool["applicant_email"] = ""
                        pool["applicant_phone"] = ""
                        pool["applicant_position"] = ""
            
            return {
                "success": True,
                "candidate_pools": candidate_pools,
                "pagination": result["pagination"]
            }
        else:
            return {
                "success": False,
                "error": result.get("error", "Unknown error"),
                "candidate_pools": [],
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
        frappe.log_error(f"Error in get_candidate_pools_paginated: {str(e)}")
        return {
            "success": False,
            "error": str(e),
            "candidate_pools": [],
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
def get_candidate_pool_stats():
    """
    Get candidate pool statistics - READ ONLY
    """
    try:
        total = frappe.db.count("Mira Talent")
        
        # Count by status
        shortlisted_count = frappe.db.count("Mira Talent")
        offered_count = frappe.db.count("Mira Talent")
        hired_count = frappe.db.count("Mira Talent")
        rejected_count = frappe.db.count("Mira Talent")
        
        # Recently active (modified in last 7 days)
        from frappe.utils import add_days
        week_ago = add_days(nowdate(), -7)
        recent_count = frappe.db.count("Mira Talent", {"modified": [">", week_ago]})
        
        # Average evaluation score
        avg_score_result = frappe.db.sql("""
            SELECT AVG(evaluation_score) as avg_score 
            FROM `tabMira Talent` 
            WHERE evaluation_score IS NOT NULL AND evaluation_score > 0
        """, as_dict=True)
        avg_score = 0
        
        return {
            "success": True,
            "stats": {
                "total": total,
                "shortlisted": shortlisted_count,
                "offered": offered_count,
                "hired": hired_count,
                "rejected": rejected_count,
                "recent": recent_count,
                "avg_evaluation_score": avg_score
            }
        }
        
    except Exception as e:
        frappe.log_error(f"Error in get_candidate_pool_stats: {str(e)}")
        return {
            "success": False,
            "error": str(e)
        }


@frappe.whitelist()
def search_candidate_pools(query="", limit=10):
    """
    Quick search candidate pools for autocomplete - READ ONLY
    """
    try:
        if not query:
            return {"success": True, "candidate_pools": []}
        
        candidate_pools = frappe.get_list(
            "Mira Talent",
            fields=["name", "applicant_id", "status", "evaluation_score"],
            filters=[
                ["applicant_id", "like", f"%{query}%"],
                ["status", "like", f"%{query}%"],
                ["notes", "like", f"%{query}%"]
            ],
            limit=limit,
            order_by="modified desc"
        )
        
        # Enhance with applicant details
        for pool in candidate_pools:
            if pool.get("applicant_id"):
                try:
                    applicant = frappe.get_doc("ApplicantPool", pool["applicant_id"])
                    pool["applicant_name"] = applicant.get("full_name", "")
                    pool["applicant_email"] = applicant.get("email", "")
                except:
                    pool["applicant_name"] = pool["applicant_id"]
                    pool["applicant_email"] = ""
        
        return {"success": True, "candidate_pools": candidate_pools}
        
    except Exception as e:
        frappe.log_error(f"Error in search_candidate_pools: {str(e)}")
        return {"success": False, "error": str(e)}


@frappe.whitelist()
def get_candidate_pool_by_name(name):
    """
    Get candidate pool details by name - READ ONLY
    """
    try:
        result = get_form_data("Mira Talent", name)
        if result.get("success"):
            candidate_pool = result["data"]
            
            # Enhance with applicant details
            if candidate_pool.get("applicant_id"):
                try:
                    applicant = frappe.get_doc("ApplicantPool", candidate_pool["applicant_id"])
                    candidate_pool["applicant_name"] = applicant.get("full_name", "")
                    candidate_pool["applicant_email"] = applicant.get("email", "")
                    candidate_pool["applicant_phone"] = applicant.get("phone", "")
                    candidate_pool["applicant_position"] = applicant.get("current_position", "")
                    candidate_pool["applicant_skills"] = applicant.get("skills", "")
                    candidate_pool["applicant_location"] = applicant.get("location", "")
                except:
                    candidate_pool["applicant_name"] = candidate_pool["applicant_id"]
                    candidate_pool["applicant_email"] = ""
                    candidate_pool["applicant_phone"] = ""
                    candidate_pool["applicant_position"] = ""
                    candidate_pool["applicant_skills"] = ""
                    candidate_pool["applicant_location"] = ""
            
            return {"success": True, "candidate_pool": candidate_pool}
        else:
            return {"success": False, "error": result.get("error", "Candidate pool not found")}
        
    except Exception as e:
        frappe.log_error(f"Error in get_candidate_pool_by_name: {str(e)}")
        return {"success": False, "error": str(e)}


@frappe.whitelist()
def get_candidate_pool_filter_options():
    """
    Get filter options for candidate pools - READ ONLY
    """
    try:
        # Get status options from Mira Talent doctype
        status_result = get_filter_options("Mira Talent", "status")
        status_options = status_result.get("options", []) if status_result.get("success") else []
        
        # If no options from API, provide default status options from doctype definition
        if not status_options:
            status_options = [
                {"label": "Shortlisted", "value": "Shortlisted"},
                {"label": "Offered", "value": "Offered"},
                {"label": "Hired", "value": "Hired"},
                {"label": "Rejected", "value": "Rejected"}
            ]
        
        return {
            "success": True,
            "filter_options": {
                "status": status_options
            }
        }
        
    except Exception as e:
        frappe.log_error(f"Error in get_candidate_pool_filter_options: {str(e)}")
        return {
            "success": False,
            "error": str(e)
        } 

@frappe.whitelist(allow_guest=True)
def submit_job_application():
    """
    Handle job application form submission
    Allow guest access and ignore permissions for this endpoint
    """
    try:
        # Get form data from request
        form_data = frappe.form_dict
        files = frappe.request.files
        
        # Handle file upload if exists
        if 'resume' in files:
            file = files['resume']
            file_doc = frappe.get_doc({
                'doctype': 'File',
                'file_name': file.filename,
                'content': file.stream.read(),
                'attached_to_doctype': 'Mira Talent',
                'attached_to_name': None,  # Will be set after creating the prospect
                'attached_to_field': 'resume'
            })
            file_doc.save(ignore_permissions=True)
            form_data['resume'] = file_doc.file_url

        # Basic validation
        required_fields = ['full_name', 'contact_email', 'contact_phone']
        for field in required_fields:
            if not form_data.get(field):
                return {"success": False, "error": f"Missing required field: {field}"}

        # Map form data to document fields
        doc_data = {
            'full_name': form_data.get('full_name'),
            'contact_email': form_data.get('contact_email'),
            'contact_phone': form_data.get('contact_phone'),
            'current_company': form_data.get('current_company', ''),
            'current_designation': form_data.get('current_designation', ''),
            'experience_years': form_data.get('experience_years'),
            'linkedin_profile': form_data.get('linkedin_profile', ''),
            'notes': form_data.get('notes', '')
        }
        
        # Add resume if exists
        if 'resume' in form_data:
            doc_data['resume'] = form_data['resume']

        # Create new prospect document
        doc = frappe.new_doc("Mira Talent")
        doc.update(doc_data)
        
        # Map form data to document fields
        field_mapping = {
            'full_name': 'full_name',
            'contact_email': 'email',
            'contact_phone': 'phone_number',
            'current_designation': 'current_position',
            'current_company': 'current_company',
            'experience_years': 'years_of_experience',
            'linkedin_profile': 'linkedin_profile',
            'notes': 'notes'
        }

        for form_field, doc_field in field_mapping.items():
            if form_field in form_data:
                doc.set(doc_field, form_data[form_field])

        doc.date = nowdate()

        # Handle file upload if exists
        if 'resume' in form_data and form_data['resume']:
            # You might want to handle file upload separately using frappe.upload_file()
            # For now, we'll just store the file name
            doc.resume = form_data['resume'].name

        # Save the document with ignore_permissions
        doc.flags.ignore_permissions = True
        doc.insert(ignore_permissions=True)

        # If there's a resume file, you might want to attach it here
        # This is a placeholder for file attachment logic
        # if 'resume' in form_data and form_data['resume']:
        #     attach_file_to_doc("Mira Prospect", doc.name, form_data['resume'])

        return {
            "success": True,
            "message": "Ứng tuyển thành công! Cảm ơn bạn đã nộp đơn.",
            "prospect_id": doc.name
        }

    except Exception as e:
        frappe.log_error(
            title="Job Application Error",
            message=f"Error in submit_job_application: {str(e)}\nForm Data: {form_data}"
        )
        return {
            "success": False,
            "error": "Có lỗi xảy ra khi gửi đơn ứng tuyển. Vui lòng thử lại sau."
        }

