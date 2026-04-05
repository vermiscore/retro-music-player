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
