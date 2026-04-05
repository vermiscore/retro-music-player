from PIL import Image, ImageDraw
from scenes.common import *
import subprocess

BUTTONS = [
    {"label": "|<",  "x": 70,  "y": 183, "r": 16, "action": "prev"},
    {"label": ">/||","x": 160, "y": 183, "r": 22, "action": "play"},
    {"label": ">|",  "x": 250, "y": 183, "r": 16, "action": "next"},
    {"label": "-",   "x": 30,  "y": 95,  "r": 12, "action": "vol_down"},
    {"label": "+",   "x": 90,  "y": 95,  "r": 12, "action": "vol_up"},
]

VOL_BAR_X = 18
VOL_BAR_Y = 55
VOL_BAR_W = 84
VOL_BAR_H = 7

def get_volume():
    try:
        out = subprocess.run(["mpc", "status"], capture_output=True, text=True, timeout=1).stdout
        for line in out.split("\n"):
            if "volume:" in line:
                vol = line.split("volume:")[1].strip().split("%")[0].strip()
                if vol.lstrip('-').isdigit():
                    return max(0, min(100, int(vol)))
    except:
        pass
    return 50

def draw(image, now, mpd, scroll_x):
    d = ImageDraw.Draw(image)
    d.rectangle([0,0,W,H], fill=BG)

    # ヘッダー
    d.rectangle([0,0,W,28], fill=BG2)
    d.line([(0,28),(W,28)], fill=BORDER, width=1)
    d.text((center_x("Now Playing", FONT_TINY), 7), "Now Playing", font=FONT_TINY, fill=MUTED)

    # 左側: VOLバー
    d.text((VOL_BAR_X, 36), "VOL", font=FONT_TINY, fill=MUTED)
    vol = get_volume()
    # バー背景
    d.rectangle([VOL_BAR_X, VOL_BAR_Y, VOL_BAR_X+VOL_BAR_W, VOL_BAR_Y+VOL_BAR_H],
                fill=BG2, outline=BORDER, width=1)
    # バー塗り
    fill_w = int(VOL_BAR_W * vol / 100)
    if fill_w > 0:
        d.rectangle([VOL_BAR_X, VOL_BAR_Y, VOL_BAR_X+fill_w, VOL_BAR_Y+VOL_BAR_H],
                    fill=SAGE)
    # 数値
    vol_str = f"{vol}%"
    d.text((VOL_BAR_X + VOL_BAR_W//2 - text_w(vol_str, FONT_TINY)//2, VOL_BAR_Y+10),
           vol_str, font=FONT_TINY, fill=CREAM2)

    # アルバムアート（中央〜右寄り）
    cx, cy, r = 210, 80, 45
    d.ellipse([cx-r,cy-r,cx+r,cy+r], fill=BG2, outline=BORDER, width=1)
    d.ellipse([cx-r+6,cy-r+6,cx+r-6,cy+r-6], outline=BORDER, width=1)
    d.ellipse([cx-6,cy-6,cx+6,cy+6], fill=ACCENT2)
    d.ellipse([cx-3,cy-3,cx+3,cy+3], fill=ACCENT)
    if mpd["playing"]:
        d.ellipse([cx+r-5,cy-r+2,cx+r+2,cy-r+9], fill=SAGE)

    # 状態
    state = "PLAYING" if mpd["playing"] else "PAUSED"
    d.text((center_x(state, FONT_TINY), 130), state, font=FONT_TINY,
           fill=SAGE if mpd["playing"] else MUTED)

    # 曲名
    draw_scroll_text(image, mpd["song"], FONT_SMALL, 16, 143, W-32, CREAM, scroll_x)

    # ボタン描画
    for btn in BUTTONS:
        is_main = btn["action"] == "play"
        fill    = ACCENT if is_main else BG2
        outline = ACCENT if is_main else BORDER
        d.ellipse([btn["x"]-btn["r"], btn["y"]-btn["r"],
                   btn["x"]+btn["r"], btn["y"]+btn["r"]],
                  fill=fill, outline=outline, width=1)
        lw = text_w(btn["label"], FONT_TINY)
        d.text((btn["x"]-lw//2, btn["y"]-7), btn["label"], font=FONT_TINY,
               fill=BG if is_main else CREAM2)

    draw_nav(d, SCREEN_MUSIC)

def hit_button(x, y):
    """タッチ座標がどのボタンか返す。なければNone"""
    for btn in BUTTONS:
        dx = x - btn["x"]
        dy = y - btn["y"]
        if dx*dx + dy*dy <= (btn["r"]+6)**2:
            return btn["action"]
    return None

def do_action(action, mpd):
    """ボタンアクションを実行"""
    try:
        if action == "play":
            subprocess.run(["mpc", "pause" if mpd["playing"] else "play"], timeout=1)
        elif action == "next":
            subprocess.run(["mpc", "next"], timeout=1)
        elif action == "prev":
            subprocess.run(["mpc", "prev"], timeout=1)
        elif action == "vol_up":
            subprocess.run(["mpc", "volume", "+5"], timeout=1)
        elif action == "vol_down":
            subprocess.run(["mpc", "volume", "-5"], timeout=1)
    except:
        pass
