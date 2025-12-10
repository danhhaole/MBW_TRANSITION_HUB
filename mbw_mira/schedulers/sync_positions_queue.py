import frappe
from datetime import datetime
import json

def run():
    """
    Process pending position sync jobs from queue
    NOTE: This is now deprecated as sync jobs are enqueued directly from API
    Kept for backward compatibility with any existing Pending jobs
    """
    # Get pending sync jobs (should be rare now)
    pending_syncs = frappe.get_all(
        "Mira ATS Sync Log",
        filters={
            "sync_type": "Position to Segment",
            "status": "Pending"
        },
        fields=["name", "connection", "details"],
        order_by="creation asc"
    )
    
    for sync_job in pending_syncs:
        try:
            # Get data source
            data_source = frappe.get_doc("Mira Data Source", sync_job.connection)
            
            # Update to In Progress before enqueuing
            sync_log = frappe.get_doc("Mira ATS Sync Log", sync_job.name)
            sync_log.status = "In Progress"
            sync_log.start_time = frappe.utils.now()
            sync_log.save(ignore_permissions=True)
            frappe.db.commit()
            
            # Enqueue the actual sync work
            frappe.enqueue(
                "mbw_mira.workers.ats.fetch_mbw_ats_data.sync_data_source_positions_background",
                data_source_name=data_source.name,
                sync_log_name=sync_job.name,
                queue="short",
                timeout=3600
            )
            
        except Exception as e:
            # Mark as failed if enqueue fails
            try:
                sync_log = frappe.get_doc("Mira ATS Sync Log", sync_job.name)
                sync_log.status = "Failed"
                sync_log.details = f"Failed to enqueue sync job: {str(e)}"
                sync_log.end_time = frappe.utils.now()
                sync_log.save(ignore_permissions=True)
                frappe.db.commit()
            except:
                pass
            
            frappe.log_error(f"Failed to enqueue position sync job {sync_job.name}: {str(e)}", "Position Sync Queue Error")

def cancel_sync_job(sync_log_name):
    """
    Cancel a pending or in-progress position sync job
    """
    try:
        sync_log = frappe.get_doc("Mira ATS Sync Log", sync_log_name)
        
        if sync_log.status in ["Pending", "In Progress"]:
            sync_log.status = "Cancelled"
            sync_log.end_time = frappe.utils.now()
            sync_log.details = f"Position sync cancelled by user at {frappe.utils.now()}"
            sync_log.save(ignore_permissions=True)
            frappe.db.commit()
            return True
        else:
            return False
            
    except Exception as e:
        frappe.log_error(f"Failed to cancel position sync job {sync_log_name}: {str(e)}", "Cancel Position Sync Error")
        return False

def retry_failed_sync(sync_log_name):
    """
    Retry a failed position sync job
    """
    try:
        sync_log = frappe.get_doc("Mira ATS Sync Log", sync_log_name)
        
        if sync_log.status in ["Failed", "Partially Completed", "Cancelled"]:
            # Get data source
            data_source = frappe.get_doc("Mira Data Source", sync_log.connection)
            
            # Use database transaction to prevent race condition
            existing_sync = frappe.db.sql("""
                SELECT name 
                FROM `tabMira ATS Sync Log`
                WHERE connection = %s 
                AND sync_type = %s
                AND status IN ('Pending', 'In Progress')
                AND name != %s
                LIMIT 1
                FOR UPDATE
            """, (data_source.name, "Position to Segment", sync_log_name), as_dict=True)
            
            if existing_sync:
                frappe.throw("A sync job is already running for this connection. Please wait for it to complete.")
            
            # Reset sync log and start immediately with In Progress status
            sync_log.status = "In Progress"
            sync_log.start_time = frappe.utils.now()
            sync_log.end_time = None
            sync_log.success_count = 0
            sync_log.failed_count = 0
            sync_log.error_log = None
            sync_log.details = f"Position sync retry started at {frappe.utils.now()}"
            sync_log.save(ignore_permissions=True)
            frappe.db.commit()
            
            # Enqueue background job immediately
            frappe.enqueue(
                "mbw_mira.workers.ats.fetch_mbw_ats_data.sync_data_source_positions_background",
                data_source_name=data_source.name,
                sync_log_name=sync_log_name,
                queue="short",
                timeout=3600
            )
            
            return True
        else:
            return False
            
    except Exception as e:
        frappe.log_error(f"Failed to retry position sync job {sync_log_name}: {str(e)}", "Retry Position Sync Error")
        return False
