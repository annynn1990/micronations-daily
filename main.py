import discord
from discord.ext import tasks
import feedparser
import os

intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)

TOKEN = os.environ.get("DISCORD_BOT_TOKEN")
CHANNEL_ID = int(os.environ.get("CHANNEL_ID"))

FEEDS = [
    "https://www.google.com/alerts/feeds/06026802446385447276/13935726808984734935",
    "https://reddit.com/r/micronations/.rss",
    "https://micronations.wiki/feed/",
    "https://www.micronationworld.com/feed/"
]

seen_links = set()

@client.event
async def on_ready():
    print(f"微國家新聞 Bot 上線了！{client.user}")
    channel = client.get_channel(CHANNEL_ID)
    if channel:
        await channel.send("微國家新聞 Bot 已上線！每天自動發送最新新聞～")
    daily_news.start()

@tasks.loop(hours=24)
async def daily_news():
    channel = client.get_channel(CHANNEL_ID)
    if not channel:
        return

    sent = 0
    for url in FEEDS:
        feed = feedparser.parse(url)
        source = getattr(feed.feed, "title", "未知來源")
        for entry in feed.entries[:10]:
            link = entry.link
            if link in seen_links:
                continue
            title_lower = entry.title.lower()
            if any(k in title_lower for k in ["micronation", "sealand", "molossia", "seborga", "ladonia"]):
                embed = discord.Embed(title=entry.title[:250], url=link, description=f"來源：{source}", color=0x00ff88)
                await channel.send(embed=embed)
                seen_links.add(link)
                sent += 1

    await channel.send(embed=discord.Embed(
        title="每日微國家新聞檢查",
        description=f"今天發送 {sent} 則新新聞\n機器人正常運行中～",
        color=0x00ff00
    ))

client.run(TOKEN)
