from PIL import Image, ImageDraw
from scenes.common import *
import os, glob

PHOTO_DIR      = "/home/pi/photos"
SLIDE_INTERVAL = 5 * 20

MODE_GALLERY    = 0
MODE_FULLSCREEN = 1
MODE_SLIDESHOW  = 2

_mode        = MODE_GALLERY
_photos      = []
_photo_idx   = 0
_slide_timer = 0
_cache       = {}
_gallery_page = 0  # ページ（6枚ずつ）

COLS, ROWS = 3, 2
PER_PAGE   = COLS * ROWS

def _load_photos():
    global _photos
    exts = ["jpg","jpeg","png","webp","gif","JPG","JPEG","PNG","WEBP"]
    files = []
    for ext in exts:
        files.extend(glob.glob(os.path.join(PHOTO_DIR, f"*.{ext}")))
    _photos = sorted(set(files))

def _get_thumb(path, size):
    key = (path, size)
    if key not in _cache:
        try:
            img = Image.open(path).convert("RGB")
            img.thumbnail(size, Image.LANCZOS)
            _cache[key] = img
        except:
            _cache[key] = None
    return _cache[key]

def _get_full(path):
    ph = H - NAV_H - 30
    key = (path, "full")
    if key not in _cache:
        try:
            img = Image.open(path).convert("RGB")
            iw, ih = img.size
            ratio = min(W/iw, ph/ih)
            nw, nh = int(iw*ratio), int(ih*ratio)
            img = img.resize((nw, nh), Image.LANCZOS)
            canvas = Image.new("RGB", (W, ph), BG)
            canvas.paste(img, ((W-nw)//2, (ph-nh)//2))
            _cache[key] = canvas
        except:
            _cache[key] = None
    return _cache[key]

def _btn_rect(label, cx, cy, w=60, h=22):
    return {"label": label, "x1": cx-w//2, "y1": cy-h//2, "x2": cx+w//2, "y2": cy+h//2}

def _draw_btn(d, btn, active=False):
    fill    = ACCENT if active else BG2
    outline = ACCENT if active else BORDER
    d.rounded_rectangle([btn["x1"],btn["y1"],btn["x2"],btn["y2"]], radius=4, fill=fill, outline=outline, width=1)
    lw = text_w(btn["label"], FONT_TINY)
    tx = (btn["x1"]+btn["x2"])//2 - lw//2
    ty = (btn["y1"]+btn["y2"])//2 - 7
    d.text((tx, ty), btn["label"], font=FONT_TINY, fill=BG if active else CREAM2)

def _hit_btn(btn, x, y):
    return btn["x1"] <= x <= btn["x2"] and btn["y1"] <= y <= btn["y2"]

def draw(image, now, mpd, scroll_x):
    global _slide_timer, _photo_idx, _mode
    _load_photos()
    d = ImageDraw.Draw(image)
    d.rectangle([0,0,W,H], fill=BG)

    if not _photos:
        d.text((center_x("No photos", FONT_SMALL), 90), "No photos", font=FONT_SMALL, fill=MUTED)
        d.text((center_x("Upload via WebUI", FONT_TINY), 115), "Upload via WebUI", font=FONT_TINY, fill=BORDER)
        draw_nav(d, SCREEN_PHOTO)
        return

    if _mode == MODE_GALLERY:
        _draw_gallery(image, d)
    elif _mode == MODE_FULLSCREEN:
        _draw_fullscreen(image, d)
    elif _mode == MODE_SLIDESHOW:
        _slide_timer += 1
        if _slide_timer >= SLIDE_INTERVAL:
            _slide_timer = 0
            _photo_idx = (_photo_idx + 1) % len(_photos)
        _draw_slideshow(image, d)

    draw_nav(d, SCREEN_PHOTO)

def _draw_gallery(image, d):
    global _gallery_page
    total_pages = max(1, (len(_photos) + PER_PAGE - 1) // PER_PAGE)
    _gallery_page = max(0, min(_gallery_page, total_pages - 1))

    # ヘッダー
    d.rectangle([0,0,W,26], fill=BG2)
    d.line([(0,26),(W,26)], fill=BORDER, width=1)

    # ◀▶ ページナビ（左側）
    if total_pages > 1:
        lc = ACCENT if _gallery_page > 0             else BORDER
        rc = ACCENT if _gallery_page < total_pages-1 else BORDER
        d.text((18, 6), "◀", font=FONT_TINY, fill=lc)
        d.text((32, 6), "▶", font=FONT_TINY, fill=rc)

    d.text((center_x("Photos", FONT_TINY), 6), "Photos", font=FONT_TINY, fill=ACCENT)
    page_info = f"{_gallery_page+1}/{total_pages}" if total_pages > 1 else f"{len(_photos)} photos"
    d.text((W - text_w(page_info, FONT_TINY) - 6, 6), page_info, font=FONT_TINY, fill=MUTED)

    pad = 6
    thumb_w = (W - pad*(COLS+1)) // COLS
    thumb_h = (H - NAV_H - 26 - pad*(ROWS+1) - 28) // ROWS

    start = _gallery_page * PER_PAGE
    for i in range(PER_PAGE):
        photo_i = start + i
        if photo_i >= len(_photos):
            break
        col = i % COLS
        row = i // COLS
        tx  = pad + col * (thumb_w + pad)
        ty  = 26 + pad + row * (thumb_h + pad)

        thumb = _get_thumb(_photos[photo_i], (thumb_w, thumb_h))
        bg = Image.new("RGB", (thumb_w, thumb_h), BG2)
        if thumb:
            ox = (thumb_w - thumb.width) // 2
            oy = (thumb_h - thumb.height) // 2
            bg.paste(thumb, (ox, oy))
        image.paste(bg, (tx, ty))
        d = ImageDraw.Draw(image)
        outline_col = ACCENT if photo_i == _photo_idx else BORDER
        d.rectangle([tx,ty,tx+thumb_w,ty+thumb_h], outline=outline_col, width=2 if photo_i==_photo_idx else 1)

    d = ImageDraw.Draw(image)
    btn_y = H - NAV_H - 18
    _draw_btn(d, _btn_rect("Slideshow >", W//2, btn_y, w=100, h=22))

def _draw_fullscreen(image, d):
    full = _get_full(_photos[_photo_idx])
    if full:
        image.paste(full, (0, 0))
    d = ImageDraw.Draw(image)
    counter = f"{_photo_idx+1}/{len(_photos)}"
    d.text((W - text_w(counter, FONT_TINY) - 6, 4), counter, font=FONT_TINY, fill=CREAM2)
    btn_y = H - NAV_H - 15
    for btn in [
        _btn_rect("< Prev",      55,  btn_y, w=76, h=22),
        _btn_rect("Slideshow >", 160, btn_y, w=90, h=22),
        _btn_rect("Next >",      265, btn_y, w=76, h=22),
        _btn_rect("Grid",        W-24, 4,    w=38, h=18),
    ]:
        _draw_btn(d, btn)

def _draw_slideshow(image, d):
    full = _get_full(_photos[_photo_idx])
    if full:
        image.paste(full, (0, 0))
    d = ImageDraw.Draw(image)
    counter = f"{_photo_idx+1}/{len(_photos)}"
    d.text((W - text_w(counter, FONT_TINY) - 6, 4), counter, font=FONT_TINY, fill=CREAM2)
    btn_y = H - NAV_H - 15
    _draw_btn(d, _btn_rect("Stop", 160, btn_y, w=60, h=22), active=True)

def handle_touch(x, y):
    global _mode, _photo_idx, _slide_timer, _gallery_page

    _load_photos()
    if not _photos:
        return

    total_pages = max(1, (len(_photos) + PER_PAGE - 1) // PER_PAGE)

    if _mode == MODE_GALLERY:
        # ヘッダーの◀▶
        if 0 <= y <= 26 and total_pages > 1:
            if 10 <= x <= 28 and _gallery_page > 0:
                _gallery_page -= 1
                return
            if 28 <= x <= 46 and _gallery_page < total_pages - 1:
                _gallery_page += 1
                return

        pad = 6
        thumb_w = (W - pad*(COLS+1)) // COLS
        thumb_h = (H - NAV_H - 26 - pad*(ROWS+1) - 28) // ROWS
        start = _gallery_page * PER_PAGE
        for i in range(PER_PAGE):
            photo_i = start + i
            if photo_i >= len(_photos):
                break
            col = i % COLS
            row = i // COLS
            tx  = pad + col * (thumb_w + pad)
            ty  = 26 + pad + row * (thumb_h + pad)
            if tx <= x <= tx+thumb_w and ty <= y <= ty+thumb_h:
                _photo_idx = photo_i
                _mode = MODE_FULLSCREEN
                return
        btn = _btn_rect("Slideshow >", W//2, H-NAV_H-18, w=100, h=22)
        if _hit_btn(btn, x, y):
            _mode = MODE_SLIDESHOW
            _slide_timer = 0

    elif _mode == MODE_FULLSCREEN:
        btn_y = H - NAV_H - 15
        if _hit_btn(_btn_rect("< Prev",      55,  btn_y, w=76, h=22), x, y):
            _photo_idx = (_photo_idx - 1) % len(_photos)
        elif _hit_btn(_btn_rect("Next >",    265, btn_y, w=76, h=22), x, y):
            _photo_idx = (_photo_idx + 1) % len(_photos)
        elif _hit_btn(_btn_rect("Slideshow >",160, btn_y, w=90, h=22), x, y):
            _mode = MODE_SLIDESHOW
            _slide_timer = 0
        elif _hit_btn(_btn_rect("Grid", W-24, 4, w=38, h=18), x, y):
            _mode = MODE_GALLERY

    elif _mode == MODE_SLIDESHOW:
        _mode = MODE_FULLSCREEN
