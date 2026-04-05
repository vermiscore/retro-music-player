import spidev
import RPi.GPIO as GPIO
import time

# ── キャリブレーション値 ──────────────────────────────────
X_MIN, X_MAX = 251, 3735
Y_MIN, Y_MAX = 220, 3842
SCREEN_W, SCREEN_H = 320, 240

T_IRQ = 17

GPIO.setmode(GPIO.BCM)
GPIO.setup(T_IRQ, GPIO.IN, pull_up_down=GPIO.PUD_UP)

spi = spidev.SpiDev()
spi.open(0, 1)
spi.max_speed_hz = 125000
spi.mode = 0

def read_raw():
    rx = spi.xfer2([0xD0, 0x00, 0x00])
    ry = spi.xfer2([0x90, 0x00, 0x00])
    x = ((rx[1] << 8) | rx[2]) >> 3
    y = ((ry[1] << 8) | ry[2]) >> 3
    return x, y

def read_touch():
    """タッチ座標を画面座標(0~320, 0~240)に変換して返す。タッチなしはNone"""
    if GPIO.input(T_IRQ) != 0:
        return None
    x_raw, y_raw = read_raw()
    if x_raw == 0 and y_raw == 0:
        return None
    x = SCREEN_W - int((y_raw - Y_MIN) / (Y_MAX - Y_MIN) * SCREEN_W)
    y = int((x_raw - X_MIN) / (X_MAX - X_MIN) * SCREEN_H)
    x = max(0, min(SCREEN_W - 1, x))
    y = max(0, min(SCREEN_H - 1, y))
    return (x, y)

def cleanup():
    spi.close()
    GPIO.cleanup()
