import frappe
import json
from frappe.utils import now_datetime, add_days, add_to_date

from mbw_mira.api.external_connections import share_job_posting
from mbw_mira.utils import send_email_action, send_sms_job


def process_email_action(action_name):
    """
    Worker: thực hiện SEND_EMAIL action
    """
    logger = frappe.logger()
    logger.info(f"[EMAIL] ========== START process_email_action ==========")
    logger.info(f"[EMAIL] Action name: {action_name}")
    
    now = now_datetime()
    action = frappe.db.get_value(
        "Mira Action",
        action_name,
        ["name", "talent_campaign_id", "campaign_social"],
        as_dict=1,
    )
    
    if not action:
        logger.error(f"[EMAIL] ❌ Action {action_name} not found!")
        return False
    
    logger.info(f"[EMAIL] Action found: {action.name}")
    logger.info(f"[EMAIL] Talent Campaign ID: {action.talent_campaign_id}")
    logger.info(f"[EMAIL] Campaign Social: {action.campaign_social}")
    
    try:
        # Lấy talentprofile
        talent_id = frappe.db.get_value(
            "Mira Talent Campaign", action.talent_campaign_id, "talent_id"
        )
        
        logger.info(f"[EMAIL] Talent ID: {talent_id}")
        
        if talent_id:
            logger.info(f"[EMAIL] Calling send_email_action({talent_id}, {action_name})...")
            send_email_action(talent_id, action_name)
            logger.info(f"[EMAIL] ✅ send_email_action completed")
            
            frappe.publish_realtime(
                "action_executed",
                message={
                    "talent_campaign": action.talent_campaign_id,
                    "action": action_name,
                },
            )
        else:
            logger.warning(f"[EMAIL] ⚠️ No talent_id found for talent_campaign_id: {action.talent_campaign_id}")
        
        logger.info(f"[EMAIL] ========== END process_email_action ==========")
        return True

    except Exception as e:
        logger.error(f"[EMAIL] ❌ Error processing SEND_EMAIL action {action.name}: {e}")
        logger.error(f"[EMAIL] Traceback: {frappe.get_traceback()}")
        frappe.log_error(f"Error processing SEND_EMAIL action {action.name}: {e}")
        return True


def process_sms_action(action_name):
    """
    Worker: thực hiện SEND_SMS action
    """
    now = now_datetime()
    action = frappe.db.get_value(
        "Mira Action",
        action_name,
        ["name", "talent_campaign_id", "campaign_step"],
        as_dict=1,
    )
    try:

        # TODO: Thực hiện gửi SMS ở đây
        # Ví dụ: gọi API SMS gateway
        talent_id = frappe.db.get_value(
            "Mira Talent Campaign", action.talent_campaign_id, "talent_id"
        )
        send_sms_job(talent_id, action_name, action.campaign_step)
        frappe.publish_realtime(
            "action_executed",
            message={
                "talent_campaign": action.talent_campaign_id,
                "action": action_name,
            },
        )
        return True

    except Exception as e:
        frappe.log_error(f"Error processing SEND_SMS action {action.name}: {e}")
        return True


def post_facebook_action(campaign_id, social):
    campaign = frappe.get_doc("Mira Campaign", campaign_id)
    share_job_posting(
        connection_id=social.external_connection,
        campaign_id=campaign_id,
        ladipage_url=campaign.ladipage_url,
        image_url=social.social_media_images,
        message=social.template_content,
        social_id=social.name,
    )


def check_pending_action(action_name):
    """
    Worker: cảnh báo Action pending quá lâu
    """
    action = frappe.get_doc("Mira Action", action_name)
    step_type = frappe.get_value(
        "Mira Campaign Step", action.campaign_step, "action_type"
    )
    try:
        return step_type

        # Optionally: gửi email/notification cảnh báo
        # frappe.sendmail(...)

    except Exception as e:
        frappe.log_error(f"Error while checking pending Action {action.name}: {e}")
        return True


