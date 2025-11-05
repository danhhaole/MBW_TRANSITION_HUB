# your_app/www/api/captcha.py
import io
import random
import string
import time
import base64

from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageOps

import frappe

# Optional numpy for elastic distortion (faster / better). If not installed, fallback.
try:
    import numpy as np
    _HAS_NUMPY = True
except Exception:
    _HAS_NUMPY = False

# Config
WIDTH = 260
HEIGHT = 90
LENGTH = 5
FONTS = [
    "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
    "/usr/share/fonts/truetype/liberation/LiberationSerif-Regular.ttf",
    # Thêm đường dẫn font tùy chỉnh của bạn ở đây
]
CHARS = string.ascii_uppercase + string.digits

def _random_text(length=LENGTH):
    return ''.join(random.choices(CHARS, k=length))

def _random_color(min_c=0, max_c=255):
    return tuple(random.randint(min_c, max_c) for _ in range(3))

def _create_background(width, height):
    # gradient + noise background
    base = Image.new("RGB", (width, height), (255,255,255))
    draw = ImageDraw.Draw(base)
    # gradient
    for y in range(height):
        c = int(220 + (y/height)*35)  # subtle vertical gradient
        draw.line([(0, y), (width, y)], fill=(c,c,c))
    # add textured dots
    pixels = base.load()
    for _ in range(int(width*height*0.02)):
        x = random.randint(0, width-1)
        y = random.randint(0, height-1)
        pixels[x, y] = tuple(max(0, v - random.randint(10,80)) for v in pixels[x, y])
    return base

def _draw_wave_distort(image, amplitude_range=(3,6), period_range=(30,70)):
    # simple horizontal wave
    import math
    amplitude = random.uniform(*amplitude_range)
    period = random.uniform(*period_range)
    w, h = image.size
    src = image
    dst = Image.new("RGB", (w, h), (255,255,255))
    for y in range(h):
        offset = int(amplitude * math.sin(2*math.pi*y/period))
        dst.paste(src.crop((0, y, w, y+1)), (offset, y))
    return dst

