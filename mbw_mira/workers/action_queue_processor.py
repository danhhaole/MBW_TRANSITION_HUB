# Thêm vào file mira_candidate.py hoặc tạo file riêng cho action processor

import json
import frappe
from frappe import _
from frappe.utils import now_datetime, get_datetime
from datetime import timedelta
from frappe.core.doctype.communication.email import make
from mbw_mira.api.mail import send_email, send_email_template

def process_recruitment_action_queue(action_info):
    """Background job to process pending recruitment actions"""
    try:
        # Get pending actions that are ready to execute
        result = execute_single_action(action_info["name"])
                
    except Exception as e:
        frappe.log_error(f"Error in process_recruitment_action_queue: {str(e)}")
        return {"success": False, "error": str(e)}

def execute_single_action(action_queue_id):
    """Execute a single action from queue"""
    try:
        action_doc = frappe.get_doc("MIRA_Recruitment_Action_Queue", action_queue_id)
        
        if action_doc.status != "Pending":
            return {"success": False, "error": "Action is not pending"}
        
        # Update status to processing
        action_doc.status = "Processing"
        action_doc.started_at = now_datetime()
        action_doc.save(ignore_permissions=True)
        frappe.db.commit()
        
        # Check condition if exists
        # if action_doc.condition_config:
        #     condition_passed = evaluate_action_condition(action_doc)
        #     if not condition_passed:
        #         action_doc.status = "Cancelled"
        #         action_doc.completed_at = now_datetime()
        #         action_doc.error_message = "Condition not met"
        #         action_doc.save(ignore_permissions=True)
        #         frappe.db.commit()
        #         return {"success": True, "status": "Cancelled", "reason": "condition_not_met"}
        
        # Execute the action
        result = dispatch_action(action_doc)
        
        if result.get("success"):
            action_doc.status = "Completed"
            action_doc.completed_at = now_datetime()
            action_doc.result_data = json.dumps(result.get("data", {}))
        else:
            # Handle retry logic
            action_doc.retry_count = (action_doc.retry_count or 0) + 1
            
            if action_doc.retry_count >= action_doc.max_retries:
                action_doc.status = "Failed"
                action_doc.completed_at = now_datetime()
            else:
                # Schedule retry
                action_doc.status = "Pending"
                action_doc.scheduled_time = get_datetime(now_datetime()) + timedelta(minutes=30)
            
            action_doc.error_message = result.get("error", "Unknown error")
        
        action_doc.save(ignore_permissions=True)
        frappe.db.commit()
        
        return result
        
    except Exception as e:
        # Update error status
        try:
            action_doc.status = "Failed"
            action_doc.completed_at = now_datetime()
            action_doc.error_message = str(e)
            action_doc.save(ignore_permissions=True)
            frappe.db.commit()
        except:
            pass
            
        frappe.log_error(f"Error executing action {action_queue_id}: {str(e)}")
        return {"success": False, "error": str(e)}

def evaluate_action_condition(action_doc):
    """Evaluate condition for action execution"""
    try:
        if not action_doc.condition_config:
            return True
            
        condition_config = json.loads(action_doc.condition_config)
        candidate = frappe.get_doc("MIRA_Candidate", action_doc.candidate_id)
        
        # Use same condition evaluation logic from step transaction
        transaction = frappe.new_doc("MIRA_CandidateStepTransaction")
        result = transaction._perform_condition_evaluation(candidate, condition_config)
        
        return result.get("passed", False)
        
    except Exception as e:
        frappe.log_error(f"Error evaluating action condition: {str(e)}")
        return False

def dispatch_action(action_doc):
    """Dispatch action to appropriate handler based on action type"""
    try:
        action_type = action_doc.action_type
        action_data = json.loads(action_doc.action_data) if action_doc.action_data else {}
        
        # Action handlers mapping
        action_handlers = {
            'send_email': handle_send_email,
            'send_notification': handle_send_notification,
            'create_task': handle_create_task,
            'automatic_scoring': handle_automatic_scoring,
            'send_test': handle_send_test,
            'send_offer_letter': handle_send_offer_letter,
            'schedule_interview': handle_schedule_interview,
            'video_interview_invitation': handle_video_interview,
            'api_call': handle_api_call,
            'notify_departments': handle_notify_departments,
            'notify_hiring_manager': handle_notify_hiring_manager
        }
        
        handler = action_handlers.get(action_type)
        if not handler:
            return {"success": False, "error": f"Unknown action type: {action_type}"}
        
        return handler(action_doc, action_data)
        
    except Exception as e:
        return {"success": False, "error": str(e)}

