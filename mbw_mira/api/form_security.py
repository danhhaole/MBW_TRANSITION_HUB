import ipaddress
import frappe
from frappe.utils import now_datetime
import io, random, string, base64, hashlib, hmac
from PIL import Image, ImageDraw, ImageFont


SECRET_KEY = frappe.local.conf.get("form_secret", "MY_SUPER_SECRET_KEY")


@frappe.whitelist(allow_guest=True)
def get_captcha():
    """Tạo ảnh captcha"""
    text = ''.join(random.choices(string.ascii_uppercase + string.digits, k=5))
    frappe.cache().set_value("captcha_code", text, expires_in_sec=300)

    image = Image.new('RGB', (120, 40), color=(255, 255, 255))
    draw = ImageDraw.Draw(image)
    font = ImageFont.load_default(20)
    draw.text((20, 10), text, fill=(0, 0, 0), font=font)

    # Nhiễu nhẹ
    for _ in range(5):
        x1, y1 = random.randint(0, 120), random.randint(0, 40)
        x2, y2 = random.randint(0, 120), random.randint(0, 40)
        draw.line((x1, y1, x2, y2), fill=(150, 150, 150), width=2)

    img_bytes = io.BytesIO()
    image.save(img_bytes, format='PNG')
    b64 = base64.b64encode(img_bytes.getvalue()).decode('utf-8')
    return {"image": f"data:image/png;base64,{b64}"}


@frappe.whitelist(allow_guest=True)
def validate_captcha(code):
    """Kiểm tra captcha nhập vào"""
    saved = frappe.cache().get_value("captcha_code")
    
    return {"valid": code.strip().upper() == saved}


@frappe.whitelist(allow_guest=True)
def get_form_security():
    """Tạo token bảo mật (timestamp + hash)"""
    timestamp = frappe.utils.now_datetime().isoformat()
    digest = hmac.new(SECRET_KEY.encode(), timestamp.encode(), hashlib.sha256).hexdigest()
    return {"timestamp": timestamp, "hash": digest}
def validate_submission(data):
    # 1. Honeypot
    if data.get("website"):
        frappe.throw("Bot detected.")
    # 2. Hash check
    expected = hmac.new(SECRET_KEY.encode(), data["form_timestamp"].encode(), hashlib.sha256).hexdigest()
    if data["form_hash"] != expected:
        frappe.throw("Form tampered.")


def get_real_ip():
    req = frappe.local.request
    ip = (
        req.headers.get("X-Forwarded-For")
        or req.headers.get("X-Real-IP")
        or req.remote_addr
    )
    # Lấy IP đầu tiên nếu có chuỗi danh sách
    if "," in ip:
        ip = ip.split(",")[0].strip()
    try:
        ipaddress.ip_address(ip)
    except ValueError:
        ip = "0.0.0.0"
    return ip

@frappe.whitelist(allow_guest=True)
def submit_form():
    data = frappe.form_dict
    validate_submission(data)

    # Validate captcha
    saved_code = frappe.cache().get_value("captcha_code")
    if not data.get("captcha_input") or data.get("captcha_input").strip().upper() != saved_code:
        frappe.throw("Sai mã CAPTCHA")

    ip = get_real_ip()
    user_agent = frappe.local.request.headers.get("User-Agent", "")

    # Lấy URL form gửi lên


    # Tạo document Mira Form Attraction
    doc = frappe.get_doc({
        "doctype": "Mira Form Attraction",

        # Form Identification
        "form_id": data.get("form_id") or "unknown_form",
        "source_channel": data.get("source_channel"),
        "talent_pool": data.get("talent_pool"),

        # User Data
        "full_name": data.get("full_name"),
        "email_id": data.get("email_id"),
        "phone_number": data.get("phone_number"),
        "desired_position": data.get("desired_position"),
        "key_skills": data.get("key_skills"),
        "linkedin_url": data.get("linkedin_url"),
        "current_location": data.get("current_location"),
        "candidate_cv": data.get("candidate_cv"),
        "candidate_portfolio": data.get("candidate_portfolio"),
        "candidate_photo": data.get("candidate_photo"),
        "years_of_experience": data.get("years_of_experience"),
        "highest_education": data.get("highest_education"),
        "expected_salary": data.get("expected_salary"),

        # UTM Parameters
        "utm_source": data.get("utm_source"),
        "utm_medium": data.get("utm_medium"),
        "utm_campaign": data.get("utm_campaign"),
        "utm_term": data.get("utm_term"),
        "utm_content": data.get("utm_content"),

        # Metadata Logging
        "client_ip": ip,
        "user_agent": user_agent,
        "acquisition_date": now_datetime(),
        "ladipage_form_name": data.get("ladipage_form_name"),
    })

    doc.insert(ignore_permissions=True)
    frappe.db.commit()

    return {"message": "success"}