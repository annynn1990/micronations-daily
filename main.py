import discord
import os

intents = discord.Intents.default()
intents.message_content = True   # 這行一定要開，不然看不到訊息
client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f"Bot 上線了！{client.user}")
    # 一上線就發一則訊息證明活著
    channel = client.get_channel(int(os.environ.get("CHANNEL_ID")))
    if channel:
        await channel.send("【微國家新聞機器人已上線！】\n輸入 !ping 試試看～")

@client.event
async def on_message(message):
    if message.author == client.user:
        return
    if message.content.startswith('!ping'):
        await message.channel.send("pong！微國家新聞機器人活著！")

client.run(os.environ.get("DISCORD_BOT_TOKEN"))