# Action handlers
def handle_send_email(action_doc, action_data):
    """Handle send email action"""
    try:
        candidate = frappe.get_doc("Mira Candidate", action_doc.candidate_id)
        job_opening = frappe.get_doc("Mira Job Opening", action_doc.job_opening_id)
       
        template_name = action_data.get('template', '')
        if not template_name:
            return {"success": False, "error": "Email template not specified"}
        
        # Get email template
        try:
            email_template = frappe.get_doc("Mira Email Template", template_name)
        except:
            return {"success": False, "error": f"Mira Email Template '{template_name}' not found"}
        
        # Prepare template context
        context = {
            'candidate': candidate,
            'job_opening': job_opening,
            'candidate_name': candidate.can_full_name,
            'job_title': job_opening.jo_public_title,
            'company_name': frappe.defaults.get_user_default("Company") or "Company"
        }
        
        # Render template
        subject = frappe.render_template(email_template.subject, context)
        content = frappe.render_template(email_template.response, context)
        
        # Send email
        
        send_email_template("Mira Candidate",candidate.name,[candidate.can_email],)
        
        return {
            "success": True,
            "data": {
                "email_sent_to": candidate.can_email,
                "template_used": template_name,
                "subject": subject
            }
        }
        
    except Exception as e:
        return {"success": False, "error": str(e)}

# def handle_create_task(action_doc, action_data):
#     """Handle create task action"""
#     try:
#         candidate = frappe.get_doc("Mira Candidate", action_doc.candidate_id)
#         job_opening = frappe.get_doc("Mira Job Opening", action_doc.job_opening_id)
        
#         assignee = action_data.get('assignee', '')
#         if not assignee:
#             return {"success": False, "error": "Task assignee not specified"}
        
#         # Create task
#         task_doc = frappe.get_doc({
#             "doctype": "",
#             "task_title": f"Review candidate: {candidate.can_full_name}",
#             "task_description": f"Review candidate {candidate.can_full_name} for position {job_opening.jo_public_title}",
#             "task_type": "Candidate Review",
#             "assigned_to": assignee,
#             "can_id": candidate.name,
#             "job_opening_id": job_opening.name,
#             "priority": "Medium",
#             "due_date": frappe.utils.add_days(frappe.utils.today(), 3),
#             "status": "Open"
#         })
        
#         task_doc.insert(ignore_permissions=True)
        
#         return {
#             "success": True,
#             "data": {
#                 "task_id": task_doc.name,
#                 "assigned_to": assignee,
#                 "task_title": task_doc.task_title
#             }
#         }
        
#     except Exception as e:
#         return {"success": False, "error": str(e)}

def handle_automatic_scoring(action_doc, action_data):
    """Handle automatic scoring action"""
    try:
        candidate = frappe.get_doc("Mira Candidate", action_doc.candidate_id)
        model_name = action_data.get('model', 'default_scoring_model')
        
        # Call scoring API or function
        try:
            from mbw_mira.api.matching import calculate_matching_score
            score_result = calculate_matching_score(
                candidate_id=candidate.name, 
                job_id=action_doc.job_opening_id
            )
            
            return {
                "success": True,
                "data": {
                    "model_used": model_name,
                    "score_result": score_result
                }
            }
            
        except Exception as scoring_error:
            return {"success": False, "error": f"Scoring failed: {str(scoring_error)}"}
        
    except Exception as e:
        return {"success": False, "error": str(e)}

def handle_send_notification(action_doc, action_data):
    """Handle send notification action"""
    try:
        candidate = frappe.get_doc("Mira Candidate", action_doc.candidate_id)
        
        notification_type = action_data.get('type', 'info')
        message = action_data.get('message', f'Candidate {candidate.can_full_name} status updated')
        
        # Send realtime notification
        frappe.publish_realtime(
            event="candidate_status_update",
            message={
                "candidate_id": candidate.name,
                "candidate_name": candidate.can_full_name,
                "message": message,
                "type": notification_type
            },
            user=action_data.get('recipient', frappe.session.user)
        )
        
        return {
            "success": True,
            "data": {
                "notification_sent": True,
                "message": message
            }
        }
        
    except Exception as e:
        return {"success": False, "error": str(e)}

def handle_send_test(action_doc, action_data):
    """Handle send test action"""
    try:
        candidate = frappe.get_doc("Mira Candidate", action_doc.candidate_id)
        test_type = action_data.get('test_type', 'general')
        
        # Implementation depends on your test system
        # This is a placeholder
        
        return {
            "success": True,
            "data": {
                "test_sent": True,
                "test_type": test_type,
                "candidate_email": candidate.can_email
            }
        }
        
    except Exception as e:
        return {"success": False, "error": str(e)}

