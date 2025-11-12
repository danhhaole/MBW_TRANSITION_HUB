import frappe

def run_enroll_talent_pool():
    """
    Schedule auto-segmentation jobs for DYNAMIC Mira Talent Pool
    """

    pools = frappe.get_all("Mira Segment",  fields=["name"],filters={"type":"DYNAMIC"})
    for seg in pools:
        frappe.enqueue(
            "mbw_mira.workers.auto_segment_worker.enroll_talent_pool",
            queue="short",
            pool_id=seg.name,
            job_name=f"segment-{seg.name}"
        )

    return True

#Kiểm tra talent trong pool có phù hợp không nếu tiêu chỉ thấp quá
def run_disenroll_talent_pool():
    """Lấy danh sách các pool, chạy kiểm tra scrore với các điều kiện phụ hợp. Nếu không phù hợp thì xóa ra khỏi pool
    """
    pools = frappe.get_all("Mira Segment",  fields=["name"],filters={"type":"DYNAMIC"})
    for seg in pools:
        frappe.enqueue(
            "mbw_mira.workers.auto_segment_worker.disenroll_talent_pool",
            queue="short",
            pool_id=seg.name,
            job_name=f"segment-{seg.name}"
        )

    return True