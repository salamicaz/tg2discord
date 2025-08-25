import os
import asyncio
from telethon import TelegramClient, events
import discord
from dotenv import load_dotenv

# Charger les variables depuis .env
load_dotenv()
TG_API_ID = int(os.getenv("TG_API_ID"))
TG_API_HASH = os.getenv("TG_API_HASH")
DISCORD_TOKEN = os.getenv("DISCORD_BOT_TOKEN")
DISCORD_CHANNEL_ID = int(os.getenv("DISCORD_CHANNEL_ID"))

# Discord setup
intents = discord.Intents.default()
discord_client = discord.Client(intents=intents)

# Telegram setup
tg_client = TelegramClient("tg_session", TG_API_ID, TG_API_HASH)

@tg_client.on(events.NewMessage(chats="shuffleboost"))
async def handler(event):
    text = event.message.message or "(pas de texte)"
    channel = discord_client.get_channel(DISCORD_CHANNEL_ID)
    if channel:
        await channel.send(f"🚀 **Boost Alert**\n{text}")

async def main():
    await tg_client.start()
    await asyncio.gather(
        tg_client.run_until_disconnected(),
        discord_client.start(DISCORD_TOKEN),
    )

if __name__ == "__main__":
    asyncio.run(main())
