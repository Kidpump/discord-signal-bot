import websocket
import requests
import json
import os
import threading
import time

DISCORD_TOKEN = os.environ["DISCORD_TOKEN"]
CHANNEL_ID = str(os.environ["CHANNEL_ID"])
TELEGRAM_BOT_TOKEN = os.environ["TELEGRAM_BOT_TOKEN"]
TELEGRAM_CHAT_ID = os.environ["TELEGRAM_CHAT_ID"]

def send_telegram(text):
    requests.post(
        f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage",
        data={"chat_id": TELEGRAM_CHAT_ID, "text": text}
    )

def on_message(ws, message):
    data = json.loads(message)
    if data.get("t") == "MESSAGE_CREATE":
        msg = data["d"]
        if str(msg["channel_id"]) == CHANNEL_ID:
            content = msg.get("content", "")
            if content:
                send_telegram(f"🚨 Neues Trading Signal:\n\n{content}")

def heartbeat(ws, interval):
    while True:
        time.sleep(interval / 1000)
        ws.send(json.dumps({"op": 1, "d": None}))

def on_open(ws):
    auth = {
        "op": 2,
        "d": {
            "token": DISCORD_TOKEN,
            "properties": {
                "$os": "linux",
                "$browser": "chrome",
                "$device": ""
            }
        }
    }
    ws.send(json.dumps(auth))

def on_error(ws, error):
    print(f"Fehler: {error}")

def on_close(ws, a, b):
    print("Verbindung geschlossen, neustart...")
    time.sleep(5)
    start()

def start():
    ws = websocket.WebSocketApp(
        "wss://gateway.discord.gg/?v=9&encoding=json",
        on_message=on_message,
        on_open=on_open,
        on_error=on_error,
        on_close=on_close
    )
    
    def on_hello(ws, message):
        data = json.loads(message)
        if data["op"] == 10:
            interval = data["d"]["heartbeat_interval"]
            t = threading.Thread(target=heartbeat, args=(ws, interval))
            t.daemon = True
            t.start()
        on_message(ws, message)
    
    ws.on_message = on_hello
    ws.run_forever()

print("Bot startet...")
start()
