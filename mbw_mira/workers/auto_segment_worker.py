# file: mbw_mira/workers/segment_talent.py
import frappe
from frappe.utils import now
import json

def enroll_talent_pool(pool_id: str):
    from mbw_mira.utils import find_candidates_fuzzy
    """
    Process auto-segmentation for one Mira Segment
    """
    #frappe.logger().info(f"[AutoSegment] Processing: {seg.name} - {seg.title}")
    # frappe.log_error("Lỗi",seg)
    try:
        matches = find_candidates_fuzzy(None,pool_id)
        
        if matches:
            for profile in matches:
                if not check_exists(pool_id,profile.get("name")):
                    frappe.get_doc({
                        "doctype": "Mira Talent Pool",
                        "segment_id": pool_id,
                        "talent_id": profile.get("name"),
                        "enroll_type":"Automatic",
                        "match_score":profile.get("score"),
                        "added_at": now(),
                        "added_by": frappe.session.user  # hoặc seg.owner_id
                    }).insert(ignore_permissions=True)
                    frappe.db.commit()
        frappe.publish_realtime('enroll_talent_segment', message={'segment': pool_id})
        return matches
    except Exception as e:
        frappe.log_error(frappe.get_traceback(), f"[AutoSegment Error] Segment {pool_id}")
        return None

#Xóa talent ra khỏi pool khi talent không đủ điểu kiện, chỉ xóa talent được thêm vào tự động
def disenroll_talent_pool(pool_id:str):
    from mbw_mira.utils import find_candidates_fuzzy
    try:
        #Lấy ra toàn bộ talent có scrore thấp
        matches = find_candidates_fuzzy(None,pool_id,0,True)
        if matches:
            for talent in matches:
                score = talent.get("score")
                if check_exists(pool_id,talent.get("name")) and score < 50:
                    frappe.delete_doc("Mira Talent Pool",{"segment_id": pool_id,"talent_id": talent.get("name")})
            frappe.db.commit()
                    
    except Exception as e:
        frappe.log_error(frappe.get_traceback(), f"[AutoSegment Error] Pool {pool_id}")
        return None


def check_exists(segment_id,talent_id):
    talent_degment_exists = frappe.db.exists("Mira Talent Pool",{"segment_id":segment_id,"talent_id":talent_id})
    if talent_degment_exists:
        return True
    else:
        return False

