"""
Rain scene - rainy night street with animated raindrops
draw_frame(image, now, mpd, scroll_x) を main.py から呼ぶ
"""
from PIL import Image, ImageDraw
from scenes.common import *
import random

W2, H2 = 320, 240
_bg = Image.open("/home/pi/scenes/rain_bg.png").convert("RGB").resize((W2, H2))

def tw2(text, font):
    d = ImageDraw.Draw(Image.new("RGB", (1, 1)))
    b = d.textbbox((0, 0), text, font=font)
    return b[2] - b[0]

class RainDrop:
    def __init__(self, random_y=False):
        self.reset(random_y)
    def reset(self, random_y=False):
        self.x = random.uniform(0, W2)
        self.y = random.uniform(0, H2) if random_y else random.uniform(-20, 0)
        # 奥行き：depth 0=遠い 1=近い
        self.depth = random.uniform(0.0, 1.0)
        self.speed = 5 + self.depth * 12        # 遠い→遅い、近い→速い
        self.length = 4 + self.depth * 14       # 遠い→短い、近い→長い
        self.width = max(1, int(self.depth * 2))# 遠い→1px、近い→2px
        self.angle = 0.15
        alpha = int(40 + self.depth * 120)      # 遠い→薄い、近い→濃い
        brightness = int(80 + self.depth * 60) # 遠い→やや灰、近い→白
        self.color = (brightness, int(brightness * 0.75), int(brightness * 0.45), alpha)
    def update(self):
        self.x += self.angle * self.speed * 0.3
        self.y += self.speed
        if self.y > H2 + 20:
            self.reset()
    def draw(self, img):
        dx = self.angle * self.length * 0.4
        drop = Image.new("RGBA", (W2, H2), (0, 0, 0, 0))
        d = ImageDraw.Draw(drop)
        d.line(
            [(int(self.x), int(self.y)),
             (int(self.x + dx), int(self.y + self.length))],
            fill=self.color,
            width=self.width
        )
        img.alpha_composite(drop)

# 遠い雨多め、近い雨少なめ
_drops = []
for _ in range(60):
    dr = RainDrop(random_y=True)
    dr.depth = random.uniform(0.0, 0.4)  # 遠い層
    _drops.append(dr)
for _ in range(25):
    dr = RainDrop(random_y=True)
    dr.depth = random.uniform(0.4, 0.75) # 中間層
    _drops.append(dr)
for _ in range(10):
    dr = RainDrop(random_y=True)
    dr.depth = random.uniform(0.75, 1.0) # 近い層
    _drops.append(dr)

_scroll_x = 0
_scroll_pause = 0
_last_song = ""

def draw_frame(image, now, mpd, scroll_x):
    global _scroll_x, _scroll_pause, _last_song

    img = _bg.copy().convert("RGBA")

    # 奥から手前の順に描画
    for drop in sorted(_drops, key=lambda d: d.depth):
        drop.update()
        drop.draw(img)

    img_rgb = img.convert("RGB")
    d = ImageDraw.Draw(img_rgb)

    if mpd["song"] != _last_song:
        _last_song = mpd["song"]; _scroll_x = 0; _scroll_pause = 0
    if tw2(mpd["song"], FONT_SMALL) > W2 - 36:
        if _scroll_pause < 50: _scroll_pause += 1
        else: _scroll_x += 1.2

    bar = Image.new("RGBA", (W2, 52), (10, 8, 5, 160))
    img_rgb.paste(Image.fromarray(__import__('numpy').array(bar)[:,:,:3]), (0, 0), bar)
    ts = now.strftime("%H:%M")
    tx = (W2 - tw2(ts, FONT_LARGE)) // 2
    d.text((tx+1, 5), ts, font=FONT_LARGE, fill=(20, 15, 5))
    d.text((tx, 4), ts, font=FONT_LARGE, fill=CREAM)
    d.text((W2 - tw2(now.strftime("%m/%d"), FONT_TINY) - 6, 6), now.strftime("%m/%d"), font=FONT_TINY, fill=CREAM2)

    bar2 = Image.new("RGBA", (W2, 26), (10, 8, 5, 148))
    img_rgb.paste(Image.fromarray(__import__('numpy').array(bar2)[:,:,:3]), (0, H2-26), bar2)
    icon = "▶" if mpd["playing"] else "⏸"
    d.text((7, H2-20), icon, font=FONT_TINY, fill=SAGE if mpd["playing"] else MUTED)
    sw = tw2(mpd["song"], FONT_SMALL)
    area_x = 26; area_w = W2 - area_x - 6
    if sw <= area_w:
        d.text((area_x, H2-20), mpd["song"], font=FONT_SMALL, fill=CREAM2)
    else:
        gap = 38; loop_w = sw + gap
        off = Image.new("RGB", (loop_w*2, 18), (10, 8, 5))
        od = ImageDraw.Draw(off)
        od.text((0, 1), mpd["song"], font=FONT_SMALL, fill=CREAM2)
        od.text((loop_w, 1), mpd["song"], font=FONT_SMALL, fill=CREAM2)
        crop_x = int(_scroll_x) % loop_w
        img_rgb.paste(off.crop((crop_x, 0, crop_x+area_w, 18)), (area_x, H2-20))

    image.paste(img_rgb, (0, 0))
