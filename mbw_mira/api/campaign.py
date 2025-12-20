import json
import frappe
from frappe import _
from frappe.utils import get_datetime, get_url
import qrcode
import io
import base64
import re
from mbw_mira.utils.birthday_utils import check_birthday_in_pool

@frappe.whitelist()
def check_pool_has_birthday(pool_name):
    """
    Check if the pool has any talent with upcoming birthday.
    This is used by the frontend to conditionally show/hide Birthday triggers.
    """
    if not pool_name:
        return {"has_birthday": False, "logs": []}

    has_match, debug_logs = check_birthday_in_pool(pool_name)
    return {
        "has_birthday": has_match,
        "logs": debug_logs
    }

@frappe.whitelist()
def send_test_email(recipient, subject, content):
    """
    Send a test email with the provided content.
    Used by ActionEditor options to verify email configuration.
    """
    if not recipient:
        frappe.throw(_("Recipient email is required"))

    if not subject:
        frappe.throw(_("Subject is required"))

    try:
        from mbw_mira.utils.email import send_email

        # Replace localhost URLs and relative paths with production domain
        if content:
            import re
            # Replace absolute localhost URLs
            content = content.replace('http://localhost:8080', 'https://hireos.fastwork.vn')
            content = content.replace('http://localhost:8000', 'https://hireos.fastwork.vn')
            content = content.replace('http://127.0.0.1:8080', 'https://hireos.fastwork.vn')
            content = content.replace('http://127.0.0.1:8000', 'https://hireos.fastwork.vn')

            # Replace relative paths like /files/... with full domain
            content = re.sub(r'src="/files/', 'src="https://hireos.fastwork.vn/files/', content)
            content = re.sub(r'href="/files/', 'href="https://hireos.fastwork.vn/files/', content)

        # Determine if content is HTML
        as_html = True
        # Simple heuristic: if it doesn't look like HTML, treat as plain text converted to HTML
        if content and not ('<' in content and '>' in content):
             if '\n' in content:
                 content = content.replace('\n', '<br>')

        send_email(
            recipients=[recipient],
            subject=f"{subject}",
            content=content,
            as_html=as_html
        )

        return {"status": "success", "message": f"Test email sent to {recipient}"}
    except Exception as e:
        frappe.log_error(f"Test email failed: {e}")
        return {"status": "error", "message": f"Failed to send email: {str(e)}"}

@frappe.whitelist()
def run_birthday_test_for_pool(pool_name, subject, content):
    """
    Run a test birthday check for the given pool and send the provided email content
    to any eligible candidates (whose birthday matches logic).

    Args:
        pool_name (str): The talent pool ID/Name
        subject (str): Email subject from the action editor
        content (str): Email HTML content from the action editor
    """
    if not pool_name:
        return {"status": "error", "message": "Target Pool is required"}

    from mbw_mira.utils.birthday_utils import check_birthday
    from mbw_mira.utils.email import send_email
    from frappe.utils import nowdate

    # Find talents in pool - get ALL fields for template replacement
    if frappe.db.exists("DocType", "Mira Talent Pool"):
        talents = frappe.db.sql("""
            SELECT t.*
            FROM `tabMira Talent` t
            INNER JOIN `tabMira Talent Pool` tp ON tp.talent_id = t.name
            WHERE tp.segment_id = %s
        """, (pool_name,), as_dict=True)
    else:
        # Fallback for dev env without Talent Pool doctype
        talents = frappe.db.sql("SELECT * FROM `tabMira Talent` WHERE date_of_birth IS NOT NULL", as_dict=True)

    sent_count = 0
    logs = []

    for t in talents:
        # Check eligibility
        is_eligible = check_birthday(t)
        if is_eligible and t.get('email'):
            try:
                # Prepare context for template variables
                context = t.copy()
                context['today'] = nowdate()

                # Convert EmailBuilder JSON to HTML if needed
                msg_content = get_html_from_emailbuilder(content) if content else content

                # Replace template variables - convert all values to string
                for key, value in context.items():
                    if value is not None:
                        str_value = str(value)
                        # Replace both {{ key }} and {{key}} formats
                        msg_content = msg_content.replace('{{ ' + key + ' }}', str_value)
                        msg_content = msg_content.replace('{{' + key + '}}', str_value)

                # Determine as_html
                as_html = True
                if msg_content and not ('<' in msg_content and '>' in msg_content):
                     if '\n' in msg_content:
                         msg_content = msg_content.replace('\n', '<br>')

                send_email(
                    recipients=[t.get('email')],
                    subject=subject,
                    content=msg_content,
                    as_html=as_html
                )
                sent_count += 1
                logs.append(f"Sent to {t.get('email')} (DOB: {t.get('date_of_birth')})")
            except Exception as e:
                logs.append(f"Failed to send to {t.get('email')}: {e}")
        else:
             # Log why not sent
             if not is_eligible:
                 logs.append(f"  > Skipped {t.get('email')} (DOB: {t.get('date_of_birth')}) - Not today.")
             elif not t.get('email'):
                 logs.append(f"  > Skipped {t.get('name')} - No Email.")

    return {
        "status": "success",
        "sent_count": sent_count,
        "logs": logs,
        "message": f"Test run complete. Sent {sent_count} emails to eligible talents."
    }

