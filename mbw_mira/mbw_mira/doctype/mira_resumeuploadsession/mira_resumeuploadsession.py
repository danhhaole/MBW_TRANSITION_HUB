# Copyright (c) 2025, MBWCloud Co. and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe import _
from frappe.utils.file_manager import save_file, get_file
from mbw_mira.api.ai import extract_cv_backend
from mbw_mira.helpers.map_json_resume import map_resume_json_to_talent
from frappe.utils import now_datetime, now, getdate, today
from datetime import datetime
import re, io, os
import json
import pandas as pd
import time
from typing import Dict, List, Any, Optional, Set
from frappe.model.document import Document


class MiraResumeUploadSession(Document):
	pass

# ===== PDF RESUME UPLOAD FUNCTIONS =====

def update_summary_counts(session_id: str):
    session = frappe.get_doc("Mira ResumeUploadSession", session_id)
    success = error = duplicate = pending = 0

    for f in session.files:
        if f.status == "Success":
            success += 1
        elif f.status == "Error":
            error += 1
        elif f.status == "Duplicate":
            duplicate += 1
        elif f.status in ("Pending", "Processing"):
            pending += 1

    status = "Processing" if pending > 0 else "Completed"

    session.db_set("status", status)
    session.db_set("success_count", success)
    session.db_set("failed_count", error)
    session.db_set("duplicated_count", duplicate)
    session.db_set("total_files", len(session.files))

@frappe.whitelist()
def retry_failed_files(session_name: str):
    session = frappe.get_doc("Mira ResumeUploadSession", session_name)
    retried = 0

    for file_row in session.files:
        if file_row.status == "Error":
            file_row.status = "Pending"
            file_row.error_message = ""
            frappe.enqueue(
                "mbw_mira.mbw_mira.doctype.mira_resumeuploadsession.mira_resumeuploadsession.process_resume_files",
                session_name=session_name,
                queue="default",
                job_id=f"process_retry_resume_{session_name}"
            )
            retried += 1

    session.save(ignore_permissions=True)
    frappe.db.commit()

    return {
        "retried": retried,
        "message": _(f"{retried} file(s) retried successfully.")
    }

@frappe.whitelist()
def get_session_detail(session_name):
    if not frappe.db.exists("Mira ResumeUploadSession", session_name):
        frappe.throw(_("Session not found"))

    session = frappe.get_doc("Mira ResumeUploadSession", session_name)
    files = [
        {
            "file_name": f.file_name,
            "file_url": f.file_url,
            "status": f.status,
            "error_message": f.error_message,
            "talent_id": f.talent_id,
            "processed_at": f.processed_at
        } for f in session.files
    ]

    return {
        "name": session.name,
        "upload_by": session.upload_by,
        "upload_at": session.upload_at,
        "status": session.status,
        "total_files": session.total_files,
        "success_count": session.success_count,
        "failed_count": session.failed_count,
        "duplicated_count": session.duplicated_count,
        "note": session.note,
        "files": files
    }

