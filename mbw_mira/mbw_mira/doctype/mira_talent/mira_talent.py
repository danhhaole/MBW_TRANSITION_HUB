# Copyright (c) 2025, MBWCloud Co. and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe.utils import nowdate, now_datetime, now
import json
from frappe import _
import requests
from frappe.utils.file_manager import save_file
import os
from mbw_mira.mbw_mira.doctype.mira_task_definition.mira_task_definition import (
    create_task_definitions_from_event,
)
from mbw_mira.mbw_mira.doctype.talent_activity_log.talent_activity_log import (
    create_talent_activity_log,
)
from mbw_mira.utils.ai import call_llm_convert_json_to_text, extract_cv_backend_file_url


class MiraTalent(Document):

    def after_insert(self):
        create_task_definitions_from_event(
            event_trigger="ON_CREATE",
            target_type="Mira Talent",
            target_id=self.name,
            event_payload=self.as_dict(),
        )
        if hasattr(self, "utm_campaign") and self.utm_campaign:
            self.create_talent_pool()

        # Tạo log vào
        create_talent_activity_log(
            talent_id=self.name,
            activity_type="Created",
            subject=f"New Talent Created: {self.full_name}",
            description=f"Talent {self.full_name} has been added to the system.",
            trigger_type="system",
            is_system_generated=1,
            source=self.source,
        )

    def on_update(self):
        if not self.flags.in_insert:  # nghĩa là UPDATE, không phải INSERT
            old_doc = self.get_doc_before_save()
            if (
                old_doc
                and hasattr(old_doc, "crm_status")
                and old_doc.crm_status != self.crm_status
            ):
                self.on_status_changed(old_doc.crm_status, self.crm_status)
            if old_doc and hasattr(old_doc, "tags") and old_doc.tags != self.tags:
                self.on_tag_added()

            meta_fields = self.meta.fields
            if meta_fields:
                for field in meta_fields:
                    changed_fields = self.has_value_changed(field.fieldname)
                    if changed_fields and hasattr(old_doc, field.fieldname):
                        old = old_doc.get(field.fieldname)
                        new = self.get(field.fieldname)

                        create_talent_activity_log(
                            talent_id=self.name,
                            activity_type="System Update",
                            subject=f"{field.fieldname} changed",
                            description=f"Field **{field.fieldname}** changed from **{old}** → **{new}**",
                            trigger_type="system",
                            is_system_generated=1,
                            source="system",
                        )

        # Nếu có resume thì gọi extract cv backend
        if self.resume:
            frappe.enqueue(
                "mbw_mira.mbw_mira.doctype.mira_talent.mira_talent.extract_and_summary",
                queue="default",
                talent_id=self.name,
                resume=self.resume,
            )
        else:
            resume = frappe.db.get_value("Mira Talent", self.name, "resume")
            # Nếu không có resume thì tạo theo summary chung
            if not resume:
                frappe.enqueue(
                    "mbw_mira.mbw_mira.doctype.mira_talent.mira_talent.summary_without_resume",
                    queue="default",
                    talent_id=self.name,
                )

    def on_talent_update(self):
        create_task_definitions_from_event(
            event_trigger="ON_UPDATE",
            target_type="Mira Talent",
            target_id=self.name,
            event_payload=self.as_dict(),
        )

    def on_tag_added(self):
        create_task_definitions_from_event(
            event_trigger="ON_TAG_ADDED",
            target_type="Mira Talent",
            target_id=self.name,
            event_payload={"tags": self.tags},
        )

    def on_status_changed(self, old_status, new_status):
        create_task_definitions_from_event(
            event_trigger="ON_STATUS_CHANGED",
            target_type="Mira Talent",
            target_id=self.name,
            event_payload={"old_status": old_status, "new_status": new_status},
        )

    def after_delete(self):
        try:
            frappe.delete_doc("Mira Talent Pool", filters={"talent_id": self.name})
            frappe.db.commit()

        except Exception as e:
            pass

    def after_save(self):
        pass
        # Tạo Talent Campaign
        # if hasattr(self,"campaign_id"):
        #     self.create_talent_campaign()

    def create_talent_pool(self):
        """Tạo Talent pool nếu talent được thêm vào từ chiến dịch có utm_campaign và talent pool"""
        if self.utm_campaign:
            # Lấy ra campaign kiểm tra có talent pool không
            target_pool = frappe.db.get_value(
                "Mira Campaign", self.utm_campaign, "target_pool"
            )
            if target_pool and not check_exists(target_pool, self.name):
                frappe.get_doc(
                    {
                        "doctype": "Mira Talent Pool",
                        "segment_id": target_pool,
                        "talent_id": self.name,
                        "enroll_type": "Automatic",
                        "match_score": 0,
                        "added_at": now(),
                        "added_by": frappe.session.user,  # hoặc seg.owner_id
                    }
                ).insert(ignore_permissions=True)
                frappe.db.commit()


