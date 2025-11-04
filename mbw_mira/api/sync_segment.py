import frappe

@frappe.whitelist(allow_guest=True)
def sync_positions(data_source_name):
    """
    Sync positions from ATS to Mira Segments
    
    Args:
        data_source_name (str): Name of Mira Data Source document
        
    Returns:
        dict: Status and message
    """
    from mbw_mira.workers.ats.fetch_mbw_ats_data import sync_data_source_positions
    
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
    
    # Perform sync
    try:
        sync_data_source_positions(data_source)
        return {
            "status": "success",
            "message": "Sync started successfully. Check Mira ATS Sync Log for details."
        }
    except Exception as e:
        frappe.log_error(f"Sync failed for {data_source_name}: {str(e)}", "Sync Positions Error")
        return {
            "status": "error",
            "message": f"Sync failed: {str(e)}"
        }

@frappe.whitelist()
def sync_candidates(data_source_name):
    """
    Sync candidates from ATS to Mira Talents
    
    Args:
        data_source_name (str): Name of Mira Data Source document
        
    Returns:
        dict: Status and message
    """
    from mbw_mira.workers.ats.fetch_mbw_ats_data import sync_data_source_candidates
    
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
    
    # Perform sync
    try:
        sync_data_source_candidates(data_source)
        return {
            "status": "success",
            "message": "Candidate sync started successfully. Check Mira ATS Sync Log for details."
        }
    except Exception as e:
        frappe.log_error(f"Candidate sync failed for {data_source_name}: {str(e)}", "Sync Candidates Error")
        return {
            "status": "error",
            "message": f"Candidate sync failed: {str(e)}"
        }