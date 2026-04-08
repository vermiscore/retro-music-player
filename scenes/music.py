from PIL import Image, ImageDraw
from scenes.common import *
import subprocess

GENRES = ["all", "classical", "jazz", "lofi", "acoustic", "metal", "others", "test1", "test2", "test3"]
GENRE_LABELS = ["All", "Classical", "Jazz", "Lofi", "Acoustic", "Metal", "Others", "Test1", "Test2", "Test3"]

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

# ジャンルボタン（四角）
GENRE_BTN_X = 14
GENRE_BTN_Y = 115
GENRE_BTN_W = 32
GENRE_BTN_H = 20

_current_genre = "all"
_show_genre_select = False
_genre_scroll = 0
ROWS_PER_PAGE = 4

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

def set_genre(genre):
    global _current_genre
    _current_genre = genre
    try:
        subprocess.run(["mpc", "clear"], timeout=1)
        if genre == "all":
            subprocess.run(["bash", "-c", "mpc ls | mpc add"], timeout=5)
        else:
            subprocess.run(["bash", "-c", f"mpc ls {genre} | mpc add"], timeout=5)
        subprocess.run(["mpc", "play"], timeout=1)
        import threading
        threading.Thread(target=lambda: subprocess.run(
            ["sudo", "systemctl", "restart", "i2s-fix"], timeout=10), daemon=True).start()
    except:
        pass