def check_exists(segment_id, talent_id):
    talent_degment_exists = frappe.db.exists(
        "Mira Talent Pool", {"segment_id": segment_id, "talent_id": talent_id}
    )
    if talent_degment_exists:
        return True
    else:
        return False


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
            return {"status": "error", "message": _("Talent name is required")}

        # Kiểm tra document có tồn tại không
        if not frappe.db.exists("Mira Talent", name):
            return {
                "status": "error",
                "message": _("Talent {0} does not exist").format(name),
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
            "message": _("Talent {0} deleted successfully").format(name),
        }

    except Exception as e:
        frappe.db.rollback()
        frappe.log_error(
            message=frappe.get_traceback(), title=f"Delete Talent Error: {name}"
        )
        return {"status": "error", "message": str(e)}


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
                doctype, filters={fieldname: doc.name}, fields=["name"]
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
                        title=f"Unlink Error: {doctype} - {linked_doc.name}",
                    )
                    continue

    except Exception as e:
        frappe.log_error(
            message=frappe.get_traceback(), title=f"Unlink References Error: {doc.name}"
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
        filters={"fieldtype": "Link", "options": meta.name},
        fields=["parent", "fieldname"],
    )

    linked_doctypes.extend(links)

    # Tìm trong Custom Field
    custom_links = frappe.get_all(
        "Custom Field",
        filters={"fieldtype": "Link", "options": meta.name},
        fields=["dt as parent", "fieldname"],
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
        return {"status": "error", "message": _("Talent names are required")}

    # Parse names nếu là string
    if isinstance(names, str):
        try:
            names = json.loads(names)
        except:
            names = [n.strip() for n in names.split(",") if n.strip()]

    if not names or not isinstance(names, list):
        return {"status": "error", "message": _("Invalid talent names provided")}

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
            indicator="orange",
        )

    if not existing_talents:
        return {"status": "error", "message": _("No valid talents to delete")}

    # Enqueue từng job xóa
    queued_jobs = []
    failed_jobs = []

    for name in existing_talents:
        try:
            job = frappe.enqueue(
                "mbw_mira.mbw_mira.doctype.mira_talent.mira_talent.delete_talent",
                queue="default",
                job_name=f"delete_talent_{name}",
                name=name,
            )
            queued_jobs.append(name)

        except Exception as e:
            frappe.log_error(
                message=frappe.get_traceback(),
                title=f"Queue Delete Talent Error: {name}",
            )
            failed_jobs.append(name)

    # Tạo message kết quả
    message = ""
    if queued_jobs:
        message += _("Queued {0} talent(s) for deletion: {1}").format(
            len(queued_jobs), ", ".join(queued_jobs)
        )

    if failed_jobs:
        if message:
            message += "<br>"
        message += _("Failed to queue {0} talent(s): {1}").format(
            len(failed_jobs), ", ".join(failed_jobs)
        )
    info = {
        "status": "success" if queued_jobs else "error",
        "message": message,
        "queued": len(queued_jobs),
        "failed": len(failed_jobs),
        "queued_talents": queued_jobs,
        "failed_talents": failed_jobs,
    }
    frappe.publish_realtime("bulk_remove_talent_complete", info)
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
            return {"status": "error", "message": _("Talent name is required")}

        if not frappe.db.exists("Mira Talent", name):
            return {
                "status": "error",
                "message": _("Talent {0} does not exist").format(name),
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
                limit=100,
            )

            if linked_docs:
                references.append(
                    {
                        "doctype": doctype,
                        "fieldname": fieldname,
                        "count": len(linked_docs),
                        "documents": [d.name for d in linked_docs],
                    }
                )

        return {
            "status": "success",
            "talent": name,
            "has_references": len(references) > 0,
            "references": references,
        }

    except Exception as e:
        frappe.log_error(
            message=frappe.get_traceback(), title=f"Check Talent Links Error: {name}"
        )
        return {"status": "error", "message": str(e)}


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
        if "resume" in files:
            file = files["resume"]
            file_doc = frappe.get_doc(
                {
                    "doctype": "File",
                    "file_name": file.filename,
                    "content": file.stream.read(),
                    "attached_to_doctype": "Mira Talent",
                    "attached_to_name": None,  # Will be set after creating the prospect
                    "attached_to_field": "resume",
                }
            )
            file_doc.save(ignore_permissions=True)
            form_data["resume"] = file_doc.file_url

        # Basic validation
        required_fields = ["full_name", "email", "phone"]
        for field in required_fields:
            if not form_data.get(field):
                return {"success": False, "error": f"Missing required field: {field}"}

        # Map form data to document fields
        doc_data = {
            "full_name": form_data.get("full_name"),
            "email": form_data.get("email"),
            "phone": form_data.get("phone"),
            "current_company": form_data.get("current_company", ""),
            "current_designation": form_data.get("current_designation", ""),
            "experience_years": form_data.get("experience_years"),
            "linkedin_profile": form_data.get("linkedin_profile", ""),
            "notes": form_data.get("notes", ""),
        }

        # Add resume if exists
        if "resume" in form_data:
            doc_data["resume"] = form_data["resume"]

        # Create new prospect document
        doc = frappe.new_doc("Mira Talent")
        doc.update(doc_data)

        # Map form data to document fields
        field_mapping = {
            "full_name": "full_name",
            "email": "email",
            "phone": "phone",
            "current_designation": "position",
            "current_company": "current_company",
            "experience_years": "years_of_experience",
            "linkedin_profile": "linkedin_profile",
            "notes": "notes",
        }

        for form_field, doc_field in field_mapping.items():
            if form_field in form_data:
                doc.set(doc_field, form_data[form_field])

        doc.date = nowdate()

        # Handle file upload if exists
        if "resume" in form_data and form_data["resume"]:
            # You might want to handle file upload separately using frappe.upload_file()
            # For now, we'll just store the file name
            doc.resume = form_data["resume"].name

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
            "prospect_id": doc.name,
        }

    except Exception as e:
        frappe.log_error(
            title="Job Application Error",
            message=f"Error in submit_job_application: {str(e)}\nForm Data: {form_data}",
        )
        return {
            "success": False,
            "error": "Có lỗi xảy ra khi gửi đơn ứng tuyển. Vui lòng thử lại sau.",
        }


