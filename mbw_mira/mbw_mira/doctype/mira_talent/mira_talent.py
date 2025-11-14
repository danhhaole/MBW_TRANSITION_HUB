# Copyright (c) 2025, MBWCloud Co. and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe.utils import cstr, cint, flt, add_days, nowdate, get_datetime,now_datetime
from mbw_mira.api.common import get_filter_options, get_form_data, get_list_data
import json
from frappe import _

from mbw_mira.mbw_mira.doctype.mira_task_definition.mira_task_definition import create_task_definitions_from_event

class MiraTalent(Document):

    def after_insert(self):
        create_task_definitions_from_event(
            event_trigger="ON_CREATE",
            target_type="Mira Talent",
            target_id=self.name,
            event_payload=self.as_dict()
        )
    def on_update(self):
        if not self.get("__islocal"):  # nghĩa là UPDATE, không phải INSERT
            # self.on_talent_update()
            old_doc = self.get_doc_before_save()
            if old_doc and hasattr(old_doc, 'crm_status') and old_doc.crm_status != self.crm_status:
                self.on_status_changed(old_doc.crm_status,self.crm_status)
            if old_doc and hasattr(old_doc, 'tags') and old_doc.tags != self.tags:
                self.on_tag_added()
            
    def on_talent_update(self):
        create_task_definitions_from_event(
                event_trigger="ON_UPDATE",
                target_type="Mira Talent",
                target_id=self.name,
                event_payload=self.as_dict()
            )
    
    def on_tag_added(self):
        create_task_definitions_from_event(
            event_trigger="ON_TAG_ADDED",
            target_type="Mira Talent",
            target_id=self.name,
            event_payload={"tags": self.tags}
        )
    def on_status_changed(self,old_status, new_status):
        create_task_definitions_from_event(
            event_trigger="ON_STATUS_CHANGED",
            target_type="Mira Talent",
            target_id=self.name,
            event_payload={
                "old_status": old_status,
                "new_status": new_status
            }
        )

    def after_delete(self):
        try:
            frappe.delete_doc("Mira Talent Pool",filters={"talent_id":self.name})
            frappe.db.commit()

        except Exception as e:
            pass
    
    def after_save(self):
        pass
        #Tạo Talent Campaign
        # if hasattr(self,"campaign_id"): 
        #     self.create_talent_campaign()

    # def create_talent_campaign(self):
    #     try:           
    #         first_step = get_first_campaign_step(self.campaign_id)
    #         if first_step:
    #             next_action_at = add_days(now_datetime(), first_step.get("delay_in_days") or 0)
    #             doc = frappe.get_doc(
    #             {
    #                 "doctype": "Mira Talent Campaign",
    #                 "campaign_id": self.campaign_id,
    #                 "talent_id": self.talent_id,
    #                 "status": "ACTIVE",
    #                 "enrolled_at": now_datetime(),
    #                 "current_step_order": first_step.get("step_order")  or 1,
    #                 "next_action_at": next_action_at,
    #             }
    #             )
    #             doc.insert(ignore_permissions=True)
    #             frappe.db.commit()
    #     except Exception as e:
    #         pass
# def check_exists(email):
#     exists = frappe.db.exists("Mira Contact",{"email":email})
#     if exists:
#         return True
#     else:
#         return False

@frappe.whitelist()
def delete_talent(name=None):
    """
    Xóa một talent sau khi unlink các tham chiếu
    
    Args:
        name: Tên của Mira Talent document cần xóa (từ request body)
    
    Returns:
        dict: Kết quả thực hiện
    """
    try:
        # Lấy data từ request nếu không có name
        if not name:
            data = frappe.local.form_dict
            name = data.get("name")
        
        if not name:
            return {
                "status": "error",
                "message": _("Talent name is required")
            }
        
        # Kiểm tra document có tồn tại không
        if not frappe.db.exists("Mira Talent", name):
            return {
                "status": "error",
                "message": _("Talent {0} does not exist").format(name)
            }
        
        # Load document
        doc = frappe.get_doc("Mira Talent", name)
        
        # Kiểm tra quyền xóa
        if not frappe.has_permission("Mira Talent", "delete", doc=doc):
            frappe.throw(_("No permission to delete Talent {0}").format(name))
        
        # Lấy meta để kiểm tra links
        meta = frappe.get_meta("Mira Talent")
        
        # Kiểm tra và unlink các tham chiếu
        unlink_references(doc, meta)
        
        # Sau khi unlink, chỉ xóa talent, không xóa các tham chiếu
        frappe.delete_doc("Mira Talent", name, force=0, ignore_permissions=False)
        
        frappe.db.commit()
        
        return {
            "status": "success",
            "message": _("Talent {0} deleted successfully").format(name)
        }
        
    except Exception as e:
        frappe.db.rollback()
        frappe.log_error(message=frappe.get_traceback(), title=f"Delete Talent Error: {name}")
        return {
            "status": "error",
            "message": str(e)
        }


