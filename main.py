import selfcord
import requests
import os

DISCORD_TOKEN = os.environ["DISCORD_TOKEN"]
CHANNEL_ID = int(os.environ["CHANNEL_ID"])
TELEGRAM_BOT_TOKEN = os.environ["TELEGRAM_BOT_TOKEN"]
TELEGRAM_CHAT_ID = os.environ["TELEGRAM_CHAT_ID"]

client = selfcord.Client()

@client.event
async def on_ready():
    print(f"Bot läuft!")

@client.event
async def on_message(message):
    if message.channel.id == CHANNEL_ID:
        text = f"🚨 Neues Trading Signal:\n\n{message.content}"
        requests.post(
            f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage",
            data={"chat_id": TELEGRAM_CHAT_ID, "text": text}
        )

client.run(DISCORD_TOKEN)
