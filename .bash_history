sudo raspi-config
sudo reboot
ls /dev/spi*
sudo apt install python3-pip python3-dev python3-pil -y
pip3 install luma.lcd --break-system-packages
nano test_display.py
python3 test_display.py
nano test_display.py
python3 test_display.py
nano test_display.py
python3 test_display.py
nano test_display.py
python3 test_display.py
sudo apt install fonts-dejavu -y
nano display.py
python3 display.py
python3 -c "import subprocess; r = subprocess.run(['mpc', 'current'], capture_output=True, text=True); print(repr(r.stdout))"
python3 display.py
sudo nano /etc/systemd/system/display.service
sudo systemctl enable display
sudo systemctl start display
sudo systemctl status display
sudo reboot
mpc clear
mpc add directtodreams-gymnopedie-satie-remix-267051.mp3
mpc play
mpc current
mpc next
mpc clear
mpc add .
mpc play
mpc next
mpc clear
mpc ls | mpc add
mpc play
mpc next
exit
curl -fsSL https://tailscale.com/install.sh | sh
sudo tailscale up
tailscale ip
ezit
ls ~/Downloads/app.py ~/Downloads/index.html
exit
rm -rf ~/.vscode-server[
rm -rf ~/.vscode-server
mpc status
pip3 install luma.lcd evdev --break-system-packages
ls /dev/input/
sudo evtest /dev/input/event0
sudo apt install evtest -y
sudo evtest /dev/input/event0
sudo evtest /dev/input/event1
python3 /home/pi/app.py
scp ~/Downloads/"display(1).py" pi@192.168.0.35:/home/pi/display.py
sudo systemctl restart display
sudo systemctl status display
sudo systemctl restart display
scp ~/Downloads/display.py pi@192.168.0.35:/home/pi/display.py
sudo systemctl restart display
sudo nano /etc/systemd/system/flask.service
sudo systemctl enable flask
sudo systemctl start flask
sudo systemctl status flask]
sudo systemctl status flask
pip3 install numpy --break-system-packages
sudo systemctl restart display
sudo systemctl status display
grep "draw_building_perspective" /home/pi/display.py
sudo reboot
sudo systemctl enable tailscaled
pip3 install flask python-mpd2 --break-system-packages
# PCのターミナルで（Piからexitした状態で）
scp app.py pi@192.168.0.35:/home/pi/app.py
scp index.html pi@192.168.0.35:/home/pi/templates/index.html
ssh pi@192.168.0.35 "mkdir -p /home/pi/templates /home/pi/photos"
ssh pi@192.168.0.35
ls /dev/input/
sudo nano /boot/firmware/config.txt
sudo reboot
sudo evtest /dev/input/event2
cat /boot/firmware/config.txt | tail -10
sudo nano /boot/firmware/config.txt
sudo reboot
pip3 install spidev --break-system-packages
nano /home/pi/touch_test.py
python3 /home/pi/touch_test.py
nano /home/pi/touch_test.py
python3 /home/pi/touch_test.py
sudo systemctl stop display
python3 /home/pi/touch_test.py
nano /home/pi/touch_test.py
python3 /home/pi/touch_test.py
sudo dmesg | grep -i spi
[200~sudo dmesg | grep -i "ili9341\|ads7846\|spi"~
sudo dmesg | grep -i "ili9341\|ads7846\|spi"
sudo nano /boot/firmware/config.txt
```

末尾に追加：
```
dtoverlay=ads7846,cs=1,penirq=17,penirq_pull=2,speed=500000,keep_vref_on=1,swapxy=0,pmax=255,xohms=150
sudo reboot
sudo nano /boot/firmware/config.txt
sudo reboot
python3 /home/pi/spi_test3.py
cat > /home/pi/spi_test3.py << 'EOF'
import spidev, time
import RPi.GPIO as GPIO

T_IRQ = 17
GPIO.setmode(GPIO.BCM)
GPIO.setup(T_IRQ, GPIO.IN, pull_up_down=GPIO.PUD_UP)

spi = spidev.SpiDev()
spi.open(0, 1)
spi.max_speed_hz = 125000
spi.mode = 0

print("30秒間モニタリング... 画面を押してください")
for _ in range(300):
    irq = GPIO.input(T_IRQ)
    if irq == 0:
        r = spi.xfer2([0xD0, 0x00, 0x00])
        print(f"タッチ検出! 受信: {[hex(x) for x in r]}")
    time.sleep(0.1)

spi.close()
GPIO.cleanup()
EOF

python3 /home/pi/spi_test3.py
cat > /home/pi/spi_test3.py << 'EOF'
import spidev, time
import RPi.GPIO as GPIO

T_IRQ = 17
GPIO.setmode(GPIO.BCM)
GPIO.setup(T_IRQ, GPIO.IN, pull_up_down=GPIO.PUD_UP)

spi = spidev.SpiDev()
spi.open(0, 1)
spi.max_speed_hz = 125000
spi.mode = 0

print("30秒間モニタリング... 画面を押してください")
for _ in range(300):
    if GPIO.input(T_IRQ) == 0:
        rx = spi.xfer2([0xD0, 0x00, 0x00])
        ry = spi.xfer2([0x90, 0x00, 0x00])
        x = ((rx[1] << 8) | rx[2]) >> 3
        y = ((ry[1] << 8) | ry[2]) >> 3
        print(f"X={x}, Y={y}")
    time.sleep(0.1)

spi.close()
GPIO.cleanup()
EOF

python3 /home/pi/spi_test3.py
cat > /home/pi/touch_calibrate.py << 'EOF'
import spidev, time
import RPi.GPIO as GPIO

T_IRQ = 17
GPIO.setmode(GPIO.BCM)
GPIO.setup(T_IRQ, GPIO.IN, pull_up_down=GPIO.PUD_UP)

spi = spidev.SpiDev()
spi.open(0, 1)
spi.max_speed_hz = 125000
spi.mode = 0

def read_xy():
    rx = spi.xfer2([0xD0, 0x00, 0x00])
    ry = spi.xfer2([0x90, 0x00, 0x00])
    x = ((rx[1] << 8) | rx[2]) >> 3
    y = ((ry[1] << 8) | ry[2]) >> 3
    return x, y

x_min, x_max, y_min, y_max = 9999, 0, 9999, 0

print("60秒間、画面の四隅を何度も押してください...")
for _ in range(600):
    if GPIO.input(T_IRQ) == 0:
        x, y = read_xy()
        x_min = min(x_min, x)
        x_max = max(x_max, x)
        y_min = min(y_min, y)
        y_max = max(y_max, y)
        print(f"X={x}, Y={y}  [範囲: X={x_min}~{x_max}, Y={y_min}~{y_max}]")
    time.sleep(0.1)

print(f"\n=== キャリブレーション結果 ===")
print(f"X_MIN={x_min}, X_MAX={x_max}")
print(f"Y_MIN={y_min}, Y_MAX={y_max}")

spi.close()
GPIO.cleanup()
EOF

python3 /home/pi/touch_calibrate.py
ls /home/pi/
ls /home/pi/templates/ 2>/dev/null
mkdir -p /home/pi/scenes
touch /home/pi/scenes/__init__.py
ssh pi@192.168.0.35
sudo systemctl stop display
python3 /home/pi/main.py
ssh pi@192.168.0.35
python3 /home/pi/touch_debug.py
python3 /home/pi/main.py &
python3 /home/pi/touch_debug.py
cat > /home/pi/touch_debug.py << 'EOF'
import spidev, time
import RPi.GPIO as GPIO

T_IRQ = 17
GPIO.setmode(GPIO.BCM)
GPIO.setup(T_IRQ, GPIO.IN, pull_up_down=GPIO.PUD_UP)

spi = spidev.SpiDev()
spi.open(0, 1)
spi.max_speed_hz = 125000
spi.mode = 0

X_MIN, X_MAX = 251, 3735
Y_MIN, Y_MAX = 220, 3842
W, H = 320, 240

def read():
    rx = spi.xfer2([0xD0, 0x00, 0x00])
    ry = spi.xfer2([0x90, 0x00, 0x00])
    x = ((rx[1] << 8) | rx[2]) >> 3
    y = ((ry[1] << 8) | ry[2]) >> 3
    sx = int((x - X_MIN) / (X_MAX - X_MIN) * W)
    sy = int((y - Y_MIN) / (Y_MAX - Y_MIN) * H)
    return max(0,min(W-1,sx)), max(0,min(H-1,sy))

print("画面の各部分をタップしてください...")
try:
    while True:
        if GPIO.input(T_IRQ) == 0:
            x, y = read()
            nav = y >= H - 36
            print(f"X={x:3d}, Y={y:3d}  {'[NAV]' if nav else '[CONTENT]'}")
            time.sleep(0.2)
except KeyboardInterrupt:
    spi.close()
    GPIO.cleanup()
EOF

python3 /home/pi/touch_debug.py
cat > /home/pi/touch_debug.py << 'EOF'
import sys
sys.path.insert(0, '/home/pi')
import touch, time

print("画面の各部分をタップしてください... Ctrl+Cで終了")
try:
    while True:
        pos = touch.read_touch()
        if pos:
            x, y = pos
            nav = y >= 240 - 36
            print(f"X={x:3d}, Y={y:3d}  {'[NAV]' if nav else '[CONTENT]'}")
            time.sleep(0.2)
except KeyboardInterrupt:
    pass
EOF

python3 /home/pi/touch_debug.py
kill %1
python3 /home/pi/touch_debug.py
nano /home/pi/touch.py
cat /home/pi/touch.py
python3 /home/pi/touch_debug.py
nano /home/pi/touch.py
python3 /home/pi/touch_debug.py
python3 /home/pi/main.py
sudo reboot
nano /home/pi/main.py
sudo nano /etc/systemd/system/display.service
sudo systemctl daemon-reload
sudo systemctl restart display
sudo systemctl status display
python3 /home/pi/main.py 2>&1 | head -20
hostname -I
grep -n "viewport" /home/pi/templates/index.html
head -50 /home/pi/templates/index.html
sed -n '50,150p' /home/pi/templates/index.html
sed -i 's/max-width: 600px/max-width: 768px/' /home/pi/templates/index.html
sed -n '150,250p' /home/pi/templates/index.html
grep -n "canvas\|width.*px\|min-width" /home/pi/templates/index.html | head -30
grep -n "player\|Player" /home/pi/templates/index.html | head -20
sed -n '594,650p' /home/pi/templates/index.html
cat /home/pi/scenes/landscape.py
ls -la /home/pi/scenes/
cat /home/pi/scenes/scene_select.py
cat /home/pi/main.py
tree /home/pi
sudo apt install tree -y
tree /home/pi
nano /home/pi/scenes/rain.py
ls -la /home/pi/scenes/rain.py
nano /home/pi/scenes/rain.py
sudo systemctl restart display
cat /home/pi/scenes/rain.py
cat > /home/pi/scenes/rain.py << 'EOF'
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
        self.speed = random.uniform(8, 16)
        self.length = random.uniform(4, 10)
        self.width = random.uniform(1.5, 3.0)
        self.angle = random.uniform(0.1, 0.2)
        dist = abs(self.x - W2 * 0.72)
        brightness = max(120, 220 - int(dist * 0.4))
        self.color = (brightness, brightness, min(255, brightness + 30), 80)
    def update(self):
        self.x += self.angle * self.speed * 0.3
        self.y += self.speed
        if self.y > H2 + 20:
            self.reset()
    def draw(self, img):
        dx = self.angle * self.length * 0.5
        drop = Image.new("RGBA", (W2, H2), (0, 0, 0, 0))
        d = ImageDraw.Draw(drop)
        x0 = int(self.x - self.width)
        x1 = int(self.x + self.width)
        y0 = int(self.y)
        y1 = int(self.y + self.length)
        d.ellipse([x0 + int(dx), y0, x1 + int(dx), y1], fill=self.color)
        img.alpha_composite(drop)

_drops = [RainDrop(random_y=True) for _ in range(80)]
_scroll_x = 0
_scroll_pause = 0
_last_song = ""

def draw_frame(image, now, mpd, scroll_x):
    global _scroll_x, _scroll_pause, _last_song

    img = _bg.copy().convert("RGBA")
    for drop in _drops:
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
EOF

sudo systemctl restart display
cat > /home/pi/scenes/rain.py << 'EOF'
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
        brightness = int(180 + self.depth * 75) # 遠い→やや灰、近い→白
        self.color = (brightness, brightness, min(255, brightness + 10), alpha)
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
EOF

sudo systemctl restart display
sed -i 's/brightness = int(180 + self.depth \* 75)/brightness = int(80 + self.depth * 60)/' /home/pi/scenes/rain.py
sudo systemctl restart display
sed -i 's/self.color = (brightness, brightness, min(255, brightness + 10), alpha)/self.color = (brightness, int(brightness * 0.75), int(brightness * 0.45), alpha)/' /home/pi/scenes/rain.py
sudo systemctl restart display
cat /home/pi/scenes/mail.py
cat > /home/pi/scenes/mail.py << 'EOF'
from PIL import Image, ImageDraw
from scenes.common import *
import json, textwrap

MESSAGES_FILE = "/home/pi/messages.json"

MODE_LIST   = 0
MODE_DETAIL = 1

_mode      = MODE_LIST
_sel_idx   = 0
_scroll    = 0  # リストのスクロール位置
VISIBLE    = 4  # 一度に表示する件数

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
    # ヘッダー
    d.rectangle([0,0,W,28], fill=BG2)
    d.line([(0,28),(W,28)], fill=BORDER, width=1)
    d.text((center_x("Messages", FONT_TINY), 7), "Messages", font=FONT_TINY, fill=ACCENT)
    count = f"{len(msgs)} msgs" if msgs else ""
    d.text((W - text_w(count, FONT_TINY) - 6, 7), count, font=FONT_TINY, fill=MUTED)

    if not msgs:
        d.text((center_x("No messages", FONT_SMALL), 90), "No messages", font=FONT_SMALL, fill=MUTED)
        d.text((center_x("Send from WebUI", FONT_TINY), 115), "Send from WebUI", font=FONT_TINY, fill=BORDER)
        return

    # 新しい順に並べる
    reversed_msgs = list(reversed(msgs))
    total = len(reversed_msgs)

    # スクロール範囲クランプ
    max_scroll = max(0, total - VISIBLE)
    sc = max(0, min(_scroll, max_scroll))

    item_h = 36
    for i in range(VISIBLE):
        idx = sc + i
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

    # スクロールインジケーター
    if total > VISIBLE:
        d.text((W//2 - 10, 178), f"{sc+1}-{min(sc+VISIBLE,total)}/{total}", font=FONT_TINY, fill=MUTED)
        if sc > 0:
            d.text((W-20, 40), "▲", font=FONT_TINY, fill=ACCENT)
        if sc < max_scroll:
            d.text((W-20, 160), "▼", font=FONT_TINY, fill=ACCENT)

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

        # スクロールボタン（▲▼）
        if total > VISIBLE:
            if W-28 <= x <= W and 30 <= y <= 55 and _scroll > 0:
                _scroll -= 1
                return
            if W-28 <= x <= W and 150 <= y <= 175 and _scroll < max_scroll:
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
EOF

sudo systemctl restart display
cat > /home/pi/scenes/mail.py << 'EOF'
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
        d.text((8,  7), "▲", font=FONT_TINY, fill=up_col)
        d.text((22, 7), "▼", font=FONT_TINY, fill=down_col)

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
            if 4 <= x <= 18 and _scroll > 0:
                _scroll -= 1
            elif 18 <= x <= 34 and _scroll < max_scroll:
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
EOF

sudo systemctl restart display
sed -i 's/d.text((22, 7), "▼"/d.text((32, 7), "▼"/' /home/pi/scenes/mail.py
sed -i 's/elif 18 <= x <= 34/elif 28 <= x <= 44/' /home/pi/scenes/mail.py
sudo systemctl restart display
sed -i 's/d.text((8,  7), "▲"/d.text((18, 7), "▲"/' /home/pi/scenes/mail.py
sed -i 's/d.text((32, 7), "▼"/d.text((42, 7), "▼"/' /home/pi/scenes/mail.py
sed -i 's/if 4 <= x <= 18/if 14 <= x <= 28/' /home/pi/scenes/mail.py
sed -i 's/elif 28 <= x <= 44/elif 38 <= x <= 54/' /home/pi/scenes/mail.py
sudo systemctl restart display
grep -n "scroll\|VISIBLE\|max_scroll" /home/pi/scenes/photo.py /home/pi/scenes/scene_select.py
cat /home/pi/scenes/scene_select.py
cat /home/pi/scenes/photo.py
ls /home/pi/photos/ | wc -l
cat > /home/pi/scenes/photo.py << 'EOF'
from PIL import Image, ImageDraw
from scenes.common import *
import os, glob

PHOTO_DIR      = "/home/pi/photos"
SLIDE_INTERVAL = 5 * 20

MODE_GALLERY    = 0
MODE_FULLSCREEN = 1
MODE_SLIDESHOW  = 2

_mode        = MODE_GALLERY
_photos      = []
_photo_idx   = 0
_slide_timer = 0
_cache       = {}
_gallery_page = 0  # ページ（6枚ずつ）

COLS, ROWS = 3, 2
PER_PAGE   = COLS * ROWS

def _load_photos():
    global _photos
    exts = ["jpg","jpeg","png","webp","gif","JPG","JPEG","PNG","WEBP"]
    files = []
    for ext in exts:
        files.extend(glob.glob(os.path.join(PHOTO_DIR, f"*.{ext}")))
    _photos = sorted(set(files))

def _get_thumb(path, size):
    key = (path, size)
    if key not in _cache:
        try:
            img = Image.open(path).convert("RGB")
            img.thumbnail(size, Image.LANCZOS)
            _cache[key] = img
        except:
            _cache[key] = None
    return _cache[key]

def _get_full(path):
    ph = H - NAV_H - 30
    key = (path, "full")
    if key not in _cache:
        try:
            img = Image.open(path).convert("RGB")
            iw, ih = img.size
            ratio = min(W/iw, ph/ih)
            nw, nh = int(iw*ratio), int(ih*ratio)
            img = img.resize((nw, nh), Image.LANCZOS)
            canvas = Image.new("RGB", (W, ph), BG)
            canvas.paste(img, ((W-nw)//2, (ph-nh)//2))
            _cache[key] = canvas
        except:
            _cache[key] = None
    return _cache[key]

def _btn_rect(label, cx, cy, w=60, h=22):
    return {"label": label, "x1": cx-w//2, "y1": cy-h//2, "x2": cx+w//2, "y2": cy+h//2}

def _draw_btn(d, btn, active=False):
    fill    = ACCENT if active else BG2
    outline = ACCENT if active else BORDER
    d.rounded_rectangle([btn["x1"],btn["y1"],btn["x2"],btn["y2"]], radius=4, fill=fill, outline=outline, width=1)
    lw = text_w(btn["label"], FONT_TINY)
    tx = (btn["x1"]+btn["x2"])//2 - lw//2
    ty = (btn["y1"]+btn["y2"])//2 - 7
    d.text((tx, ty), btn["label"], font=FONT_TINY, fill=BG if active else CREAM2)

def _hit_btn(btn, x, y):
    return btn["x1"] <= x <= btn["x2"] and btn["y1"] <= y <= btn["y2"]

def draw(image, now, mpd, scroll_x):
    global _slide_timer, _photo_idx, _mode
    _load_photos()
    d = ImageDraw.Draw(image)
    d.rectangle([0,0,W,H], fill=BG)

    if not _photos:
        d.text((center_x("No photos", FONT_SMALL), 90), "No photos", font=FONT_SMALL, fill=MUTED)
        d.text((center_x("Upload via WebUI", FONT_TINY), 115), "Upload via WebUI", font=FONT_TINY, fill=BORDER)
        draw_nav(d, SCREEN_PHOTO)
        return

    if _mode == MODE_GALLERY:
        _draw_gallery(image, d)
    elif _mode == MODE_FULLSCREEN:
        _draw_fullscreen(image, d)
    elif _mode == MODE_SLIDESHOW:
        _slide_timer += 1
        if _slide_timer >= SLIDE_INTERVAL:
            _slide_timer = 0
            _photo_idx = (_photo_idx + 1) % len(_photos)
        _draw_slideshow(image, d)

    draw_nav(d, SCREEN_PHOTO)

def _draw_gallery(image, d):
    global _gallery_page
    total_pages = max(1, (len(_photos) + PER_PAGE - 1) // PER_PAGE)
    _gallery_page = max(0, min(_gallery_page, total_pages - 1))

    # ヘッダー
    d.rectangle([0,0,W,26], fill=BG2)
    d.line([(0,26),(W,26)], fill=BORDER, width=1)

    # ◀▶ ページナビ（左側）
    if total_pages > 1:
        lc = ACCENT if _gallery_page > 0             else BORDER
        rc = ACCENT if _gallery_page < total_pages-1 else BORDER
        d.text((18, 6), "◀", font=FONT_TINY, fill=lc)
        d.text((32, 6), "▶", font=FONT_TINY, fill=rc)

    d.text((center_x("Photos", FONT_TINY), 6), "Photos", font=FONT_TINY, fill=ACCENT)
    page_info = f"{_gallery_page+1}/{total_pages}" if total_pages > 1 else f"{len(_photos)} photos"
    d.text((W - text_w(page_info, FONT_TINY) - 6, 6), page_info, font=FONT_TINY, fill=MUTED)

    pad = 6
    thumb_w = (W - pad*(COLS+1)) // COLS
    thumb_h = (H - NAV_H - 26 - pad*(ROWS+1) - 28) // ROWS

    start = _gallery_page * PER_PAGE
    for i in range(PER_PAGE):
        photo_i = start + i
        if photo_i >= len(_photos):
            break
        col = i % COLS
        row = i // COLS
        tx  = pad + col * (thumb_w + pad)
        ty  = 26 + pad + row * (thumb_h + pad)

        thumb = _get_thumb(_photos[photo_i], (thumb_w, thumb_h))
        bg = Image.new("RGB", (thumb_w, thumb_h), BG2)
        if thumb:
            ox = (thumb_w - thumb.width) // 2
            oy = (thumb_h - thumb.height) // 2
            bg.paste(thumb, (ox, oy))
        image.paste(bg, (tx, ty))
        d = ImageDraw.Draw(image)
        outline_col = ACCENT if photo_i == _photo_idx else BORDER
        d.rectangle([tx,ty,tx+thumb_w,ty+thumb_h], outline=outline_col, width=2 if photo_i==_photo_idx else 1)

    d = ImageDraw.Draw(image)
    btn_y = H - NAV_H - 18
    _draw_btn(d, _btn_rect("Slideshow >", W//2, btn_y, w=100, h=22))

def _draw_fullscreen(image, d):
    full = _get_full(_photos[_photo_idx])
    if full:
        image.paste(full, (0, 0))
    d = ImageDraw.Draw(image)
    counter = f"{_photo_idx+1}/{len(_photos)}"
    d.text((W - text_w(counter, FONT_TINY) - 6, 4), counter, font=FONT_TINY, fill=CREAM2)
    btn_y = H - NAV_H - 15
    for btn in [
        _btn_rect("< Prev",      55,  btn_y, w=76, h=22),
        _btn_rect("Slideshow >", 160, btn_y, w=90, h=22),
        _btn_rect("Next >",      265, btn_y, w=76, h=22),
        _btn_rect("Grid",        W-24, 4,    w=38, h=18),
    ]:
        _draw_btn(d, btn)

def _draw_slideshow(image, d):
    full = _get_full(_photos[_photo_idx])
    if full:
        image.paste(full, (0, 0))
    d = ImageDraw.Draw(image)
    counter = f"{_photo_idx+1}/{len(_photos)}"
    d.text((W - text_w(counter, FONT_TINY) - 6, 4), counter, font=FONT_TINY, fill=CREAM2)
    btn_y = H - NAV_H - 15
    _draw_btn(d, _btn_rect("Stop", 160, btn_y, w=60, h=22), active=True)

def handle_touch(x, y):
    global _mode, _photo_idx, _slide_timer, _gallery_page

    _load_photos()
    if not _photos:
        return

    total_pages = max(1, (len(_photos) + PER_PAGE - 1) // PER_PAGE)

    if _mode == MODE_GALLERY:
        # ヘッダーの◀▶
        if 0 <= y <= 26 and total_pages > 1:
            if 10 <= x <= 28 and _gallery_page > 0:
                _gallery_page -= 1
                return
            if 28 <= x <= 46 and _gallery_page < total_pages - 1:
                _gallery_page += 1
                return

        pad = 6
        thumb_w = (W - pad*(COLS+1)) // COLS
        thumb_h = (H - NAV_H - 26 - pad*(ROWS+1) - 28) // ROWS
        start = _gallery_page * PER_PAGE
        for i in range(PER_PAGE):
            photo_i = start + i
            if photo_i >= len(_photos):
                break
            col = i % COLS
            row = i // COLS
            tx  = pad + col * (thumb_w + pad)
            ty  = 26 + pad + row * (thumb_h + pad)
            if tx <= x <= tx+thumb_w and ty <= y <= ty+thumb_h:
                _photo_idx = photo_i
                _mode = MODE_FULLSCREEN
                return
        btn = _btn_rect("Slideshow >", W//2, H-NAV_H-18, w=100, h=22)
        if _hit_btn(btn, x, y):
            _mode = MODE_SLIDESHOW
            _slide_timer = 0

    elif _mode == MODE_FULLSCREEN:
        btn_y = H - NAV_H - 15
        if _hit_btn(_btn_rect("< Prev",      55,  btn_y, w=76, h=22), x, y):
            _photo_idx = (_photo_idx - 1) % len(_photos)
        elif _hit_btn(_btn_rect("Next >",    265, btn_y, w=76, h=22), x, y):
            _photo_idx = (_photo_idx + 1) % len(_photos)
        elif _hit_btn(_btn_rect("Slideshow >",160, btn_y, w=90, h=22), x, y):
            _mode = MODE_SLIDESHOW
            _slide_timer = 0
        elif _hit_btn(_btn_rect("Grid", W-24, 4, w=38, h=18), x, y):
            _mode = MODE_GALLERY

    elif _mode == MODE_SLIDESHOW:
        _mode = MODE_FULLSCREEN
EOF

cat > /home/pi/scenes/scene_select.py << 'EOF'
from PIL import Image, ImageDraw
from scenes.common import *

SCENES = [
    {"label": "Landscape", "id": "landscape", "desc": "Country road"},
    {"label": "Rain",      "id": "rain",      "desc": "Rainy night"},
    {"label": "Night",     "id": "night",     "desc": "Coming soon"},
    {"label": "Snow",      "id": "snow",      "desc": "Coming soon"},
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
EOF

sudo systemctl restart display
sed -i 's/    {"label": "Snow",      "id": "snow",      "desc": "Coming soon"},/    {"label": "Snow",      "id": "snow",      "desc": "Coming soon"},\n    {"label": "Ocean",     "id": "ocean",     "desc": "Coming soon"},\n    {"label": "Forest",    "id": "forest",    "desc": "Coming soon"},/' /home/pi/scenes/scene_select.py
sudo systemctl restart display
grep -n "route\|@app" /home/pi/app.py
sudo systemctl status tailscaled
grep -n "host\|run" /home/pi/app.py | tail -5
sudo systemctl status flask
pip3 install opencv-python-headless --break-system-packages
cat > /home/pi/scenes/dance.py << 'EOF'
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
    if _frame_skip % 2 == 0:
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
EOF

sed -i 's/{"label": "Landscape", "id": "landscape", "desc": "Country road"},/{"label": "Landscape", "id": "landscape", "desc": "Country road"},\n    {"label": "Dance",     "id": "dance",     "desc": "Steve underwater"},/' /home/pi/scenes/scene_select.py
sudo systemctl restart display
sed -i 's/_frame_skip % 2 == 0/_frame_skip % 1 == 0/' /home/pi/scenes/dance.py
sudo systemctl restart display
sed -i 's/time.sleep(0.05)/time.sleep(0.03)/' /home/pi/main.py
sudo systemctl restart display
ffprobe /home/pi/scenes/steve_dance.mp4 2>&1 | grep fps
ffprobe /home/pi/scenes/steve_dance.mp4 2>&1 | grep Video
python3 -c "import cv2; cap=cv2.VideoCapture('/home/pi/scenes/steve_dance.mp4'); print(cap.get(cv2.CAP_PROP_FPS))"
sed -i 's/ret, frame = _cap.read()/# 2フレーム読んで速く\n    _cap.grab()\n    ret, frame = _cap.read()/' /home/pi/scenes/dance.py
sudo systemctl restart display
ffmpeg -i ~/Downloads/46012-448062061_medium.mp4   -vf "fps=12,scale=2560:1440"   ~/Downloads/steve_dance_12fps.mp4
scp ~/Downloads/steve_dance_12fps.mp4 pi@192.168.0.35:/home/pi/scenes/steve_dance.mp4
sed -i '/# 2フレーム読んで速く/d; /_cap.grab()/d' /home/pi/scenes/dance.py
sudo systemctl restart display
sudo nano /etc/wpa_supplicant/wpa_supplicant.conf
cat /etc/NetworkManager/system-connections/*.nmconnection 2>/dev/null | grep -E "ssid|psk"
sudo nmcli connection show
ls /etc/NetworkManager/system-connections/
pi@raspberrypi:~ $ ls /etc/NetworkManager/system-connections/
preconfigured.nmconnection
pi@raspberrypi:~ $ 
sudo cat /etc/NetworkManager/system-connections/preconfigured.nmconnection
sudo nmcli dev wifi connect "Buffalo-C5E0" password "he8ywnsw"
sudo nmcli connection add type wifi con-name "jikka" ssid "Buffalo-C5E0" wifi-sec.key-mgmt wpa-psk wifi-sec.psk "he8ywnsw"
sudo nmcli connection show
sudo nmcli connection add type wifi con-name "jikka2" ssid "Buffalo-C5E0" wifi-sec.key-mgmt wpa-psk wifi-sec.psk "extnx7r48smtp"
sudo nmcli connection show
tree /home/pi
sed -n '125,145p' /home/pi/app.py
sudo nano /home/pi/app.py
nano /home/pi/app.py
sudo systemctl restart flask
grep -n "reboot\|Reboot" /home/pi/templates/index.html
sed -i 's/<button class="sys-btn" onclick="systemReboot()">↺ Reboot<\/button>/<button class="sys-btn" onclick="systemReboot()">↺ Reboot<\/button>\n      <button class="sys-btn" onclick="systemShutdown()">⏻ Shutdown<\/button>/' /home/pi/templates/index.html
sed -i 's/async function systemReboot() {/async function systemShutdown() {\n  if (!confirm("Shutdown the device?")) return;\n  await api("\/api\/system\/shutdown","POST");\n  toast("Shutting down...");\n}\nasync function systemReboot() {/' /home/pi/templates/index.html
sudo systemctl restart flask
nano /home/pi/main.py
sudo systemctl restart display
nano /home/pi/main.py
sudo systemctl restart display
nano /home/pi/main.py
grep -n "import subprocess" /home/pi/main.py
nano /home/pi/main.py
sudo systemctl restart display
tree
sudo nano /boot/firmware/config.txt
sudo reboot
aplay -l
aplay -D hw:0,0 /usr/share/sounds/alsa/Front_Left.wav
aplay -D hw:0,0 -c 2 /usr/share/sounds/alsa/Front_Left.wav
sudo nano /boot/firmware/config.txt
sudo reboot
pinout
cat /boot/firmware/config.txt
sudo nano /boot/firmware/config.txt
sudo reboot
cat /boot/firmware/overlays/README | grep -A 20 "max98357a"
lsmod | grep snd_soc_max98357a
cat /boot/firmware/config.txt
sudo nano /boot/firmware/config.txt
sudo reboot
speaker-test -D hw:0,0 -c 2 -t wav
dmesg | grep -i i2s
dmesg | grep -i max98357
aplay -l
sudo nano /boot/firmware/config.txt
dtoverlay=max98357a,no-sdmode
sudo reboot
speaker-test -D hw:0,0 -c 2 -t wav
sudo nano /boot/firmware/config.txt
reboot
sudo reboot
sudo nano /boot/firmware/config.txt
cat config.txt
cat /boot/firmware/config.txt
sudo reboot
speaker-test -D hw:0,0 -c 2 -t wav
cat /sys/kernel/debug/pinctrl/pinctrl-bcm2835/pins 2>/dev/null | grep -E "19|20|21|18"
raspi-gpio get 18,19,20,21
raspi-gpio 
raspi-gpio get
raspi-gpio get 18,19,20,21
sudo reboot
raspi-gpio get 18,19,20,21
pinctrl get 18,19,20,21
cat /boot/firmware/config.txt | tail -5
sudo nano /boot/firmware/config.txt
sudo reboot
pinctrl get 18,19,20,21
cat /boot/firmware/config.txt | tail -5
dmesg | grep -i pcm
dmesg | grep -i i2s
dmesg | grep -i simple-card
dmesg | grep -i sound
dmesg | grep -i max
aplay -l
speaker-test -D hw:0,0 -c 2 -t wav &
pinctrl get 18,19,20,21
exit
pinctrl get 18,19,20,21
speaker-test -D hw:0,0 -c 2 -t wav > /dev/null 2>&1 &
sleep 2
pinctrl get 18,19,20,21
kill %1
speaker-test -D hw:0,0 -c 2 -t wav
sudo fuser /dev/snd/*
ps aux | grep 5801
kill 5801
speaker-test -D hw:0,0 -c 2 -t wav
pinctrl set 18 a0
pinctrl get 18,19,20,21
speaker-test -D hw:0,0 -c 2 -t wav
sudo nano /boot/firmware/config.txt
sudo reboot
speaker-test -D hw:0,0 -c 2 -t wav
pinctrl get 18,19,20,21
speaker-test -D hw:0,0 -c 2 -t wav > /dev/null 2>&1 &
sleep 1
pinctrl set 18 a0
exit
pinctrl get 18,19,20,21
sudo nano /boot/firmware/config.txt
sudo reboot
pinctrl get 18,19,20,21
sudo nano /boot/firmware/config.txt
pinctrl get 18,19,20,21
sudo reboot
pinctrl get 18,19,20,21
sudo nano /etc/systemd/system/i2s-fix.service
sudo systemctl enable i2s-fix
sudo systemctl start i2s-fix
pinctrl get 18,19,20,21
sudo nano /etc/systemd/system/i2s-fix.service
sudo systemctl daemon-reload
sudo reboot
pinctrl get 18,19,20,21
mpc play
sudo nano /etc/systemd/system/aplay-silence.service
sudo systemctl enable aplay-silence
sudo systemctl start aplay-silence
mpc play
pinctrl get 18,19,20,21
sudo systemctl stop aplay-silence
sudo systemctl disable aplay-silence
mpc
sudo fuser /dev/snd/*
sudo reboot
mpc
cat /etc/mpd.conf | grep -A 10 "audio_output"
sudo nano /etc/mpd.conf
cat /etc/mpd.conf
sudo nano /etc/mpd.conf
sudo systemctl restart mpd
mpc play
sudo reboot
sudo nano /etc/mpd.conf
sudo systemctl restart mpd
sudo reboot
nano /home/pi/i2s_monitor.py
python3 /home/pi/i2s_monitor.py &
mpc play
nano /home/pi/i2s_monitor.py
kill %1
python3 /home/pi/i2s_monitor.py &
mpc next
kill %1
nano /home/pi/i2s_monitor.py
python3 /home/pi/i2s_monitor.py &
mpc next
sudo nano /etc/asound.conf
sudo nano /etc/mpd.conf
sudo nano /etc/systemd/system/aplay-silence.service
sudo systemctl enable aplay-silence
sudo systemctl daemon-reload
sudo reboot
sudo journalctl -u mpd -n 20
cat /etc/asound.conf
sudo nano /etc/asound.conf
sudo systemctl restart mpd
sudo systemctl restart aplay-silence
mpc play
sudo nano /etc/mpd.conf
sudo systemctl restart mpd
mpc play
sudo reboot
sudo apt install shairport-sync -y
pip3 install gtts --break-system-packages
sudo apt install mpg123 -y
python3 -c "from gtts import gTTS; tts = gTTS('Hello, this is a test', lang='en'); tts.save('/tmp/test.mp3')"
mpg123 /tmp/test.mp3
mpg123 -f 10000 /tmp/test.mp3
mpg123 -f 8000 /tmp/test.mp3
mpg123 -f 6000 /tmp/test.mp3
mpg123 -f 5000 /tmp/test.mp3
cat /home/pi/app.py
nano /home/pi/app.py
sudo systemctl restart flask
cat /home/pi/main.py
head -10 /home/pi/main.py
nano /home/pi/main.py
cat /home/pi/main.py
nano /home/pi/main.py
cat /home/pi/main.py
sudo systemctl restart display
sudo fuser /dev/snd/*
ps aux | grep -E "357|504" | grep -v grep
mpc play
sudo systemctl status mpd
mpc status
sudo systemctl status aplay-silence
pinctrl get 18
sudo systemctl status i2s-fix
pinctrl set 18 a0
mpc play
sudo nano /etc/systemd/system/i2s-fix.service
sudo systemctl daemon-reload
sudo reboot
sudo systemctl status flask
python3 /home/pi/app.py
sudo fuser -k 5000/tcp
sudo systemctl restart flask
hostname -I
sudo systemctl status flask
python3 /home/pi/app.py 2>&1
sudo fuser 5000/tcp
sudo kill 5984
sudo systemctl restart flask
sudo apt install fonts-noto-color-emoji -y
cat /home/pi/scenes/common.py | grep FONT
nano /home/pi/main.py
sudo systemctl restart display
pinctrl set 18 a0
sudo systemctl restart i2s-fix
pinctrl get 18
nano /home/pi/main.py
grep -n "notification" /home/pi/main.py
nano /home/pi/main.py
cat /home/pi/main.py
sudo systemctl restart display && sudo systemctl restart i2s-fix
sudo reboot
sudo fuser -k 5000/tcp
sudo systemctl restart flask
sudo systemctl status flask
python3 /home/pi/app.py
sudo fuser -k 5000/tcp
sleep 2
sudo systemctl start flask
sudo systemctl status flask
sudo systemctl stop flask
sudo fuser -k 5000/tcp
sleep 3
sudo systemctl start flask
sudo fuser 5000/tcp
sudo kill <5759>
sudo systemctl start flask
sudo kill 5759
sudo systemctl start flask
sudo nano /etc/systemd/system/flask.service
sudo systemctl daemon-reload
sudo nano /etc/systemd/system/flask.service
sudo systemctl daemon-reload
sudo reboot
sudo nano /etc/systemd/system/flask.service
sudo fuser 5000/tcp
sudo kill 557
sudo systemctl start flask
cat /etc/systemd/system/flask.service
ps aux | grep 557 | grep -v grep
sudo nano /etc/systemd/system/flask.service
sudo systemctl daemon-reload
sudo reboot
sudo nano /etc/systemd/system/flask.service
sudo systemctl daemon-reload
sudo reboot
sudo fuser 5000/tcp
sudo kill 559
sudo kill $(sudo fuser 5000/tcp 2>/dev/null)
sudo systemctl start flask
echo "alias fixflask='sudo kill \$(sudo fuser 5000/tcp 2>/dev/null); sudo systemctl start flask'" >> ~/.bashrc
source ~/.bashrc
fixflask
