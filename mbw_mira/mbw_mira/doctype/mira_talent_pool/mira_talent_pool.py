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

@frappe.whitelist(allow_guest=True)
def get_talent_pool(segment_title=None):
    conditions = ""
    values = {}

    if segment_title:
        conditions += " AND seg.title LIKE %(segment_title)s"
        values["segment_title"] = f"%{segment_title}%"

    query = """
        SELECT 
            tp.name,
            tp.creation,
            tp.owner,
            tp.match_score,
            tp.talent_id,
            t.full_name AS full_name,
            t.email AS contact_email,
            t.phone AS contact_phone,
            t.skills,
            t.source,
            t.linkedin_profile,
            t.facebook_profile,
            t.zalo_profile,
            tp.segment_id,
            seg.title AS title
        FROM `tabMira Talent Pool` tp
        LEFT JOIN `tabMira Segment` seg ON seg.name = tp.segment_id
        LEFT JOIN `tabMira Talent` t ON t.name = tp.talent_id
        WHERE tp.name IS NOT NULL
        {conditions}
        ORDER BY tp.creation DESC
    """.format(conditions=conditions)

    return frappe.db.sql(query, values, as_dict=True)

@frappe.whitelist(allow_guest=True)
def get_talent_pool_detail(name):
    if not name:
        frappe.throw("Talent Pool name is required")

    query = """
        SELECT 
            tp.name,
            tp.creation,
            tp.owner,
            tp.match_score,
            tp.talent_id,
            t.full_name AS full_name,
            t.email AS contact_email,
            t.phone AS contact_phone,
            t.skills,
            t.source,
            t.linkedin_profile,
            t.facebook_profile,
            t.zalo_profile,
            tp.segment_id,
            seg.title AS title
        FROM `tabMira Talent Pool` tp
        LEFT JOIN `tabMira Segment` seg ON seg.name = tp.segment_id
        LEFT JOIN `tabMira Talent` t ON t.name = tp.talent_id
        WHERE tp.name = %(name)s
    """

    result = frappe.db.sql(query, {"name": name}, as_dict=True)
    if not result:
        frappe.throw(f"Talent Pool {name} not found", frappe.DoesNotExistError)
    
    return result[0]

@frappe.whitelist()
def update_talent_pools_segment(names, segment_id):
    try:
        # Convert string to list if it's a string (handles JSON string from frontend)
        if isinstance(names, str):
            import json
            names = json.loads(names)
        
        # Update each talent pool
        for name in names:
            frappe.db.set_value('Mira Talent Pool', name, {
                'segment_id': segment_id
            })
        
        frappe.db.commit()
        return {"status": "success", "message": f"Updated {len(names)} talent pool(s)"}
    
    except Exception as e:
        frappe.log_error(f"Error in update_talent_pools_segment: {str(e)}")
        frappe.throw(f"Failed to update talent pools: {str(e)}")

@frappe.whitelist(allow_guest=True)
def get_talent_interactions(talent_pool_id: str):
    # 1.Lấy thông tin bản ghi Talent Pool
    pool = frappe.get_doc("Mira Talent Pool", talent_pool_id)

    # 2️.Lấy thông tin Talent
    talent = frappe.get_doc("Mira Talent", pool.talent_id)

    # 3️.Lấy thông tin Contact
    contact_id = talent.contact_id

    # 4️.Lấy tất cả các Interaction thuộc Contact đó
    interactions = frappe.get_all(
        "Mira Interaction",
        filters={"talent_id": contact_id},
        fields=["name", "interaction_type", "action", "url", "description", "creation"]
    )

    # 5. Map action details nếu có
    for itrc in interactions:
        if itrc.get("action"):
            action_doc = frappe.get_doc("Action", itrc["action"])
            itrc["action_status"] = action_doc.status
            itrc["campaign_step"] = action_doc.campaign_step
            itrc["scheduled_at"] = action_doc.scheduled_at
            itrc["executed_at"] = action_doc.executed_at
        else:
            itrc["action_status"] = None
            itrc["campaign_step"] = None
            itrc["scheduled_at"] = None
            itrc["executed_at"] = None

    # 6️. Trả kết quả
    return {
        "talent_pool": pool.name,
        "talent": {
            "id": talent.name,
            "full_name": talent.full_name,
            "email": talent.email,
            "phone": talent.phone,
            "skills": talent.skills,
            "source": talent.source,
            "linkedin_profile": talent.linkedin_profile,
            "facebook_profile": talent.facebook_profile,
            "zalo_profile": talent.zalo_profile     
        },
        "contact_id": contact_id,
        "interactions": interactions
    }