def enroll_talent_campaign(social):
    # Lấy danh sách talent từ campaign (talent pool và filter)
    talent_profiles = _get_combined_talent(social.campaign_id)
    count = 0
    try:
        print("count", len(talent_profiles))
        if talent_profiles:
            for profile in talent_profiles:
                _create_talent_campaign(social, profile)

                count += 1
        # frappe.publish_realtime('enroll_talent_campaign', message={'campaign': campaign})
        return count
    except Exception as e:
        frappe.log_error(frappe.get_traceback())
        return count


def _get_combined_talent(campaign_id):
    try:
        campaign = frappe.get_doc("Mira Campaign", campaign_id)
        if isinstance(campaign.condition_filter, str):
            conditions = (
                json.loads(campaign.condition_filter)
                if campaign.condition_filter
                else []
            )

        # Start with base filters
        filters = {}
        talent_ids = None

        # Step 1: Get talent IDs from segment if provided
        if campaign.target_pool:
            # Get talents from Mira Talent Pool by segment_id
            pool_records = frappe.get_all(
                "Mira Talent Pool",
                filters={"segment_id": campaign.target_pool},
                pluck="talent_id",
            )
            talent_ids = set(pool_records)

        # Step 2: Add condition filters
        # Conditions format: [["field", "operator", "value"], ...]
        if conditions and len(conditions) > 0:
            for condition in conditions:
                # Handle both list format and dict format
                if isinstance(condition, list) and len(condition) >= 3:
                    field = condition[0]
                    operator = condition[1]
                    value = condition[2]
                elif isinstance(condition, dict):
                    field = condition.get("field")
                    operator = condition.get("operator", "=")
                    value = condition.get("value")
                else:
                    continue

                if not field:
                    continue

                # Map operators to Frappe format
                # Special handling for comma-separated fields (skills, tags, etc.)
                if field in ["skills", "tags", "soft_skills"] and operator in [
                    "=",
                    "==",
                ]:
                    # Use LIKE for comma-separated fields
                    filters[field] = ["like", f"%{value}%"]
                elif operator in ["=", "=="]:
                    filters[field] = value
                elif operator in ["!=", "<>"]:
                    filters[field] = ["!=", value]
                elif operator == "in":
                    filters[field] = ["in", value]
                elif operator == "not in":
                    filters[field] = ["not in", value]
                elif operator in ["like", "LIKE"]:
                    filters[field] = ["like", f"%{value}%"]
                elif operator == ">":
                    filters[field] = [">", value]
                elif operator == "<":
                    filters[field] = ["<", value]
                elif operator == ">=":
                    filters[field] = [">=", value]
                elif operator == "<=":
                    filters[field] = ["<=", value]
                else:
                    filters[field] = value

        # Step 3: Combine segment IDs with condition filters
        if talent_ids is not None:
            # Filter by talent IDs from segment
            filters["name"] = ["in", list(talent_ids)]

        # Step 4: Count
        talents = frappe.db.get_list("Mira Talent", filters=filters, fields=["*"])

        return talents
    except Exception as e:
        return []


def _create_talent_campaign(social, profile):
    """
    Tạo mới Mira Talent Campaign, chỉ set current_step_order nếu có
    """
    try:
        if social.post_schedule_time:
            next_action_at = add_days(social.post_schedule_time, 0)
        if not _check_exists(social.campaign_id, profile.name) and profile.name:
            doc = frappe.get_doc(
                {
                    "doctype": "Mira Talent Campaign",
                    "campaign_id": social.campaign_id,
                    "talent_id": profile.name,
                    "campaign_social": social.name,
                    "status": "ACTIVE",
                    "enrolled_at": now_datetime(),
                    "current_step_order": 1,
                    "next_action_at": next_action_at,
                }
            )
            doc.insert(ignore_permissions=True)
            frappe.db.commit()
            return doc.name
        else:
            return None
    except Exception as e:
        frappe.log_error(f"talent_profiles {e}")
        return None


def _check_exists(campaign_id, talent_id):
    talent_campaign_exists = frappe.db.exists(
        "Mira Talent Campaign", {"campaign_id": campaign_id, "talent_id": talent_id}
    )
    if talent_campaign_exists:
        return True
    else:
        return False
