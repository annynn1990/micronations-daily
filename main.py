import discord
import os
import feedparser

# 強制騙過 audioop（關鍵！）
import types
sys.modules['audioop'] = types.ModuleType('audioop')

client = discord.Client(intents=discord.Intents.all())

@client.event
async def on_ready():
    print(f"【微國家 Grok】上線啦！{client.user}")

@client.event
async def on_message(message):
    if message.author == client.user:
        return
    if message.content.startswith("!!"):
        query = message.content[2:].strip()
        # 這裡之後你可以讓它呼叫任何 API、抓新聞、聊天都行
        await message.channel.send(f"收到啦：{query}\n等我 3 秒，我正在翻整篇微國家情報給你～")

client.run(os.environ.get("DISCORD_BOT_TOKEN"))
