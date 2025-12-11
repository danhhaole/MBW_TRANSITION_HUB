import json
import frappe
from frappe import _
from frappe.utils import get_datetime, get_url
import qrcode
import io
import base64
import re

def get_html_from_emailbuilder(content):
    """
    Convert EmailBuilder JSON format to HTML for email sending.
    Similar to getPreviewContent function in EmailEditor.vue
    Preserves HTML structure and converts newlines to <br> tags
    """
    if not content:
        return ''

    try:
        design = json.loads(content) if isinstance(content, str) else content

        # Handle EmailBuilder format
        if design and 'blocks' in design and isinstance(design['blocks'], list):
            preview_html = ''

            for block in design['blocks']:
                # Handle text blocks - preserve HTML content and convert newlines
                if block.get('type') == 'text' and block.get('props', {}).get('content'):
                    block_content = block['props']['content']
                    # Convert newlines to <br> tags for proper email formatting
                    block_content = block_content.replace('\n', '<br>')
                    preview_html += block_content

                # Handle nested blocks in layout columns
                if 'children' in block and isinstance(block['children'], list):
                    for column in block['children']:
                        if isinstance(column, list):
                            for child_block in column:
                                if child_block.get('type') == 'text' and child_block.get('props', {}).get('content'):
                                    child_content = child_block['props']['content']
                                    # Convert newlines to <br> tags
                                    child_content = child_content.replace('\n', '<br>')
                                    preview_html += child_content

            # Limit preview length if too long (but preserve HTML)
            if len(preview_html) > 2000:
                # For long content, truncate but keep HTML structure
                return preview_html[:2000] + '...'

            return preview_html or '<p>Email template created with EmailBuilder</p>'

        # Handle Unlayer design format (backward compatibility)
        if design and 'body' in design and 'rows' in design['body']:
            preview_html = ''  # Keep HTML instead of plain text

            for row in design['body']['rows']:
                for column in row.get('columns', []):
                    for content_item in column.get('contents', []):
                        if content_item.get('type') == 'text' and content_item.get('values', {}).get('text'):
                            item_content = content_item['values']['text']
                            # Convert newlines to <br> tags
                            item_content = item_content.replace('\n', '<br>')
                            preview_html += item_content  # Keep HTML

            if len(preview_html) > 2000:
                return preview_html[:2000] + '...'

            return preview_html or '<p>Email template created with visual editor</p>'

    except Exception as e:
        frappe.logger().warning(f'Failed to parse content as design JSON: {e}')

    # Fallback for non-JSON content - convert newlines to <br> if it looks like plain text
    if '<' in content and '>' in content:
        return content  # Already HTML, return as-is
    elif len(content) > 200:
        # Convert newlines to <br> for plain text
        return content.replace('\n', '<br>')[:200] + '...'
    else:
        # Convert newlines to <br> for plain text
        return content.replace('\n', '<br>')

def _parse_datetime(value):
    if not value:
        return None
    try:
        dt = get_datetime(value)
        if dt and hasattr(dt, 'replace'):
            return dt.replace(tzinfo=None)
        return dt
    except Exception as e:
        print(f"❌ Error parsing datetime '{value}': {e}")
        return None

@frappe.whitelist(allow_guest=True)
def create_campaign(**kwargs):
    """
    Create Campaign via ORM, allowing any valid status.
    Accepted fields:
    - campaign_name (required)
    - description
    - type (NURTURING|ATTRACTION|REFERRAL|EVENT)
    - status (DRAFT|ACTIVE|PAUSED|ARCHIVED)
    - start_date (datetime string)
    - end_date (datetime string)
    - is_active (0/1 or bool)
    - source_type (DataSource|File|Search)
    - source_file
    - source_config (JSON or string)
    - target_segment
    - job_opening (optional, ignored if field not exists)
    - select_pages (JSON string or list)
    """
    campaign_name = (kwargs.get("campaign_name") or "").strip()
    if not campaign_name:
        raise frappe.ValidationError(_("campaign_name is required"))

    allowed_status = {"DRAFT", "ACTIVE", "PAUSED", "ARCHIVED"}
    status = (kwargs.get("status") or "DRAFT").upper()
    if status not in allowed_status:
        status = "DRAFT"

    doc = frappe.new_doc("Mira Campaign")
    doc.campaign_name = campaign_name
    doc.description = kwargs.get("description") or ""
    doc.type = kwargs.get("type") or "NURTURING"
    doc.status = status
    doc.is_active = 1 if str(kwargs.get("is_active")).lower() in (
        "1",
        "true",
        "yes",
    ) else 0

    # Datetime fields - MySQL expects naive datetimes
    doc.start_date = _parse_datetime(kwargs.get("start_date"))
    doc.end_date = _parse_datetime(kwargs.get("end_date"))

    # Source info
    source_type = kwargs.get("source_type") or "Search"
    if source_type not in ("DataSource", "File", "Search"):
        source_type = "Search"
    doc.source_type = source_type
    doc.source_file = kwargs.get("source_file") or ""

    # JSON fields
    source_config = kwargs.get("source_config")
    if isinstance(source_config, str):
        try:
            source_config = json.loads(source_config)
        except Exception:
            pass
    # Nếu vẫn là list/dict, chuyển thành chuỗi JSON để lưu DB
    if isinstance(source_config, (list, dict)):
        try:
            source_config = json.dumps(source_config)
        except Exception:
            source_config = None
    doc.source_config = source_config

    select_pages = kwargs.get("select_pages")
    # Campaign DocType field may not accept list directly -> store as JSON string
    if isinstance(select_pages, (list, dict)):
        try:
            select_pages = json.dumps(select_pages)
        except Exception:
            select_pages = None
    elif isinstance(select_pages, str):
        # keep as-is (assume client already JSON-stringified)
        pass
    else:
        select_pages = None
    doc.select_pages = select_pages

    # Optional links
    doc.target_segment = kwargs.get("target_segment") or None

    # Social media fields
    doc.social_page_id = kwargs.get("social_page_id") or ""
    doc.social_page_name = kwargs.get("social_page_name") or ""
    doc.post_schedule_time = _parse_datetime(kwargs.get("post_schedule_time"))
    doc.template_content = kwargs.get("template_content") or ""

    # Handle social_media_images which could be a JSON string or list
    social_media_images = kwargs.get("social_media_images")
    if social_media_images:
        if isinstance(social_media_images, str):
            try:
                # Try to parse if it's a JSON string
                social_media_images = json.loads(social_media_images)
            except json.JSONDecodeError:
                # If not JSON, keep as is
                pass
        doc.social_media_images = json.dumps(social_media_images) if isinstance(social_media_images, (list, dict)) else social_media_images

    doc.insert(ignore_permissions=True)
    print(f"🔍 Campaign created: name={doc.name}, campaign_name={doc.campaign_name}")
    print(f"🔍 Social media info - page_id: {doc.social_page_id}, scheduled: {doc.post_schedule_time}")
    return {"status": "success", "data": doc.as_dict()}

