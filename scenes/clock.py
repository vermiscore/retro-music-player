from PIL import Image, ImageDraw
from scenes.common import *
import subprocess, random, datetime

CAT_IMG = Image.open("/home/pi/scenes/cat_mascot.png").convert("RGBA").resize((80, 80))

def get_speech(now, mpd):
    h = now.hour
    if 5 <= h < 10:
        greetings = ["Good morning!", "Rise and shine!", "A new day!", "Morning!"]
    elif 10 <= h < 14:
        greetings = ["How's it going?", "Hope you're well!", "Feeling good?", "Hello there!"]
    elif 14 <= h < 18:
        greetings = ["Hang in there!", "Take a break!", "Afternoon vibes", "Almost done!"]
    elif 18 <= h < 22:
        greetings = ["Good evening!", "Well done today!", "Time to relax", "Good night soon"]
    else:
        greetings = ["Burning midnight oil?", "Sleep well!", "Quiet night...", "Rest up!"]
    if mpd["playing"]:
        music_lines = ["Great tune!", "Love this song!", "Nice melody~", "Feeling the music!"]
        greetings += music_lines
    return random.choice(greetings)

def get_sysinfo():
    info = {}
    try:
        temp = subprocess.run(["vcgencmd", "measure_temp"], capture_output=True, text=True, timeout=1).stdout
        info["temp"] = temp.replace("temp=","").strip()
    except:
        info["temp"] = "N/A"
    try:
        mem = subprocess.run(["free", "-m"], capture_output=True, text=True, timeout=1).stdout
        lines = mem.split("\n")
        parts = lines[1].split()
        used = int(parts[2]); total = int(parts[1])
        info["mem"] = f"{used}/{total}MB"
    except:
        info["mem"] = "N/A"
    try:
        ip = subprocess.run(["hostname", "-I"], capture_output=True, text=True, timeout=1).stdout.strip().split()[0]
        info["ip"] = ip
    except:
        info["ip"] = "N/A"
    try:
        up = subprocess.run(["uptime", "-p"], capture_output=True, text=True, timeout=1).stdout.strip()
        info["uptime"] = up.replace("up ","")
    except:
        info["uptime"] = "N/A"
    return info

_speech = ""
_speech_timer = 0

def handle_touch(x, y, now, mpd):
    global _speech, _speech_timer
    if x > 220 and y > 120 and y < H - NAV_H:
        _speech = get_speech(now, mpd)
        _speech_timer = 90
        subprocess.Popen(["aplay", "/home/pi/meow_quiet.wav"])

def draw(image, now, mpd, scroll_x):
    global _speech_timer
    d = ImageDraw.Draw(image)
    d.rectangle([0, 0, W, H], fill=BG)

    # ヘッダー
    d.rectangle([0, 0, W, 28], fill=BG2)
    d.line([(0,28),(W,28)], fill=BORDER, width=1)
    label = "System"
    d.text((center_x(label, FONT_TINY), 8), label, font=FONT_TINY, fill=ACCENT)

    # システム情報
    info = get_sysinfo()
    items = [
        ("Temp",   info["temp"]),
        ("Memory", info["mem"]),
        ("IP",     info["ip"]),
        ("Uptime", info["uptime"]),
    ]
    y = 40
    for label, value in items:
        d.text((14, y), label, font=FONT_TINY, fill=MUTED)
        d.text((90, y), value, font=FONT_TINY, fill=CREAM)
        d.line([(14, y+16),(200, y+16)], fill=BORDER, width=1)
        y += 24

    # ヒント
    y += 4
    hints = ["Scene: choose wallpaper", "Photo: slideshow", "Mail: send message"]
    for hint in hints:
        d.text((14, y), "• " + hint, font=FONT_TINY, fill=MUTED)
        y += 16

    # 猫マスコット（右下）
    cat_x, cat_y = 230, 120
    image.paste(CAT_IMG, (cat_x, cat_y), CAT_IMG)

    # 吹き出し
    if _speech_timer > 0:
        _speech_timer -= 1
        sw = text_w(_speech, FONT_TINY) + 16
        bx = min(cat_x - sw//2, W - sw - 8)
        bx = max(8, bx)
        by = cat_y - 30
        d.rounded_rectangle([bx, by, bx+sw, by+22], radius=6, fill=CREAM, outline=ACCENT, width=1)
        d.text((bx+8, by+4), _speech, font=FONT_TINY, fill=BG)
        d.polygon([(cat_x+20, by+22),(cat_x+28, by+22),(cat_x+24, by+30)], fill=CREAM)

    draw_nav(d, SCREEN_CLOCK)
