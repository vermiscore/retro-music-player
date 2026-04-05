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