@frappe.whitelist(allow_guest=True)
def update_campaign(**kwargs):
    """
    Update Campaign via ORM.
    Required: name (Campaign ID)
    Optional fields:
    - campaign_name, description, type, status
    - start_date, end_date, is_active
    - source_type, source_file, source_config
    - target_segment, job_opening, template_used
    - steps_count, select_pages, mira_talent_campaign
    """
    name = kwargs.get("name")
    if not name:
        raise frappe.ValidationError(_("Campaign name is required for update"))

    try:
        doc = frappe.get_doc("Mira Campaign", name)
    except frappe.DoesNotExistError:
        raise frappe.ValidationError(_("Campaign {0} not found").format(name))

    # Update basic fields
    if "campaign_name" in kwargs:
        doc.campaign_name = kwargs.get("campaign_name", "").strip()

    if "description" in kwargs:
        doc.description = kwargs.get("description", "")

    if "type" in kwargs:
        doc.type = kwargs.get("type", "NURTURING")

    if "status" in kwargs:
        allowed_status = {"DRAFT", "ACTIVE", "PAUSED", "ARCHIVED"}
        status = kwargs.get("status", "DRAFT").upper()
        if status in allowed_status:
            doc.status = status

    if "is_active" in kwargs:
        doc.is_active = 1 if str(kwargs.get("is_active")).lower() in ("1", "true", "yes") else 0

    # Datetime fields
    if "start_date" in kwargs:
        doc.start_date = _parse_datetime(kwargs.get("start_date"))

    if "end_date" in kwargs:
        doc.end_date = _parse_datetime(kwargs.get("end_date"))

    # Source info
    if "source_type" in kwargs:
        source_type = kwargs.get("source_type", "Search")
        doc.source_type = source_type

    if "source_file" in kwargs:
        doc.source_file = kwargs.get("source_file", "")

    # Handle JSON fields
    if 'source_config' in kwargs:
        source_config = kwargs['source_config']
        if isinstance(source_config, str):
            try:
                source_config = json.loads(source_config)
            except Exception:
                pass
        if isinstance(source_config, (list, dict)):
            try:
                source_config = json.dumps(source_config)
            except Exception:
                source_config = None
        doc.source_config = source_config

    if 'mira_talent_campaign' in kwargs:
        mira_talent_campaign = kwargs['mira_talent_campaign']
        if isinstance(mira_talent_campaign, (list, dict)):
            try:
                mira_talent_campaign = json.dumps(mira_talent_campaign)
            except Exception:
                mira_talent_campaign = None
        doc.mira_talent_campaign = mira_talent_campaign

    # Handle social media fields
    if 'social_page_id' in kwargs:
        doc.social_page_id = kwargs.get('social_page_id') or ''
    if 'social_page_name' in kwargs:
        doc.social_page_name = kwargs.get('social_page_name') or ''
    if 'post_schedule_time' in kwargs:
        doc.post_schedule_time = _parse_datetime(kwargs.get('post_schedule_time'))
    if 'template_content' in kwargs:
        doc.template_content = kwargs.get('template_content') or ''

    # Handle social_media_images which could be a JSON string or list
    if 'social_media_images' in kwargs:
        social_media_images = kwargs['social_media_images']
        if social_media_images:
            if isinstance(social_media_images, str):
                try:
                    # Try to parse if it's a JSON string
                    social_media_images = json.loads(social_media_images)
                except json.JSONDecodeError:
                    # If not JSON, keep as is
                    pass
            doc.social_media_images = json.dumps(social_media_images) if isinstance(social_media_images, (list, dict)) else social_media_images
        else:
            doc.social_media_images = ''

    if "select_pages" in kwargs:
        select_pages = kwargs.get("select_pages")
        if isinstance(select_pages, (list, dict)):
            try:
                select_pages = json.dumps(select_pages)
            except Exception:
                select_pages = None
        elif isinstance(select_pages, str):
            pass  # keep as-is
        else:
            select_pages = None
        doc.select_pages = select_pages

    # Optional links
    if "target_segment" in kwargs:
        doc.target_segment = kwargs.get("target_segment") or None

    if "job_opening" in kwargs:
        doc.job_opening = kwargs.get("job_opening") or None

    if "template_used" in kwargs:
        doc.template_used = kwargs.get("template_used") or None

    if "steps_count" in kwargs:
        doc.steps_count = kwargs.get("steps_count", 0)

    doc.save(ignore_permissions=True)
    print(f"🔍 Campaign updated: name={doc.name}, campaign_name={doc.campaign_name}")
    return {"status": "success", "data": doc.as_dict()}

