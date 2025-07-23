# file: mbw_mira/workers/segment_talent.py
import frappe
from frappe.utils import now
import json

from mbw_mira.utils import find_candidates_fuzzy

def process_segment(segment_id: str):
    """
    Process auto-segmentation for one TalentSegment
    """
    #frappe.logger().info(f"[AutoSegment] Processing: {seg.name} - {seg.title}")
    # frappe.log_error("Lỗi",seg)
    try:
        matches = find_candidates_fuzzy(None,segment_id)
        
        if matches:
            for profile in matches:
                if not check_exists(segment_id,profile.get("name")):
                    frappe.get_doc({
                        "doctype": "TalentProfilesSegment",
                        "segment_id": segment_id,
                        "talent_id": profile.get("name"),
                        "added_at": now(),
                        "added_by": frappe.session.user  # hoặc seg.owner_id
                    }).insert(ignore_permissions=True)
                    frappe.db.commit()
        frappe.publish_realtime('enroll_talent_segment', data={'segment': segment_id})
        return matches
    except Exception as e:
        frappe.log_error(frappe.get_traceback(), f"[AutoSegment Error] Segment {segment_id}")
        return None


def check_exists(segment_id,talent_id):
    talent_degment_exists = frappe.db.exists("TalentProfilesSegment",{"segment_id":segment_id,"talent_id":talent_id})
    if talent_degment_exists:
        return True
    else:
        return False