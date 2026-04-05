from PIL import Image, ImageDraw
from scenes.common import *

def draw(image, now, mpd, scroll_x):
    d = ImageDraw.Draw(image)
    d.rectangle([0,0,W,H], fill=BG)

    # 装飾
    _botanical(d, 18,  120, 0.7)
    _botanical(d, W-18,120, 0.6)

    # 時刻
    time_str = now.strftime("%H:%M")
    d.text((center_x(time_str, FONT_LARGE), 18), time_str, font=FONT_LARGE, fill=CREAM)

    # 日付
    date_str = now.strftime("%Y.%m.%d")
    d.text((center_x(date_str, FONT_SMALL), 74), date_str, font=FONT_SMALL, fill=CREAM2)

    # 曜日バッジ
    day = now.strftime("%a").upper()
    dw  = text_w(day, FONT_TINY)
    bx  = (W - dw - 12) // 2
    d.rounded_rectangle([bx, 98, bx+dw+12, 116], radius=4, fill=ACCENT2)
    d.text((bx+6, 99), day, font=FONT_TINY, fill=CREAM)

    # 区切り
    d.line([(40,128),(W-40,128)], fill=BORDER, width=1)
    d.ellipse([W//2-3,125,W//2+3,131], fill=ACCENT2)

    # 曲名
    icon  = "▶" if mpd["playing"] else "♪"
    color = SAGE if mpd["playing"] else MUTED
    d.text((14, 143), icon, font=FONT_TINY, fill=color)
    draw_scroll_text(image, mpd["song"], FONT_SMALL, 32, 141, W-44, CREAM2, scroll_x)

    draw_nav(d, SCREEN_HOME)

def _botanical(d, x, y, scale):
    s = scale
    d.line([(x,y),(x,int(y-40*s))], fill=BORDER, width=1)
    d.ellipse([int(x-18*s),int(y-35*s),int(x-2*s),int(y-22*s)], outline=BORDER, width=1)
    d.ellipse([int(x+2*s),int(y-28*s),int(x+18*s),int(y-15*s)], outline=BORDER, width=1)
    d.ellipse([int(x-8*s),int(y-52*s),int(x+8*s),int(y-38*s)], outline=BORDER, width=1)
    d.ellipse([int(x-5*s),int(y-58*s),int(x+5*s),int(y-48*s)], fill=ACCENT2, outline=ACCENT)
