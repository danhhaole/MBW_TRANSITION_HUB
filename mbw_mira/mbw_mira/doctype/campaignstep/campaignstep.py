# Copyright (c) 2025, MBWCloud Co. and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe.utils import cint
from mbw_mira.api.common import delete_doc, get_filter_options, get_form_data, get_list_data, save_doc

class CampaignStep(Document):
	pass

	def after_insert(self):
		if self.campaign:
			update_total_campaign_step(self)

	
	def after_delete(self):
		if self.campaign:
			update_total_campaign_step(self)

def update_total_campaign_step(self):
	campaign = frappe.get_doc("Campaign",self.campaign)
	total_step = frappe.db.count("CampaignStep",{"campaign":self.campaign})
	campaign.update({
		"total":total_step
    })
	campaign.save(ignore_permissions=True)
	frappe.db.commit()


@frappe.whitelist()
def get_campaign_steps_paginated(
    page=1,
    limit=12,
    search="",
    campaign="",
    action_type="",
    order_by="step_order asc"
):
    """
    Get paginated campaign steps using common list data function
    """
    try:
        # Calculate start position
        start = (cint(page) - 1) * cint(limit)
        
        # Build filters
        filters = {}
        if campaign:
            filters["campaign"] = campaign
        if action_type:
            filters["action_type"] = action_type
        
        # Build search conditions
        search_conditions = []
        if search:
            search_conditions = [
                {"campaign_step_name": ["like", f"%{search}%"]},
                {"template": ["like", f"%{search}%"]},
                {"action_type": ["like", f"%{search}%"]}
            ]
        
        if search_conditions:
            filters["search_text"] = search_conditions
        
        # Fields to fetch
        fields = [
            "name", "campaign_step_name", "campaign", "step_order", 
            "action_type", "delay_in_days", "template", "action_config",
            "modified", "creation"
        ]
        
        # Get data using common function
        result = get_list_data(
            doctype="CampaignStep",
            filters=filters,
            order_by=order_by,
            page_length=limit,
            start=start,
            fields=fields
        )
        
        if result.get("success"):
            return {
                "success": True,
                "data": result["data"],
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
        frappe.log_error(f"Error in get_campaign_steps_paginated: {str(e)}")
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
def get_campaign_step_by_name(name):
    """
    Get campaign step details by name
    """
    try:
        return get_form_data("CampaignStep", name)
    except Exception as e:
        frappe.log_error(f"Error in get_campaign_step_by_name: {str(e)}")
        return {"success": False, "error": str(e)}


@frappe.whitelist()
def create_campaign_step(data):
    """
    Create new campaign step
    """
    try:
        # Validate required fields
        if not data.get("campaign_step_name"):
            return {"success": False, "error": "Campaign step name is required"}
        if not data.get("campaign"):
            return {"success": False, "error": "Campaign is required"}
        if not data.get("action_type"):
            return {"success": False, "error": "Action type is required"}
        
        # Auto-assign step order if not provided
        if not data.get("step_order"):
            max_order = frappe.db.get_value(
                "CampaignStep", 
                {"campaign": data.get("campaign")}, 
                "MAX(step_order)"
            ) or 0
            data["step_order"] = max_order + 1
        
        return save_doc("CampaignStep", data)
    except Exception as e:
        frappe.log_error(f"Error in create_campaign_step: {str(e)}")
        return {"success": False, "error": str(e)}


@frappe.whitelist()
def update_campaign_step(name, data):
    """
    Update existing campaign step
    """
    try:
        # Validate required fields
        if not data.get("campaign_step_name"):
            return {"success": False, "error": "Campaign step name is required"}
        if not data.get("campaign"):
            return {"success": False, "error": "Campaign is required"}
        if not data.get("action_type"):
            return {"success": False, "error": "Action type is required"}
        
        return save_doc("CampaignStep", data, name)
    except Exception as e:
        frappe.log_error(f"Error in update_campaign_step: {str(e)}")
        return {"success": False, "error": str(e)}


@frappe.whitelist()
def delete_campaign_step(name):
    """
    Delete campaign step
    """
    try:
        return delete_doc("CampaignStep", name)
    except Exception as e:
        frappe.log_error(f"Error in delete_campaign_step: {str(e)}")
        return {"success": False, "error": str(e)}


@frappe.whitelist()
def get_campaign_step_stats():
    """
    Get campaign step statistics
    """
    try:
        total_steps = frappe.db.count("CampaignStep")
        
        # Count by action type
        action_type_stats = frappe.db.sql("""
            SELECT action_type, COUNT(*) as count
            FROM `tabCampaignStep`
            GROUP BY action_type
        """, as_dict=True)
        
        # Count by campaign
        campaign_stats = frappe.db.sql("""
            SELECT campaign, COUNT(*) as count
            FROM `tabCampaignStep`
            GROUP BY campaign
            ORDER BY count DESC
            LIMIT 5
        """, as_dict=True)
        
        return {
            "success": True,
            "total_steps": total_steps,
            "action_type_stats": action_type_stats,
            "campaign_stats": campaign_stats
        }
    except Exception as e:
        frappe.log_error(f"Error in get_campaign_step_stats: {str(e)}")
        return {"success": False, "error": str(e)}


@frappe.whitelist()
def search_campaign_steps(query, limit=10):
    """
    Search campaign steps for autocomplete
    """
    try:
        if not query:
            return []
        
        results = frappe.db.sql("""
            SELECT name, campaign_step_name, campaign, action_type, step_order
            FROM `tabCampaignStep`
            WHERE campaign_step_name LIKE %(query)s
            OR template LIKE %(query)s
            ORDER BY step_order
            LIMIT %(limit)s
        """, {
            "query": f"%{query}%",
            "limit": limit
        }, as_dict=True)
        
        return results
    except Exception as e:
        frappe.log_error(f"Error in search_campaign_steps: {str(e)}")
        return []


@frappe.whitelist()
def get_campaign_step_filter_options():
    """
    Get filter options for campaign steps
    """
    try:
        options = {}
        
        # Action type options
        action_type_result = get_filter_options("CampaignStep", "action_type")
        if action_type_result.get("success"):
            options["action_type"] = action_type_result["options"]
        
        # Campaign options  
        campaign_result = get_filter_options("CampaignStep", "campaign")
        if campaign_result.get("success"):
            options["campaign"] = campaign_result["options"]
            
        return {"success": True, "options": options}
    except Exception as e:
        frappe.log_error(f"Error in get_campaign_step_filter_options: {str(e)}")
        return {"success": False, "error": str(e)}


@frappe.whitelist()
def get_steps_by_campaign(campaign):
    """
    Get all steps for a specific campaign
    """
    try:
        steps = frappe.db.get_all(
            "CampaignStep",
            filters={"campaign": campaign},
            fields=["name", "campaign_step_name", "step_order", "action_type", "delay_in_days", "template"],
            order_by="step_order asc"
        )
        
        return {
            "success": True,
            "data": steps
        }
    except Exception as e:
        frappe.log_error(f"Error in get_steps_by_campaign: {str(e)}")
        return {"success": False, "error": str(e)}


@frappe.whitelist()
def reorder_campaign_steps(campaign, step_orders):
    """
    Reorder campaign steps
    step_orders: [{"name": "step_name", "order": 1}, ...]
    """
    try:
        for step_order in step_orders:
            frappe.db.set_value(
                "CampaignStep",
                step_order["name"],
                "step_order",
                step_order["order"]
            )
        
        frappe.db.commit()
        return {"success": True}
    except Exception as e:
        frappe.log_error(f"Error in reorder_campaign_steps: {str(e)}")
        return {"success": False, "error": str(e)}