@frappe.whitelist()
def upload_resumes():
    """
    Handle multipart FormData upload of multiple PDF files, create Mira ResumeUploadSession
    and Mira ResumeUploadFile records, and enqueue a background job for processing.
    """
    try:
        if not frappe.request.files:
            frappe.throw(_("No files provided in the request."))

        files = frappe.request.files.getlist("file")
        note = frappe.request.form.get("note", "")
        segment = frappe.request.form.get("segment", "")
        
        # Validate all files are PDFs
        for file in files:
            if not file.filename.lower().endswith(".pdf"):
                frappe.throw(_("Only PDF files are allowed. File: {0}").format(file.filename))

        # Create a new Mira ResumeUploadSession
        session = frappe.new_doc("Mira ResumeUploadSession")
        session.upload_by = frappe.session.user
        session.upload_at = now()
        session.status = "Pending"
        session.note = note
        session.total_files = len(files)
        session.success_count = 0
        session.failed_count = 0
        session.duplicated_count = 0
        session.segment = segment
        session.save(ignore_permissions=True)

        # Process each file
        for file in files:
            file_doc = save_file(
                fname=file.filename,
                content=file.read(),
                dt="Mira ResumeUploadSession",
                dn=session.name,
                is_private=1,
            )

            resume_file = {
                "file_name": file_doc.file_name,
                "file_url": file_doc.file_url,
                "status": "Pending",
                "parent": session.name,
                "parenttype": "Mira ResumeUploadSession",
                "parentfield": "files"
            }
            session.append("files", resume_file)

        session.save(ignore_permissions=True)
        frappe.db.commit()

        # Enqueue background job to process files
        frappe.enqueue(
            "mbw_mira.mbw_mira.doctype.mira_resumeuploadsession.mira_resumeuploadsession.process_resume_files",
            queue="short",
            job_id=f"process_resume_{session.name}",
            session_name=session.name
        )

        return {
            "status": "success",
            "session_name": session.name,
            "message": _(f"Upload session {0} created successfully. Processing in the background.", session.name)
        }

    except Exception as e:
        frappe.log_error(message=str(e), title="Resume Upload Error")
        frappe.throw(_("Failed to process upload: {0}").format(str(e)))

