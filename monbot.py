# monbot.py
import os
import asyncio
import discord
from dotenv import load_dotenv

from telethon import events
from telethon import TelegramClient
from telethon.sessions import StringSession

# Local seulement (inoffensif sur Render)
load_dotenv()

# --- Variables d'environnement ---
API_ID = int(os.getenv("TG_API_ID"))
API_HASH = os.getenv("TG_API_HASH")
TG_SESSION = os.getenv("TG_SESSION")  # StringSession générée avec gen_session.py

DISCORD_TOKEN = os.getenv("DISCORD_BOT_TOKEN")
DISCORD_CHANNEL_ID = int(os.getenv("DISCORD_CHANNEL_ID"))  # juste le nombre

# --- Discord ---
intents = discord.Intents.default()
discord_client = discord.Client(intents=intents)

# --- Telegram (IMPORTANT: StringSession + connect, PAS start) ---
tg_client = TelegramClient(StringSession(TG_SESSION), API_ID, API_HASH)

# ⚠️ Remplace "shuffleboost" par le @ exact (ou l'id) de la chaîne/canal Telegram source
SOURCE_CHATS = ("shuffleboost",)

@tg_client.on(events.NewMessage(chats=SOURCE_CHATS))
async def on_telegram_message(event):
    text = event.message.message or ""
    channel = discord_client.get_channel(DISCORD_CHANNEL_ID)
    if channel and text.strip():
        await channel.send(f"🚨 **Boost Alert**\n{text}")

async def main():
    # pas de prompt → pas de .start()
    await tg_client.connect()

    # si la session est invalide, on le dit clairement
    if not await tg_client.is_user_authorized():
        raise RuntimeError(
            "TG_SESSION invalide/expirée. Regénère-la avec gen_session.py puis mets la valeur dans la variable d'environnement TG_SESSION."
        )

    # lancer discord + rester connecté à telegram
    await asyncio.gather(
        discord_client.start(DISCORD_TOKEN),
        tg_client.run_until_disconnected()
    )

if __name__ == "__main__":
    asyncio.run(main())