@frappe.whitelist(allow_guest=True)
def save_campaign_step(**kwargs):
    print(f"🔍 save_campaign_step called with kwargs: {kwargs}")
    print(f"🔍 Available fields in kwargs: {list(kwargs.keys())}")
    """
    Create or update CampaignStep with datetime normalization.
    - name (optional): if provided, update existing; else insert new
    - campaign, campaign_step_name, template, image, step_order, delay_in_days,
    action_config (JSON or string), scheduled_at (datetime string)
    """
    name = kwargs.get("name")
    is_update = bool(name)

    if is_update:
        doc = frappe.get_doc("Mira Campaign Step", name)
    else:
        doc = frappe.new_doc("Mira Campaign Step")
    # Xử lý campaign field đặc biệt
    campaign_value = kwargs.get("campaign")
    if campaign_value:
        # Set campaign field (Link field đến Campaign)
        print(f"🔍 Setting campaign = {campaign_value} (Link to Campaign)")
        doc.campaign = campaign_value

        # Lấy campaign_name từ Campaign để set vào campaign_step_name
        try:
            campaign_doc = frappe.get_doc("Mira Campaign", campaign_value)
            campaign_name = campaign_doc.campaign_name
            print(f"🔍 Setting campaign_step_name = {campaign_name} (from Campaign {campaign_value})")
            doc.campaign_step_name = campaign_name
        except Exception as e:
            print(f"🔍 Error getting campaign_name: {e}")
            # Fallback: sử dụng campaign_step_name từ kwargs
            doc.campaign_step_name = kwargs.get("campaign_step_name", campaign_value)
    else:
        # Không có campaign, chỉ set campaign_step_name
        doc.campaign_step_name = kwargs.get("campaign_step_name")

    # assign other simple fields
    print(f"🔍 Assigning other fields to CampaignStep...")
    for field in [
        "template",
        "image",
        "delay_in_days",
    ]:
        if field in kwargs:
            print(f"🔍 Setting {field} = {kwargs.get(field)}")
            setattr(doc, field, kwargs.get(field))

    # Auto-increment step_order nếu không được cung cấp hợp lệ
    provided_step_order = kwargs.get("step_order")
    if is_update:
        # Update: tôn trọng step_order nếu người dùng gửi
        if provided_step_order is not None:
            try:
                doc.step_order = int(provided_step_order)
            except Exception:
                pass
    else:
        # Create mới: nếu không gửi hoặc không hợp lệ, tự gán = max(step_order) + 1 trong Campaign
        next_order = None
        try:
            if provided_step_order is not None and int(provided_step_order) > 0:
                next_order = int(provided_step_order)
            elif campaign_value:
                max_rows = frappe.get_all(
                    "Mira Campaign Step",
                    filters={"campaign": campaign_value},
                    fields=["max(step_order) as max_order"],
                )
                max_order = 0
                if max_rows and isinstance(max_rows, list):
                    row = max_rows[0] or {}
                    max_order = (row.get("max_order") or 0) or 0
                next_order = int(max_order) + 1
        except Exception as e:
            print(f"🔍 Failed to compute next step_order: {e}")
            next_order = None
        if next_order:
            doc.step_order = next_order

    # action_config may be JSON

    # action_config may be JSON
    action_config = kwargs.get("action_config")
    if isinstance(action_config, str):
        try:
            action_config = json.loads(action_config)
        except Exception:
            pass
    doc.action_config = action_config

    # normalize scheduled_at
    scheduled = _parse_datetime(kwargs.get("scheduled_at"))
    doc.scheduled_at = scheduled

    if is_update:
        doc.save()
    else:
        doc.insert(ignore_permissions=True)

    # KHÔNG cập nhật Campaign nữa - chỉ lưu scheduled_at vào CampaignStep
    print(f"✅ CampaignStep saved with scheduled_at: {scheduled}")

    print(f"🔍 CampaignStep saved: name={doc.name}, campaign_step_name={doc.campaign_step_name}")
    return {"status": "success", "data": doc.as_dict()}

@frappe.whitelist(allow_guest=True)
def test_auto_post_scheduler(**kwargs):
    """
    Test API để chạy auto post scheduler thủ công
    """
    try:
        from mbw_mira.schedulers.post_to_facebook_action import run
        print("🧪 Running auto post scheduler manually...")
        run()
        return {"status": "success", "message": "Auto post scheduler completed"}
    except Exception as e:
        print(f"❌ Error running auto post scheduler: {e}")
        return {"status": "error", "message": str(e)}

@frappe.whitelist(allow_guest=True)
def dev_seed_autopost_test(**kwargs):
    """
    Seed dữ liệu test tự động share bài:
    Inputs:
    - page_id: external_account_id hợp lệ có trong
      External Connection Account
    - job_title (optional)
    - campaign_name (optional)
    - message (optional) - nội dung post
    - minutes_from_now (optional, default 0) - lệch phút so với
      hiện tại cho start/scheduled
    """
    from datetime import datetime, timedelta
    import json

    page_id = kwargs.get("page_id")
    if not page_id:
        raise frappe.ValidationError(_("page_id is required"))

    job_title = kwargs.get("job_title", "Senior React Developer")
    campaign_name = kwargs.get("campaign_name", f"Test Campaign {datetime.now().strftime('%Y%m%d_%H%M%S')}")
    message = kwargs.get("message", f"🚀 Tuyển dụng {job_title} - Cơ hội nghề nghiệp hấp dẫn!")
    minutes_from_now = int(kwargs.get("minutes_from_now", 0))

    now = datetime.now()
    scheduled_time = now + timedelta(minutes=minutes_from_now)

    # 1) Tạo JobOpening
    job_doc = frappe.new_doc("Mira Job Opening")
    job_doc.job_title = job_title
    job_doc.job_code = f"TEST-{datetime.now().strftime('%Y%m%d%H%M%S')}"
    job_doc.description = f"Mô tả công việc {job_title}"
    job_doc.requirements = f"Yêu cầu cho vị trí {job_title}"
    job_doc.benefits = f"Quyền lợi khi làm {job_title}"
    job_doc.is_active = 1
    job_doc.insert(ignore_permissions=True)

    # 2) Tạo Campaign
    campaign_doc = frappe.new_doc("Mira Campaign")
    campaign_doc.campaign_name = campaign_name
    campaign_doc.description = f"Campaign test auto post cho {job_title}"
    campaign_doc.type = "ATTRACTION"
    campaign_doc.status = "ACTIVE"
    campaign_doc.is_active = 1
    campaign_doc.source_type = "DataSource"
    campaign_doc.start_date = now
    campaign_doc.end_date = now + timedelta(days=30)
    campaign_doc.job_opening = job_doc.name
    campaign_doc.select_pages = json.dumps([{"page_id": page_id}])
    campaign_doc.insert(ignore_permissions=True)

    # 3) Tạo CampaignStep với scheduled_at
    step_doc = frappe.new_doc("Mira Campaign Step")
    step_doc.campaign = campaign_doc.name
    step_doc.campaign_step_name = f"Post {job_title}"
    step_doc.step_order = 1
    step_doc.action_type = "SEND_EMAIL"
    step_doc.template = message
    step_doc.scheduled_at = scheduled_time
    step_doc.delay_in_days = 0
    step_doc.insert(ignore_permissions=True)

    return {
        "status": "success",
        "data": {
            "job_opening": job_doc.name,
            "campaign": campaign_doc.name,
            "campaign_step": step_doc.name,
            "scheduled_at": scheduled_time.isoformat(),
            "message": f"Created test data: JobOpening {job_doc.name}, Campaign {campaign_doc.name}, CampaignStep {step_doc.name} scheduled at {scheduled_time}"
        }
    }