def get_test_email_template():
    """
    Returns a default test email template in EmailBuilder JSON format
    """
    return {
        "blocks": [
            {
                "id": "test_block_1",
                "type": "text",
                "props": {
                    "content": "Xin chào {{ full_name }},\n\nĐây là email kiểm tra từ hệ thống.\n\nThông tin chi tiết:\n- Email: {{ email }}\n- Ngày gửi: {{ today }}\n\nTrân trọng,\nBan quản trị",
                    "textType": "paragraph",
                    "fontFamily": "Arial, sans-serif",
                    "fontSize": 14,
                    "color": "#333333",
                    "lineHeight": 1.6,
                    "textAlign": "left"
                }
            }
        ],
        "emailSettings": {
            "backgroundColor": "#ffffff",
            "contentWidth": 600,
            "contentAlign": "left",
            "fontFamily": "Arial, sans-serif"
        }
    }

@frappe.whitelist()
def run_mass_email_for_pool(pool_name, subject, content=None, **kwargs):
    """
    Send email to ALL talents in the pool (for testing non-birthday triggers).
    If no content is provided, uses a default test template.
    """
    if not pool_name:
        return {"status": "error", "message": "Target Pool is required"}

    from mbw_mira.utils.email import send_email
    from frappe.utils import nowdate
    import json

    # Find talents in pool
    if frappe.db.exists("DocType", "Mira Talent Pool"):
        talents = frappe.db.sql("""
            SELECT t.*
            FROM `tabMira Talent` t
            INNER JOIN `tabMira Talent Pool` tp ON tp.talent_id = t.name
            WHERE tp.segment_id = %s
        """, (pool_name,), as_dict=True)
    else:
        # Fallback for dev env without Talent Pool doctype
        talents = frappe.db.sql("SELECT * FROM `tabMira Talent` WHERE email IS NOT NULL", as_dict=True)

    sent_count = 0
    logs = []

    # Use provided content or default test template
    email_content = content if content else json.dumps(get_test_email_template())

    for t in talents:
        if t.get('email'):
            try:
                # Prepare context for template variables
                context = t.copy()
                context['today'] = nowdate()

                # Convert EmailBuilder JSON to HTML with context
                msg_content = get_html_from_emailbuilder(email_content)

                # Replace template variables - convert all values to string
                for key, value in context.items():
                    if value is not None:
                        # Convert value to string for replacement
                        str_value = str(value)
                        # Replace both {{ key }} and {{key}} formats
                        msg_content = msg_content.replace('{{ ' + key + ' }}', str_value)
                        msg_content = msg_content.replace('{{' + key + '}}', str_value)

                # Send the email
                send_email(
                    recipients=[t.get('email')],
                    subject=f"{subject}",
                    content=msg_content,
                    as_html=True
                )
                sent_count += 1
                logs.append(f"Sent to {t.get('email')}")
            except Exception as e:
                logs.append(f"Failed to send to {t.get('email')}: {str(e)}")

    return {
        "status": "success",
        "sent_count": sent_count,
        "logs": logs,
        "message": f"Test email sent to {sent_count} pool members."
    }