def process_resume_files(session_name):
    """
    Background job to process uploaded resume files, call external API to extract data,
    and create ATS_Candidate records.
    """
    try:
        print('========================= session_name 1: ', session_name, flush=True)
        session = frappe.get_doc("Mira ResumeUploadSession", session_name)
        print(f'========================= session loaded - segment: {session.segment}', flush=True)
        print(f'========================= session data: {session.as_dict()}', flush=True)
        session.status = "Processing"
        
        # Log session start
        session.append("logs", {
            "timestamp": now(),
            "log_type": "Info",
            "message": f"Started processing {len(session.files)} file(s)" + (f" for segment {session.segment}" if session.segment else "")
        })
        session.save(ignore_permissions=True)

        for file in session.files:
            try:
                fname = frappe.get_doc("File", {"file_name": file.file_name})
                print('========================= fname 2: ', fname, flush=True)
                print('========================= fname.name 3: ', fname.name, flush=True)
                # Call external API to extract data
                candidate_data = extract_cv_backend(fname.name)
                if not candidate_data:
                    file.status = "Error"
                    file.error_message = "Failed to extract data from CV."
                    session.failed_count += 1
                    
                    # Log extraction failure
                    session.append("logs", {
                        "timestamp": now(),
                        "log_type": "Error",
                        "message": f"Failed to extract data from {file.file_name}"
                    })
                    continue
                else:
                    # Check for duplicate email
                    data = candidate_data.get("data", candidate_data)
                    personal_info = data.get("personal_info", {})
                    email = personal_info.get("can_email") or personal_info.get("email")
                    
                    if email:
                        existing = frappe.db.exists("Mira Talent", {"email": email})
                        if existing:
                            file.status = "Duplicate"
                            file.talent_id = existing
                            session.duplicated_count += 1
                            
                            # Log duplicate
                            session.append("logs", {
                                "timestamp": now(),
                                "log_type": "Warning",
                                "message": f"Duplicate email found for {file.file_name}: {email}",
                                "talent_id": existing
                            })
                            continue
                    
                    # Use map_resume_json_to_talent helper to create talent
                    try:
                        candidate_dict = map_resume_json_to_talent(candidate_data)
                        candidate = frappe.get_doc("Mira Talent", candidate_dict.get("name"))
                        
                        # Set additional fields
                        candidate.source = "Import CV"
                        candidate.crm_status = "New"
                        
                        # Attach the CV file to the resume field
                        if file.file_url:
                            candidate.resume = file.file_url
                            print(f'========================= Attached CV file: {file.file_url} to talent {candidate.name}', flush=True)
                        
                        candidate.save(ignore_permissions=True)
                        frappe.db.commit()
                        
                        file.status = "Success"
                        file.talent_id = candidate.name
                        file.processed_at = now()
                        session.success_count += 1
                        
                        # Log success
                        session.append("logs", {
                            "timestamp": now(),
                            "log_type": "Success",
                            "message": f"Successfully created talent from {file.file_name}: {candidate.full_name} (CV attached)",
                            "talent_id": candidate.name
                        })
                        
                        # Add talent to segment pool if segment is selected
                        print(f'========================= session.segment: {session.segment}', flush=True)
                        if session.segment:
                            try:
                                print(f'========================= Creating talent pool for {candidate.name} in segment {session.segment}', flush=True)
                                talent_pool = frappe.new_doc("Mira Talent Pool")
                                talent_pool.talent_id = candidate.name
                                talent_pool.segment_id = session.segment
                                talent_pool.added_at = now()
                                talent_pool.added_by = session.upload_by
                                print(f'========================= Inserting talent pool: {talent_pool.as_dict()}', flush=True)
                                talent_pool.insert(ignore_permissions=True)
                                frappe.db.commit()
                                print(f'========================= Talent pool created successfully: {talent_pool.name}', flush=True)
                                
                                # Log the talent pool assignment
                                session.append("logs", {
                                    "timestamp": now(),
                                    "log_type": "Success",
                                    "message": f"Added talent {candidate.full_name} ({candidate.name}) to segment pool {session.segment}",
                                    "talent_id": candidate.name,
                                    "segment_id": session.segment
                                })
                            except Exception as pool_error:
                                # Log the error but don't fail the entire process
                                print(f'========================= ERROR creating talent pool: {str(pool_error)}', flush=True)
                                import traceback
                                print(f'========================= Traceback: {traceback.format_exc()}', flush=True)
                                session.append("logs", {
                                    "timestamp": now(),
                                    "log_type": "Error",
                                    "message": f"Failed to add talent {candidate.name} to segment pool: {str(pool_error)}",
                                    "talent_id": candidate.name,
                                    "segment_id": session.segment
                                })
                                frappe.log_error(message=str(pool_error), title=f"Talent Pool Assignment Error - {candidate.name}")
                                
                    except Exception as map_error:
                        file.status = "Error"
                        file.error_message = f"Failed to map CV data: {str(map_error)}"
                        session.failed_count += 1
                        
                        # Log mapping error
                        session.append("logs", {
                            "timestamp": now(),
                            "log_type": "Error",
                            "message": f"Failed to map data from {file.file_name}: {str(map_error)}"
                        })
                        frappe.log_error(message=str(map_error), title=f"Resume Mapping Error - {file.file_name}")
                        continue

            except Exception as e:
                file.status = "Error"
                file.error_message = str(e)
                session.failed_count += 1

            session.save(ignore_permissions=True)
            frappe.db.commit()
            
        frappe.publish_realtime('resume_upload_update', {'session_name': session_name})
        session.status = "Completed"
        
        # Log session completion
        session.append("logs", {
            "timestamp": now(),
            "log_type": "Success",
            "message": f"Processing completed: {session.success_count} successful, {session.failed_count} failed, {session.duplicated_count} duplicates"
        })
        session.save(ignore_permissions=True)

    except Exception as e:
        frappe.log_error(message=str(e), title="Resume Processing Error")
        session.status = "Error"
        session.save(ignore_permissions=True)
        frappe.db.commit()

@frappe.whitelist(allow_guest=False)
def get_upload_history():
    """Fetch upload session history for the frontend."""
    sessions = frappe.get_all(
        "Mira ResumeUploadSession",
        fields=[
            "name", "upload_by", "upload_at", "status", "total_files",
            "success_count", "failed_count", "duplicated_count", "note", "segment"
        ],
        order_by="upload_at desc",
        limit=50
    )

    for session in sessions:
        session["files"] = frappe.get_all(
            "Mira ResumeUploadFile",
            filters={"parent": session.name},
            fields=["file_name", "file_url", "status", "error_message", "talent_id", "processed_at"]
        )

    return sessions
