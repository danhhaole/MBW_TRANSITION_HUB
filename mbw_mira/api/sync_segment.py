import frappe
import json
from frappe import _

def build_filter_description(filter_obj):
    """
    Build human-readable description from filter object
    
    Args:
        filter_obj: {
            'conditions': [...],
            'logic': 'AND'
        }
    
    Returns:
        str: Human-readable filter description
    """
    if not filter_obj or not filter_obj.get('conditions'):
        return ""
    
    descriptions = []
    
    def process_condition(cond):
        if cond['type'] == 'condition':
            field = cond['field']
            operator = cond['operator']
            value = cond['value']
            
            # Format value
            if isinstance(value, list):
                value_str = ', '.join(str(v) for v in value)
            else:
                value_str = str(value)
            
            # Map operator to readable text
            op_map = {
                '==': '=',
                '!=': '≠',
                'in': 'IN',
                'not in': 'NOT IN',
                'like': 'LIKE',
                'not like': 'NOT LIKE',
                '>': '>',
                '<': '<',
                '>=': '≥',
                '<=': '≤'
            }
            op_str = op_map.get(operator, operator)
            
            return f"{field} {op_str} ({value_str})"
        
        elif cond['type'] == 'group':
            nested_descs = []
            for nested_cond in cond['conditions']:
                nested_descs.append(process_condition(nested_cond))
            
            logic = cond.get('logic', 'AND')
            return f"({f' {logic} '.join(nested_descs)})"
        
        return ""
    
    for condition in filter_obj['conditions']:
        desc = process_condition(condition)
        if desc:
            descriptions.append(desc)
    
    main_logic = filter_obj.get('logic', 'AND')
    return f" {main_logic} ".join(descriptions)

@frappe.whitelist()
def sync_positions(data_source_name):
    """
    Queue positions sync from ATS to Mira Segments
    
    Args:
        data_source_name (str): Name of Mira Data Source document
        
    Returns:
        dict: Status and message with sync_log_name
    """
    # Validate data source exists
    if not frappe.db.exists("Mira Data Source", data_source_name):
        frappe.throw(f"Data Source {data_source_name} not found")
    
    # Get data source document
    data_source = frappe.get_doc("Mira Data Source", data_source_name)
    
    # Validate data source is ATS type
    if data_source.source_type != "ATS":
        frappe.throw(f"Data Source type is {data_source.source_type}. Only 'ATS' type can sync positions.")
    
    # Validate data source is active
    if data_source.status != "Active":
        frappe.throw(f"Data Source status is {data_source.status}. Only 'Active' sources can sync.")
    
    if not data_source.is_active:
        frappe.throw("Data Source is not active")
    
    # Validate sync direction
    if data_source.sync_direction not in ("Pull", "Both"):
        frappe.throw(f"Sync direction is {data_source.sync_direction}. Must be 'Pull' or 'Both' to sync from ATS.")
    
    # Create sync log for queue processing
    try:
        # Check if ANY sync log exists for this connection (regardless of status)
        # User must retry existing log instead of creating new one
        existing_sync = frappe.db.sql("""
            SELECT name, status
            FROM `tabMira ATS Sync Log`
            WHERE connection = %s 
            AND sync_type = %s
            ORDER BY creation DESC
            LIMIT 1
            FOR UPDATE
        """, (data_source.name, "Position to Segment"), as_dict=True)
        
        if existing_sync:
            status = existing_sync[0].status
            if status in ["Pending", "In Progress"]:
                frappe.throw(f"A sync job is already running for this connection. Please wait for it to complete or cancel it.")
            else:
                frappe.throw(f"A sync log already exists for this connection with status '{status}'. Please use Retry to run sync again.")
        
        # Create sync log with In Progress status (start immediately)
        sync_log = frappe.get_doc({
            "doctype": "Mira ATS Sync Log",
            "connection": data_source.name,
            "sync_type": "Position to Segment",
            "status": "In Progress",
            "start_time": frappe.utils.now(),
            "details": f"Position sync started for {data_source.source_title} ({data_source.source_name})"
        })
        sync_log.insert(ignore_permissions=True)
        frappe.db.commit()
        
        # Enqueue background job immediately
        frappe.enqueue(
            "mbw_mira.workers.ats.fetch_mbw_ats_data.sync_data_source_positions_background",
            data_source_name=data_source.name,
            sync_log_name=sync_log.name,
            queue="short",
            timeout=3600  # 1 hour timeout
        )
        
        return {
            "status": "success",
            "message": "Position sync has been started. Check sync history for progress.",
            "sync_log_name": sync_log.name
        }
    except Exception as e:
        frappe.db.rollback()
        frappe.log_error(f"Failed to start position sync for {data_source_name}: {str(e)}", "Start Position Sync Error")
        return {
            "status": "error",
            "message": f"Failed to start sync: {str(e)}"
        }

