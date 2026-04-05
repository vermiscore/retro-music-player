from PIL import Image, ImageDraw
from scenes.common import *

def draw(image, now, mpd, scroll_x):
    d = ImageDraw.Draw(image)
    d.rectangle([0,0,W,H], fill=BG)

    # 装飾
    _botanical(d, 25,  193, 0.85)
    _botanical(d, W-25,193, 0.85)

    # 大きな時刻
    time_str = now.strftime("%H:%M")
    d.text((center_x(time_str, FONT_HUGE), 28), time_str, font=FONT_HUGE, fill=CREAM)

    # 日付
    date_str = now.strftime("%B %d, %Y")
    d.text((center_x(date_str, FONT_SMALL), 136), date_str, font=FONT_SMALL, fill=CREAM2)

    # 曜日
    day_str = now.strftime("%A")
    d.text((center_x(day_str, FONT_TINY), 160), day_str, font=FONT_TINY, fill=MUTED)

    # ミニ曲名
    if mpd["song"] != "No song":
        icon = "▶" if mpd["playing"] else "♪"
        d.text((14, 182), icon, font=FONT_TINY, fill=SAGE if mpd["playing"] else MUTED)
        draw_scroll_text(image, mpd["song"], FONT_TINY, 30, 182, W-44, MUTED, scroll_x)

    draw_nav(d, SCREEN_CLOCK)

def _botanical(d, x, y, scale):
    s = scale
    d.line([(x,y),(x,int(y-38*s))], fill=BORDER, width=1)
    d.ellipse([int(x-16*s),int(y-33*s),int(x-2*s),int(y-21*s)], outline=BORDER, width=1)
    d.ellipse([int(x+2*s),int(y-26*s),int(x+16*s),int(y-14*s)], outline=BORDER, width=1)
    d.ellipse([int(x-7*s),int(y-50*s),int(x+7*s),int(y-36*s)], outline=BORDER, width=1)
    d.ellipse([int(x-4*s),int(y-55*s),int(x+4*s),int(y-46*s)], fill=ACCENT2, outline=ACCENT)
