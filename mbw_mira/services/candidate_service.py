import frappe
from frappe import _
from frappe.utils import now_datetime, add_days

#Tạo CandidateSegment từ Campaign
def handle_candidate_segment(campaigns: list[str]):
    """
    Xử lý các CandidateCampaign từ danh sách Campaigns.
    Mỗi Campaign sẽ lấy danh sách Candidate từ CandidateSegment,
    sau đó insert vào CandidateCampaign.
    """
    if not campaigns:
        frappe.logger("campaign").info("[SKIP] No active campaigns found.")
        return

    for campaign in campaigns:
        segment = frappe.get_value("Campaign", campaign, "target_segment")
        if not segment:
            frappe.logger("campaign").info(f"[SKIP] Campaign {campaign} has no target segment.")
            continue

        # Mỗi campaign sẽ có thông tin segment,
        # lấy danh sách candidate từ CandidateSegment
        candidate_ids = candidate_segment_by_campaign(segment)
        if not candidate_ids:
            frappe.logger("campaign").info(f"[SKIP] No candidates found for segment {segment}.")
            continue

        # Insert vào CandidateSegment
        frappe.enqueue(
            "mbw_mira.services.candidate_service.insert_candidate_segment",
            queue="default",
            timeout=300,
            candidates=candidate_ids,
            segment=segment
        )

def insert_candidate_segment(**kwargs) -> list[str]:
    """
    Thêm nhiều CandidateSegment từ dữ liệu,
    đảm bảo duy nhất theo (candidate, segment).
    Bỏ qua các candidate đã tồn tại trong segment.
    """
        
    segment_id = kwargs.get("segment")
    candidate_ids = kwargs.get("candidates")
    added_by = kwargs.get("added_by", None)

    if not segment_id or not candidate_ids:
        frappe.throw(_("Both 'segment' and 'candidates' are required."))

    if not isinstance(candidate_ids, (list, tuple)):
        frappe.throw(_("Parameter 'candidates' must be a list."))

    added_by = added_by or frappe.session.user
    added_at = now_datetime()
    inserted_names = []

    # Lấy tất cả các candidate đã tồn tại trong segment
    existing_candidates = frappe.get_all(
        "CandidateSegment",
        filters={"segment_id": segment_id, "candidate_id": ["in", candidate_ids]},
        fields=["candidate_id"],
    )
    existing_candidate_ids = {x.candidate_id for x in existing_candidates}

    for candidate_id in candidate_ids:
        if candidate_id in existing_candidate_ids:
            # Bỏ qua nếu đã tồn tại
            continue

        doc = frappe.get_doc(
            {
                "doctype": "CandidateSegment",
                "candidate_id": candidate_id,
                "segment_id": segment_id,
                "added_at": added_at,
                "added_by": added_by,
            }
        )
        doc.insert(ignore_permissions=True)
        inserted_names.append(doc.name)

        # có thể publish realtime từng bản ghi hoặc gom lại
        frappe.publish_realtime("candidate_segment_created", data=doc)
        frappe.enqueue(
            "mbw_mira.services.candidate_service.insert_candidate_campaign",
            queue="default",
            timeout=300,
            campaign=doc.name,
            segment=segment_id
        )

    frappe.db.commit()

    
    
    return inserted_names


def insert_candidate_campaign(**kwargs):
    campaign_id = kwargs.get("campaign")
    segment = kwargs.get("segment")    

    if not campaign_id or not segment:
        frappe.throw(_("Both 'campaign' and 'segment' are required."))

    candidate_ids = candidate_segment_by_campaign(segment)
    
    # lấy step trong Campaign theo campaign
    step = frappe.get_all(
        "CampaignStep",
        filters={"campaign_id": campaign_id},
        fields=[
            "name",
            "campaign_step_name",
            "step_order",
            "action_type",
            "delay_in_days",
            "template",
            "action_config",
        ],
        order_by="step_order asc",
        page_length=1,
    )
    step = step[0]
    # tính next_action_at
    now = now_datetime()
    next_action_at = add_days(now, step["delay_in_days"] or 0)

    # Lấy tất cả các candidate đã tồn tại trong CandidateCampaign
    existing_candidates = frappe.get_all(
        "CandidateCampaign",
        filters={"campaign_id": campaign_id, "candidate_id": ["in", candidate_ids]},
        fields=["candidate_id"],
    )
    existing_candidate_ids = {x.candidate_id for x in existing_candidates}
    # Mặc định là active
    status = "ACTIVE"
    enrolled_at = now_datetime()
    current_step_order = (step["step_order"],)
    for candidate_id in candidate_ids:
        if candidate_id in existing_candidate_ids:
            # Bỏ qua nếu đã tồn tại
            continue

        doc = frappe.get_doc(
            {
                "doctype": "CandidateCampaign",
                "candidate_id": candidate_id,
                "segment_id": campaign_id,
                "status": status,
                "enrolled_at": enrolled_at,
                "current_step_order": current_step_order,
                "next_action_at": next_action_at,
            }
        )
        doc.insert(ignore_permissions=True)

        # có thể publish realtime từng bản ghi hoặc gom lại
        frappe.publish_realtime("candidate_segment_created", data=doc)

    frappe.db.commit()




# lấy danh sách candidate từ CandidateSegment
def candidate_segment_by_campaign(segment) -> list[str]:
    candidate_segments = frappe.get_all(
        "CandidateSegment", filters={"segment_id": segment}, fields=["candidate_id"]
    )
    candidate_ids = {x.candidate_id for x in candidate_segments}
    return candidate_ids