@frappe.whitelist()
def sync_candidates(data_source_name, filters=None):
    """
    Queue candidates sync from ATS to Mira Talents
    
    Args:
        data_source_name (str): Name of Mira Data Source document
        
    Returns:
        dict: Status and message with sync_log_name
    """
    # Validate data source exists
    if not frappe.db.exists("Mira Data Source", data_source_name):
        frappe.throw(f"Data Source {data_source_name} not found")
    
    # Get data source document
    data_source = frappe.get_doc("Mira Data Source", data_source_name)
    
    # Validate data source is ATS type
    if data_source.source_type != "ATS":
        frappe.throw(f"Data Source type is {data_source.source_type}. Only 'ATS' type can sync candidates.")
    
    # Validate data source is active
    if data_source.status != "Active":
        frappe.throw(f"Data Source status is {data_source.status}. Only 'Active' sources can sync.")
    
    if not data_source.is_active:
        frappe.throw("Data Source is not active")
    
    # Validate sync direction
    if data_source.sync_direction not in ("Pull", "Both"):
        frappe.throw(f"Sync direction is {data_source.sync_direction}. Must be 'Pull' or 'Both' to sync from ATS.")
    
    # Create sync log for queue processing
    try:
        # Check if ANY sync log exists for this connection (regardless of status)
        # User must retry existing log instead of creating new one
        existing_sync = frappe.db.sql("""
            SELECT name, status
            FROM `tabMira ATS Sync Log`
            WHERE connection = %s 
            AND sync_type = %s
            ORDER BY creation DESC
            LIMIT 1
            FOR UPDATE
        """, (data_source.name, "Candidate to Talent"), as_dict=True)
        
        if existing_sync:
            status = existing_sync[0].status
            if status in ["Pending", "In Progress"]:
                frappe.throw(f"A sync job is already running for this connection. Please wait for it to complete or cancel it.")
            else:
                frappe.throw(f"A sync log already exists for this connection with status '{status}'. Please use Retry to run sync again.")
        

        # Parse filters if provided
        parsed_filters = None
        filter_description = ""
        if filters:
            parsed_filters = json.loads(filters) if isinstance(filters, str) else filters
            filter_description = build_filter_description(parsed_filters)
        
        # Create sync log with In Progress status (start immediately)
        details = f"Sync started for {data_source.source_title} ({data_source.source_name})"
        if filter_description:
            details += f"\nFilters: {filter_description}"
        
        sync_log = frappe.get_doc({
            "doctype": "Mira ATS Sync Log",
            "connection": data_source.name,
            "sync_type": "Candidate to Talent",
            "status": "In Progress",
            "start_time": frappe.utils.now(),
            "details": details
        })
        sync_log.insert(ignore_permissions=True)
        frappe.db.commit()
        
        # Enqueue background job immediately with filters
        frappe.enqueue(
            "mbw_mira.workers.ats.fetch_mbw_ats_data.sync_data_source_candidates_background",
            data_source_name=data_source.name,
            sync_log_name=sync_log.name,
            filters=parsed_filters,
            queue="short",
            timeout=3600  # 1 hour timeout
        )
        
        return {
            "status": "success",
            "message": "Candidate sync has been started. Check sync history for progress.",
            "sync_log_name": sync_log.name
        }
    except Exception as e:
        frappe.db.rollback()
        frappe.log_error(f"Failed to start candidate sync for {data_source_name}: {str(e)}", "Start Sync Error")
        return {
            "status": "error",
            "message": f"Failed to start sync: {str(e)}"
        }

