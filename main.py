import os
import sys

# 強制讓 discord.py 跳過 audioop（語音功能我們根本不用）
sys.modules['audioop'] = object()

import discord
from discord.ext import tasks
import feedparser

intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f"微國家新聞 Bot 上線了！{client.user}")
    channel = client.get_channel(int(os.environ.get("CHANNEL_ID")))
    if channel:
        await channel.send("微國家新聞 Bot 成功啟動！\n每天會自動發送最新微國家新聞～")
        await channel.send("輸入 !ping 試試看我有沒有活著！")

@client.event
async def on_message(message):
    if message.author == client.user:
        return
    if message.content == "!ping":
        await message.channel.send("pong！微國家新聞機器人活著！")

client.run(os.environ.get("DISCORD_BOT_TOKEN"))
