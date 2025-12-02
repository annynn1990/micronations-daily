import discord
import os
import asyncio

client = discord.Client(intents=discord.Intents.all())  # 開全部 Intent

@client.event
async def on_ready():
    print(f"瘋狂測試版上線！{client.user}")
    channel = client.get_channel(int(os.environ.get("CHANNEL_ID")))
    if channel:
        for i in range(10):
            await channel.send(f"【終極測試第 {i+1}/10 條】\n微國家新聞機器人真的活了！\n時間：{discord.utils.utcnow()}")
            await asyncio.sleep(1)  # 每秒一條
    else:
        print("找不到頻道！CHANNEL_ID 可能錯了")

client.run(os.environ.get("DISCORD_BOT_TOKEN"))
