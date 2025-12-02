import discord
import os
import feedparser

client = discord.Client(intents=discord.Intents.none())

@client.event
async def on_ready():
    print(f"微國家新聞 Bot 上線了！{client.user}")
    channel = client.get_channel(int(os.environ.get("CHANNEL_ID")))
    if channel:
        await channel.send("【微國家新聞 Bot 成功啟動！】\n從現在開始每天會自動發送最新微國家新聞～")
    else:
        print("找不到頻道！")

client.run(os.environ.get("DISCORD_BOT_TOKEN"))
