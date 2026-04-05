import subprocess
import time
from mpd import MPDClient

def set_gpio18(mode):
    if mode == "pcm":
        subprocess.run(["pinctrl", "set", "18", "a0"])
    else:
        subprocess.run(["pinctrl", "set", "18", "op"])

client = MPDClient()
last_state = None
stop_timer = None

while True:
    try:
        client.connect("localhost", 6600)
        status = client.status()
        state = status["state"]
        
        if state == "play":
            stop_timer = None
            if last_state != "play":
                set_gpio18("pcm")
                time.sleep(0.05)  # PCM_CLK安定待ち
        else:
            if stop_timer is None:
                stop_timer = time.time()
            elif time.time() - stop_timer > 5.0:  # 5秒後にoutputに戻す
                set_gpio18("output")
                stop_timer = None
        
        last_state = state
        client.disconnect()
    except Exception as e:
        pass
    
    time.sleep(0.1)  # より細かく監視

