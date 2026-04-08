from luma.lcd.device import ili9341
from luma.core.interface.serial import spi as luma_spi
from PIL import Image
import time, datetime, threading, json

import touch
from scenes.common import *
from scenes import home, music, clock, mail, photo, scene_select

import importlib
import os
import subprocess
import RPi.GPIO as GPIO

# GPIO3シャットダウンボタン設定
GPIO.setmode(GPIO.BCM)
GPIO.setup(3, GPIO.IN, pull_up_down=GPIO.PUD_UP)

# デバイス初期化
serial = luma_spi(port=0, device=0, gpio_DC=24, gpio_RST=25, bus_speed_hz=16000000)
device = ili9341(serial, width=320, height=240, rotate=0)

# 状態
current_screen   = SCREEN_HOME
current_scene_id = "landscape"
was_playing      = False
idle_timer       = 0
IDLE_BACK        = 15 * 20

scroll_x     = 0
scroll_pause = 0
last_song    = ""

# 通知バナー

notification_text  = ""
notification_timer = 0
last_notified_time = ""

# 起動時の最新メッセージ時刻を記録
try:
    with open("/home/pi/messages.json") as f:
        msgs = json.load(f)
    if msgs:
        last_notified_time = msgs[-1]["time"]
except:
    pass

# 起動時i2s-fix
subprocess.Popen(["sudo", "systemctl", "restart", "i2s-fix"])

# タッチ排他ロック
touch_lock      = threading.Lock()
last_touch_time = 0
DEBOUNCE        = 0.4

def get_scene_module():
    try:
        return importlib.import_module(f"scenes.{current_scene_id}")
    except:
        from scenes import landscape
        return landscape

# メインループ
while True:
    now = datetime.datetime.now()
    mpd = get_mpd()

    # メッセージ通知チェック
    try:
        with open("/home/pi/messages.json") as f:
            msgs = json.load(f)
        if msgs and msgs[-1]["time"] != last_notified_time:
            notification_text = "* You got a message! *"
            notification_timer = 100
            last_notified_time = msgs[-1]["time"]
    except:
        pass

    if notification_timer > 0:
        notification_timer -= 1

    # シャットダウンボタン
    if GPIO.input(3) == GPIO.LOW:
        time.sleep(0.5)
        if GPIO.input(3) == GPIO.LOW:
            subprocess.call(["sudo", "sh", "-c", "echo 0 > /sys/class/backlight/*/brightness"])
            os.system("sudo shutdown -h now")

    # タッチ処理
    pos = touch.read_touch()
    now_t = time.time()

    if pos and (now_t - last_touch_time) > DEBOUNCE:
        tx, ty = pos
        last_touch_time = now_t
        idle_timer = 0

        nav_target = hit_nav(tx, ty)
        if nav_target is not None:
            current_screen = nav_target

        elif current_screen == SCREEN_MUSIC:
            action = music.hit_button(tx, ty)
            if action:
                music.do_action(action, mpd)

        elif current_screen == SCREEN_SCENE:
            sid = scene_select.hit_scene(tx, ty)
            if sid:
                current_scene_id = sid
                current_screen   = SCREEN_LANDSCAPE

        elif current_screen == SCREEN_MAIL:
            mail.handle_touch(tx, ty)

        elif current_screen == SCREEN_PHOTO:
            photo.handle_touch(tx, ty)

    # 自動Landscape起動
    if mpd["playing"] and not was_playing:
        current_screen = SCREEN_LANDSCAPE
    was_playing = mpd["playing"]

    # スクロール更新
    if mpd["song"] != last_song:
        last_song    = mpd["song"]
        scroll_x     = 0
        scroll_pause = 0

    if text_w(mpd["song"], FONT_SMALL) > W - 50:
        if scroll_pause < 50:
            scroll_pause += 1
        else:
            scroll_x += 1.2

    # 描画
    image = Image.new("RGB", (W, H), BG)

    if current_screen == SCREEN_HOME:
        home.draw(image, now, mpd, scroll_x)

    elif current_screen == SCREEN_MUSIC:
        music.draw(image, now, mpd, scroll_x)

    elif current_screen == SCREEN_CLOCK:
        clock.draw(image, now, mpd, scroll_x)

    elif current_screen == SCREEN_MAIL:
        mail.draw(image, now, mpd, scroll_x)

    elif current_screen == SCREEN_PHOTO:
        photo.draw(image, now, mpd, scroll_x)

    elif current_screen == SCREEN_SCENE:
        scene_select.draw(image, now, mpd, current_scene_id)

    elif current_screen == SCREEN_LANDSCAPE:
        scene_mod = get_scene_module()
        if hasattr(scene_mod, "draw_frame"):
            scene_mod.draw_frame(image, now, mpd, scroll_x)
        else:
            home.draw(image, now, mpd, scroll_x)

        from PIL import ImageDraw as ID
        d = ID.Draw(image)
        d.rounded_rectangle([8, H-28, 70, H-6], radius=4, fill=BG2, outline=BORDER, width=1)
        d.text((14, H-24), "⌂ Home", font=FONT_TINY, fill=CREAM2)

    # 通知バナー描画
    if notification_timer > 0:
        from PIL import ImageDraw as ID2
        d2 = ID2.Draw(image)
        d2.rounded_rectangle([0, 0, W, 30], radius=0, fill=(40, 80, 40))
        d2.text((10, 7), notification_text, font=FONT_SMALL, fill=(200, 255, 200))

    device.display(image)
    time.sleep(0.03)
