from PIL import Image, ImageDraw, ImageFont
import subprocess

W, H = 320, 240
NAV_H = 36

# ── 画面ID ──────────────────────────────────────────────
SCREEN_HOME      = 0
SCREEN_MUSIC     = 1
SCREEN_SCENE     = 2
SCREEN_PHOTO     = 3
SCREEN_MAIL      = 4
SCREEN_CLOCK     = 5
SCREEN_LANDSCAPE = 6  # 自動起動（ナビ非表示）

NAV_TABS = [
    ("Home",  SCREEN_HOME),
    ("Music", SCREEN_MUSIC),
    ("Scene", SCREEN_SCENE),
    ("Photo", SCREEN_PHOTO),
    ("Mail",  SCREEN_MAIL),
    ("Clock", SCREEN_CLOCK),
]

# ── カラー ──────────────────────────────────────────────
BG     = (28, 45, 28)
BG2    = (45, 65, 45)
CREAM  = (245, 238, 220)
CREAM2 = (200, 190, 165)
SAGE   = (150, 200, 150)
ACCENT = (220, 170, 120)
ACCENT2= (200, 130, 85)
MUTED  = (130, 170, 130)
BORDER = (80, 110, 80)

# ── フォント ────────────────────────────────────────────
try:
    FONT_HUGE  = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 72)
    FONT_LARGE = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 44)
    FONT_MED   = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 22)
    FONT_SMALL = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 18)
    FONT_TINY  = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 13)
except:
    FONT_HUGE = FONT_LARGE = FONT_MED = FONT_SMALL = FONT_TINY = ImageFont.load_default()

# ── MPD ─────────────────────────────────────────────────
def get_mpd():
    try:
        st  = subprocess.run(["mpc","status"],  capture_output=True, text=True, timeout=1).stdout
        cur = subprocess.run(["mpc","current"], capture_output=True, text=True, timeout=1).stdout.strip()
        return {"playing": "[playing]" in st, "song": cur or "No song"}
    except:
        return {"playing": False, "song": "No song"}

# ── ユーティリティ ───────────────────────────────────────
def text_w(text, font):
    d = ImageDraw.Draw(Image.new("RGB",(1,1)))
    b = d.textbbox((0,0), text, font=font)
    return b[2] - b[0]

def center_x(text, font, area_w=W, offset=0):
    return offset + (area_w - text_w(text, font)) // 2

def draw_scroll_text(image, text, font, x, y, max_w, color, scroll_x, bg=BG):
    tw = text_w(text, font)
    d  = ImageDraw.Draw(image)
    if tw <= max_w:
        d.text((x, y), text, font=font, fill=color)
        return
    gap    = 40
    loop_w = tw + gap
    off    = Image.new("RGB", (loop_w*2, 24), bg)
    od     = ImageDraw.Draw(off)
    od.text((0, 0),       text, font=font, fill=color)
    od.text((loop_w, 0),  text, font=font, fill=color)
    crop_x  = int(scroll_x) % loop_w
    cropped = off.crop((crop_x, 0, crop_x+max_w, 24))
    image.paste(cropped, (x, y))

def draw_nav(draw, active):
    y0    = H - NAV_H
    tab_w = W // len(NAV_TABS)
    draw.rectangle([0, y0, W, H], fill=BG2)
    draw.line([(0, y0),(W, y0)], fill=BORDER, width=1)
    for i, (label, sid) in enumerate(NAV_TABS):
        tx  = i * tab_w + tab_w // 2
        col = ACCENT if active == sid else MUTED
        lw  = text_w(label, FONT_TINY)
        draw.text((tx - lw//2, y0+10), label, font=FONT_TINY, fill=col)
        if active == sid:
            draw.ellipse([tx-2, y0+3, tx+2, y0+7], fill=ACCENT)

def hit_nav(x, y):
    """タッチ座標がナビのどのタブか返す。ナビ外はNone"""
    y0    = H - NAV_H
    tab_w = W // len(NAV_TABS)
    if y < y0:
        return None
    idx = x // tab_w
    if 0 <= idx < len(NAV_TABS):
        return NAV_TABS[idx][1]
    return None