def unlink_references(doc, meta):
    """
    Unlink tất cả các tham chiếu của document trước khi xóa
    
    Args:
        doc: Mira Talent document
        meta: Meta object của Mira Talent
    """
    try:
        # Lấy danh sách các doctype có link đến Mira Talent
        linked_doctypes = get_linked_doctypes(meta)
        
        if not linked_doctypes:
            return
        
        # Duyệt qua từng doctype có link
        for link_info in linked_doctypes:
            doctype = link_info.get("parent")
            fieldname = link_info.get("fieldname")
            
            if not doctype or not fieldname:
                continue
            
            # Tìm các document tham chiếu đến talent này
            linked_docs = frappe.get_all(
                doctype,
                filters={fieldname: doc.name},
                fields=["name"]
            )
            
            # Unlink từng document
            for linked_doc in linked_docs:
                try:
                    ref_doc = frappe.get_doc(doctype, linked_doc.name)
                    
                    # Kiểm tra quyền write
                    if not frappe.has_permission(doctype, "write", doc=ref_doc):
                        continue
                    
                    # Set field về None/empty để unlink
                    ref_doc.set(fieldname, None)
                    ref_doc.flags.ignore_validate = True
                    ref_doc.flags.ignore_mandatory = True
                    ref_doc.save(ignore_permissions=False)
                    
                    # frappe.msgprint(
                    #     _("Unlinked {0} from {1}").format(doc.name, ref_doc.name),
                    #     alert=True
                    # )
                    
                except Exception as e:
                    frappe.log_error(
                        message=frappe.get_traceback(),
                        title=f"Unlink Error: {doctype} - {linked_doc.name}"
                    )
                    continue
                    
    except Exception as e:
        frappe.log_error(
            message=frappe.get_traceback(),
            title=f"Unlink References Error: {doc.name}"
        )
        raise


def get_linked_doctypes(meta):
    """
    Lấy danh sách các doctype có link field trỏ đến doctype này
    
    Args:
        meta: Meta object
        
    Returns:
        list: Danh sách các doctype có link
    """
    linked_doctypes = []
    
    # Tìm trong DocField
    links = frappe.get_all(
        "DocField",
        filters={
            "fieldtype": "Link",
            "options": meta.name
        },
        fields=["parent", "fieldname"]
    )
    
    linked_doctypes.extend(links)
    
    # Tìm trong Custom Field
    custom_links = frappe.get_all(
        "Custom Field",
        filters={
            "fieldtype": "Link",
            "options": meta.name
        },
        fields=["dt as parent", "fieldname"]
    )
    
    linked_doctypes.extend(custom_links)
    
    return linked_doctypes


