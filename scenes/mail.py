from PIL import Image, ImageDraw
from scenes.common import *
import json, textwrap

MESSAGES_FILE = "/home/pi/messages.json"

MODE_LIST   = 0
MODE_DETAIL = 1

_mode      = MODE_LIST
_sel_idx   = 0
_scroll    = 0
VISIBLE    = 4

def load_messages():
    try:
        with open(MESSAGES_FILE, "r") as f:
            return json.load(f)
    except:
        return []

def save_messages(msgs):
    try:
        with open(MESSAGES_FILE, "w") as f:
            json.dump(msgs, f, ensure_ascii=False, indent=2)
    except:
        pass

def _btn(label, cx, cy, w=65, h=22):
    return {"label": label, "x1": cx-w//2, "y1": cy-h//2, "x2": cx+w//2, "y2": cy+h//2}

def _draw_btn(d, btn, active=False):
    fill    = ACCENT if active else BG2
    outline = ACCENT if active else BORDER
    d.rounded_rectangle([btn["x1"],btn["y1"],btn["x2"],btn["y2"]], radius=4, fill=fill, outline=outline, width=1)
    lw = text_w(btn["label"], FONT_TINY)
    tx = (btn["x1"]+btn["x2"])//2 - lw//2
    ty = (btn["y1"]+btn["y2"])//2 - 7
    d.text((tx, ty), btn["label"], font=FONT_TINY, fill=BG if active else CREAM2)

def _hit(btn, x, y):
    return btn["x1"] <= x <= btn["x2"] and btn["y1"] <= y <= btn["y2"]

def draw(image, now, mpd, scroll_x):
    d = ImageDraw.Draw(image)
    d.rectangle([0,0,W,H], fill=BG)
    msgs = load_messages()
    if _mode == MODE_LIST:
        _draw_list(image, d, msgs)
    else:
        _draw_detail(image, d, msgs)
    draw_nav(d, SCREEN_MAIL)

def _draw_list(image, d, msgs):
    global _scroll
    reversed_msgs = list(reversed(msgs))
    total = len(reversed_msgs)
    max_scroll = max(0, total - VISIBLE)
    _scroll = max(0, min(_scroll, max_scroll))

    # ヘッダー
    d.rectangle([0,0,W,28], fill=BG2)
    d.line([(0,28),(W,28)], fill=BORDER, width=1)

    # ▲▼ 左側（スクロールある時だけ）
    if total > VISIBLE:
        up_col   = ACCENT if _scroll > 0          else BORDER
        down_col = ACCENT if _scroll < max_scroll else BORDER
        d.text((18, 7), "▲", font=FONT_TINY, fill=up_col)
        d.text((42, 7), "▼", font=FONT_TINY, fill=down_col)

    d.text((center_x("Messages", FONT_TINY), 7), "Messages", font=FONT_TINY, fill=ACCENT)
    count = f"{len(msgs)} msgs" if msgs else ""
    d.text((W - text_w(count, FONT_TINY) - 6, 7), count, font=FONT_TINY, fill=MUTED)

    if not msgs:
        d.text((center_x("No messages", FONT_SMALL), 90), "No messages", font=FONT_SMALL, fill=MUTED)
        d.text((center_x("Send from WebUI", FONT_TINY), 115), "Send from WebUI", font=FONT_TINY, fill=BORDER)
        return

    item_h = 36
    for i in range(VISIBLE):
        idx = _scroll + i
        if idx >= total:
            break
        msg = reversed_msgs[idx]
        real_idx = total - 1 - idx
        y = 30 + i * item_h

        bg_col = BG2 if real_idx == _sel_idx else BG
        d.rectangle([0, y, W, y+item_h-1], fill=bg_col)
        d.line([(0, y+item_h-1),(W, y+item_h-1)], fill=BORDER, width=1)

        d.text((W - text_w(msg.get("time",""), FONT_TINY) - 8, y+5),
               msg.get("time",""), font=FONT_TINY, fill=MUTED)

        preview = msg.get("text","").split('\n')[0][:28]
        d.text((10, y+5), preview, font=FONT_TINY, fill=CREAM)

        lines = textwrap.wrap(msg.get("text",""), width=32)
        if len(lines) > 1:
            d.text((10, y+20), lines[1][:30]+"...", font=FONT_TINY, fill=MUTED)

def _draw_detail(image, d, msgs):
    if not msgs or _sel_idx >= len(msgs):
        return
    msg = msgs[_sel_idx]

    d.rectangle([0,0,W,28], fill=BG2)
    d.line([(0,28),(W,28)], fill=BORDER, width=1)

    btn_back = _btn("< Back", 35, 14, w=52, h=20)
    btn_del  = _btn("Delete", W-35, 14, w=52, h=20)
    _draw_btn(d, btn_back)
    _draw_btn(d, btn_del)

    counter = f"{_sel_idx+1}/{len(msgs)}"
    d.text((center_x(counter, FONT_TINY), 7), counter, font=FONT_TINY, fill=MUTED)

    d.text((12, 34), msg.get("time",""), font=FONT_TINY, fill=ACCENT)
    d.line([(12,50),(W-12,50)], fill=BORDER, width=1)

    lines = []
    for para in msg.get("text","").split('\n'):
        wrapped = textwrap.wrap(para, width=28)
        lines.extend(wrapped if wrapped else [''])

    y = 56
    for line in lines[:8]:
        d.text((12, y), line, font=FONT_TINY, fill=CREAM)
        y += 17

def handle_touch(x, y):
    global _mode, _sel_idx, _scroll

    msgs = load_messages()
    reversed_msgs = list(reversed(msgs))
    total = len(reversed_msgs)
    max_scroll = max(0, total - VISIBLE)

    if _mode == MODE_LIST:
        if not msgs:
            return

        # ヘッダー内の▲▼タップ
        if 0 <= y <= 28:
            if 14 <= x <= 28 and _scroll > 0:
                _scroll -= 1
            elif 38 <= x <= 54 and _scroll < max_scroll:
                _scroll += 1
            return

        # アイテムタップ
        item_h = 36
        for i in range(VISIBLE):
            idx = _scroll + i
            if idx >= total:
                break
            iy = 30 + i * item_h
            if iy <= y <= iy + item_h - 1:
                _sel_idx = total - 1 - idx
                _mode = MODE_DETAIL
                return

    elif _mode == MODE_DETAIL:
        btn_back = _btn("< Back", 35, 14, w=52, h=20)
        btn_del  = _btn("Delete", W-35, 14, w=52, h=20)

        if _hit(btn_back, x, y):
            _mode = MODE_LIST
        elif _hit(btn_del, x, y):
            msgs.pop(_sel_idx)
            save_messages(msgs)
            if _sel_idx >= len(msgs):
                _sel_idx = max(0, len(msgs)-1)
            _mode = MODE_LIST