@frappe.whitelist()
def test_check_no_email_open_trigger(test_mode=False):
    """
    Test API để chạy thủ công job kiểm tra email không được mở quá N ngày.
    Dùng để test logic trước khi chạy scheduled job tự động.

    Args:
        test_mode: Nếu True, dùng MINUTES thay vì DAYS (để test trên localhost)
                   Ví dụ: days_without_click=5 sẽ là 5 PHÚT thay vì 5 NGÀY

    Returns:
        dict: Kết quả test với số campaigns đã xử lý và số talents đã trigger

    Usage:
        # Test với 5 phút (localhost)
        frappe.call('mbw_mira.api.campaign.test_check_no_email_open_trigger', {'test_mode': True})

        # Test với ngày thật (production)
        frappe.call('mbw_mira.api.campaign.test_check_no_email_open_trigger', {'test_mode': False})
    """
    try:
        from mbw_mira.utils.email_tracking import check_no_email_open_trigger

        # Convert string to boolean
        if isinstance(test_mode, str):
            test_mode = test_mode.lower() in ('true', '1', 'yes')

        result = check_no_email_open_trigger(test_mode=test_mode)

        mode_text = "TEST MODE (minutes)" if test_mode else "PRODUCTION MODE (days)"

        return {
            "status": "success",
            "message": f"Test completed successfully in {mode_text}",
            "data": result,
            "test_mode": test_mode
        }
    except Exception as e:
        frappe.log_error(f"Test check_no_email_open_trigger failed: {e}")
        return {
            "status": "error",
            "message": f"Test failed: {str(e)}"
        }



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
                # Handle text blocks - wrap in paragraph tags for proper spacing
                if block.get('type') == 'text' and block.get('props', {}).get('content'):
                    block_content = block['props']['content']
                    # Convert newlines to <br> tags for proper email formatting
                    block_content = block_content.replace('\n', '<br>')
                    # Wrap in paragraph tag để xuống dòng giữa các đoạn
                    preview_html += '<p>' + block_content + '</p>'

                # Handle nested blocks in layout columns
                if 'children' in block and isinstance(block['children'], list):
                    for column in block['children']:
                        if isinstance(column, list):
                            for child_block in column:
                                if child_block.get('type') == 'text' and child_block.get('props', {}).get('content'):
                                    child_content = child_block['props']['content']
                                    # Convert newlines to <br> tags
                                    child_content = child_content.replace('\n', '<br>')
                                    # Wrap in paragraph tag
                                    preview_html += '<p>' + child_content + '</p>'

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

    # Map target_segment (old) or target_pool (new) to target_pool field
    doc.target_pool = kwargs.get("target_pool") or kwargs.get("target_segment") or None

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
    # doc.target_pool is already set above


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
    if "target_pool" in kwargs:
        doc.target_pool = kwargs.get("target_pool") or None
    elif "target_segment" in kwargs:
        doc.target_pool = kwargs.get("target_segment") or None

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


def strip_mjml_tables(html_content):
	"""
	Remove MJML-generated nested table structure and ALL styling constraints.
	MJML creates complex <table><tr><td> structures that don't format well in emails.
	This function removes tables, max-width, padding, and centering constraints.

	Args:
		html_content (str): HTML content that may contain MJML tables

	Returns:
		str: Cleaned HTML or plain text
	"""
	import re

	if not html_content:
		return html_content

	try:
		cleaned = html_content

		# Remove ALL table-related tags (MJML creates nested table bloat)
		cleaned = re.sub(r'</?table[^>]*>', '', cleaned, flags=re.IGNORECASE)
		cleaned = re.sub(r'</?tbody[^>]*>', '', cleaned, flags=re.IGNORECASE)
		cleaned = re.sub(r'</?tr[^>]*>', '', cleaned, flags=re.IGNORECASE)
		cleaned = re.sub(r'</?td[^>]*>', '', cleaned, flags=re.IGNORECASE)
		cleaned = re.sub(r'</?th[^>]*>', '', cleaned, flags=re.IGNORECASE)

		frappe.log_error(f"🔥 Removed MJML table structure (before: {len(html_content)}, after: {len(cleaned)})")

		# 🔥 AGGRESSIVE: Remove ALL inline styling constraints that limit email width/padding
		# Remove max-width constraints (both CSS and attributes)
		cleaned = re.sub(r'\bmax-width\s*:\s*[^;]+;?', '', cleaned, flags=re.IGNORECASE)
		cleaned = re.sub(r'\s+max-width=["\']?[^"\'>\s]+["\']?', '', cleaned, flags=re.IGNORECASE)

		# Remove padding attributes/styles (user wants NO padding)
		cleaned = re.sub(r'\bpadding\s*:\s*[^;]+;?', '', cleaned, flags=re.IGNORECASE)
		cleaned = re.sub(r'\s+padding=["\']?[^"\'>\s]+["\']?', '', cleaned, flags=re.IGNORECASE)

		# Remove margin constraints that center content
		cleaned = re.sub(r'\bmargin\s*:\s*[^;]*auto[^;]*;?', 'margin:0;', cleaned, flags=re.IGNORECASE)
		cleaned = re.sub(r'\s+margin=["\']?[^"\'>\s]+["\']?', '', cleaned, flags=re.IGNORECASE)

		# Force width to 100%
		cleaned = re.sub(r'\bwidth\s*:\s*[0-9]+px', 'width:100%', cleaned, flags=re.IGNORECASE)

		# Remove ALL align="center" attributes
		cleaned = re.sub(r'\s+align\s*=\s*["\']?center["\']?', ' align="left"', cleaned, flags=re.IGNORECASE)

		# Override centering in CSS
		cleaned = re.sub(r'text-align\s*:\s*center', 'text-align:left !important', cleaned, flags=re.IGNORECASE)

		# Add aggressive CSS override to force clean layout
		aggressive_css = '''<style type="text/css">
body, table, tr, td, div, p, span, h1, h2, h3, h4, h5, h6 {
  margin: 0 !important;
  padding: 0 !important;
  text-align: left !important;
  width: 100% !important;
  max-width: none !important;
}
.email-container, .email-body {
  background-color: #ffffff !important;
  width: 100% !important;
  max-width: none !important;
  margin: 0 !important;
  padding: 0 !important;
}
</style>'''

		# Insert style tag at beginning or replace existing one
		if '<style' in cleaned.lower():
			# Replace first style tag with aggressive version
			cleaned = re.sub(r'<style[^>]*>.*?</style>', aggressive_css, cleaned, flags=re.IGNORECASE | re.DOTALL)
		elif '<head' in cleaned.lower():
			# Insert after <head
			cleaned = re.sub(r'<head', f'<head>{aggressive_css}', cleaned, flags=re.IGNORECASE)
		else:
			# Prepend to content
			cleaned = aggressive_css + '\n' + cleaned

		frappe.log_error(f"� CLEANED: Removed all padding, max-width, and centering from email HTML")
		return cleaned

	except Exception as e:
		frappe.log_error(f"⚠️ Error stripping MJML tables: {e}")
		return html_content


