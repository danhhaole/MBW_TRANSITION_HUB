import time, hmac, hashlib, base64, urllib.parse
from frappe import get_site_config

SECRET = get_site_config().get("form_signed_secret", "change_this_secret")


def generate_signed_url(base_url: str, payload: dict, ttl_seconds: int = 3600):
    """
    payload: dict of params to include (e.g. {"email":"a@b.com", "form":"lead"})
    returns: base_url + ?params...&expires=...&sig=...
    """
    params = payload.copy()
    expires = int(time.time()) + ttl_seconds
    params["expires"] = str(expires)
    # sort params for deterministic signature
    items = sorted(params.items())
    qs = urllib.parse.urlencode(items)
    mac = hmac.new(SECRET.encode(), qs.encode(), hashlib.sha256).digest()
    sig = base64.urlsafe_b64encode(mac).decode().rstrip("=")
    return f"{base_url}?{qs}&sig={urllib.parse.quote(sig)}"


def verify_signed_params(params: dict) -> bool:
    sig = params.pop("sig", None)
    expires = int(params.get("expires", "0"))
    if int(time.time()) > expires:
        return False
    items = sorted(params.items())
    qs = urllib.parse.urlencode(items)
    mac = hmac.new(SECRET.encode(), qs.encode(), hashlib.sha256).digest()
    expected = base64.urlsafe_b64encode(mac).decode().rstrip("=")
    # compare in constant time
    return hmac.compare_digest(expected, sig)
