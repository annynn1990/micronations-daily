from discord_webhook import DiscordWebhook, DiscordEmbed
import feedparser
import os
import time

webhook_url = os.environ.get("WEBHOOK_URL")
feeds = [
    "https://www.google.com/alerts/feeds/06026802446385447276/13935726808984734935",
    "https://reddit.com/r/micronations/.rss",
    "https://micronations.wiki/feed/",
]

# 簡單記錄已發連結（用檔案）
seen_file = "/tmp/seen_links.txt"
seen = set()
if os.path.exists(seen_file):
    with open(seen_file) as f:
        seen = set(f.read().splitlines())

webhook = DiscordWebhook(url=webhook_url, rate_limit_retry=True)

sent = 0
for url in feeds:
    feed = feedparser.parse(url)
    for entry in feed.entries[:5]:
        link = entry.link
        if link in seen:
            continue
        title = entry.title
        if any(k in title.lower() for k in ["micronation", "sealand", "molossia", "seborga"]):
            embed = DiscordEmbed(title=title, url=link, color=0x00ff00)
            embed.set_footer(text="每日微國家快訊")
            webhook.add_embed(embed)
            seen.add(link)
            sent += 1

# 每天發一則存活訊息
embed = DiscordEmbed(title="微國家新聞機器人存活檢查", description=f"今天發送 {sent} 則新聞\n完全正常運行中～", color=0x00ff00)
webhook.add_embed(embed)

webhook.execute()

# 儲存已發連結
with open(seen_file, "w") as f:
    f.write("\n".join(seen))

print(f"完成！發送 {sent} 則新聞")