@frappe.whitelist(allow_guest=True)
def bulk_create_campaign_records(**kwargs):
    """
    Bulk create campaign records for better performance.
    Args:
        records: List of record objects to create
        doctype: Target doctype (Mira Talent Campaign or Mira Contact Campaign)
    """
    records = kwargs.get('records', [])
    doctype = kwargs.get('doctype')

    if not records:
        return {"status": "error", "message": "No records provided"}

    if not doctype:
        return {"status": "error", "message": "Doctype is required"}

    if doctype not in ['Mira Talent Campaign', 'Mira Contact Campaign']:
        return {"status": "error", "message": "Invalid doctype"}

    try:
        created_records = []

        # Process records in batches to avoid memory issues
        batch_size = 100
        total_records = len(records)

        for i in range(0, total_records, batch_size):
            batch = records[i:i + batch_size]

            for record_data in batch:
                try:
                    # Remove doctype from record_data if it exists
                    if 'doctype' in record_data:
                        del record_data['doctype']

                    # Create new document
                    doc = frappe.new_doc(doctype)

                    # Set fields from record_data
                    for field, value in record_data.items():
                        if hasattr(doc, field):
                            setattr(doc, field, value)

                    # Insert the document
                    doc.insert(ignore_permissions=True)
                    created_records.append(doc.name)

                except Exception as record_error:
                    print(f"Error creating record: {record_error}")
                    # Continue with next record instead of failing entire batch
                    continue

            # Commit after each batch
            frappe.db.commit()

        return {
            "status": "success",
            "message": f"Successfully created {len(created_records)} records",
            "created_count": len(created_records),
            "total_requested": total_records,
            "created_records": created_records
        }

    except Exception as e:
        frappe.db.rollback()
        print(f"Bulk insert error: {e}")
        return {
            "status": "error",
            "message": f"Bulk insert failed: {str(e)}"
        }


@frappe.whitelist()
def get_job_qrcode(campaign_id, target_url=None):
    """
    Generate QR code for campaign job opening

    Args:
        campaign_id: ID of the campaign
        target_url: Optional custom URL (for now using fixed URL)

    Returns:
        Dict with url and base64 image
    """
    try:
        # Verify campaign exists
        if not frappe.db.exists("Mira Campaign", campaign_id):
            return {"status": "error", "message": "Campaign not found"}

        # Use provided target_url or generate default
        if not target_url:
            # Get site URL and build job URL
            site_url = frappe.utils.get_url()
            target_url = f"{site_url}/mbw_mira/jobs/tuyen-lap-trinh-vien-python"



        # Generate QR code
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        qr.add_data(target_url)
        qr.make(fit=True)

        # Create QR code image
        img = qr.make_image(fill_color="black", back_color="white")

        # Convert to base64
        buffer = io.BytesIO()
        img.save(buffer, format='PNG')
        img_str = base64.b64encode(buffer.getvalue()).decode()

        return {
            "status": "success",
            "url": target_url,
            "image": f"data:image/png;base64,{img_str}"
        }

    except Exception as e:
        frappe.log_error(f"QR Code generation error: {str(e)}")
        return {
            "status": "error",
            "message": f"Failed to generate QR code: {str(e)}"
        }

@frappe.whitelist()
def delete_campaign_with_links(campaign_name, force_delete=False):
    """
    Delete campaign and handle linked documents

    Args:
        campaign_name: Name of the campaign to delete
        force_delete: If True, will delete linked documents first

    Returns:
        Dict with status and message
    """
    try:
        # Check if campaign exists
        if not frappe.db.exists("Mira Campaign", campaign_name):
            return {
                "status": "error",
                "message": f"Campaign {campaign_name} not found"
            }

        # Get linked documents
        linked_docs = []

        # Check for linked Mira Flow
        flows = frappe.get_all(
            "Mira Flow",
            filters={"campaign_id": campaign_name},
            fields=["name", "title"]
        )
        if flows:
            linked_docs.extend([{"doctype": "Mira Flow", "name": f.name, "title": f.title} for f in flows])

        # Check for linked Talent Campaign records
        talent_campaigns = frappe.get_all(
            "Mira Talent Campaign",
            filters={"campaign_id": campaign_name},
            fields=["name"]
        )
        if talent_campaigns:
            linked_docs.extend([{"doctype": "Mira Talent Campaign", "name": tc.name} for tc in talent_campaigns])

        # If there are linked documents and force_delete is False, return the list
        if linked_docs and not force_delete:
            return {
                "status": "error",
                "error_type": "LinkExistsError",
                "message": f"Cannot delete campaign because it has {len(linked_docs)} linked document(s)",
                "linked_documents": linked_docs
            }

        # If force_delete is True, delete all linked documents first
        if force_delete and linked_docs:
            deleted_count = 0
            for doc_info in linked_docs:
                try:
                    frappe.delete_doc(doc_info["doctype"], doc_info["name"], ignore_permissions=True, force=True)
                    deleted_count += 1
                except Exception as e:
                    print(f"Error deleting {doc_info['doctype']} {doc_info['name']}: {e}")

            frappe.db.commit()
            print(f"Deleted {deleted_count} linked documents")

        # Now delete the campaign
        frappe.delete_doc("Mira Campaign", campaign_name, ignore_permissions=True, force=True)
        frappe.db.commit()

        return {
            "status": "success",
            "message": f"Campaign {campaign_name} deleted successfully",
            "deleted_links": len(linked_docs) if force_delete else 0
        }

    except Exception as e:
        frappe.db.rollback()
        error_msg = str(e)
        print(f"Error deleting campaign: {error_msg}")

        return {
            "status": "error",
            "message": f"Failed to delete campaign: {error_msg}"
        }

