import frappe
from frappe import _
from frappe.utils import now_datetime, add_days, now


def create_campaign_step_from_template(campaign_id, template_data):
    """
    Create campaign steps from template
    """
    try:
        steps = []
        for step_data in template_data:
            doc = frappe.new_doc("CampaignStep")
            doc.campaign = campaign_id
            doc.campaign_step_name = step_data.get("name")
            doc.step_order = step_data.get("order", 1)
            doc.action_type = step_data.get("action_type")
            doc.delay_in_days = step_data.get("delay_in_days", 0)
            doc.template = step_data.get("template", "")
            doc.action_config = step_data.get("action_config", {})
            doc.save()
            steps.append(doc)
        
        return {"success": True, "steps": steps}
    except Exception as e:
        frappe.log_error(f"Error in create_campaign_step_from_template: {str(e)}")
        return {"success": False, "error": str(e)}


def duplicate_campaign_steps(source_campaign_id, target_campaign_id):
    """
    Duplicate steps from one campaign to another
    """
    try:
        source_steps = frappe.get_all(
            "CampaignStep",
            filters={"campaign": source_campaign_id},
            fields=["campaign_step_name", "step_order", "action_type", "delay_in_days", "template", "action_config"],
            order_by="step_order"
        )
        
        new_steps = []
        for step in source_steps:
            doc = frappe.new_doc("CampaignStep")
            doc.campaign = target_campaign_id
            doc.campaign_step_name = step.campaign_step_name
            doc.step_order = step.step_order
            doc.action_type = step.action_type
            doc.delay_in_days = step.delay_in_days
            doc.template = step.template
            doc.action_config = step.action_config
            doc.save()
            new_steps.append(doc)
        
        return {"success": True, "steps": new_steps}
    except Exception as e:
        frappe.log_error(f"Error in duplicate_campaign_steps: {str(e)}")
        return {"success": False, "error": str(e)}


def validate_campaign_step_flow(campaign_id):
    """
    Validate that campaign steps have proper flow (no gaps in step order)
    """
    try:
        steps = frappe.get_all(
            "CampaignStep",
            filters={"campaign": campaign_id},
            fields=["step_order"],
            order_by="step_order"
        )
        
        if not steps:
            return {"success": True, "valid": True}
        
        step_orders = [step.step_order for step in steps]
        step_orders.sort()
        
        # Check for gaps
        for i in range(len(step_orders)):
            if step_orders[i] != i + 1:
                return {
                    "success": True,
                    "valid": False,
                    "error": f"Gap found in step order. Missing step {i + 1}"
                }
        
        # Check for duplicates
        if len(step_orders) != len(set(step_orders)):
            return {
                "success": True,
                "valid": False,
                "error": "Duplicate step orders found"
            }
        
        return {"success": True, "valid": True}
    except Exception as e:
        frappe.log_error(f"Error in validate_campaign_step_flow: {str(e)}")
        return {"success": False, "error": str(e)}


def reorder_campaign_steps_batch(campaign_id, reorder_data):
    """
    Reorder multiple campaign steps at once
    reorder_data: [{"step_name": "name", "new_order": 1}, ...]
    """
    try:
        # First, validate the new order doesn't have gaps or duplicates
        new_orders = [item["new_order"] for item in reorder_data]
        if len(new_orders) != len(set(new_orders)):
            return {"success": False, "error": "Duplicate step orders in new arrangement"}
        
        new_orders.sort()
        for i, order in enumerate(new_orders):
            if order != i + 1:
                return {"success": False, "error": f"Gap found in new step order. Missing step {i + 1}"}
        
        # Update each step
        for item in reorder_data:
            frappe.db.set_value(
                "CampaignStep",
                item["step_name"],
                "step_order",
                item["new_order"]
            )
        
        frappe.db.commit()
        return {"success": True, "message": "Steps reordered successfully"}
    except Exception as e:
        frappe.log_error(f"Error in reorder_campaign_steps_batch: {str(e)}")
        return {"success": False, "error": str(e)}


def get_campaign_step_templates():
    """
    Get predefined campaign step templates
    """
    try:
        templates = [
            {
                "name": "Welcome Email",
                "action_type": "SEND_EMAIL",
                "delay_in_days": 0,
                "template": "Welcome to our talent pool! We're excited to have you join us.",
                "description": "Initial welcome email to new candidates"
            },
            {
                "name": "Follow-up Email",
                "action_type": "SEND_EMAIL",
                "delay_in_days": 3,
                "template": "Just following up on our previous conversation. Are you still interested in opportunities?",
                "description": "Follow-up email after initial contact"
            },
            {
                "name": "Skills Assessment",
                "action_type": "MANUAL_TASK",
                "delay_in_days": 7,
                "template": "Please complete the skills assessment: [LINK]",
                "description": "Request for skills assessment completion"
            },
            {
                "name": "Interview Invitation",
                "action_type": "SEND_EMAIL",
                "delay_in_days": 14,
                "template": "We'd like to invite you for an interview. Please let us know your availability.",
                "description": "Interview invitation email"
            },
            {
                "name": "Reminder Call",
                "action_type": "MANUAL_CALL",
                "delay_in_days": 21,
                "template": "Call candidate to remind about pending application",
                "description": "Manual reminder call to candidate"
            }
        ]
        
        return {"success": True, "templates": templates}
    except Exception as e:
        frappe.log_error(f"Error in get_campaign_step_templates: {str(e)}")
        return {"success": False, "error": str(e)}


