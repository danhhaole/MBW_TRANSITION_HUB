import hmac
import hashlib
import frappe


def make_signature(data: str) -> str:
    #data = f"candidate_id={candidate_id}&action={action}&url={url}"
    SECRET_KEY = frappe.conf.get("tracking_secret_key") or "email_track_aff07b5a10af788e14e6fedb38ce39d9"
    return hmac.new(SECRET_KEY.encode(), data.encode(), hashlib.sha256).hexdigest()
def verify_signature(data, sig):
    expected = make_signature(data)
    return hmac.compare_digest(expected, sig)