@frappe.whitelist()
def check_sync_status(data_source_name, sync_type="Candidate to Talent"):
    """
    Check if a sync log exists for this connection
    
    Args:
        data_source_name (str): Name of Mira Data Source
        sync_type (str): Type of sync - "Candidate to Talent" or "Position to Segment"
        
    Returns:
        dict: {
            "has_sync_log": bool,
            "sync_log_name": str or None,
            "status": str or None,
            "can_start_new": bool
        }
    """
    existing_sync = frappe.db.get_value(
        "Mira ATS Sync Log",
        {
            "connection": data_source_name,
            "sync_type": sync_type
        },
        ["name", "status"],
        order_by="creation desc"
    )
    
    if existing_sync:
        return {
            "has_sync_log": True,
            "sync_log_name": existing_sync[0],
            "status": existing_sync[1],
            "can_start_new": False
        }
    else:
        return {
            "has_sync_log": False,
            "sync_log_name": None,
            "status": None,
            "can_start_new": True
        }

@frappe.whitelist()
def cancel_sync(sync_log_name):
    """
    Cancel a pending or in-progress sync job
    
    Args:
        sync_log_name (str): Name of Mira ATS Sync Log document
        
    Returns:
        dict: Status and message
    """
    try:
        # Get sync log to determine sync type
        sync_log = frappe.get_doc("Mira ATS Sync Log", sync_log_name)
        
        if sync_log.sync_type == "Candidate to Talent":
            from mbw_mira.schedulers.sync_candidates_queue import cancel_sync_job
        elif sync_log.sync_type == "Position to Segment":
            from mbw_mira.schedulers.sync_positions_queue import cancel_sync_job
        else:
            return {
                "status": "error",
                "message": f"Unknown sync type: {sync_log.sync_type}"
            }
        
        if cancel_sync_job(sync_log_name):
            return {
                "status": "success",
                "message": "Sync job cancelled successfully."
            }
        else:
            return {
                "status": "error",
                "message": "Cannot cancel sync job. It may already be completed or failed."
            }
    except Exception as e:
        frappe.log_error(f"Failed to cancel sync {sync_log_name}: {str(e)}", "Cancel Sync Error")
        return {
            "status": "error",
            "message": f"Failed to cancel sync: {str(e)}"
        }

@frappe.whitelist()
def retry_sync(sync_log_name):
    """
    Retry a failed sync job
    
    Args:
        sync_log_name (str): Name of Mira ATS Sync Log document
        
    Returns:
        dict: Status and message
    """
    try:
        # Get sync log to determine sync type
        sync_log = frappe.get_doc("Mira ATS Sync Log", sync_log_name)
        
        if sync_log.sync_type == "Candidate to Talent":
            from mbw_mira.schedulers.sync_candidates_queue import retry_failed_sync
        elif sync_log.sync_type == "Position to Segment":
            from mbw_mira.schedulers.sync_positions_queue import retry_failed_sync
        else:
            return {
                "status": "error",
                "message": f"Unknown sync type: {sync_log.sync_type}"
            }
        
        if retry_failed_sync(sync_log_name):
            return {
                "status": "success",
                "message": "Sync job queued for retry successfully."
            }
        else:
            return {
                "status": "error",
                "message": "Cannot retry sync job. It may not be in failed or partially completed state."
            }
    except Exception as e:
        frappe.log_error(f"Failed to retry sync {sync_log_name}: {str(e)}", "Retry Sync Error")
        return {
            "status": "error",
            "message": f"Failed to retry sync: {str(e)}"
        }