def bulk_update_campaign_steps(campaign_id, updates):
    """
    Update multiple campaign steps at once
    updates: [{"step_name": "name", "field": "value"}, ...]
    """
    try:
        results = []
        for update in updates:
            step_name = update.get("step_name")
            if not step_name:
                results.append({"step_name": step_name, "status": "error", "message": "Step name is required"})
                continue
            
            try:
                doc = frappe.get_doc("CampaignStep", step_name)
                
                # Update fields
                for field, value in update.items():
                    if field != "step_name" and hasattr(doc, field):
                        setattr(doc, field, value)
                
                doc.save()
                results.append({"step_name": step_name, "status": "success"})
            except Exception as e:
                results.append({"step_name": step_name, "status": "error", "message": str(e)})
        
        return {"success": True, "results": results}
    except Exception as e:
        frappe.log_error(f"Error in bulk_update_campaign_steps: {str(e)}")
        return {"success": False, "error": str(e)}


def get_campaign_step_performance(campaign_id, step_order=None):
    """
    Get performance metrics for campaign steps
    """
    try:
        conditions = ["cs.campaign = %(campaign_id)s"]
        params = {"campaign_id": campaign_id}
        
        if step_order:
            conditions.append("cs.step_order = %(step_order)s")
            params["step_order"] = step_order
        
        query = f"""
            SELECT 
                cs.name,
                cs.campaign_step_name,
                cs.step_order,
                cs.action_type,
                COUNT(a.name) as total_actions,
                SUM(CASE WHEN a.status = 'EXECUTED' THEN 1 ELSE 0 END) as executed_actions,
                SUM(CASE WHEN a.status = 'FAILED' THEN 1 ELSE 0 END) as failed_actions,
                SUM(CASE WHEN a.status = 'SKIPPED' THEN 1 ELSE 0 END) as skipped_actions,
                ROUND(SUM(CASE WHEN a.status = 'EXECUTED' THEN 1 ELSE 0 END) * 100.0 / COUNT(a.name), 2) as success_rate
            FROM `tabCampaignStep` cs
            LEFT JOIN `tabAction` a ON cs.name = a.campaign_step
            WHERE {' AND '.join(conditions)}
            GROUP BY cs.name, cs.campaign_step_name, cs.step_order, cs.action_type
            ORDER BY cs.step_order
        """
        
        performance = frappe.db.sql(query, params, as_dict=True)
        
        return {"success": True, "data": performance}
    except Exception as e:
        frappe.log_error(f"Error in get_campaign_step_performance: {str(e)}")
        return {"success": False, "error": str(e)}


def auto_optimize_campaign_steps(campaign_id):
    """
    Auto-optimize campaign steps based on performance
    """
    try:
        performance = get_campaign_step_performance(campaign_id)
        
        if not performance.get("success"):
            return performance
        
        suggestions = []
        
        for step in performance["data"]:
            if step.get("success_rate", 0) < 50 and step.get("total_actions", 0) > 10:
                suggestions.append({
                    "step_name": step["campaign_step_name"],
                    "step_order": step["step_order"],
                    "issue": "Low success rate",
                    "success_rate": step["success_rate"],
                    "suggestion": "Consider revising the template or changing the action type"
                })
            
            if step.get("failed_actions", 0) > step.get("executed_actions", 0):
                suggestions.append({
                    "step_name": step["campaign_step_name"],
                    "step_order": step["step_order"],
                    "issue": "High failure rate",
                    "failed_actions": step["failed_actions"],
                    "suggestion": "Check for technical issues or template problems"
                })
        
        return {"success": True, "suggestions": suggestions}
    except Exception as e:
        frappe.log_error(f"Error in auto_optimize_campaign_steps: {str(e)}")
        return {"success": False, "error": str(e)}


def get_next_step_in_campaign(campaign_id, current_step_order):
    """
    Get the next step in a campaign
    """
    try:
        next_step = frappe.db.get_value(
            "CampaignStep",
            {
                "campaign": campaign_id,
                "step_order": current_step_order + 1
            },
            ["name", "campaign_step_name", "step_order", "action_type", "delay_in_days"],
            as_dict=True
        )
        
        return {"success": True, "next_step": next_step}
    except Exception as e:
        frappe.log_error(f"Error in get_next_step_in_campaign: {str(e)}")
        return {"success": False, "error": str(e)}


def create_actions_for_campaign_step(campaign_step_name, candidate_campaign_ids):
    """
    Create actions for multiple candidate campaigns for a specific campaign step
    """
    try:
        if isinstance(candidate_campaign_ids, str):
            import json
            candidate_campaign_ids = json.loads(candidate_campaign_ids)
        
        campaign_step = frappe.get_doc("CampaignStep", campaign_step_name)
        
        actions = []
        for cc_id in candidate_campaign_ids:
            # Check if action already exists
            exists = frappe.db.exists("Action", {
                "candidate_campaign_id": cc_id,
                "campaign_step": campaign_step_name
            })
            
            if not exists:
                doc = frappe.new_doc("Action")
                doc.candidate_campaign_id = cc_id
                doc.campaign_step = campaign_step_name
                doc.status = "SCHEDULED"
                doc.scheduled_at = add_days(now(), campaign_step.delay_in_days or 0)
                doc.save()
                actions.append(doc)
        
        return {"success": True, "actions": actions}
    except Exception as e:
        frappe.log_error(f"Error in create_actions_for_campaign_step: {str(e)}")
        return {"success": False, "error": str(e)}
