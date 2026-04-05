from luma.lcd.device import ili9341
from luma.core.interface.serial import spi
from luma.core.render import canvas
from PIL import Image, ImageDraw, ImageFont
import time
import datetime
import subprocess

# ── デバイス初期化 ──────────────────────────────────────────
serial = spi(port=0, device=0, gpio_DC=24, gpio_RST=25, bus_speed_hz=16000000)
device = ili9341(serial, width=320, height=240, rotate=0)

# ── フォント ────────────────────────────────────────────────
try:
    font_huge  = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 72)
    font_large = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 48)
    font_med   = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 24)
    font_small = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 18)
    font_tiny  = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 14)
except:
    font_huge = font_large = font_med = font_small = font_tiny = ImageFont.load_default()

# ── カラーパレット（ボタニカルグリーン） ──────────────────
BG       = (28, 45, 28)       # ダークグリーン背景
BG2      = (45, 65, 45)       # カード背景（明るめ）
CREAM    = (245, 238, 220)    # クリームテキスト（より明るく）
CREAM2   = (200, 190, 165)    # サブテキスト
SAGE     = (150, 200, 150)    # セージグリーン（鮮やかに）
ACCENT   = (220, 170, 120)    # テラコッタ/アンバー（明るく）
ACCENT2  = (200, 130, 85)     # ダークテラコッタ
MUTED    = (130, 170, 130)    # ミュートグリーン（明るく）
BORDER   = (80, 110, 80)      # ボーダー（見やすく）
BLACK    = (0, 0, 0)

# ── 画面定数 ────────────────────────────────────────────────
W, H = 320, 240
NAV_H = 36          # ボトムナビの高さ
SCREEN_HOME  = 0
SCREEN_MUSIC = 1
SCREEN_CLOCK = 2

# ── 状態 ────────────────────────────────────────────────────
current_screen = SCREEN_HOME
scroll_x       = 0
scroll_pause   = 0
last_song      = ""

# ── MPD情報取得 ──────────────────────────────────────────────
def get_mpd_info():
    try:
        status = subprocess.run(["mpc", "status"], capture_output=True, text=True, timeout=1).stdout
        current = subprocess.run(["mpc", "current"], capture_output=True, text=True, timeout=1).stdout.strip()
        playing = "[playing]" in status
        song = current if current else "No song"
        return {"playing": playing, "song": song}
    except:
        return {"playing": False, "song": "No song"}

# ── テキスト幅計測 ───────────────────────────────────────────
def text_width(text, font):
    dummy = Image.new("RGB", (1, 1))
    d = ImageDraw.Draw(dummy)
    bbox = d.textbbox((0, 0), text, font=font)
    return bbox[2] - bbox[0]

def text_center_x(text, font, area_w, offset_x=0):
    w = text_width(text, font)
    return offset_x + (area_w - w) // 2

# ── 植物デコレーション描画 ────────────────────────────────────
def draw_botanical(draw, x, y, scale=1.0, alpha_color=BORDER):
    """シンプルな植物モチーフを描く"""
    s = scale
    # 茎
    draw.line([(x, y), (x, int(y - 40*s))], fill=alpha_color, width=1)
    # 左の葉
    draw.ellipse([int(x-18*s), int(y-35*s), int(x-2*s), int(y-22*s)], outline=alpha_color, width=1)
    # 右の葉
    draw.ellipse([int(x+2*s), int(y-28*s), int(x+18*s), int(y-15*s)], outline=alpha_color, width=1)
    # 上の葉
    draw.ellipse([int(x-8*s), int(y-52*s), int(x+8*s), int(y-38*s)], outline=alpha_color, width=1)
    # 小さい花
    draw.ellipse([int(x-5*s), int(y-58*s), int(x+5*s), int(y-48*s)], fill=ACCENT2, outline=ACCENT)