@frappe.whitelist()
def delete_sequence_with_links(sequence_name, force_delete=False):
    """
    Delete sequence and handle linked documents

    Args:
        sequence_name: Name of the sequence to delete
        force_delete: If True, will delete linked documents first

    Returns:
        Dict with status and message
    """
    try:
        # Check if sequence exists
        if not frappe.db.exists("Mira Sequence", sequence_name):
            return {
                "status": "error",
                "message": f"Sequence {sequence_name} not found"
            }

        # Get linked documents
        linked_docs = []

        # Check for linked Mira Flow
        flows = frappe.get_all(
            "Mira Flow",
            filters={"sequence_id": sequence_name},
            fields=["name", "title"]
        )
        if flows:
            linked_docs.extend([{"doctype": "Mira Flow", "name": f.name, "title": f.title} for f in flows])

        # If there are linked documents and force_delete is False, return the list
        if linked_docs and not force_delete:
            return {
                "status": "error",
                "error_type": "LinkExistsError",
                "message": f"Cannot delete sequence because it has {len(linked_docs)} linked document(s)",
                "linked_documents": linked_docs
            }

        # If force_delete is True, delete all linked documents first
        if force_delete and linked_docs:
            deleted_count = 0
            for doc_info in linked_docs:
                try:
                    frappe.delete_doc(doc_info["doctype"], doc_info["name"], ignore_permissions=True, force=True)
                    deleted_count += 1
                except Exception as e:
                    print(f"Error deleting {doc_info['doctype']} {doc_info['name']}: {e}")

            frappe.db.commit()
            print(f"Deleted {deleted_count} linked documents")

        # Now delete the sequence
        frappe.delete_doc("Mira Sequence", sequence_name, ignore_permissions=True, force=True)
        frappe.db.commit()

        return {
            "status": "success",
            "message": f"Sequence {sequence_name} deleted successfully",
            "deleted_links": len(linked_docs) if force_delete else 0
        }

    except Exception as e:
        frappe.db.rollback()
        error_msg = str(e)
        print(f"Error deleting sequence: {error_msg}")

        return {
            "status": "error",
            "message": f"Failed to delete sequence: {error_msg}"
        }


@frappe.whitelist()
def get_pool_candidate_count(config_data):
    """
    Get candidate count from pool/segment configuration

    Args:
        config_data: Pool configuration object

    Returns:
        {"count": 123}
    """
    try:
        if isinstance(config_data, str):
            config_data = json.loads(config_data)

        count = 0

        if config_data.get('segment_id'):
            # Get count from Mira Talent Pool by segment_id
            count = frappe.db.count('Mira Talent Pool', {
                'segment_id': config_data.get('segment_id')
            })
        elif config_data.get('filters'):
            # Apply custom filters to Mira Talent
            filters = config_data.get('filters', {})
            count = frappe.db.count('Mira Talent', filters)
        else:
            # Default: count all talents
            count = frappe.db.count('Mira Talent')

        return {"count": count}

    except Exception as e:
        frappe.log_error(f"Error getting pool candidate count: {str(e)}")
        return {"count": 0, "error": str(e)}


@frappe.whitelist()
def get_conditions_candidate_count(doctype, conditions):
    """
    Get candidate count from filter conditions

    Args:
        doctype: Target doctype (e.g., 'Mira Talent')
        conditions: List of conditions in format [["field", "operator", "value"], ...]

    Returns:
        {"count": 123}
    """
    try:
        if isinstance(conditions, str):
            conditions = json.loads(conditions)

        if not conditions or len(conditions) == 0:
            # No conditions, return total count
            count = frappe.db.count(doctype)
            return {"count": count}

        # Build filters from conditions
        filters = {}

        for condition in conditions:
            # Handle both list format and dict format
            if isinstance(condition, list) and len(condition) >= 3:
                field = condition[0]
                operator = condition[1]
                value = condition[2]
            elif isinstance(condition, dict):
                field = condition.get('field')
                operator = condition.get('operator', '=')
                value = condition.get('value')
            else:
                continue

            if not field:
                continue

            # Map operators to Frappe filter format
            # Special handling for comma-separated fields (skills, tags, etc.)
            if field in ['skills', 'tags', 'soft_skills'] and operator in ['=', '==']:
                # Use LIKE for comma-separated fields
                filters[field] = ['like', f'%{value}%']
            elif operator in ['=', '==']:
                filters[field] = value
            elif operator in ['!=', '<>']:
                filters[field] = ['!=', value]
            elif operator == 'in':
                filters[field] = ['in', value]
            elif operator == 'not in':
                filters[field] = ['not in', value]
            elif operator in ['like', 'LIKE']:
                filters[field] = ['like', f'%{value}%']
            elif operator == '>':
                filters[field] = ['>', value]
            elif operator == '<':
                filters[field] = ['<', value]
            elif operator == '>=':
                filters[field] = ['>=', value]
            elif operator == '<=':
                filters[field] = ['<=', value]
            else:
                filters[field] = value

        count = frappe.db.count(doctype, filters)

        return {"count": count}

    except Exception as e:
        frappe.log_error(f"Error getting conditions candidate count: {str(e)}")
        return {"count": 0, "error": str(e)}


