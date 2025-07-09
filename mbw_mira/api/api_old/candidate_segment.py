import frappe
import json
from frappe.utils import cstr, cint, flt, getdate, nowdate, get_datetime, now
from frappe import _
from .common import get_list_data, get_form_data, save_doc, delete_doc, get_filter_options


@frappe.whitelist()
def get_candidate_segments_paginated(
    page=1,
    limit=12,
    search="",
    segment_id="",
    candidate_id="",
    order_by="added_at desc"
):
    """
    Get paginated candidate segments using common list data function
    """
    try:
        # Calculate start position
        start = (cint(page) - 1) * cint(limit)
        
        # Build filters
        filters = {}
        if segment_id:
            filters["segment_id"] = segment_id
        if candidate_id:
            filters["candidate_id"] = candidate_id
        
        # Build search conditions
        search_conditions = []
        if search:
            search_conditions = [
                {"candidate_id": ["like", f"%{search}%"]},
                {"segment_id": ["like", f"%{search}%"]}
            ]
        
        if search_conditions:
            filters["search_text"] = search_conditions
        
        # Fields to fetch
        fields = [
            "name", "candidate_id", "segment_id", "added_at", "added_by",
            "modified", "creation"
        ]
        
        # Get data using common function
        result = get_list_data(
            doctype="CandidateSegment",
            filters=filters,
            order_by=order_by,
            page_length=limit,
            start=start,
            fields=fields
        )
        
        if result.get("success"):
            # Enrich data with candidate and segment details
            enriched_data = []
            for item in result["data"]:
                # Get candidate details
                candidate = frappe.get_doc("Candidate", item.get("candidate_id"))
                segment = frappe.get_doc("TalentSegment", item.get("segment_id"))
                
                item.update({
                    "candidate_name": candidate.full_name,
                    "candidate_email": candidate.email,
                    "candidate_headline": candidate.headline,
                    "segment_title": segment.title,
                    "segment_type": segment.type
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
        frappe.log_error(f"Error in get_candidate_segments_paginated: {str(e)}")
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
def get_candidate_segment_by_name(name):
    """
    Get candidate segment details by name
    """
    try:
        return get_form_data("CandidateSegment", name)
    except Exception as e:
        frappe.log_error(f"Error in get_candidate_segment_by_name: {str(e)}")
        return {"success": False, "error": str(e)}


@frappe.whitelist()
def create_candidate_segment(data):
    """
    Create new candidate segment
    """
    try:
        # Validate required fields
        if not data.get("candidate_id"):
            return {"success": False, "error": "Candidate is required"}
        if not data.get("segment_id"):
            return {"success": False, "error": "Segment is required"}
        
        # Check if relationship already exists
        exists = frappe.db.exists("CandidateSegment", {
            "candidate_id": data.get("candidate_id"),
            "segment_id": data.get("segment_id")
        })
        
        if exists:
            return {"success": False, "error": "Candidate is already in this segment"}
        
        # Set default values
        data["added_at"] = now()
        data["added_by"] = frappe.session.user
        
        return save_doc("CandidateSegment", data)
    except Exception as e:
        frappe.log_error(f"Error in create_candidate_segment: {str(e)}")
        return {"success": False, "error": str(e)}


@frappe.whitelist()
def update_candidate_segment(name, data):
    """
    Update existing candidate segment
    """
    try:
        # Validate required fields
        if not data.get("candidate_id"):
            return {"success": False, "error": "Candidate is required"}
        if not data.get("segment_id"):
            return {"success": False, "error": "Segment is required"}
        
        # Check if relationship already exists (excluding current record)
        exists = frappe.db.exists("CandidateSegment", {
            "candidate_id": data.get("candidate_id"),
            "segment_id": data.get("segment_id"),
            "name": ["!=", name]
        })
        
        if exists:
            return {"success": False, "error": "Candidate is already in this segment"}
        
        return save_doc("CandidateSegment", data, name)
    except Exception as e:
        frappe.log_error(f"Error in update_candidate_segment: {str(e)}")
        return {"success": False, "error": str(e)}


@frappe.whitelist()
def delete_candidate_segment(name):
    """
    Delete candidate segment
    """
    try:
        return delete_doc("CandidateSegment", name)
    except Exception as e:
        frappe.log_error(f"Error in delete_candidate_segment: {str(e)}")
        return {"success": False, "error": str(e)}


@frappe.whitelist()
def get_candidate_segment_stats():
    """
    Get candidate segment statistics
    """
    try:
        total_relations = frappe.db.count("CandidateSegment")
        
        # Count by segment
        segment_stats = frappe.db.sql("""
            SELECT cs.segment_id, ts.title, COUNT(*) as candidate_count
            FROM `tabCandidateSegment` cs
            LEFT JOIN `tabTalentSegment` ts ON cs.segment_id = ts.name
            GROUP BY cs.segment_id, ts.title
            ORDER BY candidate_count DESC
            LIMIT 10
        """, as_dict=True)
        
        # Recent additions
        recent_additions = frappe.db.sql("""
            SELECT cs.name, cs.candidate_id, c.full_name, cs.segment_id, ts.title, cs.added_at
            FROM `tabCandidateSegment` cs
            LEFT JOIN `tabCandidate` c ON cs.candidate_id = c.name
            LEFT JOIN `tabTalentSegment` ts ON cs.segment_id = ts.name
            ORDER BY cs.added_at DESC
            LIMIT 5
        """, as_dict=True)
        
        return {
            "success": True,
            "total_relations": total_relations,
            "segment_stats": segment_stats,
            "recent_additions": recent_additions
        }
    except Exception as e:
        frappe.log_error(f"Error in get_candidate_segment_stats: {str(e)}")
        return {"success": False, "error": str(e)}


@frappe.whitelist()
def search_candidate_segments(query, limit=10):
    """
    Search candidate segments for autocomplete
    """
    try:
        if not query:
            return []
        
        results = frappe.db.sql("""
            SELECT cs.name, cs.candidate_id, c.full_name, cs.segment_id, ts.title
            FROM `tabCandidateSegment` cs
            LEFT JOIN `tabCandidate` c ON cs.candidate_id = c.name
            LEFT JOIN `tabTalentSegment` ts ON cs.segment_id = ts.name
            WHERE c.full_name LIKE %(query)s
            OR c.email LIKE %(query)s
            OR ts.title LIKE %(query)s
            ORDER BY cs.added_at DESC
            LIMIT %(limit)s
        """, {
            "query": f"%{query}%",
            "limit": limit
        }, as_dict=True)
        
        return results
    except Exception as e:
        frappe.log_error(f"Error in search_candidate_segments: {str(e)}")
        return []


@frappe.whitelist()
def get_candidate_segment_filter_options():
    """
    Get filter options for candidate segments
    """
    try:
        options = {}
        
        # Segment options
        segment_result = get_filter_options("CandidateSegment", "segment_id")
        if segment_result.get("success"):
            options["segment_id"] = segment_result["options"]
        
        # Candidate options
        candidate_result = get_filter_options("CandidateSegment", "candidate_id")
        if candidate_result.get("success"):
            options["candidate_id"] = candidate_result["options"]
            
        return {"success": True, "options": options}
    except Exception as e:
        frappe.log_error(f"Error in get_candidate_segment_filter_options: {str(e)}")
        return {"success": False, "error": str(e)}


@frappe.whitelist()
def get_candidates_by_segment(segment_id):
    """
    Get all candidates in a specific segment
    """
    try:
        candidates = frappe.db.sql("""
            SELECT cs.name, cs.candidate_id, c.full_name, c.email, 
                   c.headline, c.status, cs.added_at
            FROM `tabCandidateSegment` cs
            LEFT JOIN `tabCandidate` c ON cs.candidate_id = c.name
            WHERE cs.segment_id = %(segment_id)s
            ORDER BY cs.added_at DESC
        """, {"segment_id": segment_id}, as_dict=True)
        
        return {
            "success": True,
            "data": candidates
        }
    except Exception as e:
        frappe.log_error(f"Error in get_candidates_by_segment: {str(e)}")
        return {"success": False, "error": str(e)}


@frappe.whitelist()
def get_segments_by_candidate(candidate_id):
    """
    Get all segments for a specific candidate
    """
    try:
        segments = frappe.db.sql("""
            SELECT cs.name, cs.segment_id, ts.title, ts.type, 
                   ts.description, cs.added_at
            FROM `tabCandidateSegment` cs
            LEFT JOIN `tabTalentSegment` ts ON cs.segment_id = ts.name
            WHERE cs.candidate_id = %(candidate_id)s
            ORDER BY cs.added_at DESC
        """, {"candidate_id": candidate_id}, as_dict=True)
        
        return {
            "success": True,
            "data": segments
        }
    except Exception as e:
        frappe.log_error(f"Error in get_segments_by_candidate: {str(e)}")
        return {"success": False, "error": str(e)}


@frappe.whitelist()
def bulk_add_candidates_to_segment(segment_id, candidate_ids):
    """
    Add multiple candidates to a segment
    """
    try:
        if isinstance(candidate_ids, str):
            candidate_ids = json.loads(candidate_ids)
        
        results = []
        for candidate_id in candidate_ids:
            # Check if relationship already exists
            exists = frappe.db.exists("CandidateSegment", {
                "candidate_id": candidate_id,
                "segment_id": segment_id
            })
            
            if not exists:
                doc = frappe.new_doc("CandidateSegment")
                doc.candidate_id = candidate_id
                doc.segment_id = segment_id
                doc.added_at = now()
                doc.added_by = frappe.session.user
                doc.save()
                results.append({"candidate_id": candidate_id, "status": "added"})
            else:
                results.append({"candidate_id": candidate_id, "status": "already_exists"})
        
        return {"success": True, "results": results}
    except Exception as e:
        frappe.log_error(f"Error in bulk_add_candidates_to_segment: {str(e)}")
        return {"success": False, "error": str(e)}


@frappe.whitelist()
def bulk_remove_candidates_from_segment(segment_id, candidate_ids):
    """
    Remove multiple candidates from a segment
    """
    try:
        if isinstance(candidate_ids, str):
            candidate_ids = json.loads(candidate_ids)
        
        results = []
        for candidate_id in candidate_ids:
            # Find and delete relationship
            relation = frappe.db.exists("CandidateSegment", {
                "candidate_id": candidate_id,
                "segment_id": segment_id
            })
            
            if relation:
                frappe.delete_doc("CandidateSegment", relation)
                results.append({"candidate_id": candidate_id, "status": "removed"})
            else:
                results.append({"candidate_id": candidate_id, "status": "not_found"})
        
        return {"success": True, "results": results}
    except Exception as e:
        frappe.log_error(f"Error in bulk_remove_candidates_from_segment: {str(e)}")
        return {"success": False, "error": str(e)}