def process_tracking_to_talent(tracking_doc_name):
    """
    Hàm xử lý nghiệp vụ: chuyển dữ liệu từ DocType Tracking sang DocType Mira Talent.
    """
    try:
        # Lấy dữ liệu từ DocType Mira Talent Tracking đã lưu
        tracking_doc = frappe.get_doc("Mira Talent Tracking", tracking_doc_name)
        data = tracking_doc.as_dict()  # Lấy toàn bộ fields

        # 1. Kiểm tra các trường bắt buộc (đã kiểm tra ở bước trước nhưng kiểm tra lại)
        email = data.get("email")
        phone = data.get("phone")
        if not tracking_doc.notes:
            tracking_doc.notes = ""
        if not data.get("full_name") or (not email and not phone):
            # Cập nhật trạng thái lỗi và dừng xử lý
            tracking_doc.db_set("processing_status", "Failed")
            tracking_doc.db_set(
                "notes",
                tracking_doc.notes
                + "\nThiếu thông tin bắt buộc (Full Name, Email/Phone).",
            )
            frappe.db.commit()
            return {"status": "error", "message": "Thông tin thiếu."}

        # 2. Tìm kiếm Talent hiện có
        talent = None
        # ... (Logic tìm kiếm Talent hiện có bằng Email/Phone giữ nguyên như phần trước)
        if email:
            talent_list = frappe.get_all(
                "Mira Talent", filters={"email": email}, limit=1
            )
            if talent_list:
                talent = frappe.get_doc("Mira Talent", talent_list[0].name)

        if not talent and phone:
            talent_list = frappe.get_all(
                "Mira Talent", filters={"phone": phone}, limit=1
            )
            if talent_list:
                talent = frappe.get_doc("Mira Talent", talent_list[0].name)

        # 3. Tạo mới hoặc Cập nhật Talent Doc
        is_new_talent = talent is None
        is_cv_apply = data.get("source") in ["MBW ATS", "Apply Form"]

        # (Phần logic tạo mới/cập nhật TalentDoc và thiết lập các trường mặc định)
        if is_new_talent:
            new_talent_doc = frappe.new_doc("Mira Talent")
            new_talent_doc.crm_status = "New"
            new_talent_doc.source = data.get("source", "Nurturing Interaction")
            if is_cv_apply:
                new_talent_doc.recruitment_readiness = "High"
                new_talent_doc.priority_level = "High"
        else:
            new_talent_doc = talent
            if is_cv_apply:
                new_talent_doc.crm_status = "Profiling"
                new_talent_doc.recruitment_readiness = "High"
                new_talent_doc.priority_level = "High"
                new_talent_doc.source = data.get("source")

        # 4. Mapping Dữ liệu và Xử lý Resume URL
        valid_fieldnames = [
            f.fieldname
            for f in new_talent_doc.meta.fields
            if f.fieldname
            not in [
                "docstatus",
                "name",
                "creation",
                "modified",
                "owner",
                "idx",
                "parent",
            ]
        ]

        for field_name in valid_fieldnames:
            if (
                field_name in data
                and field_name not in ["resume"]
                and data.get(field_name)
            ):  # resume được xử lý riêng
                # Thiết lập giá trị cho trường nếu có trong dữ liệu Tracking
                new_talent_doc.set(field_name, data.get(field_name))

        # Xử lý Resume URL
        resume_url = data.get("resume")
        if resume_url and (
            resume_url.startswith("http") or resume_url.startswith("/files/")
        ):
            try:
                # Nếu là URL bên ngoài (http/https)
                if resume_url.startswith("http"):
                    response = requests.get(resume_url, stream=True, timeout=30)
                    response.raise_for_status()
                    content = response.content

                    filename = os.path.basename(resume_url).split("?")[0]
                    if not filename or "." not in filename:
                        filename = f"CV_{new_talent_doc.full_name.replace(' ', '_')}_{now_datetime()}.pdf"

                # Nếu là đường dẫn tệp Frappe (/files/...)
                elif resume_url.startswith("/files/"):
                    # Tệp đã có sẵn trong Frappe, chỉ cần cập nhật trường Attach
                    new_talent_doc.resume = resume_url
                    content = None  # Đã có sẵn, không cần tải/lưu
                    filename = None

                if content:
                    file_doc = save_file(
                        fname=filename,
                        content=content,
                        doctype="Mira Talent",
                        docname=new_talent_doc.name,
                        is_private=1,
                    )
                    new_talent_doc.resume = file_doc.file_url

            except requests.exceptions.RequestException as req_err:
                note = (
                    f"\n[Lỗi] Không thể tải CV từ URL: {resume_url}. Error: {req_err}"
                )
                new_talent_doc.interaction_notes = (
                    new_talent_doc.interaction_notes or ""
                ) + note
                frappe.log_error(note, "Resume Download Failed")
            except Exception as save_err:
                note = f"\n[Lỗi] Lỗi khi lưu file CV: {save_err}"
                new_talent_doc.interaction_notes = (
                    new_talent_doc.interaction_notes or ""
                ) + note
                frappe.log_error(note, "Resume Save Failed")
        else:
            # Nếu không phải URL, giả sử là tên file đã có sẵn hoặc trống
            new_talent_doc.resume = resume_url

        # 5. Cập nhật các trường cuối và Lưu Doc
        new_talent_doc.last_interaction_date = nowdate()
        new_talent_doc.interaction_notes = (
            new_talent_doc.interaction_notes or ""
        ) + f"\n--- Dữ liệu tracking từ {tracking_doc.name}"

        new_talent_doc.save(ignore_permissions=True)
        frappe.db.commit()

        # Cập nhật trạng thái thành công cho Doc Tracking
        tracking_doc.db_set("processing_status", "Success")
        tracking_doc.db_set(
            "notes", f"Đã chuyển thành công sang Talent: {new_talent_doc.name}"
        )
        frappe.db.commit()

        return {
            "status": "success",
            "message": f"Hồ sơ Talent {new_talent_doc.name} được tạo/cập nhật thành công.",
            "talent_id": new_talent_doc.name,
        }

    except Exception as e:
        # Cập nhật trạng thái lỗi nếu logic nghiệp vụ thất bại
        frappe.log_error(
            frappe.get_traceback(), f"Talent Processing Failed for {tracking_doc_name}"
        )
        if "tracking_doc" in locals():
            tracking_doc.db_set("processing_status", "Failed")
            tracking_doc.db_set("notes", tracking_doc.notes + f"\n[Lỗi Xử lý] {e}")
            frappe.db.commit()

        return {"status": "error", "message": f"Lỗi xử lý nghiệp vụ: {e}"}