def _elastic_transform(image, alpha=36, sigma=8):
    # Requires numpy
    if not _HAS_NUMPY:
        return _draw_wave_distort(image)
    arr = np.array(image)
    shape = arr.shape
    dx = (np.random.rand(*shape[:2]) * 2 - 1)
    dy = (np.random.rand(*shape[:2]) * 2 - 1)
    dx = (dx * alpha).astype(np.float32)
    dy = (dy * alpha).astype(np.float32)
    # gaussian filter for smoothness
    from scipy.ndimage.filters import gaussian_filter  # optional: scipy
    try:
        dx = gaussian_filter(dx, sigma)
        dy = gaussian_filter(dy, sigma)
    except Exception:
        # fallback: reduce intensity
        dx = gaussian_filter(dx, max(1, sigma//2))
        dy = gaussian_filter(dy, max(1, sigma//2))
    x, y = np.meshgrid(np.arange(shape[1]), np.arange(shape[0]))
    indices_x = (y + dy).clip(0, shape[0]-1).astype(np.int32)
    indices_y = (x + dx).clip(0, shape[1]-1).astype(np.int32)
    new_arr = arr[indices_x, indices_y]
    return Image.fromarray(new_arr)

def generate_advanced_captcha(text=None):
    if text is None:
        text = _random_text()

    # Background
    image = _create_background(WIDTH, HEIGHT)
    draw = ImageDraw.Draw(image)

    # Draw random shapes in background for occlusion
    for _ in range(random.randint(3,6)):
        x0 = random.randint(0, WIDTH//2)
        y0 = random.randint(0, HEIGHT//2)
        x1 = x0 + random.randint(30, WIDTH//2)
        y1 = y0 + random.randint(20, HEIGHT//2)
        shape_color = _random_color(180, 255)
        draw.ellipse([x0,y0,x1,y1], outline=shape_color, width=1)

    # Draw each char separately with random transform
    avg_width = WIDTH // (len(text) + 1)
    x = avg_width // 2
    for ch in text:
        font_path = random.choice(FONTS)
        font_size = random.randint(30, 44)
        try:
            font = ImageFont.truetype(font_path, font_size)
        except Exception:
            font = ImageFont.load_default()
        # create char image
        char_img = Image.new("RGBA", (avg_width, HEIGHT), (0,0,0,0))
        if char_img.size != image.size:
            char_img = char_img.resize(image.size)

        char_draw = ImageDraw.Draw(char_img)
        # random color with moderate contrast
        color = _random_color(0, 80)
        # slight vertical jitter
        y_jitter = random.randint(-8, 8)
        char_draw.text((10, (HEIGHT - font_size)//2 + y_jitter), ch, font=font, fill=color)
        # per-char transforms: rotate, shear, scale
        angle = random.uniform(-35, 35)
        char_img = char_img.rotate(angle, resample=Image.BICUBIC, expand=1)
        # paste with random vertical offset
        px = x + random.randint(-6, 6)
        py = random.randint(-12, 12)
        image.paste(
            Image.alpha_composite(Image.new("RGBA", image.size), char_img).convert("RGB"),
            (0, 0),
            char_img
        )

        x += avg_width + random.randint(-8, 8)

    # Add occluding lines/arcs
    for _ in range(random.randint(5, 10)):
        x1 = random.randint(0, WIDTH)
        y1 = random.randint(0, HEIGHT)
        x2 = random.randint(0, WIDTH)
        y2 = random.randint(0, HEIGHT)
        draw.line((x1,y1,x2,y2), fill=_random_color(80,180), width=random.randint(1,3))
    for _ in range(random.randint(3,6)):
        bbox = [random.randint(-20, WIDTH), random.randint(-20, HEIGHT),
                random.randint(0, WIDTH+20), random.randint(0, HEIGHT+20)]
        draw.arc(bbox, start=random.randint(0,360), end=random.randint(0,360), fill=_random_color(80,200))

    # Add speckle noise
    pixels = image.load()
    for _ in range(int(WIDTH*HEIGHT*0.01)):
        x_n = random.randint(0, WIDTH-1)
        y_n = random.randint(0, HEIGHT-1)
        r = max(0, min(255, pixels[x_n, y_n][0] + random.randint(-60, 60)))
        g = max(0, min(255, pixels[x_n, y_n][1] + random.randint(-60, 60)))
        b = max(0, min(255, pixels[x_n, y_n][2] + random.randint(-60, 60)))
        pixels[x_n, y_n] = (r,g,b)

    # Global distort (wave or elastic)
    if _HAS_NUMPY:
        try:
            image = _elastic_transform(image, alpha=random.randint(20, 36), sigma=random.randint(4, 8))
        except Exception:
            image = _draw_wave_distort(image)
    else:
        image = _draw_wave_distort(image)

    # local blur/sharpen randomly
    if random.random() > 0.6:
        image = image.filter(ImageFilter.GaussianBlur(radius=random.uniform(0.3,1.2)))
    if random.random() > 0.7:
        image = image.filter(ImageFilter.UnsharpMask(radius=1, percent=120, threshold=3))

    # final vignette / contrast tweak
    image = ImageOps.autocontrast(image, cutoff=random.randint(0,5))

    # convert to bytes
    buf = io.BytesIO()
    image.save(buf, format="PNG")
    b64 = base64.b64encode(buf.getvalue()).decode("utf-8")

    return {"text": text, "image": f"data:image/png;base64,{b64}"}

# Frappe endpoints
@frappe.whitelist(allow_guest=True)
def get_captcha():
    obj = generate_advanced_captcha()
    # Save to cache with small TTL (one-time)
    captcha_id = frappe.generate_hash()
    frappe.cache().set_value(f"captcha:{captcha_id}", obj["text"], expires_in_sec=180)
    return {"captcha_id": captcha_id, "image": obj["image"]}

@frappe.whitelist(allow_guest=True)
def validate_captcha(captcha_id=None, code=None):
    if not captcha_id or not code:
        return {"valid": False}
    saved = frappe.cache().get_value(f"captcha:{captcha_id}")
    if not saved:
        return {"valid": False}
    # case-insensitive compare
    ok = saved.strip().lower() == code.strip().lower()
    if ok:
        frappe.cache().delete_key(f"captcha:{captcha_id}")
    return {"valid": ok}