@frappe.whitelist()
def get_combined_candidate_count(config_data, conditions):
    """
    Get candidate count combining both segment and conditions

    Args:
        config_data: Pool/segment configuration (optional)
        conditions: Filter conditions (optional)

    Returns:
        {"count": 123}
    """
    try:
        if isinstance(config_data, str):
            config_data = json.loads(config_data) if config_data else {}
        if isinstance(conditions, str):
            conditions = json.loads(conditions) if conditions else []

        # Start with base filters
        filters = {}
        talent_ids = None

        # Step 1: Get talent IDs from segment if provided
        if config_data and len(config_data) > 0:
            if config_data.get('selectedSegment'):
                # Get talents from Mira Talent Pool by segment_id
                pool_records = frappe.get_all('Mira Talent Pool',
                    filters={'segment_id': config_data.get('selectedSegment')},
                    pluck='talent_id'
                )
                talent_ids = set(pool_records)
            elif config_data.get('filters'):
                # Apply segment filters
                segment_filters = config_data.get('filters', {})
                filters.update(segment_filters)

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
                    field = condition.get('field')
                    operator = condition.get('operator', '=')
                    value = condition.get('value')
                else:
                    continue

                if not field:
                    continue

                # Map operators to Frappe format
                # Special handling for comma-separated fields (skills, tags, etc.)
                if field in ['skills', 'tags', 'soft_skills'] and operator in ['=', '==']:
                    # Use LIKE for comma-separated fields
                    filters[field] = ['like', f'%{value}%']
                elif operator in ['=', '==']:
                    filters[field] = value
                elif operator in ['!=', '<>']:
                    filters[field] = ['!=', value]
                elif operator == 'in':
                    filters[field] = ['in', value]
                elif operator == 'not in':
                    filters[field] = ['not in', value]
                elif operator in ['like', 'LIKE']:
                    filters[field] = ['like', f'%{value}%']
                elif operator == '>':
                    filters[field] = ['>', value]
                elif operator == '<':
                    filters[field] = ['<', value]
                elif operator == '>=':
                    filters[field] = ['>=', value]
                elif operator == '<=':
                    filters[field] = ['<=', value]
                else:
                    filters[field] = value

        # Step 3: Combine segment IDs with condition filters
        if talent_ids is not None:
            # Filter by talent IDs from segment
            filters['name'] = ['in', list(talent_ids)]

        # Step 4: Count
        count = frappe.db.count('Mira Talent', filters)

        return {"count": count}

    except Exception as e:
        frappe.log_error(f"Error getting combined candidate count: {str(e)}")
        return {"count": 0, "error": str(e)}


@frappe.whitelist()
def create_talent_campaigns_from_pool(campaign_id):
	"""
	Tạo Mira Talent Campaign records từ Pool/Segment của Campaign

	Args:
		campaign_id: ID của campaign

	Returns:
		dict: {"success": True/False, "created": số records được tạo}
	"""
	logger = frappe.logger("campaign")

	try:
		# Lấy campaign
		campaign = frappe.get_doc("Mira Campaign", campaign_id)
		logger.info(f"🚀 Creating talent campaigns from pool for: {campaign.name}")
		logger.info(f"📋 Campaign target_pool: {campaign.target_pool}, source_config: {campaign.source_config}")

		# Lấy talent IDs từ pool/segment
		talent_ids = []

		# Nếu có target_pool - đây là segment_id
		if campaign.target_pool:
			logger.info(f"🔍 Looking for talents in segment: {campaign.target_pool}")
			pool_records = frappe.get_all(
				"Mira Talent Pool",
				filters={"segment_id": campaign.target_pool},
				fields=["talent_id"],
				limit_page_length=0
			)
			talent_ids = [r["talent_id"] for r in pool_records]
			logger.info(f"📊 Found {len(talent_ids)} talents from segment: {campaign.target_pool}")

		# Nếu có source_config (từ conditions)
		if not talent_ids and campaign.source_config:
			try:
				source_config = json.loads(campaign.source_config) if isinstance(campaign.source_config, str) else campaign.source_config
				logger.info(f"📋 Parsing source_config: {source_config}")

				# Nếu có selectedSegment
				if source_config.get("selectedSegment"):
					logger.info(f"🔍 Looking for talents in selectedSegment: {source_config.get('selectedSegment')}")
					pool_records = frappe.get_all(
						"Mira Talent Pool",
						filters={"segment_id": source_config.get("selectedSegment")},
						fields=["talent_id"],
						limit_page_length=0
					)
					talent_ids = [r["talent_id"] for r in pool_records]
					logger.info(f"📊 Found {len(talent_ids)} talents from segment: {source_config.get('selectedSegment')}")
			except Exception as e:
				logger.warning(f"⚠️ Could not parse source_config: {str(e)}")

		if not talent_ids:
			logger.warning(f"⚠️ No talents found for campaign {campaign_id}")
			logger.warning(f"⚠️ target_pool: {campaign.target_pool}, source_config: {campaign.source_config}")
			return {"success": False, "message": "No talents found", "created": 0}

		# Kiểm tra xem đã có Mira Talent Campaign nào chưa
		existing_count = frappe.db.count(
			"Mira Talent Campaign",
			{"campaign_id": campaign_id}
		)

		if existing_count > 0:
			logger.info(f"ℹ️ Campaign already has {existing_count} talent campaigns")
			return {"success": True, "message": f"Campaign already has {existing_count} talent campaigns", "created": 0}

		# Tạo Mira Talent Campaign cho mỗi talent
		created_count = 0
		for talent_id in talent_ids:
			try:
				# Kiểm tra talent có tồn tại không
				if not frappe.db.exists("Mira Talent", talent_id):
					logger.warning(f"⚠️ Talent {talent_id} not found")
					continue

				# Tạo Mira Talent Campaign
				tc = frappe.get_doc({
					"doctype": "Mira Talent Campaign",
					"campaign_id": campaign_id,
					"talent_id": talent_id,
					"status": "ACTIVE"  # Valid status: ACTIVE, PAUSED, COMPLETED, CANCELLED
				})
				tc.insert(ignore_permissions=True)
				created_count += 1

			except Exception as e:
				logger.error(f"❌ Error creating talent campaign for {talent_id}: {str(e)}")
				continue

		frappe.db.commit()
		logger.info(f"✅ Created {created_count} talent campaigns")

		return {
			"success": True,
			"created": created_count,
			"message": f"Created {created_count} talent campaigns"
		}

	except Exception as e:
		logger.error(f"❌ Error in create_talent_campaigns_from_pool: {str(e)}")
		frappe.log_error(f"Error in create_talent_campaigns_from_pool: {str(e)}")
		return {"success": False, "error": str(e), "created": 0}


