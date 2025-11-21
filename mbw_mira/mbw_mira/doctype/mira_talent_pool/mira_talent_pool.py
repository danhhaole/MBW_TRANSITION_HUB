# Copyright (c) 2025, MBWCloud Co. and contributors
# For license information, please see license.txt

import frappe
from frappe import _
from frappe.model.document import Document
import json

from mbw_mira.mbw_mira.doctype.talent_activity_log.talent_activity_log import create_talent_activity_log

class MiraTalentPool(Document):
    

    def validate(self):
        validate_unique_candidate_segment(self)

    def after_save(self):
        create_talent_activity_log(
                            talent_id=self.name,
                            activity_type="Added to Pool",
                            subject=f"Talent Added to Pool by {self.enroll_type}",
                            description=f"Added to Pool {self.name} by {self.enroll_type}",
                            trigger_type="system",
                            is_system_generated=1,
                            source="system"
                        )

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
        frappe.db.set_value("Mira Segment",segment_id,"candidate_count",total_candidate)
        frappe.db.commit()
    except Exception as e:
        pass


@frappe.whitelist()
def bulk_insert_segments():
    """
    Bulk insert Mira Talent Pool records directly (no queue).
    Accepts JSON body or form_dict['data'].
    Returns status per record: success / duplicate / fail
    """

    try:
        # 1. Get data from request body (sent as JSON)
        payload = None
        
        # Try to get from request body first (when sent via fetch with JSON body)
        if frappe.request and frappe.request.data:
            try:
                payload = frappe.request.get_json()
                if payload and isinstance(payload, list):
                    # Direct JSON array in body
                    pass
                elif payload and isinstance(payload, dict) and 'data' in payload:
                    # Wrapped in {data: [...]}
                    payload = payload['data']
            except Exception as e:
                frappe.logger().error(f"Failed to parse request body: {e}")
        
        # If not found, try form_dict (when sent via frappe-ui call())
        if payload is None:
            raw_data = frappe.form_dict.get("data")
            if raw_data:
                if isinstance(raw_data, list):
                    payload = raw_data
                elif isinstance(raw_data, str):
                    try:
                        payload = json.loads(raw_data)
                    except Exception as e:
                        frappe.logger().error(f"Failed to parse form_dict data: {e}")
                        frappe.throw(_("Invalid JSON format"))
            else:
                payload = []
        
        # 2. Validate
        if not isinstance(payload, list):
            frappe.throw(_(f"Input data must be a list of records. Got type: {type(payload).__name__}"))
        

        result = []
        inserted_count = 0
        
        for idx, item in enumerate(payload):
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
                

                # Check if exists
                existing = frappe.db.exists("Mira Talent Pool", filters)
                if existing:
                    status_entry["status"] = "duplicate"
                    status_entry["message"] = f"Record already exists: {existing}"
                    frappe.logger().debug(f"  → Duplicate found: {existing}")
                else:
                    # Insert new record
                    doc = frappe.new_doc("Mira Talent Pool")
                    doc.update(item)
                    doc.update({"enroll_type":"Manual"})
                    doc.insert(ignore_permissions=True)
                    
                    # Commit immediately to prevent race condition
                    frappe.db.commit()
                    
                    inserted_count += 1
                    status_entry["status"] = "success"
                    status_entry["message"] = f"Inserted: {doc.name}"
            except Exception as e:
                status_entry["status"] = "fail"
                status_entry["message"] = str(e)
                frappe.log_error(frappe.get_traceback(), "Bulk Insert Error")

            result.append(status_entry)        
        # Calculate summary
        summary = {
            "success": sum(1 for r in result if r["status"] == "success"),
            "duplicate": sum(1 for r in result if r["status"] == "duplicate"),
            "fail": sum(1 for r in result if r["status"] == "fail")
        }

        return {
            "status": "completed",
            "total": len(payload),
            "summary": summary,
            "results": result
        }

    except Exception as e:
        frappe.log_error(frappe.get_traceback(), "Bulk Insert API Error")
        frappe.throw(_("Failed to process bulk insert."))

@frappe.whitelist()
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
            action_doc = frappe.get_doc("Mira Action", itrc["action"])
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

