"""Snow scene - snowflakes falling"""
from PIL import Image, ImageDraw
from scenes.common import *
import random

W2, H2 = 320, 240
_bg = Image.open("/home/pi/scenes/snow_bg.png").convert("RGB").resize((W2, H2))

def tw2(text, font):
    d = ImageDraw.Draw(Image.new("RGB", (1, 1)))
    b = d.textbbox((0, 0), text, font=font)
    return b[2] - b[0]

class Snowflake:
    def __init__(self, random_y=False):
        self.reset(random_y)
    def reset(self, random_y=False):
        self.x = random.uniform(0, W2)
        self.y = random.uniform(0, H2) if random_y else random.uniform(-10, 0)
        self.size = random.uniform(1.5, 4.0)
        self.speed = random.uniform(0.8, 2.5)
        self.drift = random.uniform(-0.3, 0.3)
        self.alpha = random.randint(160, 240)
    def update(self):
        self.x += self.drift
        self.y += self.speed
        if self.y > H2 + 10:
            self.reset()
    def draw(self, img):
        flake = Image.new("RGBA", (W2, H2), (0, 0, 0, 0))
        d = ImageDraw.Draw(flake)
        s = self.size
        d.ellipse([self.x-s, self.y-s, self.x+s, self.y+s],
                  fill=(240, 248, 255, self.alpha))
        img.alpha_composite(flake)

_flakes = [Snowflake(random_y=True) for _ in range(80)]
_scroll_x = 0
_scroll_pause = 0
_last_song = ""

def draw_frame(image, now, mpd, scroll_x):
    global _scroll_x, _scroll_pause, _last_song
    img = _bg.copy().convert("RGBA")
    for f in _flakes:
        f.update()
        f.draw(img)
    img_rgb = img.convert("RGB")
    d = ImageDraw.Draw(img_rgb)
    if mpd["song"] != _last_song:
        _last_song = mpd["song"]; _scroll_x = 0; _scroll_pause = 0
    if tw2(mpd["song"], FONT_SMALL) > W2 - 36:
        if _scroll_pause < 50: _scroll_pause += 1
        else: _scroll_x += 1.2
    bar = Image.new("RGBA", (W2, 52), (20, 30, 40, 160))
    img_rgb.paste(Image.fromarray(__import__('numpy').array(bar)[:,:,:3]), (0, 0), bar)
    ts = now.strftime("%H:%M")
    tx = (W2 - tw2(ts, FONT_LARGE)) // 2
    d.text((tx+1, 5), ts, font=FONT_LARGE, fill=(20, 30, 40))
    d.text((tx, 4), ts, font=FONT_LARGE, fill=CREAM)
    d.text((W2 - tw2(now.strftime("%m/%d"), FONT_TINY) - 6, 6), now.strftime("%m/%d"), font=FONT_TINY, fill=CREAM2)
    bar2 = Image.new("RGBA", (W2, 26), (20, 30, 40, 148))
    img_rgb.paste(Image.fromarray(__import__('numpy').array(bar2)[:,:,:3]), (0, H2-26), bar2)
    icon = "▶" if mpd["playing"] else "⏸"
    d.text((7, H2-20), icon, font=FONT_TINY, fill=SAGE if mpd["playing"] else MUTED)
    sw = tw2(mpd["song"], FONT_SMALL)
    area_x = 26; area_w = W2 - area_x - 6
    if sw <= area_w:
        d.text((area_x, H2-20), mpd["song"], font=FONT_SMALL, fill=CREAM2)
    else:
        gap = 38; loop_w = sw + gap
        off = Image.new("RGB", (loop_w*2, 18), (20, 30, 40))
        od = ImageDraw.Draw(off)
        od.text((0, 1), mpd["song"], font=FONT_SMALL, fill=CREAM2)
        od.text((loop_w, 1), mpd["song"], font=FONT_SMALL, fill=CREAM2)
        crop_x = int(_scroll_x) % loop_w
        img_rgb.paste(off.crop((crop_x, 0, crop_x+area_w, 18)), (area_x, H2-20))
    image.paste(img_rgb, (0, 0))