@frappe.whitelist()
def delete_multiple_talents(names=None):
    """
    Xóa nhiều talent bằng cách enqueue từng job xóa riêng lẻ    
    Args:
        names: JSON string hoặc list các tên talent cần xóa (từ request body)
        
    Returns:
        dict: Kết quả thực hiện
    """
    
    # Lấy data từ request nếu không có names
    if not names:
        data = frappe.local.form_dict
        names = data.get("names")
    
    if not names:
        return {
            "status": "error",
            "message": _("Talent names are required")
        }
    
    # Parse names nếu là string
    if isinstance(names, str):
        try:
            names = json.loads(names)
        except:
            names = [n.strip() for n in names.split(",") if n.strip()]
    
    if not names or not isinstance(names, list):
        return {
            "status": "error",
            "message": _("Invalid talent names provided")
        }
    
    # Kiểm tra tất cả talents có tồn tại không
    existing_talents = []
    missing_talents = []
    
    for name in names:
        if frappe.db.exists("Mira Talent", name):
            existing_talents.append(name)
        else:
            missing_talents.append(name)
    
    if missing_talents:
        frappe.msgprint(
            _("Following talents do not exist: {0}").format(", ".join(missing_talents)),
            alert=True,
            indicator="orange"
        )
    
    if not existing_talents:
        return {
            "status": "error",
            "message": _("No valid talents to delete")
        }
    
    # Enqueue từng job xóa
    queued_jobs = []
    failed_jobs = []
    
    for name in existing_talents:
        try:
            job = frappe.enqueue(
                "mbw_mira.mbw_mira.doctype.mira_talent.mira_talent.delete_talent",
                queue="default",
                job_name=f"delete_talent_{name}",
                name=name
            )
            queued_jobs.append(name)
            
        except Exception as e:
            frappe.log_error(
                message=frappe.get_traceback(),
                title=f"Queue Delete Talent Error: {name}"
            )
            failed_jobs.append(name)
    
    # Tạo message kết quả
    message = ""
    if queued_jobs:
        message += _("Queued {0} talent(s) for deletion: {1}").format(
            len(queued_jobs),
            ", ".join(queued_jobs)
        )
    
    if failed_jobs:
        if message:
            message += "<br>"
        message += _("Failed to queue {0} talent(s): {1}").format(
            len(failed_jobs),
            ", ".join(failed_jobs)
        )
    info = {
        "status": "success" if queued_jobs else "error",
        "message": message,
        "queued": len(queued_jobs),
        "failed": len(failed_jobs),
        "queued_talents": queued_jobs,
        "failed_talents": failed_jobs
    }
    frappe.publish_realtime('bulk_remove_talent_complete', info)
    return info


@frappe.whitelist(allow_guest=True)
def check_talent_links(name=None):
    """
    Kiểm tra các link references của một talent    
    Args:
        name: Tên của Mira Talent (từ request body)        
    Returns:
        dict: Danh sách các tham chiếu
    """
    try:
        # Lấy data từ request nếu không có name
        if not name:
            data = frappe.local.form_dict
            name = data.get("name")
        
        if not name:
            return {
                "status": "error",
                "message": _("Talent name is required")
            }
        
        if not frappe.db.exists("Mira Talent", name):
            return {
                "status": "error",
                "message": _("Talent {0} does not exist").format(name)
            }
        
        doc = frappe.get_doc("Mira Talent", name)
        meta = frappe.get_meta("Mira Talent")
        
        linked_doctypes = get_linked_doctypes(meta)
        
        references = []
        for link_info in linked_doctypes:
            doctype = link_info.get("parent")
            fieldname = link_info.get("fieldname")
            
            if not doctype or not fieldname:
                continue
            
            linked_docs = frappe.get_all(
                doctype,
                filters={fieldname: doc.name},
                fields=["name", "modified"],
                limit=100
            )
            
            if linked_docs:
                references.append({
                    "doctype": doctype,
                    "fieldname": fieldname,
                    "count": len(linked_docs),
                    "documents": [d.name for d in linked_docs]
                })
        
        return {
            "status": "success",
            "talent": name,
            "has_references": len(references) > 0,
            "references": references
        }
        
    except Exception as e:
        frappe.log_error(
            message=frappe.get_traceback(),
            title=f"Check Talent Links Error: {name}"
        )
        return {
            "status": "error",
            "message": str(e)
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
        required_fields = ['full_name', 'email', 'phone']
        for field in required_fields:
            if not form_data.get(field):
                return {"success": False, "error": f"Missing required field: {field}"}

        # Map form data to document fields
        doc_data = {
            'full_name': form_data.get('full_name'),
            'email': form_data.get('email'),
            'phone': form_data.get('phone'),
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
            'email': 'email',
            'phone': 'phone',
            'current_designation': 'position',
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