@frappe.whitelist(allow_guest=True)
def get_talent_detail_view(pool_id: str):
    """
    Lấy dữ liệu chi tiết Talent thông qua Mira Talent Pool:
    - Thông tin ứng viên (bên trái)
    - Tab Chiến dịch / Hành động / Thực hiện (bên phải)
    """

    # Lấy thông tin từ Mira Talent Pool
    pool = frappe.get_doc("Mira Talent Pool", pool_id)
    talent_id = pool.talent_id

    if not talent_id:
        frappe.throw("Không tìm thấy Talent tương ứng trong Mira Talent Pool")

    # 1. Thông tin Talent
    talent = frappe.get_doc("Mira Talent", talent_id)
    contact = None
    if talent.contact_id:
        contact = frappe.db.get_value(
            "Mira Contact",
            talent.contact_id,
            ["full_name", "email", "phone"],
            as_dict=True
        )

    talent_info = {
        "id": talent.name,
        "full_name": talent.full_name,
        "email": talent.email,
        "phone": talent.phone,
        "status": talent.current_status,
        "source": talent.source,
        "skills": talent.skills,
        "gender": talent.gender,
        "date_of_birth": talent.date_of_birth,
        "linkedin_profile": talent.linkedin_profile,
        "facebook_profile": talent.facebook_profile,
        "zalo_profile": talent.zalo_profile,
    }

    # 2. Tab "Chiến dịch" - các campaign mà Talent tham gia
    campaigns = frappe.get_all(
        "Mira Talent Campaign",
        filters={"talent_id": talent_id},
        fields=["name", "campaign_id", "status", "enrolled_at", "next_action_at", "current_step_order"]
    )

    campaign_data = []
    for c in campaigns:
        campaign_info = frappe.db.get_value(
            "Mira Campaign",
            c.campaign_id,
            ["campaign_name", "name"],
            as_dict=True
        )

        campaign_data.append({
            "name": campaign_info.name if campaign_info else None,
            "id": c.name,
            "campaign_name": campaign_info.campaign_name if campaign_info else None,
            "status": c.status,
            "enrolled_at": c.enrolled_at,
            "next_action_at": c.next_action_at,
            "current_step_order": c.current_step_order
        })

    # 3. Tab "Hành động" - tất cả Action từ các campaign
    all_actions = []
    for c in campaigns:
        actions = frappe.get_all(
            "Mira Action",
            filters={"talent_campaign_id": c.name},
            fields=["name", "campaign_step", "status", "scheduled_at", "executed_at", "result"]
        )

        for a in actions:
            step = frappe.db.get_value(
                "Mira Campaign Step",
                a.campaign_step,
                ["campaign_step_name", "action_type", "step_order"],
                as_dict=True
            )
            a["campaign_id"] = c.campaign_id
            a["campaign_name"] = frappe.db.get_value("Mira Campaign", c.campaign_id, "campaign_name")
            a["step_name"] = step.campaign_step_name if step else None
            a["action_type"] = step.action_type if step else None
            a["step_order"] = step.step_order if step else None

        all_actions.extend(actions)

    # 4. Tab "Thực hiện" - tất cả Interaction từ các action
    all_interactions = []
    for a in all_actions:
        interactions = frappe.get_all(
            "Mira Interaction",
            filters={"action": a.name},
            fields=["name", "interaction_type", "url", "description", "creation"]
        )
        for i in interactions:
            i["action_id"] = a.name
            i["campaign_name"] = a.get("campaign_name")
            i["step_name"] = a.get("step_name")
        all_interactions.extend(interactions)

    # 5. Sắp xếp gọn gàng
    all_actions.sort(key=lambda x: x.get("scheduled_at") or "", reverse=True)
    all_interactions.sort(key=lambda x: x.get("creation") or "", reverse=True)

    # 6. Trả về dữ liệu tổng hợp
    return {
        "talent_info": talent_info,        # cột trái
        "campaigns": campaign_data,        # tab Chiến dịch
        "actions": all_actions,            # tab Hành động
        "interactions": all_interactions   # tab Thực hiện
    }