def extract_and_summary(talent_id, resume):
    profile = extract_cv_backend_file_url(resume)
    # Cập nhật thông tin vào profile
    if profile:
        frappe.db.set_value(
            "Mira Talent", talent_id, "resume_extract", json.dumps(profile)
        )
        # Summary lại json
        summary_json = call_llm_convert_json_to_text(profile)
        if summary_json:
            frappe.db.set_value(
                "Mira Talent", talent_id, "resume_summary", json.dumps(summary_json)
            )
            # Lưu vào Mira talent vecto để tạo vecto phục vụ cho việc tìm pool theo AI
            if check_exists_vecto(talent_id):
                doc = frappe.get_doc("Mira Talent Vecto", {"mira_talent": talent_id})
                doc.update({"summary_text": summary_json.get("summary")})
                doc.save(ignore_permissions=True)
            else:
                doc = frappe.new_doc("Mira Talent Vecto")
                doc.update(
                    {
                        "mira_talent": talent_id,
                        "summary_text": summary_json.get("summary"),
                    }
                )
                doc.insert(ignore_permissions=True)
            frappe.db.commit()


# Summary without resume
def summary_without_resume(talent_id):
    talent = frappe.db.get_value(
        "Mira Talent",
        talent_id,
        [
            "full_name",
            "gender",
            "date_of_birth",
            "email",
            "phone",
            "linkedin_profile",
            "facebook_profile",
            "zalo_profile",
            "current_city",
            "skills",
            "tags",
            "source",
            "total_years_of_experience",
            "education",
            "experience",
            "certifications",
            "languages",
            "current_status",
            "notes",
            "desired_role",
            "domain_expertise",
            "cultural_fit",
            "hard_skills",
            "soft_skills",
            "latest_company",
            "highest_education",
            "current_salary",
            "expected_salary",
            "preferred_work_model",
            "availability_date",
            "recruiter_owner_id",
            "internal_rating",
            "interaction_notes",
            "latest_title",
        ],as_dict=1
    )

    # Summary lại json
    summary_json = call_llm_convert_json_to_text(talent)
    if summary_json:
        frappe.db.set_value(
            "Mira Talent", talent_id, "resume_summary", json.dumps(summary_json)
        )
        # Lưu vào Mira talent vecto để tạo vecto phục vụ cho việc tìm pool theo AI
        if check_exists_vecto(talent_id):
            doc = frappe.get_doc("Mira Talent Vecto", {"mira_talent": talent_id})
            doc.update({"summary_text": summary_json.get("summary")})
            doc.save(ignore_permissions=True)
        else:
            doc = frappe.new_doc("Mira Talent Vecto")
            doc.update(
                {"mira_talent": talent_id, "summary_text": summary_json.get("summary")}
            )
            doc.insert(ignore_permissions=True)
        frappe.db.commit()


def check_exists_vecto(talent_id):
    exists_vecto = frappe.db.exists("Mira Talent Vecto", {"mira_talent": talent_id})
    if exists_vecto:
        return True
    else:
        return False
