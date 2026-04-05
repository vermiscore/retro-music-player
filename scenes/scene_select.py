from PIL import Image, ImageDraw
from scenes.common import *

SCENES = [
    {"label": "Landscape", "id": "landscape", "desc": "Country road"},
    {"label": "Dance",     "id": "dance",     "desc": "Steve underwater"},
    {"label": "Rain",      "id": "rain",      "desc": "Rainy night"},
    {"label": "Night",     "id": "night",     "desc": "Coming soon"},
    {"label": "Snow",      "id": "snow",      "desc": "Coming soon"},
    {"label": "Ocean",     "id": "ocean",     "desc": "Coming soon"},
    {"label": "Forest",    "id": "forest",    "desc": "Coming soon"},
]

ITEM_H  = 38
VISIBLE = 4
_scroll = 0

def draw(image, now, mpd, current_scene_id):
    global _scroll
    d = ImageDraw.Draw(image)
    d.rectangle([0,0,W,H], fill=BG)

    total      = len(SCENES)
    max_scroll = max(0, total - VISIBLE)
    _scroll    = max(0, min(_scroll, max_scroll))

    # ヘッダー
    d.rectangle([0,0,W,30], fill=BG2)
    d.line([(0,30),(W,30)], fill=BORDER, width=1)

    # ▲▼（シーンが多い時だけ）
    if total > VISIBLE:
        uc = ACCENT if _scroll > 0          else BORDER
        dc = ACCENT if _scroll < max_scroll else BORDER
        d.text((18, 8), "▲", font=FONT_TINY, fill=uc)
        d.text((32, 8), "▼", font=FONT_TINY, fill=dc)

    d.text((center_x("Scenes", FONT_TINY), 8), "Scenes", font=FONT_TINY, fill=ACCENT)

    for i in range(VISIBLE):
        idx = _scroll + i
        if idx >= total:
            break
        scene = SCENES[idx]
        y = 36 + i * ITEM_H
        active = scene["id"] == current_scene_id
        fill   = BG2 if active else BG
        border = ACCENT if active else BORDER
        d.rectangle([8, y, W-8, y+ITEM_H-4], fill=fill, outline=border, width=1)
        d.text((18, y+6),  scene["label"], font=FONT_SMALL, fill=CREAM if active else CREAM2)
        d.text((18, y+22), scene["desc"],  font=FONT_TINY,  fill=ACCENT if active else MUTED)
        if active:
            d.text((W-30, y+10), "✓", font=FONT_SMALL, fill=ACCENT)

    draw_nav(d, SCREEN_SCENE)

def hit_scene(x, y):
    global _scroll
    total      = len(SCENES)
    max_scroll = max(0, total - VISIBLE)

    # ヘッダーの▲▼
    if 0 <= y <= 30 and total > VISIBLE:
        if 14 <= x <= 28 and _scroll > 0:
            _scroll -= 1
            return None
        if 28 <= x <= 44 and _scroll < max_scroll:
            _scroll += 1
            return None

    for i in range(VISIBLE):
        idx = _scroll + i
        if idx >= total:
            break
        sy = 36 + i * ITEM_H
        if sy <= y <= sy + ITEM_H - 4 and 8 <= x <= W-8:
            return SCENES[idx]["id"]
    return None
