"""Night scene - starry night with twinkling stars"""
from PIL import Image, ImageDraw
from scenes.common import *
import random, math

W2, H2 = 320, 240
_bg = Image.open("/home/pi/scenes/night_bg.png").convert("RGB").resize((W2, H2))

def tw2(text, font):
    d = ImageDraw.Draw(Image.new("RGB", (1, 1)))
    b = d.textbbox((0, 0), text, font=font)
    return b[2] - b[0]

class Star:
    def __init__(self):
        self.x = random.randint(0, W2)
        self.y = random.randint(0, H2 // 2)
        self.phase = random.uniform(0, math.pi * 2)
        self.speed = random.uniform(0.03, 0.08)
        self.size = random.randint(1, 3)
    def update(self):
        self.phase += self.speed
    def draw(self, img):
        alpha = int((math.sin(self.phase) + 1) / 2 * 200 + 55)
        star = Image.new("RGBA", (W2, H2), (0, 0, 0, 0))
        d = ImageDraw.Draw(star)
        d.ellipse([self.x - self.size, self.y - self.size,
                   self.x + self.size, self.y + self.size],
                  fill=(255, 255, 200, alpha))
        img.alpha_composite(star)

_stars = [Star() for _ in range(60)]
_scroll_x = 0
_scroll_pause = 0
_last_song = ""

def draw_frame(image, now, mpd, scroll_x):
    global _scroll_x, _scroll_pause, _last_song
    img = _bg.copy().convert("RGBA")
    for s in _stars:
        s.update()
        s.draw(img)
    img_rgb = img.convert("RGB")
    d = ImageDraw.Draw(img_rgb)
    if mpd["song"] != _last_song:
        _last_song = mpd["song"]; _scroll_x = 0; _scroll_pause = 0
    if tw2(mpd["song"], FONT_SMALL) > W2 - 36:
        if _scroll_pause < 50: _scroll_pause += 1
        else: _scroll_x += 1.2
    bar = Image.new("RGBA", (W2, 52), (10, 8, 20, 160))
    img_rgb.paste(Image.fromarray(__import__('numpy').array(bar)[:,:,:3]), (0, 0), bar)
    ts = now.strftime("%H:%M")
    tx = (W2 - tw2(ts, FONT_LARGE)) // 2
    d.text((tx+1, 5), ts, font=FONT_LARGE, fill=(10, 8, 20))
    d.text((tx, 4), ts, font=FONT_LARGE, fill=CREAM)
    d.text((W2 - tw2(now.strftime("%m/%d"), FONT_TINY) - 6, 6), now.strftime("%m/%d"), font=FONT_TINY, fill=CREAM2)
    bar2 = Image.new("RGBA", (W2, 26), (10, 8, 20, 148))
    img_rgb.paste(Image.fromarray(__import__('numpy').array(bar2)[:,:,:3]), (0, H2-26), bar2)
    icon = "▶" if mpd["playing"] else "⏸"
    d.text((7, H2-20), icon, font=FONT_TINY, fill=SAGE if mpd["playing"] else MUTED)
    sw = tw2(mpd["song"], FONT_SMALL)
    area_x = 26; area_w = W2 - area_x - 6
    if sw <= area_w:
        d.text((area_x, H2-20), mpd["song"], font=FONT_SMALL, fill=CREAM2)
    else:
        gap = 38; loop_w = sw + gap
        off = Image.new("RGB", (loop_w*2, 18), (10, 8, 20))
        od = ImageDraw.Draw(off)
        od.text((0, 1), mpd["song"], font=FONT_SMALL, fill=CREAM2)
        od.text((loop_w, 1), mpd["song"], font=FONT_SMALL, fill=CREAM2)
        crop_x = int(_scroll_x) % loop_w
        img_rgb.paste(off.crop((crop_x, 0, crop_x+area_w, 18)), (area_x, H2-20))
    image.paste(img_rgb, (0, 0))
