import discord
import os

client = discord.Client(intents=discord.Intents.default())

@client.event
async def on_ready():
    print(f"Bot 上線了！{client.user}")
    channel = client.get_channel(int(os.environ.get("CHANNEL_ID")))
    if channel:
        await channel.send("【測試成功】純文字版機器人已上線！\n從現在開始每天會發微國家新聞～")
    else:
        print("找不到頻道！請確認 CHANNEL_ID 正確")

client.run(os.environ.get("DISCORD_BOT_TOKEN"))
