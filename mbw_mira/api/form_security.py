import frappe
import io, random, string, base64, hashlib, hmac
from PIL import Image, ImageDraw, ImageFont

SECRET_KEY = frappe.local.conf.get("form_secret", "MY_SUPER_SECRET_KEY")


@frappe.whitelist(allow_guest=True)
def get_captcha():
    """Tạo ảnh captcha"""
    text = ''.join(random.choices(string.ascii_uppercase + string.digits, k=5))
    frappe.session.data["captcha_code"] = text
    frappe.session.save()

    image = Image.new('RGB', (120, 40), color=(255, 255, 255))
    draw = ImageDraw.Draw(image)
    font = ImageFont.load_default()
    draw.text((20, 10), text, fill=(0, 0, 0), font=font)

    # Nhiễu nhẹ
    for _ in range(5):
        x1, y1 = random.randint(0, 120), random.randint(0, 40)
        x2, y2 = random.randint(0, 120), random.randint(0, 40)
        draw.line((x1, y1, x2, y2), fill=(150, 150, 150), width=1)

    img_bytes = io.BytesIO()
    image.save(img_bytes, format='PNG')
    b64 = base64.b64encode(img_bytes.getvalue()).decode('utf-8')
    return {"image": f"data:image/png;base64,{b64}"}


@frappe.whitelist(allow_guest=True)
def validate_captcha(code):
    """Kiểm tra captcha nhập vào"""
    saved = frappe.session.data.get("captcha_code")
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