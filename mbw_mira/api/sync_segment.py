import frappe

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
        # Create sync log with Pending status
        sync_log = frappe.get_doc({
            "doctype": "Mira ATS Sync Log",
            "connection": data_source.name,
            "sync_type": "Position to Segment",
            "status": "Pending",
            "details": f"Position sync queued for {data_source.source_title} ({data_source.source_name})"
        })
        sync_log.insert(ignore_permissions=True)
        frappe.db.commit()
        
        return {
            "status": "success",
            "message": "Position sync has been queued successfully. Check sync history for progress.",
            "sync_log_name": sync_log.name
        }
    except Exception as e:
        frappe.log_error(f"Failed to queue position sync for {data_source_name}: {str(e)}", "Queue Position Sync Error")
        return {
            "status": "error",
            "message": f"Failed to queue sync: {str(e)}"
        }

@frappe.whitelist()
def sync_candidates(data_source_name):
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
        # Create sync log with Pending status
        sync_log = frappe.get_doc({
            "doctype": "Mira ATS Sync Log",
            "connection": data_source.name,
            "sync_type": "Candidate to Talent",
            "status": "Pending",
            "details": f"Sync queued for {data_source.source_title} ({data_source.source_name})"
        })
        sync_log.insert(ignore_permissions=True)
        frappe.db.commit()
        
        return {
            "status": "success",
            "message": "Candidate sync has been queued successfully. Check sync history for progress.",
            "sync_log_name": sync_log.name
        }
    except Exception as e:
        frappe.log_error(f"Failed to queue candidate sync for {data_source_name}: {str(e)}", "Queue Sync Error")
        return {
            "status": "error",
            "message": f"Failed to queue sync: {str(e)}"
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