def handle_send_offer_letter(action_doc, action_data):
    """Handle send offer letter action"""
    try:
        # Similar to send_email but specific for offer letters
        return handle_send_email(action_doc, {
            'template': action_data.get('offer_type', 'standard') + '_offer_template'
        })
        
    except Exception as e:
        return {"success": False, "error": str(e)}

def handle_schedule_interview(action_doc, action_data):
    """Handle schedule interview action"""
    try:
        candidate = frappe.get_doc("Mira Candidate", action_doc.candidate_id)
        
        # Create interview schedule placeholder
        # Implementation depends on your scheduling system
        
        return {
            "success": True,
            "data": {
                "interview_scheduled": True,
                "candidate_id": candidate.name
            }
        }
        
    except Exception as e:
        return {"success": False, "error": str(e)}

def handle_video_interview(action_doc, action_data):
    """Handle video interview action"""
    try:
        candidate = frappe.get_doc("Mira Candidate", action_doc.candidate_id)
        interview_session = frappe.new_doc("MIRA Interview Sessions")
        interview_session._send_interview_email(candidate)
        
        return {
            "success": True,
            "data": {
                "interview_scheduled": True,
                "candidate_id": candidate.name
            }
        }
        
    except Exception as e:
        return {"success": False, "error": str(e)}

def handle_api_call(action_doc, action_data):
    """Handle external API call action"""
    try:
        import requests
        
        url = action_data.get('url', '')
        method = action_data.get('method', 'POST')
        payload = action_data.get('payload', {})
        
        if not url:
            return {"success": False, "error": "API URL not specified"}
        
        response = requests.request(method, url, json=payload, timeout=30)
        
        return {
            "success": response.status_code < 400,
            "data": {
                "status_code": response.status_code,
                "response": response.json() if response.content else {}
            }
        }
        
    except Exception as e:
        return {"success": False, "error": str(e)}

def handle_notify_departments(action_doc, action_data):
    """Handle notify departments action"""
    try:
        # Send notification to relevant departments
        departments = action_data.get('departments', [])
        
        for dept in departments:
            # Send notification logic here
            pass
            
        return {
            "success": True,
            "data": {
                "departments_notified": departments
            }
        }
        
    except Exception as e:
        return {"success": False, "error": str(e)}

def handle_notify_hiring_manager(action_doc, action_data):
    """Handle notify hiring manager action"""
    try:
        job_opening = frappe.get_doc("Mira Job Opening", action_doc.job_opening_id)
        hiring_manager = job_opening.hiring_manager
        
        if hiring_manager:
            # Send notification to hiring manager
            frappe.publish_realtime(
                event="candidate_update",
                message={
                    "candidate_id": action_doc.candidate_id,
                    "job_opening_id": action_doc.job_opening_id,
                    "action": "status_update"
                },
                user=hiring_manager
            )
        
        return {
            "success": True,
            "data": {
                "hiring_manager_notified": hiring_manager
            }
        }
        
    except Exception as e:
        return {"success": False, "error": str(e)}

def clean_action_cancel(action):
    frappe.db.delete("MIRA_Recruitment_Action_Queue",action)
    frappe.db.commit()

# API Functions
@frappe.whitelist()
def manually_process_action_queue():
    """Manually trigger action queue processing"""
    try:
        result = process_recruitment_action_queue()
        return result
    except Exception as e:
        return {"success": False, "error": str(e)}

@frappe.whitelist()
def retry_failed_action(action_queue_id):
    """Retry a failed action"""
    try:
        action_doc = frappe.get_doc("MIRA_Recruitment_Action_Queue", action_queue_id)
        
        if action_doc.status not in ["Failed", "Error"]:
            return {"success": False, "error": "Action is not in failed status"}
        
        # Reset for retry
        action_doc.status = "Pending"
        action_doc.retry_count = 0
        action_doc.scheduled_time = now_datetime()
        action_doc.error_message = ""
        action_doc.save(ignore_permissions=True)
        
        return {"success": True, "message": "Action queued for retry"}
        
    except Exception as e:
        return {"success": False, "error": str(e)}

@frappe.whitelist()
def get_action_queue_stats():
    """Get action queue statistics"""
    try:
        stats = {}
        
        # Count by status
        for status in ["Pending", "Processing", "Completed", "Failed", "Cancelled"]:
            count = frappe.db.count("MIRA_Recruitment_Action_Queue", {"status": status})
            stats[status.lower()] = count
        
        # Count by action type
        action_types = frappe.db.get_all(
            "MIRA_Recruitment_Action_Queue",
            fields=["action_type", "count(*) as count"],
            group_by="action_type"
        )
        
        stats["by_action_type"] = {item["action_type"]: item["count"] for item in action_types}
        
        return {"success": True, "stats": stats}
        
    except Exception as e:
        return {"success": False, "error": str(e)}