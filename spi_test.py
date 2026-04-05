import spidev

spi = spidev.SpiDev()
spi.open(0, 1)
spi.max_speed_hz = 500000
spi.mode = 0

# テストデータ送信
result = spi.xfer2([0xAA, 0x55, 0xFF])
print(f"送信: [0xAA, 0x55, 0xFF]")
print(f"受信: {[hex(x) for x in result]}")

spi.close()
