import frappe

def run():
    """
    Schedule auto-segmentation jobs for DYNAMIC TalentSegments
    """
    frappe.logger().info("[AutoSegment] Scheduler started")

    segments = frappe.get_all("TalentSegment",  fields=["name"])
    for seg in segments:
        frappe.enqueue(
            "mbw_mira.workers.auto_segment_worker.process_segment",
            queue="short",
            segment_id=seg.name,
            job_name=f"segment-{seg.name}"
        )

    frappe.logger().info(f"[AutoSegment] Scheduled {len(segments)} segments.")