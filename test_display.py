from luma.lcd.device import ili9341
from luma.core.interface.serial import spi
from luma.core.render import canvas
import time

serial = spi(port=0, device=0, gpio_DC=24, gpio_RST=25, bus_speed_hz=16000000)
device = ili9341(serial, width=320, height=240, rotate=0)

with canvas(device) as draw:
    draw.rectangle([0, 0, 319, 239], fill="red")
    draw.text((10, 10), "Hello!", fill="white")

print("Done!")
time.sleep(10)

