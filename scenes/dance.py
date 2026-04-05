"""
Dance scene - Steve dancing underwater
draw_frame(image, now, mpd, scroll_x) を main.py から呼ぶ
"""
from PIL import Image, ImageDraw
from scenes.common import *
import cv2
import numpy as np

W2, H2 = 320, 240

_bg = Image.open("/home/pi/scenes/ocean_bg.png").convert("RGB").resize((W2, H2))
_bg_np = np.array(_bg)

_cap = cv2.VideoCapture("/home/pi/scenes/steve_dance.mp4")
_total_frames = int(_cap.get(cv2.CAP_PROP_FRAME_COUNT))

def tw2(text, font):
    d = ImageDraw.Draw(Image.new("RGB", (1, 1)))
    b = d.textbbox((0, 0), text, font=font)
    return b[2] - b[0]

def _get_next_frame():
    ret, frame = _cap.read()
    if not ret:
        _cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
    ret, frame = _cap.read()
    if not ret:
        return None
    # リサイズ
    frame = cv2.resize(frame, (W2, H2))
    # グリーンバック除去
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    lower_green = np.array([40, 40, 40])
    upper_green = np.array([80, 255, 255])
    mask = cv2.inRange(hsv, lower_green, upper_green)
    mask_inv = cv2.bitwise_not(mask)
    # 背景と合成
    bg = _bg_np.copy()
    fg = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    bg[mask_inv > 0] = fg[mask_inv > 0]
    return Image.fromarray(bg)

_scroll_x = 0
_scroll_pause = 0
_last_song = ""
_frame_skip = 0

def draw_frame(image, now, mpd, scroll_x):
    global _scroll_x, _scroll_pause, _last_song, _frame_skip

    # 2フレームに1回だけ読む（負荷軽減）
    _frame_skip += 1
    if _frame_skip % 1 == 0:
        frame = _get_next_frame()
        if frame:
            image.paste(frame, (0, 0))
            draw_frame._last_frame = frame
    elif hasattr(draw_frame, '_last_frame'):
        image.paste(draw_frame._last_frame, (0, 0))

    d = ImageDraw.Draw(image)

    if mpd["song"] != _last_song:
        _last_song = mpd["song"]; _scroll_x = 0; _scroll_pause = 0
    if tw2(mpd["song"], FONT_SMALL) > W2 - 36:
        if _scroll_pause < 50: _scroll_pause += 1
        else: _scroll_x += 1.2

    # 下部バー
    bar2 = Image.new("RGBA", (W2, 26), (0, 20, 40, 160))
    image.paste(Image.fromarray(np.array(bar2)[:,:,:3]), (0, H2-26), bar2)
    icon = "▶" if mpd["playing"] else "⏸"
    d.text((7, H2-20), icon, font=FONT_TINY, fill=SAGE if mpd["playing"] else MUTED)
    sw = tw2(mpd["song"], FONT_SMALL)
    area_x = 26; area_w = W2 - area_x - 6
    if sw <= area_w:
        d.text((area_x, H2-20), mpd["song"], font=FONT_SMALL, fill=CREAM2)
    else:
        gap = 38; loop_w = sw + gap
        off = Image.new("RGB", (loop_w*2, 18), (0, 20, 40))
        od = ImageDraw.Draw(off)
        od.text((0, 1), mpd["song"], font=FONT_SMALL, fill=CREAM2)
        od.text((loop_w, 1), mpd["song"], font=FONT_SMALL, fill=CREAM2)
        crop_x = int(_scroll_x) % loop_w
        image.paste(off.crop((crop_x, 0, crop_x+area_w, 18)), (area_x, H2-20))
