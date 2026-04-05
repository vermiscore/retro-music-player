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
