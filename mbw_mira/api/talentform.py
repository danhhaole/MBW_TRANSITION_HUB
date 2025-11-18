import frappe
import json
from frappe.exceptions import ValidationError
from mbw_mira.mbw_mira.doctype.mira_access_token.mira_access_token import validate_test_token, get_token_from_header

@frappe.whitelist(allow_guest=True)
def form_nurturing():
    token = get_token_from_header()
    token_doc = validate_test_token(token)

    # Parse JSON body
    if frappe.request.data:
        data = json.loads(frappe.request.data)
        form_data = data.get("data", {})
    else:
        frappe.throw("Thiếu dữ liệu cập nhật.")

    if not form_data:
        frappe.throw("Body không có dữ liệu cập nhật.")

    # Lấy document Mira Talent theo talent ID trong token
    talent = frappe.get_doc("Mira Talent", token_doc.talent)
    updated_fields = []

    # Gắn mặc định source nếu không được gửi lên
    if not form_data.get("source"):
        form_data["source"] = "Nurturing Interaction"

    # Cập nhật field hợp lệ
    for field, value in form_data.items():
        if hasattr(talent, field):
            setattr(talent, field, value)
            updated_fields.append(field)

    # Lưu thay đổi
    talent.save(ignore_permissions=True)

    # Đánh dấu token đã sử dụng (nếu cần)
    frappe.db.set_value("Mira Access Token", token_doc.name, "is_used", 1)
    frappe.db.commit()

    return {
        "success": True,
        "updated_fields": updated_fields,
        "talent_id": talent.name,
    }

@frappe.whitelist(allow_guest=True)
def form_event():
    """
    API cập nhật thông tin Talent khi điền form Event.
    Token đính kèm trong header: Authorization: Bearer <token>
    Source sẽ tự động là 'Event'
    """
    token = get_token_from_header()
    token_doc = validate_test_token(token)

    # Parse JSON body
    if frappe.request.data:
        data = json.loads(frappe.request.data)
        form_data = data.get("data", {})
    else:
        frappe.throw("Thiếu dữ liệu cập nhật.")

    if not form_data:
        frappe.throw("Body không có dữ liệu cập nhật.")

    # Field bắt buộc
    required_fields = ["full_name", "email", "latest_title"]
    missing = [f for f in required_fields if not form_data.get(f)]
    if missing:
        frappe.throw(f"Thiếu thông tin bắt buộc: {', '.join(missing)}")

    # Gán giá trị cố định
    form_data["source"] = "Event"

    # Lấy tài liệu Talent tương ứng token
    talent = frappe.get_doc("Mira Talent", token_doc.talent)
    updated_fields = {}

    for field, value in form_data.items():
        if hasattr(talent, field):
            setattr(talent, field, value)
            updated_fields[field] = value

    # Lưu thay đổi
    talent.save(ignore_permissions=True)

    # Đánh dấu token đã dùng (tùy chọn)
    frappe.db.set_value("Mira Access Token", token_doc.name, "is_used", 1)
    frappe.db.commit()

    return {
        "success": True,
        "message": "Cập nhật thông tin Event Talent thành công",
        "source": "Event",
        "updated_values": updated_fields,
        "talent_id": talent.name,
    }


# Hàm API để nhận dữ liệu từ form và lưu vào Mira Talent
@frappe.whitelist(allow_guest=True)
def submit_tracking_data():
    """
    Hàm API công khai: Nhận dữ liệu thô và lưu vào DocType Mira Talent Tracking.
    Sau đó, gọi process_tracking_to_talent() để xử lý.
    """
    try:
        data = frappe.form_dict
        
        # 1. Kiểm tra tối thiểu
        if not data.get("full_name") or (not data.get("email") and not data.get("phone")):
            frappe.throw("Full Name và Email hoặc Phone là bắt buộc.", title="Dữ liệu Thiếu")

        # 2. Tạo DocType Tracking
        tracking_doc = frappe.new_doc("Mira Talent Tracking")
        # Mapping tất cả các trường từ Request vào DocType Tracking
        
        for field in tracking_doc.meta.fields:
            
            if field.fieldname in data:                
                tracking_doc.set(field.fieldname, data.get(field.fieldname))

        # Thiết lập trạng thái ban đầu
        tracking_doc.processing_status = "Pending"
        tracking_doc.save(ignore_permissions=True)
        frappe.db.commit()
        
        tracking_doc_name = tracking_doc.name

        # 3. Kích hoạt Hàm Xử lý sau khi lưu Tracking Doc thành công
        # Sử dụng frappe.enqueue để xử lý bất đồng bộ (giúp API phản hồi nhanh hơn)
        frappe.enqueue(
            "mbw_mira.mbw_mira.doctype.mira_talent.mira_talent.process_tracking_to_talent",
            tracking_doc_name=tracking_doc_name,
            queue='default', # Có thể chọn queue khác nếu cần
        )
        
        return {
            "status": "success",
            "message": "Dữ liệu tracking đã được ghi nhận và đang chờ xử lý.",
            "tracking_id": tracking_doc_name
        }

    except Exception as e:
        frappe.log_error(frappe.get_traceback(), "Public Tracking API Failed")
        return {
            "status": "error",
            "message": f"Có lỗi xảy ra: {e}"
        }