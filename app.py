from flask import Flask, render_template, jsonify, request, send_from_directory
from mpd import MPDClient
import os, subprocess, json
import datetime

app = Flask(__name__)

MUSIC_DIR     = "/home/pi/music"
PHOTO_DIR     = "/home/pi/photos"
MESSAGES_FILE = "/home/pi/messages.json"

os.makedirs(MUSIC_DIR, exist_ok=True)
os.makedirs(PHOTO_DIR, exist_ok=True)

def mpd_cmd(func):
    client = MPDClient()
    try:
        client.connect("localhost", 6600)
        result = func(client)
        client.disconnect()
        return result
    except Exception as e:
        return {"error": str(e)}

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/api/status")
def status():
    def f(c):
        s = c.status()
        song = c.currentsong()
        return {
            "state": s.get("state", "stop"),
            "volume": s.get("volume", "0"),
            "song": song.get("title") or song.get("file", "").split("/")[-1] or "No song",
            "elapsed": s.get("elapsed", "0"),
            "duration": s.get("duration", "0"),
            "repeat": s.get("repeat", "0"),
        }
    return jsonify(mpd_cmd(f))

@app.route("/api/playlist")
def playlist():
    def f(c): return c.playlistinfo()
    return jsonify(mpd_cmd(f))

@app.route("/api/play", methods=["POST"])
def play():
    data = request.get_json(silent=True) or {}
    def f(c):
        if "pos" in data:
            c.play(data["pos"])
        else:
            status = c.status()
            if status.get("state") == "pause":
                c.pause()
            else:
                c.play()
        return {"ok": True}
    return jsonify(mpd_cmd(f))

@app.route("/api/pause", methods=["POST"])
def pause():
    def f(c): c.pause(); return {"ok": True}
    return jsonify(mpd_cmd(f))

@app.route("/api/next", methods=["POST"])
def next_song():
    def f(c): c.next(); return {"ok": True}
    return jsonify(mpd_cmd(f))

@app.route("/api/prev", methods=["POST"])
def prev_song():
    def f(c): c.previous(); return {"ok": True}
    return jsonify(mpd_cmd(f))

@app.route("/api/volume", methods=["POST"])
def volume():
    vol = request.json.get("volume", 80)
    def f(c): c.setvol(int(vol)); return {"ok": True}
    return jsonify(mpd_cmd(f))

@app.route("/api/repeat", methods=["POST"])
def repeat():
    data = request.get_json(silent=True) or {}
    state = data.get("state", 1)
    def f(c): c.repeat(int(state)); return {"ok": True}
    return jsonify(mpd_cmd(f))

@app.route("/api/update", methods=["POST"])
def update_db():
    import time
    def f(c):
        c.update()
        time.sleep(2)
        c.clear()
        for song in c.listall():
            if 'file' in song:
                c.add(song['file'])
        return {"ok": True}
    return jsonify(mpd_cmd(f))

@app.route("/api/files")
def list_files():
    directory = request.args.get("dir", MUSIC_DIR)
    if not os.path.abspath(directory).startswith("/home/pi"):
        return jsonify({"error": "forbidden"}), 403
    try:
        items = []
        for name in sorted(os.listdir(directory)):
            path = os.path.join(directory, name)
            items.append({"name": name, "path": path, "is_dir": os.path.isdir(path),
                          "size": os.path.getsize(path) if os.path.isfile(path) else 0})
        return jsonify({"dir": directory, "items": items})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/api/files/upload", methods=["POST"])
def upload_file():
    directory = request.args.get("dir", MUSIC_DIR)
    if not os.path.abspath(directory).startswith("/home/pi"):
        return jsonify({"error": "forbidden"}), 403
    if "file" not in request.files:
        return jsonify({"error": "no file"}), 400
    f = request.files["file"]
    f.save(os.path.join(directory, f.filename))
    return jsonify({"ok": True, "name": f.filename})

@app.route("/api/files/delete", methods=["POST"])
def delete_file():
    path = request.json.get("path", "")
    if not os.path.abspath(path).startswith("/home/pi"):
        return jsonify({"error": "forbidden"}), 403
    try:
        os.remove(path)
        return jsonify({"ok": True})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/api/files/serve")
def serve_file():
    path = request.args.get("path", "")
    if not os.path.abspath(path).startswith("/home/pi"):
        return jsonify({"error": "forbidden"}), 403
    return send_from_directory(os.path.dirname(path), os.path.basename(path))

@app.route("/api/system/update", methods=["POST"])
def system_update():
    subprocess.Popen(["sudo", "apt", "update", "&&", "sudo", "apt", "upgrade", "-y"], shell=False)
    return jsonify({"ok": True, "message": "Update started"})

@app.route("/api/system/reboot", methods=["POST"])
def reboot():
    subprocess.Popen(["sudo", "reboot"])
    return jsonify({"ok": True})

@app.route("/api/system/shutdown", methods=["POST"])
def shutdown():
    subprocess.Popen(["sudo", "shutdown", "-h", "now"])

    return jsonify({"ok": True})
def load_messages():
    try:
        with open(MESSAGES_FILE, "r") as f:
            return json.load(f)
    except:
        return []

def save_messages(msgs):
    with open(MESSAGES_FILE, "w") as f:
        json.dump(msgs, f, ensure_ascii=False, indent=2)

@app.route("/api/message", methods=["GET"])
def get_messages():
    return jsonify(load_messages())

@app.route("/api/message", methods=["POST"])
def send_message():
    msg = request.json.get("message", "").strip()
    if msg:
        msgs = load_messages()
        msgs.append({"text": msg, "time": datetime.datetime.now().strftime("%m/%d %H:%M")})
        save_messages(msgs)
        # gTTS読み上げ
        def speak():
            from gtts import gTTS
            tts = gTTS("You've got a message! " + msg, lang='en')
            tts.save('/tmp/message.mp3')
            subprocess.run(['mpg123', '-f', '6000', '/tmp/message.mp3'])
        import threading
        threading.Thread(target=speak, daemon=True).start()
    return jsonify({"ok": True})

@app.route("/api/message/<int:idx>", methods=["DELETE"])
def delete_message(idx):
    msgs = load_messages()
    if 0 <= idx < len(msgs):
        msgs.pop(idx)
        save_messages(msgs)
    return jsonify({"ok": True})

if __name__ == "__main__":
    try:
        with MPDClient() as c:
            c.connect("localhost", 6600)
            c.repeat(1)
    except:
        pass
    app.run(host="0.0.0.0", port=5000, debug=False)