@frappe.whitelist()
def send_campaign_welcome_emails(campaign_id):
	"""
	Gửi email chào mừng cho tất cả ứng viên trong campaign khi campaign chuyển sang ACTIVE

	Args:
		campaign_id: ID của campaign

	Returns:
		dict: {"success": True/False, "sent": số email gửi thành công, "failed": số email thất bại}
	"""
	from mbw_mira.utils.email import send_email

	logger = frappe.logger("campaign")

	try:
		# Lấy campaign
		campaign = frappe.get_doc("Mira Campaign", campaign_id)
		logger.info(f"🚀 Starting email send for campaign: {campaign.name}")

		# Bước 1: Tạo Mira Talent Campaign từ Pool nếu chưa có
		talent_campaign_count = frappe.db.count(
			"Mira Talent Campaign",
			{"campaign_id": campaign_id}
		)

		if talent_campaign_count == 0:
			logger.info(f"📝 Creating talent campaigns from pool...")
			create_result = create_talent_campaigns_from_pool(campaign_id)
			if create_result.get("created", 0) > 0:
				logger.info(f"✅ Created {create_result['created']} talent campaigns")
			else:
				logger.warning(f"⚠️ No talent campaigns created")

		# Lấy tất cả Mira Campaign Social của campaign này
		campaign_socials = frappe.get_all(
			"Mira Campaign Social",
			filters={"campaign_id": campaign_id},
			fields=["name", "subject", "template_content", "block_content"]
		)

		if not campaign_socials:
			logger.warning(f"⚠️ No campaign socials found for campaign {campaign_id}")
			return {"success": False, "message": "No campaign socials found", "sent": 0, "failed": 0}

		logger.info(f"📊 Found {len(campaign_socials)} campaign socials")

		# Lấy tất cả talent campaign của campaign này
		talent_campaigns = frappe.get_all(
			"Mira Talent Campaign",
			filters={"campaign_id": campaign_id},
			fields=["name", "talent_id"]
		)

		if not talent_campaigns:
			logger.warning(f"⚠️ No talent campaigns found for campaign {campaign_id}")
			return {"success": False, "message": "No talent campaigns found", "sent": 0, "failed": 0}

		logger.info(f"📋 Found {len(talent_campaigns)} talent campaigns")

		sent_count = 0
		failed_count = 0

		# Gửi email trực tiếp cho mỗi talent campaign
		for tc in talent_campaigns:
			try:
				talent_id = tc["talent_id"]

				# Lấy talent profile
				talent = frappe.get_doc("Mira Talent", talent_id)
				logger.info(f"📧 Processing talent: {talent.name} ({talent.email})")

				# Kiểm tra email hợp lệ
				if not talent.email:
					logger.warning(f"⚠️ Talent {talent.name} has no email")
					failed_count += 1
					continue

				if talent.email_opt_out:
					logger.warning(f"⚠️ Talent {talent.name} has unsubscribed")
					failed_count += 1
					continue

				# Lấy campaign social đầu tiên
				email_social = campaign_socials[0]

				logger.info(f"📧 Using campaign social: {email_social['name']}")

				# Lấy subject và content từ fields
				subject = email_social.get("subject", "Chào mừng")
				# Ưu tiên template_content (HTML đã render), sau đó block_content (JSON render sẵn)
				content = email_social.get("template_content") or email_social.get("block_content", "")
				# Chuẩn hoá đường dẫn ảnh để không dùng localhost dev server
				try:
					if content:
						site_url = get_url()
						# /files/... -> {site_url}/files/...
						content = content.replace('src="/files/', f'src="{site_url}/files/')
						# Bất kỳ URL localhost dev nào -> domain hireos.fastwork.vn
						content = content.replace('http://localhost:8080/', 'https://hireos.fastwork.vn/')
				except Exception:
					pass

				# Log lại các ảnh trong content để debug
				try:
					if content:
						import re
						img_tags = re.findall(r"<img[^>]+>", content)
						logger.info(f"🖼 Email HTML image tags for {talent.email}: {img_tags}")
						srcs = re.findall(r"src=\"([^\"]+)\"", content)
						logger.info(f"🖼 Email image src list for {talent.email}: {srcs}")
				except Exception as e:
					logger.warning(f"⚠️ Failed to log image tags: {e}")

				sender = ""  # Sẽ dùng default sender từ Email Account

				if not subject or not content:
					logger.warning(f"⚠️ Missing email content for {talent.name}")
					logger.warning(f"⚠️ Subject: {subject}, Content length: {len(content) if content else 0}")
					failed_count += 1
					continue

				# Gửi email
				try:
					print(f"\n===== CAMPAIGN EMAIL DEBUG START =====")
					print(f"DEBUG: Sending email to {talent.email}")
					print(f"DEBUG: Content type before conversion: {type(content)}")
					print(f"DEBUG: Content starts with JSON: {content.startswith('{') if content else False}")

					# Convert EmailBuilder JSON to HTML if needed
					if content and (content.startswith('{') or content.startswith('[')):
						print("DEBUG: Content is JSON, converting to HTML...")
						print(f"DEBUG: Raw JSON content preview: {content[:200]}...")
						# If content is JSON, convert it to HTML using get_html_from_emailbuilder
						content = get_html_from_emailbuilder(content)
						print(f"DEBUG: Converted to HTML length: {len(content)}")
						print(f"DEBUG: Converted HTML preview: {content[:200]}...")
					else:
						print("DEBUG: Content is already HTML, using as-is")
						print(f"DEBUG: HTML content preview: {content[:200]}...")

					# Remove problematic inline styles that cause width limitation
					if content:
						import re
						# Remove style="margin:0px auto;max-width:600px;" and variations
						content = re.sub(r'style="[^"]*margin:\s*0px\s*auto;[^"]*max-width:\s*600px;[^"]*"', 'style="width:100%;margin:0;"', content)
						content = re.sub(r'style="[^"]*max-width:\s*600px;[^"]*margin:\s*0px\s*auto;[^"]*"', 'style="width:100%;margin:0;"', content)
						content = re.sub(r'style="[^"]*max-width:\s*600px;[^"]*"', 'style="width:100%;"', content)
						content = re.sub(r'style="[^"]*margin:\s*0px\s*auto;[^"]*"', 'style="margin:0;"', content)
						print("DEBUG: Removed width-limiting inline styles")


					# Process content to ensure proper line breaks
					if content:
						# Check if content is plain text (no HTML tags)
						if not ('<' in content and '>' in content):
							print("DEBUG: Content is plain text, converting line breaks to HTML")
							# Replace double newlines with <p> tags for proper paragraph spacing
							# content = content.replace('\n', '<p>')
							# Wrap in paragraph tags if not already wrapped
							if not content.strip().startswith('<p>') and not content.strip().startswith('<div>'):
								content = f'<p>{content}</p>'
						else:
							print("DEBUG: Content already has HTML, ensuring proper line break formatting")
							# For HTML content, ensure line breaks are preserved
							# Convert any remaining newlines to <br> tags if they're not already in HTML
							if not ('<br>' in content or '<br/>' in content or '<p>' in content):
								content = content.replace('\n', '<p>')
						print("DEBUG: Processed line breaks in content")

					# Check if content already has HTML tags
					if content and ('<' in content and '>' in content):
						print("DEBUG: Content already has HTML tags")
					else:
						print("DEBUG: Content does not have HTML tags")

					# Check if content is already a complete HTML email
					if content and (content.strip().startswith('<!DOCTYPE') or
									content.strip().startswith('<html>') or
									'<title>' in content or
									'<!--[if' in content):
						print("DEBUG: Content is already a complete HTML email, adding CSS for better formatting...")
						# Add CSS to improve formatting for inline content
						css_fix = """
<style>
	div[style*="font-family:Arial"] {
		line-height: 1.6 !important;
		margin-bottom: 8px !important;
	}
	div[style*="font-family:Arial"] img {
		margin-right: 8px !important;
		vertical-align: middle !important;
	}
	div[style*="font-family:Arial"] br {
		line-height: 1.6 !important;
	}
	p {
		margin-bottom: 8px !important;
		line-height: 1.6 !important;
		word-wrap: break-word !important;
	}
	br {
		line-height: 1.6 !important;
		display: block !important;
		content: "" !important;
		margin-bottom: 4px !important;
	}
	/* Remove all empty paragraphs with any content */
	p:empty,
	p:empty,
	p:not(:has(img, span, div, a, strong, em, b, i, u, table, td, tr)),
	p[style*="margin:1em 0!important"]:empty,
	p[style*="margin:1em 0!important"]:not(:has(img, span, div, a, strong, em, b, i, u, table, td, tr)) {
		display: none !important;
		height: 0 !important;
		margin: 0 !important;
		padding: 0 !important;
	}
	/* Also hide paragraphs with only whitespace */
	p:has(> :empty),
	p:has(> text():empty),
	p:has(> text():only-child):not(:has(> text():not(:empty)) {
		display: none !important;
		height: 0 !important;
		margin: 0 !important;
		padding: 0 !important;
	}
</style>
"""
						# Insert CSS after <head> tag
						if '<head>' in content:
							content = content.replace('<head>', f'<head>{css_fix}')
						elif '<head>' in content.lower():
							content = content.replace('<head>', f'<head>{css_fix}')
						print("DEBUG: CSS formatting added to complete HTML email")
						# Don't wrap complete HTML emails
					elif content and not content.strip().startswith('<!DOCTYPE') and not content.strip().startswith('<html'):
						print("DEBUG: Wrapping content in HTML structure...")
						content = f"""
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{subject}</title>
    <style>
        body {{
            font-family: Arial, sans-serif;
            line-height: 1.6;
            color: #333;
            max-width: 600px;
            margin: 0 auto;
            padding: 20px;
            background-color: #f4f4f4;
        }}
        .container {{
            background-color: white;
            padding: 30px;
            border-radius: 8px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }}
        /* Proper spacing for paragraphs and line breaks */
        p {{
            margin-bottom: 8px !important;
            line-height: 1.6 !important;
            word-wrap: break-word !important;
        }}
        br {{
            line-height: 1.6 !important;
            display: block !important;
            content: "" !important;
            margin-bottom: 4px !important;
        }}
        div[style*="font-family:Arial"] {{
            line-height: 1.6 !important;
            margin-bottom: 8px !important;
            word-wrap: break-word !important;
        }}
        div[style*="font-family:Arial"] img {{
            margin-right: 8px !important;
            vertical-align: middle !important;
        }}
        div[style*="font-family:Arial"] br {{
            line-height: 1.6 !important;
            display: block !important;
            content: "" !important;
            margin-bottom: 4px !important;
        }}
        /* Remove empty paragraphs */
        p:empty {{
            display: none !important;
        }}
    </style>
</head>
<body>
    <div class="container">
        {content}
    </div>
</body>
</html>
"""
						print("DEBUG: Content wrapped in HTML structure")

					print(f"DEBUG: Final content length: {len(content)}")
					print(f"DEBUG: Final content starts with <!DOCTYPE: {content.startswith('<!DOCTYPE')}")

					result = send_email(
						recipients=[talent.email],
						subject=subject,
						content=content,
						sender=sender,
						as_html=True,
						debug=True,
						inline_css=True
					)
					print(f"DEBUG: Email send result: {result}")
					print("===== CAMPAIGN EMAIL DEBUG END =====\n")
					sent_count += 1
					logger.info(f"✅ Email sent to {talent.email}")
				except Exception as e:
					failed_count += 1
					logger.error(f"❌ Error sending email to {talent.email}: {str(e)}")

			except Exception as e:
				failed_count += 1
				logger.error(f"❌ Error processing talent {tc.get('talent_id')}: {str(e)}")
				frappe.log_error(f"Error processing talent {tc.get('talent_id')}: {str(e)}")

		logger.info(f"📊 Email send complete: {sent_count} sent, {failed_count} failed")

		return {
			"success": True,
			"sent": sent_count,
			"failed": failed_count,
			"message": f"Sent {sent_count} emails, {failed_count} failed"
		}

	except Exception as e:
		logger.error(f"❌ Error in send_campaign_welcome_emails: {str(e)}")
		import traceback
		logger.error(traceback.format_exc())
		frappe.log_error(f"Error in send_campaign_welcome_emails: {str(e)}")
		return {"success": False, "error": str(e), "sent": 0, "failed": 0}