# ── ボトムナビ描画 ──────────────────────────────────────────
def draw_nav(draw, active):
    y0 = H - NAV_H
    draw.rectangle([0, y0, W, H], fill=BG2)
    draw.line([(0, y0), (W, y0)], fill=BORDER, width=1)

    tabs = [("Home", SCREEN_HOME), ("Music", SCREEN_MUSIC), ("Clock", SCREEN_CLOCK)]
    tab_w = W // len(tabs)

    for i, (label, screen_id) in enumerate(tabs):
        tx = i * tab_w + tab_w // 2
        ty = y0 + NAV_H // 2 - 7
        color = ACCENT if active == screen_id else MUTED
        bbox = draw.textbbox((0, 0), label, font=font_tiny)
        lw = bbox[2] - bbox[0]
        draw.text((tx - lw//2, ty), label, font=font_tiny, fill=color)
        if active == screen_id:
            dot_x = tx
            draw.ellipse([dot_x-2, y0+3, dot_x+2, y0+7], fill=ACCENT)

# ── スクロールテキスト描画 ───────────────────────────────────
def draw_scroll_text(image, text, font, x, y, max_w, color, scroll_offset):
    tw = text_width(text, font)
    if tw <= max_w:
        draw = ImageDraw.Draw(image)
        draw.text((x, y), text, font=font, fill=color)
        return

    gap = 50
    loop_w = tw + gap
    off = Image.new("RGB", (loop_w * 2, 30), BG)
    od = ImageDraw.Draw(off)
    od.text((0, 0), text, font=font, fill=color)
    od.text((loop_w, 0), text, font=font, fill=color)
    crop_x = int(scroll_offset) % loop_w
    cropped = off.crop((crop_x, 0, crop_x + max_w, 30))
    image.paste(cropped, (x, y))

# ── HOME画面 ────────────────────────────────────────────────
def draw_home(image, now, mpd):
    draw = ImageDraw.Draw(image)
    content_h = H - NAV_H

    # 背景
    draw.rectangle([0, 0, W, H], fill=BG)

    # 装飾（左・右）
    draw_botanical(draw, 18, 120, scale=0.7, alpha_color=BORDER)
    draw_botanical(draw, W-18, 120, scale=0.6, alpha_color=BORDER)

    # 時刻（大きく中央）
    time_str = now.strftime("%H:%M")
    tx = text_center_x(time_str, font_large, W)
    draw.text((tx, 20), time_str, font=font_large, fill=CREAM)

    # 日付
    date_str = now.strftime("%Y. %m. %d")
    dx = text_center_x(date_str, font_small, W)
    draw.text((dx, 78), date_str, font=font_small, fill=CREAM2)

    # 曜日バッジ
    day_str = now.strftime("%a").upper()
    dw = text_width(day_str, font_tiny)
    bx = (W - dw - 12) // 2
    draw.rounded_rectangle([bx, 100, bx + dw + 12, 118], radius=4, fill=ACCENT2)
    draw.text((bx + 6, 101), day_str, font=font_tiny, fill=CREAM)

    # 区切り線（装飾付き）
    lx = 40
    draw.line([(lx, 130), (W - lx, 130)], fill=BORDER, width=1)
    draw.ellipse([W//2 - 3, 127, W//2 + 3, 133], fill=ACCENT2)

    # 再生状態アイコン
    state_icon = "▶" if mpd["playing"] else "⏸"
    state_color = SAGE if mpd["playing"] else MUTED
    draw.text((14, 148), state_icon, font=font_tiny, fill=state_color)

    # 曲名スクロール
    draw_scroll_text(image, mpd["song"], font_small,
                     32, 145, W - 44, CREAM2, scroll_x)

    draw_nav(draw, SCREEN_HOME)

# ── MUSIC画面 ───────────────────────────────────────────────
def draw_music(image, now, mpd):
    draw = ImageDraw.Draw(image)
    content_h = H - NAV_H

    draw.rectangle([0, 0, W, H], fill=BG)

    # ヘッダー
    draw.rectangle([0, 0, W, 32], fill=BG2)
    draw.line([(0, 32), (W, 32)], fill=BORDER, width=1)
    title = "Now Playing"
    tx = text_center_x(title, font_tiny, W)
    draw.text((tx, 9), title, font=font_tiny, fill=MUTED)

    # アルバムアート風の円
    cx, cy = W // 2, 90
    r = 50
    draw.ellipse([cx-r, cy-r, cx+r, cy+r], fill=BG2, outline=BORDER, width=1)
    draw.ellipse([cx-r+8, cy-r+8, cx+r-8, cy+r-8], outline=BORDER, width=1)
    # 中心の花
    draw.ellipse([cx-8, cy-8, cx+8, cy+8], fill=ACCENT2)
    draw.ellipse([cx-4, cy-4, cx+4, cy+4], fill=ACCENT)
    # 再生中なら点滅ドット
    if mpd["playing"]:
        draw.ellipse([cx+r-6, cy-r+2, cx+r+2, cy-r+10], fill=SAGE)

    # 曲名
    draw_scroll_text(image, mpd["song"], font_small,
                     20, 152, W - 40, CREAM, scroll_x)

    # 状態テキスト
    state = "PLAYING" if mpd["playing"] else "PAUSED"
    sw = text_center_x(state, font_tiny, W)
    draw.text((sw, 175), state, font=font_tiny,
              fill=SAGE if mpd["playing"] else MUTED)

    # ボタン（将来タッチ対応）
    btn_y = 195
    buttons = [("⏮", 60), ("⏯", 160), ("⏭", 260)]
    for label, bx in buttons:
        is_main = bx == 160
        r2 = 18 if is_main else 14
        fill = ACCENT if is_main else BG2
        outline = ACCENT if is_main else BORDER
        draw.ellipse([bx-r2, btn_y-r2, bx+r2, btn_y+r2], fill=fill, outline=outline, width=1)
        lw = text_width(label, font_tiny)
        draw.text((bx - lw//2, btn_y - 7), label, font=font_tiny,
                  fill=BG if is_main else CREAM2)

    draw_nav(draw, SCREEN_MUSIC)

# ── CLOCK画面 ───────────────────────────────────────────────
def draw_clock(image, now, mpd):
    draw = ImageDraw.Draw(image)
    content_h = H - NAV_H

    draw.rectangle([0, 0, W, H], fill=BG)

    # 装飾
    draw_botanical(draw, 25, 195, scale=0.9, alpha_color=BORDER)
    draw_botanical(draw, W-25, 195, scale=0.9, alpha_color=BORDER)

    # 大きな時刻（中央）
    time_str = now.strftime("%H:%M")
    tx = text_center_x(time_str, font_huge, W)
    draw.text((tx, 30), time_str, font=font_huge, fill=CREAM)

    # 日付
    date_str = now.strftime("%B %d,  %Y")
    dx = text_center_x(date_str, font_small, W)
    draw.text((dx, 140), date_str, font=font_small, fill=CREAM2)

    # 曜日
    day_str = now.strftime("%A")
    dw2 = text_center_x(day_str, font_tiny, W)
    draw.text((dw2, 165), day_str, font=font_tiny, fill=MUTED)

    # ミニ曲名
    if mpd["song"] != "No song":
        icon = "▶" if mpd["playing"] else "⏸"
        draw.text((14, 186), icon, font=font_tiny, fill=SAGE)
        draw_scroll_text(image, mpd["song"], font_tiny,
                         30, 186, W - 44, MUTED, scroll_x)

    draw_nav(draw, SCREEN_CLOCK)

# ── 画面切り替えロジック ──────────────────────────────────────
SCREEN_DURATION = 10   # 各画面の表示秒数
screen_timer = 0

# ── メインループ ────────────────────────────────────────────
frame = 0
while True:
    now = datetime.datetime.now()
    mpd = get_mpd_info()

    # 画面を自動でローテーション: Home → Music → Clock → Home...
    screen_timer += 1
    if screen_timer >= SCREEN_DURATION * 20:
        screen_timer = 0
        current_screen = (current_screen + 1) % 3

    # スクロール更新
    if mpd["song"] != last_song:
        last_song = mpd["song"]
        scroll_x = 0
        scroll_pause = 0

    tw = text_width(mpd["song"], font_small)
    if tw > W - 60:
        if scroll_pause < 60:
            scroll_pause += 1
        else:
            scroll_x += 1.5

    # 描画
    image = Image.new("RGB", (W, H), BG)

    if current_screen == SCREEN_HOME:
        draw_home(image, now, mpd)
    elif current_screen == SCREEN_MUSIC:
        draw_music(image, now, mpd)
    elif current_screen == SCREEN_CLOCK:
        draw_clock(image, now, mpd)

    device.display(image)

    frame += 1
    time.sleep(0.05)  # 約20fps