def draw(image, now, mpd, scroll_x):
    global _show_genre_select

    d = ImageDraw.Draw(image)
    d.rectangle([0, 0, W, H], fill=BG)

    if _show_genre_select:
        _draw_genre_select(d)
        return

    # ヘッダー
    d.rectangle([0, 0, W, 28], fill=BG2)
    d.line([(0, 28), (W, 28)], fill=BORDER, width=1)
    d.text((center_x("Now Playing", FONT_TINY), 7), "Now Playing", font=FONT_TINY, fill=MUTED)

    # 左側: VOLバー
    d.text((VOL_BAR_X, 36), "VOL", font=FONT_TINY, fill=MUTED)
    vol = get_volume()
    d.rectangle([VOL_BAR_X, VOL_BAR_Y, VOL_BAR_X+VOL_BAR_W, VOL_BAR_Y+VOL_BAR_H],
                fill=BG2, outline=BORDER, width=1)
    fill_w = int(VOL_BAR_W * vol / 100)
    if fill_w > 0:
        d.rectangle([VOL_BAR_X, VOL_BAR_Y, VOL_BAR_X+fill_w, VOL_BAR_Y+VOL_BAR_H],
                    fill=SAGE)
    vol_str = f"{vol}%"
    d.text((VOL_BAR_X + VOL_BAR_W//2 - text_w(vol_str, FONT_TINY)//2, VOL_BAR_Y+10),
           vol_str, font=FONT_TINY, fill=CREAM2)

    # ジャンルボタン（四角）
    d.rectangle([GENRE_BTN_X, GENRE_BTN_Y,
                 GENRE_BTN_X+GENRE_BTN_W, GENRE_BTN_Y+GENRE_BTN_H],
                fill=BG2, outline=SAGE, width=1)
    genre_short = _current_genre[:3].upper()
    lw = text_w(genre_short, FONT_TINY)
    d.text((GENRE_BTN_X + GENRE_BTN_W//2 - lw//2, GENRE_BTN_Y + 3),
           genre_short, font=FONT_TINY, fill=SAGE)

    # アルバムアート
    cx, cy, r = 210, 80, 45
    d.ellipse([cx-r, cy-r, cx+r, cy+r], fill=BG2, outline=BORDER, width=1)
    d.ellipse([cx-r+6, cy-r+6, cx+r-6, cy+r-6], outline=BORDER, width=1)
    d.ellipse([cx-6, cy-6, cx+6, cy+6], fill=ACCENT2)
    d.ellipse([cx-3, cy-3, cx+3, cy+3], fill=ACCENT)
    if mpd["playing"]:
        d.ellipse([cx+r-5, cy-r+2, cx+r+2, cy-r+9], fill=SAGE)

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


def _draw_genre_select(d):
    cols = 2
    btn_w = 130
    btn_h = 28
    pad_x = 15
    pad_y = 8
    start_y = 38

    # ヘッダー
    d.rectangle([0, 0, W, 28], fill=BG2)
    d.line([(0, 28), (W, 28)], fill=BORDER, width=1)

    # ▲▼ボタン（横並び、左上）- 四角で大きめ
    up_x, up_y, up_w, up_h = 4, 4, 18, 20
    dn_x, dn_y, dn_w, dn_h = 25, 4, 18, 20
    max_scroll = max(0, (len(GENRES) + cols - 1) // cols - ROWS_PER_PAGE)

    d.rectangle([up_x, up_y, up_x+up_w, up_y+up_h], fill=BG2, outline=BORDER, width=1)
    d.text((up_x+4, up_y+4), "▲", font=FONT_TINY,
           fill=MUTED if _genre_scroll == 0 else CREAM2)

    d.rectangle([dn_x, dn_y, dn_x+dn_w, dn_y+dn_h], fill=BG2, outline=BORDER, width=1)
    d.text((dn_x+4, dn_y+4), "▼", font=FONT_TINY,
           fill=MUTED if _genre_scroll >= max_scroll else CREAM2)

    # タイトル（▲▼の右側、中央寄せ）
    title = "Select Genre"
    title_area_start = 50
    title_area_w = W - title_area_start
    lw = text_w(title, FONT_TINY)
    d.text((title_area_start + (title_area_w - lw)//2, 7),
           title, font=FONT_TINY, fill=MUTED)

    # ジャンルボタン
    items_per_page = cols * ROWS_PER_PAGE
    start_idx = _genre_scroll * cols
    visible = list(zip(GENRES, GENRE_LABELS))[start_idx:start_idx + items_per_page]

    for i, (genre, label) in enumerate(visible):
        col = i % cols
        row = i // cols
        x = pad_x + col * (btn_w + pad_x)
        y = start_y + row * (btn_h + pad_y)

        is_active = genre == _current_genre
        fill = ACCENT2 if is_active else BG2
        outline = ACCENT if is_active else BORDER

        d.rectangle([x, y, x+btn_w, y+btn_h], fill=fill, outline=outline, width=1)
        lw = text_w(label, FONT_TINY)
        text_color = BG if is_active else CREAM2
        d.text((x + btn_w//2 - lw//2, y + btn_h//2 - 6), label, font=FONT_TINY, fill=text_color)

    # Closeボタン
    close_y = start_y + ROWS_PER_PAGE * (btn_h + pad_y) + 2
    close_h = 22
    d.rectangle([pad_x, close_y, pad_x + btn_w*2 + pad_x, close_y + close_h],
                fill=BG2, outline=BORDER, width=1)
    lw = text_w("Close", FONT_TINY)
    d.text((W//2 - lw//2, close_y + close_h//2 - 6), "Close", font=FONT_TINY, fill=MUTED)
    draw_nav(d, SCREEN_MUSIC)




def hit_button(x, y):
    global _show_genre_select

    if _show_genre_select:
        return _hit_genre_select(x, y)

    # ジャンルボタン（四角）
    if GENRE_BTN_X <= x <= GENRE_BTN_X+GENRE_BTN_W and GENRE_BTN_Y <= y <= GENRE_BTN_Y+GENRE_BTN_H:
        return "genre_menu"

    for btn in BUTTONS:
        dx = x - btn["x"]
        dy = y - btn["y"]
        if dx*dx + dy*dy <= (btn["r"]+6)**2:
            return btn["action"]
    return None


def _hit_genre_select(x, y):
    global _genre_scroll

    cols = 2
    btn_w = 130
    btn_h = 28
    pad_x = 15
    pad_y = 8
    start_y = 38

    # ▲ボタン（タッチ範囲広め）
    up_x, up_y, up_w, up_h = 4, 4, 18, 20
    if up_x <= x <= up_x+up_w and up_y <= y <= up_y+up_h:
        if _genre_scroll > 0:
            _genre_scroll -= 1
        return "genre_scroll"

    # ▼ボタン
    dn_x, dn_y, dn_w, dn_h = 25, 4, 18, 20
    if dn_x <= x <= dn_x+dn_w and dn_y <= y <= dn_y+dn_h:
        max_scroll = max(0, (len(GENRES) + cols - 1) // cols - ROWS_PER_PAGE)
        if _genre_scroll < max_scroll:
            _genre_scroll += 1
        return "genre_scroll"

    # ジャンルボタン
    items_per_page = cols * ROWS_PER_PAGE
    start_idx = _genre_scroll * cols
    visible_genres = GENRES[start_idx:start_idx + items_per_page]

    for i, genre in enumerate(visible_genres):
        col = i % cols
        row = i // cols
        bx = pad_x + col * (btn_w + pad_x)
        by = start_y + row * (btn_h + pad_y)
        if bx <= x <= bx+btn_w and by <= y <= by+btn_h:
            return f"genre_{genre}"

    # Closeボタン
    close_y = start_y + ROWS_PER_PAGE * (btn_h + pad_y) + 2
    close_h = 22
    if pad_x <= x <= pad_x + btn_w*2 + pad_x and close_y <= y <= close_y + close_h:
        return "genre_close"

    return None


def do_action(action, mpd):
    global _show_genre_select

    if action == "genre_menu":
        _show_genre_select = True
        return

    if action == "genre_close":
        _show_genre_select = False
        return

    if action == "genre_scroll":
        return

    if action and action.startswith("genre_"):
        genre = action[6:]
        set_genre(genre)
       # _show_genre_select = False
        return
    
    try:
        if action == "play":
            subprocess.run(["mpc", "pause" if mpd["playing"] else "play"], timeout=1)
            if not mpd["playing"]:
                import threading
                threading.Thread(target=lambda: subprocess.run(
                    ["sudo", "systemctl", "restart", "i2s-fix"], timeout=10), daemon=True).start()
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

