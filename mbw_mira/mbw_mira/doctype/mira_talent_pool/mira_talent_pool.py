# Copyright (c) 2025, MBWCloud Co. and contributors
# For license information, please see license.txt

import frappe
from frappe import _
from frappe.model.document import Document
import json

class MiraTalentPool(Document):
    

    def validate(self):
        validate_unique_candidate_segment(self)

    def on_update(self):
        count_talentprofile_segment(self.segment_id)
        #Cập nhật phân trạng thái CATEGORIZED vào thông tin hồ sơ
        

def validate_unique_candidate_segment(doc):
    """
    Kiểm tra xem đã tồn tại Mira Talent Pool với cùng
    talent_id + segment_id (ngoại trừ chính nó) hay chưa.
    """
    filters = {
        "talent_id": doc.talent_id,
        "segment_id": doc.segment_id,
    }

    existing = frappe.db.exists("Mira Talent Pool", filters)

    if existing and existing != doc.name:
        frappe.throw(
            frappe._("A Mira Talent Pool with Candidate <b>{0}</b> and Segment <b>{1}</b> already exists: <a href='/app/candidate-segment/{2}'>{2}</a>").format(
                doc.talent_id,
                doc.segment_id,
                existing
            ),
            title=frappe._("Duplicate Mira Talent Pool")
        )

def count_talentprofile_segment(segment_id):
    try:
        total_candidate = frappe.db.count("Mira Talent Pool",filters={"segment_id":segment_id})
        print("===========total_candidate==============",total_candidate)
        if total_candidate and total_candidate > 0:
            frappe.db.set_value("Mira Segment",segment_id,"candidate_count",total_candidate)
            frappe.db.commit()
    except Exception as e:
        pass

def update_status_talent_profile(talent_id):
    #Trạng thái đã được phân loại
    frappe.db.set_value("Mira Prospect",talent_id,"status","CATEGORIZED")
    frappe.db.commit()

@frappe.whitelist(allow_guest=False)
def bulk_insert_segments():
    """
    Bulk insert Mira Talent Pool records directly (no queue).
    Accepts JSON body or form_dict['data'].
    Returns status per record: success / duplicate / fail
    """

    try:
        # 1. Lấy dữ liệu từ JSON body hoặc form_dict
        if frappe.request and frappe.request.data:
            payload = frappe.request.get_json()
        else:
            raw_data = frappe.form_dict.get("data")
            payload = json.loads(raw_data) if raw_data else []

        # 2. Validate
        if not isinstance(payload, list):
            frappe.throw(_("Input data must be a list of records"))

        result = []
        for item in payload:
            status_entry = {
                "data": item,
                "status": "pending",
                "message": ""
            }

            try:
                filters = {
                    "talent_id": item.get("talent_id"),
                    "segment_id": item.get("segment_id"),
                }

                if frappe.db.exists("Mira Talent Pool", filters):
                    status_entry["status"] = "duplicate"
                    status_entry["message"] = "Record already exists"
                else:
                    doc = frappe.new_doc("Mira Talent Pool")
                    doc.update(item)
                    doc.insert(ignore_permissions=True)

                    status_entry["status"] = "success"
                    status_entry["message"] = f"Inserted: {doc.name}"
            except Exception as e:
                status_entry["status"] = "fail"
                status_entry["message"] = str(e)
                frappe.log_error(frappe.get_traceback(), "Bulk Insert Error")

            result.append(status_entry)

        return {
            "status": "completed",
            "total": len(payload),
            "results": result
        }

    except Exception as e:
        frappe.log_error(frappe.get_traceback(), "Bulk Insert API Error")
        frappe.throw(_("Failed to process bulk insert."))