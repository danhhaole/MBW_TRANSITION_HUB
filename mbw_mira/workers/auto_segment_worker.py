# file: mbw_mira/workers/segment_talent.py
import frappe
from frappe.utils import now
import json

from mbw_mira.utils import find_candidates_fuzzy

def process_segment(segment_id: str):
    """
    Process auto-segmentation for one TalentSegment
    """
    seg = frappe.db.get_value("TalentSegment", segment_id,["name","title","criteria"],as_dict=1)
    #frappe.logger().info(f"[AutoSegment] Processing: {seg.name} - {seg.title}")
    # frappe.log_error("Lỗi",seg)
    try:
        criteria = json.loads(seg.criteria or "{}")
        matches = find_candidates_fuzzy(criteria,segment_id)
        
        if matches:
            for profile in matches:
                frappe.get_doc({
                    "doctype": "TalentProfilesSegment",
                    "segment_id": seg.name,
                    "talent_id": profile.name,
                    "added_at": now(),
                    "added_by": frappe.session.user  # hoặc seg.owner_id
                }).insert(ignore_permissions=True)
                frappe.db.commit()


    except Exception as e:
        frappe.log_error(frappe.get_traceback(), f"[AutoSegment Error] Segment {seg.name}")


