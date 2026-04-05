import spidev, time

spi = spidev.SpiDev()
spi.open(0, 1)
spi.max_speed_hz = 125000  # かなり遅く
spi.mode = 0

for _ in range(5):
    r = spi.xfer2([0xD0, 0x00, 0x00])
    print(f"受信: {[hex(x) for x in r]}")
    time.sleep(0.1)

spi.close()
