import frappe
from frappe import _
from frappe.utils import now_datetime, add_days,now

#Tạo CandidateSegment từ Campaign
def handle_candidate_segment():
    from mbw_mira.campaign.utils import find_candidates_fuzzy
    campaigns = _get_active_campaigns()
    
    if not campaigns:
        frappe.logger("campaign").info("[SKIP] No active campaigns found.")
        return
    
    for campaign in campaigns:
        if not campaign.target_segment:
            frappe.logger("campaign").info(f"[SKIP] Campaign {campaign} has no target segment.")
            continue

        # Mỗi campaign sẽ có thông tin segment,
        # lấy danh sách candidate từ CandidateSegment
        candidate_ids = candidate_segment_by_campaign(campaign.target_segment)

        #Lấy danh sách Candidate từ AI 
        # candidate_ids = None
        # candidate_segments = find_candidates_fuzzy(campaign.target_segment)
        # if candidate_segments:
        #     candidate_ids = [s.get("candidate_name") for s in candidate_segments]
        
        if not candidate_ids:
            frappe.logger("campaign").info(f"[SKIP] No candidates found for segment {campaign.target_segment}.")
            continue
        print("=======================handle_candidate_segment============================= ",campaign.target_segment)
        # Insert vào CandidateSegment
        frappe.enqueue(
            "mbw_mira.services.candidate_service.insert_candidate_segment",
            queue="default",
            timeout=300,
            candidates=candidate_ids,
            segment=campaign.target_segment,
            campaign= campaign.name,
            job_name = "insert_candidate_segment"
        )

def handle_candidate_campaign():
    candidate_campaigns = _get_active_candidate_campaigns()
    if not candidate_campaigns:
        frappe.logger("candidate_campaigns").info("[SKIP] No active candidate_campaigns found.")
        return

    for can_campaign in candidate_campaigns:
        segment = frappe.get_value("Campaign", can_campaign.campaign_id, "target_segment")
        if not segment:
            continue
        frappe.enqueue(
            "mbw_mira.campaign.background_jobs.process_next_step",
            candidate_campaign_id=can_campaign.name,
            queue="default",
            timeout=300,
            job_name = "process_next_step"
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
    campaign = kwargs.get("campaign")
    print("=======================insert_candidate_segment============================= ",segment_id)
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
        fields=["candidate_id"]
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
        frappe.publish_realtime("candidate_segment_created", doc)
    frappe.db.commit()
    count_candidate_segment(segment_id)
    frappe.enqueue(
            "mbw_mira.services.candidate_service.insert_candidate_campaign",
            queue="default",
            timeout=300,
            campaign=campaign,
            segment=segment_id,
            job_name = "insert_candidate_campaign"
        )
    
    return inserted_names


def insert_candidate_campaign(**kwargs):
    campaign_id = kwargs.get("campaign")
    segment = kwargs.get("segment")    

    print("=======================insert_candidate_campaign============================= ", campaign_id)

    if not campaign_id or not segment:
        frappe.throw(_("Both 'campaign' and 'segment' are required."))

    # lấy danh sách candidate từ segment
    candidate_ids = candidate_segment_by_campaign(segment)

    if not candidate_ids:
        frappe.msgprint(_("No candidates found in segment {}").format(segment))
        return

    # Lấy step đầu tiên trong Campaign theo campaign_id
    step = frappe.get_all(
        "CampaignStep",
        filters={"campaign": campaign_id},
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

    if not step:
        frappe.throw(_("No Campaign Step found for Campaign {}").format(campaign_id))
        return

    step = step[0]

    # Tính toán next_action_at
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
    enrolled_at = now
    current_step_order = step["step_order"] or 1

    inserted_count = 0

    for candidate_id in candidate_ids:
        if candidate_id in existing_candidate_ids:
            # Bỏ qua nếu đã tồn tại
            continue

        doc = frappe.get_doc({
            "doctype": "CandidateCampaign",
            "campaign_id": campaign_id,
            "candidate_id": candidate_id,
            "segment_id": segment,  # SỬA: segment_id đúng
            "status": status,
            "enrolled_at": enrolled_at,
            "current_step_order": current_step_order,
            "next_action_at": next_action_at,
        })
        doc.insert(ignore_permissions=True)

        # Có thể publish realtime từng bản ghi hoặc gom lại
        frappe.publish_realtime("candidate_campaign_created", doc)

        inserted_count += 1

    frappe.db.commit()

    frappe.msgprint(_("Inserted {0} candidates into Campaign {1}").format(inserted_count, campaign_id))



# lấy danh sách candidate từ CandidateSegment
def candidate_segment_by_campaign(segment) -> list[str]:
    candidate_segments = frappe.get_all(
        "CandidateSegment",
        filters={"segment_id": segment},
        fields=["candidate_id"]
    )
    return [x["candidate_id"] for x in candidate_segments]

#Tổng số lượng candidate theo segment
def count_candidate_segment(segment):
    try:
        total_candidate = frappe.db.count("CandidateSegment",filters={"segment_id":segment})
        if total_candidate and total_candidate > 0:
            frappe.db.set_value("TalentSegment",segment,"candidate_count",total_candidate)
            frappe.db.commit()
    except Exception as e:
        pass

def _get_active_campaigns():
    """
    Lấy danh sách Campaign:
    - status = ACTIVE
    - is_active = 1
    - start_date <= hôm nay
    - end_date >= hôm nay
    """
    current_date = now()  # yyyy-mm-dd
    campaigns = frappe.get_all(
        "Campaign",
        filters={
            "status": "ACTIVE",
            "is_active": 1,
            "start_date": ["<=", current_date],
            "end_date": [">=", current_date]
        },
        fields=[
            "name",
            "campaign_name",
            "start_date",
            "end_date",
            "status",
            "is_active",
            "target_segment"
        ],
        order_by="start_date asc"
    )

    return campaigns


def _get_active_candidate_campaigns() ->dict:
    """
    Lấy danh sách CandidateCampaign:
    - status = ACTIVE
    - next_action_at <= hôm nay
    """

    candidate_campaigns = frappe.get_all(
        "CandidateCampaign",
        filters={"status": "ACTIVE", "next_action_at": ["<=", now_datetime()]},
        fields=[
            "*"
        ]
    )

    return candidate_campaigns