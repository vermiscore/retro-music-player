import spidev, time
import RPi.GPIO as GPIO

T_IRQ = 17

GPIO.setmode(GPIO.BCM)
GPIO.setup(T_IRQ, GPIO.IN, pull_up_down=GPIO.PUD_UP)

spi = spidev.SpiDev()
spi.open(0, 1)  # SPI0, CS1（GPIO7）をハードウェアで使う
spi.max_speed_hz = 500000
spi.mode = 0

def read_touch():
    r = spi.xfer2([0xD0, 0x00, 0x90, 0x00, 0x00])
    x = ((r[1] << 8) | r[2]) >> 3
    y = ((r[3] << 8) | r[4]) >> 3
    return x, y

print("タッチしてください... Ctrl+Cで終了")
try:
    while True:
        if GPIO.input(T_IRQ) == 0:
            x, y = read_touch()
            print(f"X={x}, Y={y}")
            time.sleep(0.05)
except KeyboardInterrupt:
    spi.close()
    GPIO.cleanup()