def ensure_clean_html(html_content):
	"""
	Ensure HTML is clean - add DOCTYPE, body, and proper styling if missing.
	This helps with email client compatibility.
	"""
	if not html_content:
		return html_content

	# If it's already a full HTML document (has <!DOCTYPE), use as-is with cleanup
	if '<!DOCTYPE' in html_content:
		return strip_mjml_tables(html_content)

	# If it's just HTML fragments, wrap in proper document
	if not html_content.strip().startswith('<html'):
		# It's a fragment - wrap it properly
		cleaned = strip_mjml_tables(html_content)
		wrapped = f'''<!DOCTYPE html>
<html>
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <style type="text/css">
    body {{ margin: 0 !important; padding: 0 !important; background-color: #ffffff; text-align: left !important; }}
    div, p, span, table, td {{ text-align: left !important; margin: 0 !important; }}
  </style>
</head>
<body>
{cleaned}
</body>
</html>'''
		return wrapped

	return strip_mjml_tables(html_content)


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

		# Print rõ ràng ra console
		print("\n")
		print("=" * 80)
		print(f"🚀 EMAIL SEND PROCESS FOR CAMPAIGN: {campaign.name}")
		print("=" * 80)
		print(f"Campaign ID: {campaign_id}")
		print(f"Campaign Type: {campaign.type}")
		print(f"Target Pool: {campaign.target_pool}")
		print("=" * 80)
		print("\n")

		logger.info(f"🚀 Starting email send for campaign: {campaign.name}")
		logger.info(f"📋 Campaign details - ID: {campaign_id}, Type: {campaign.type}, Target Pool: {campaign.target_pool}")

		# Bước 1: Tạo Mira Talent Campaign từ Pool nếu chưa có
		talent_campaign_count = frappe.db.count(
			"Mira Talent Campaign",
			{"campaign_id": campaign_id}
		)
		logger.info(f"📊 Existing Talent Campaigns for this campaign: {talent_campaign_count}")

		print(f"\n📊 STEP 1: Check Mira Talent Campaigns")
		print(f"   Existing count: {talent_campaign_count}")

		if talent_campaign_count == 0:
			logger.info(f"📝 Creating talent campaigns from pool...")
			create_result = create_talent_campaigns_from_pool(campaign_id)
			if create_result.get("created", 0) > 0:
				logger.info(f"✅ Created {create_result['created']} talent campaigns")
				print(f"   ✅ Created {create_result['created']} new talent campaigns")
			else:
				logger.warning(f"⚠️ No talent campaigns created")
				print(f"   ⚠️ No talent campaigns created from pool!")
		else:
			logger.info(f"✅ Already have {talent_campaign_count} talent campaigns")
			print(f"   ✅ Already have {talent_campaign_count} talent campaigns\n")

		# Initializes counters
		total_sent = 0
		total_failed = 0
		messages = []

		# --- PART 1: Check for Birthday Triggers (Always run this check) ---
		birthday_flows = frappe.get_all("Mira Flow", filters={"campaign_id": campaign_id, "status": "Active"}, fields=["name"])
		logger.info(f"🎂 Found {len(birthday_flows)} Active flows for campaign")
		has_birthday_trigger = False

		for flow_info in birthday_flows:
			try:
				flow = frappe.get_doc("Mira Flow", flow_info.name)
				logger.info(f"📍 Checking flow: {flow.name}, has triggers: {bool(flow.trigger_id)}")
				if not flow.trigger_id:
					logger.info(f"⏭️ Flow {flow.name} has no triggers, skipping")
					continue

				for trigger in flow.trigger_id:
					logger.info(f"   📌 Trigger type: {trigger.trigger_type}")
					if trigger.trigger_type == 'ON_BIRTHDAY':
						has_birthday_trigger = True
						logger.info(f"🎂 Found Birthday Trigger in flow: {flow.name}. Executing birthday check...")

						for action in flow.action_id:
							logger.info(f"      🔧 Action type: {action.action_type}")
							if action.action_type == 'EMAIL':
								try:
									params = json.loads(action.action_parameters) if isinstance(action.action_parameters, str) else action.action_parameters
									subject = params.get('email_subject') or "Happy Birthday"
									content = params.get('content') or params.get('email_content') or ""
									logger.info(f"      📧 Email Subject: {subject[:50]}...")

									# Run birthday check
									from mbw_mira.api.campaign import run_birthday_test_for_pool
									target_pool = campaign.target_pool
									logger.info(f"      🎯 Target pool: {target_pool}")
									if target_pool:
										res = run_birthday_test_for_pool(target_pool, subject, content)
										sent = res.get("sent_count", 0)
										total_sent += sent
										logger.info(f"      ✅ Birthday check result: Sent {sent}")
										if sent > 0:
											messages.append(f"Birthday: Sent {sent}")
										else:
											messages.append("Birthday: No eligible candidates today")
									else:
										logger.warning(f"      ⚠️ No target pool found!")
										messages.append("Birthday: No target pool")
								except Exception as e:
									logger.error(f"❌ Error executing birthday action: {e}")
									total_failed += 1
						break # One birthday trigger per flow is enough
			except Exception as e:
				logger.error(f"❌ Error processing flow {flow_info.name}: {e}")

		if has_birthday_trigger:
			logger.info("✅ Birthday trigger processing complete")

		# --- PART 2: Check for Campaign Socials (Welcome Emails) ---
		print(f"\n[DEBUG] About to query Campaign Socials...")
		print(f"[DEBUG] Query filter: campaign_id = {campaign_id}")

		campaign_socials = frappe.get_all(
			"Mira Campaign Social",
			filters={"campaign_id": campaign_id},
			fields=["name", "subject", "template_content", "block_content"]
		)

		print(f"[DEBUG] Query returned: {type(campaign_socials)} with {len(campaign_socials) if campaign_socials else 0} items")

		logger.info(f"🔍 Looking for Campaign Socials with campaign_id: {campaign_id}")

		print(f"\n📧 STEP 2: Check Campaign Socials")
		print(f"   Query: campaign_id = {campaign_id}")
		print(f"   Found: {len(campaign_socials)} campaign socials")

		if campaign_socials:
			print(f"   ✅ Campaign Socials Found:")
			for idx, social in enumerate(campaign_socials, 1):
				subject = social.get('subject') or 'N/A'
				subject_preview = subject[:50] if subject and subject != 'N/A' else 'N/A'
				print(f"      [{idx}] {social.get('name')} - Subject: {subject_preview}")
				print(f"          Has template_content: {bool(social.get('template_content'))}")
				print(f"          Has block_content: {bool(social.get('block_content'))}")
		else:
			print(f"   ⚠️ NO Campaign Socials found!")

		if campaign_socials:
			logger.info(f"📊 Found {len(campaign_socials)} campaign socials. Processing welcome emails...")

			# Get talent campaigns
			talent_campaigns = frappe.get_all(
				"Mira Talent Campaign",
				filters={"campaign_id": campaign_id},
				fields=["name", "talent_id"]
			)

			# Debug: Check all Mira Talent Campaigns
			all_tc = frappe.get_all("Mira Talent Campaign", fields=["name", "campaign_id", "talent_id"])
			print(f"\n   DEBUG: Total Mira Talent Campaigns in DB: {len(all_tc)}")

			logger.info(f"👥 Found {len(talent_campaigns)} talent campaigns for this campaign")

			print(f"\n👥 STEP 3: Get Talent Campaigns")
			print(f"   Query Filter: campaign_id = {campaign_id}")
			print(f"   Found: {len(talent_campaigns)} talent campaigns")

			if len(talent_campaigns) == 0 and len(all_tc) > 0:
				print(f"   ⚠️ WARNING: No talent campaigns found with filter, but {len(all_tc)} exist in DB")
				print(f"   Checking first 5 records in DB:")
				for idx, tc in enumerate(all_tc[:5], 1):
					print(f"      [{idx}] {tc.get('name')} - campaign_id: {tc.get('campaign_id')}, talent_id: {tc.get('talent_id')}")

			if talent_campaigns:
				print(f"\n📅 STEP 4: Process Talents")
				print(f"   Campaign Type: {campaign.type}")
				print(f"   Today's date: {frappe.utils.today()}")

				# Determine if we should check birthday (only for ATTRACTION campaigns)
				should_check_birthday = (campaign.type == "ATTRACTION")
				print(f"   Should check birthday: {should_check_birthday}")

				for idx, tc in enumerate(talent_campaigns, 1):
					try:
						talent_id = tc["talent_id"]
						talent = frappe.get_doc("Mira Talent", talent_id)

						print(f"   [{idx}/{len(talent_campaigns)}] Talent: {talent.name}")
						print(f"       Email: {talent.email}")
						print(f"       DOB: {talent.date_of_birth}")
						print(f"       Email Opt-out: {talent.email_opt_out}")

						logger.info(f"   [{idx}] Processing talent: {talent.name}")
						logger.info(f"       Email: {talent.email}, DOB: {talent.date_of_birth}, OptOut: {talent.email_opt_out}")

						if not talent.email:
							print(f"       ❌ SKIP - No email")
							logger.warning(f"       ⚠️ No email found, SKIPPING")
							continue

						if talent.email_opt_out:
							print(f"       ❌ SKIP - Email opt-out enabled")
							logger.warning(f"       ⚠️ Email opt-out enabled, SKIPPING")
							continue

						# ✅ CHECK BIRTHDAY - ONLY FOR ATTRACTION CAMPAIGNS
						if should_check_birthday:
							# For ATTRACTION campaigns: only send if birthday is today
							if not talent.date_of_birth:
								print(f"       ❌ SKIP - No date of birth")
								logger.warning(f"       ⚠️ No date of birth, SKIPPING")
								continue

							try:
								# Manually check birthday - compare month and day
								from frappe.utils import getdate, nowdate
								today_date = getdate(nowdate())
								dob_date = getdate(talent.date_of_birth)
								is_birthday = (dob_date.month == today_date.month and dob_date.day == today_date.day)

								print(f"       📅 DOB: {dob_date}, Today: {today_date}, Is Birthday: {is_birthday}")
								logger.info(f"       📅 DOB: {dob_date}, Today: {today_date}, Is Birthday: {is_birthday}")
							except Exception as check_error:
								print(f"       ❌ Birthday check failed: {str(check_error)}")
								logger.error(f"       ❌ Birthday check failed: {str(check_error)}")
								is_birthday = False

							if not is_birthday:
								print(f"       ⏭️ SKIP - Not birthday today")
								logger.info(f"       ⏭️ Not birthday today, SKIPPING")
								continue

							print(f"       🎉 BIRTHDAY FOUND - Sending birthday email!")
							subject = "🎂 Chúc mừng sinh nhật!"
							use_birthday_template = True
						else:
							# For NURTURING campaigns: send to all talents
							print(f"       ✅ Processing for NURTURING campaign (no birthday check)")
							use_birthday_template = False
							subject = None

						print(f"       ✅ Ready to send email")
						logger.info(f"       ✅ Ready to send email")

						# Get email subject and content
						if use_birthday_template:
							# Use birthday template for ATTRACTION
							email_subject = "🎂 Chúc mừng sinh nhật!"

							# Create beautiful birthday email content
							birthday_content = f"""
<html>
<head>
	<style>
		body {{ font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; margin: 0; padding: 0; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); }}
		.container {{ max-width: 600px; margin: 0 auto; padding: 20px; }}
		.card {{ background: white; border-radius: 12px; box-shadow: 0 10px 30px rgba(0,0,0,0.2); overflow: hidden; }}
		.header {{ background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white;  text-align: center; }}
		.header h1 {{ margin: 0; font-size: 32px; font-weight: 700; }}
		.header p {{ margin: 10px 0 0 0; font-size: 16px; opacity: 0.9; }}
		.content {{ padding: 40px; text-align: center; }}
		.emoji {{ font-size: 60px; margin-bottom: 20px; }}
		.greeting {{ font-size: 24px; color: #333; font-weight: 600; margin-bottom: 15px; }}
		.message {{ font-size: 16px; color: #666; line-height: 1.6; margin: 20px 0; }}
		.cta {{ display: inline-block; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 12px 30px; text-decoration: none; border-radius: 6px; font-weight: 600 }}
		.footer {{ text-align: center; font-size: 12px; color: #999; }}
	</style>
</head>
<body>
	<div class="container">
		<div class="card">
			<div class="header">
				<div class="emoji">🎂🎉🎊</div>
				<h1>Chúc mừng sinh nhật</h1>
				<p>Một ngày đặc biệt dành cho bạn</p>
			</div>
			<div class="content">
				<p class="greeting">Xin chào {talent.name},</p>
				<div class="message">
					<p>Hôm nay là ngày đặc biệt của bạn! 🎈</p>
					<p>Chúng tôi xin gửi lời chúc mừng sinh nhật chân thành nhất. Hy vọng ngày này sẽ mang đến cho bạn những khoảnh khắc tuyệt vời, những tràng cười vui vẻ và những điều kỳ diệu.</p>
					<p>Cảm ơn bạn vì đã là một phần của chúng tôi. Chúng tôi trân trọng sự hợp tác và tin tưởng của bạn.</p>
					<p>Chúc bạn một năm mới tràn đầy sức khỏe, hạnh phúc và thành công! 🌟</p>
				</div>
			</div>
			<div class="footer">
				<p>© 2025 MOBIWORK. All rights reserved.</p>
			</div>
		</div>
	</div>
</body>
</html>
"""
							email_content = birthday_content
							email_type = "Birthday"
						else:
							# For NURTURING: use Campaign Social content
							email_social = campaign_socials[0] if campaign_socials else None
							if not email_social:
								print(f"       ⏭️ SKIP - No campaign social found")
								logger.warning(f"       ⚠️ No campaign social found, SKIPPING")
								continue

							email_subject = email_social.get("subject", "Chào mừng")
							email_content = email_social.get("template_content") or email_social.get("block_content", "")
							email_type = "Welcome"

							if not email_subject or not email_content:
								print(f"       ⏭️ SKIP - No subject or content in social")
								logger.warning(f"       ⚠️ No subject or content in social, SKIPPING")
								continue

						logger.info(f"       📧 Using {email_type} email template")
						logger.info(f"       📝 Subject: {email_subject if email_subject else 'N/A'}")
						logger.info(f"       📄 Content length: {len(email_content) if email_content else 0}")

						print(f"       📧 {email_type} Email Template")
						print(f"       📝 Subject: {email_subject if email_subject else 'N/A'}")
						print(f"       📄 Content length: {len(email_content) if email_content else 0}")

						# Queue email (or send directly)
						# Here we send directly as per original code
						if email_subject:
							logger.info(f"       🚀 SENDING EMAIL to {talent.email}")
							logger.info(f"          Subject: {email_subject}")
							logger.info(f"          Content length: {len(email_content) if email_content else 0} chars")
							print(f"       🚀 ATTEMPTING TO SEND EMAIL...")
							print(f"          To: {talent.email}")
							print(f"          Subject: {email_subject}")
							print(f"          Content length: {len(email_content) if email_content else 0}")
							try:
								print(f"       [BEFORE SEND] Recipients: {[talent.email]}")
								print(f"       [BEFORE SEND] Subject: {email_subject}")
								print(f"       [BEFORE SEND] Content type: {type(email_content).__name__}")
								print(f"       [BEFORE SEND] as_html: True")

								# Create email tracking for nurturing campaigns
								tracking_result = None
								if campaign.type == "NURTURING":
									try:
										from mbw_mira.api.email_tracking import create_email_tracking
										tracking_result = create_email_tracking(
											talent_id=talent.name,
											campaign_id=campaign_id,
											email_subject=email_subject,
											email_content=email_content if email_content else email_subject
										)
										print(f"       📊 Email tracking created: {tracking_result.get('tracking_id')}")
									except Exception as tracking_error:
										print(f"       ⚠️ Email tracking creation failed: {str(tracking_error)}")

								# Add tracking link to email content if tracking was created
								final_content = email_content if email_content else f"<p>{email_subject}</p>"
								if tracking_result and tracking_result.get("tracking_url"):
									if use_birthday_template:
										# For plain text birthday emails, add simple tracking
										final_content += f"\n\n---\nClick here to confirm receipt: {tracking_result['tracking_url']}"
									else:
										# For HTML emails, add invisible tracking pixel
										final_content += f'<img src="{tracking_result["tracking_url"]}" width="1" height="1" style="display:none;" />'

								result = send_email(
									recipients=[talent.email],
									subject=email_subject,
									content=final_content,
									as_html=True
								)

								print(f"       [AFTER SEND] Result: {result}")
								logger.info(f"       ✅ EMAIL SENT SUCCESS to {talent.email}")
								print(f"       ✅ EMAIL SENT SUCCESSFULLY")
								total_sent += 1
							except Exception as send_error:
								logger.error(f"       ❌ EMAIL SEND FAILED: {str(send_error)}")
								logger.error(f"          Exception type: {type(send_error).__name__}")
								print(f"       ❌ EMAIL SEND FAILED")
								print(f"          Error: {str(send_error)}")
								print(f"          Type: {type(send_error).__name__}")
								import traceback
								tb_text = traceback.format_exc()
								logger.error(f"          Traceback: {tb_text}")
								print(f"          Traceback: {tb_text}")
								total_failed += 1
						else:
							logger.warning(f"       ⚠️ No subject, cannot send email")
							print(f"       ❌ SKIP - No subject")
							total_failed += 1

					except Exception as e:
						logger.error(f"       ❌ Exception processing talent {talent_id}: {e}")
						logger.error(f"          Exception type: {type(e).__name__}")
						import traceback
						logger.error(f"          Traceback: {traceback.format_exc()}")
						total_failed += 1

				logger.info(f"📧 Welcome Email Summary: Sent {total_sent}, Failed {total_failed}")
				if total_sent > 0 or total_failed > 0:
					messages.append(f"Welcome: Sent {total_sent}, Failed {total_failed}")
			else:
				logger.warning(f"⚠️ No talent campaigns found for welcome emails")
				print(f"\n   ⚠️ NO TALENT CAMPAIGNS FOUND")
		else:
			logger.info("ℹ️ No campaign socials found (skipping welcome emails)")
			logger.info("   To send welcome emails, create a Mira Campaign Social record")
			print(f"\n   ⚠️ NO CAMPAIGN SOCIALS FOUND - Need to create Mira Campaign Social")
			print(f"      Steps:")
			print(f"      1. Go to Campaign: {campaign_id}")
			print(f"      2. Create a new 'Mira Campaign Social' record")
			print(f"      3. Add email subject and template content")
			print(f"      4. Change campaign status to ACTIVE again")

		# --- Final Result ---
		# Success if we did *something* (Birthday check ran OR Socials found)
		success = has_birthday_trigger or (len(campaign_socials) > 0)

		print(f"\n{'='*80}")
		print(f"📊 FINAL SUMMARY")
		print(f"{'='*80}")
		print(f"Total Sent: {total_sent}")
		print(f"Total Failed: {total_failed}")
		print(f"Success: {success}")
		print(f"{'='*80}\n")

		logger.info(f"\n{'='*70}")
		logger.info(f"📊 FINAL SUMMARY FOR CAMPAIGN: {campaign_id}")
		logger.info(f"   Total Sent: {total_sent}")
		logger.info(f"   Total Failed: {total_failed}")
		logger.info(f"   Messages: {messages}")
		logger.info(f"   Success: {success}")
		logger.info(f"{'='*70}\n")

		final_msg = ", ".join(messages) if messages else "No actions performed"
		if success and not messages:
			final_msg = "Checks executed (no emails sent)"

		return {
			"success": success,
			"sent": total_sent,
			"failed": total_failed,
			"message": final_msg
		}
	except Exception as e:
		import traceback
		tb = traceback.format_exc()
		logger.error(f"❌ Error in send_campaign_welcome_emails: {str(e)}")
		logger.error(tb)
		frappe.log_error(f"Error in send_campaign_welcome_emails: {str(e)}\n{tb}")
		print(f"\n{'='*80}")
		print(f"❌ CRITICAL ERROR IN SEND_CAMPAIGN_WELCOME_EMAILS")
		print(f"{'='*80}")
		print(f"Error: {str(e)}")
		print(f"\nFull Traceback:")
		print(tb)
		print(f"{'='*80}\n")
		return {"success": False, "error": str(e), "sent": 0, "failed": 0}
