from discord_webhook import DiscordWebhook, DiscordEmbed
import feedparser
import os
import time

webhook_url = os.environ.get("WEBHOOK_URL")
if not webhook_url:
    print("錯誤：沒找到 WEBHOOK_URL")
    exit()

feeds = [
    "https://www.google.com/alerts/feeds/06026802446385447276/13935726808984734935",  # micronation 關鍵字
    "https://reddit.com/r/micronations/.rss",
    "https://micronations.wiki/feed/",
    "https://www.micronationworld.com/feed/"
]

seen_file = "/tmp/seen_links.txt"
seen = set()
if os.path.exists(seen_file):
    with open(seen_file) as f:
        seen = set(f.read().splitlines())

webhook = DiscordWebhook(url=webhook_url, rate_limit_retry=True)

sent_count = 0
news_list = []

for url in feeds:
    feed = feedparser.parse(url)
    source_name = feed.feed.get("title", "未知來源")
    for entry in feed.entries:
        link = entry.link.strip()
        if link in seen:
            continue
            
        title = entry.title
        title_lower = title.lower()
        if any(keyword in title_lower for keyword in ["micronation", "sealand", "molossia", "seborga", "ladonia", "hutt river", "christiania", "asgardia", "micro-nation", "microstate"]):
            news_list.append(f"**{title}**\n來源：{source_name}\n{link}")
            seen.add(link)
            sent_count += 1

# 發送所有新聞（每則一條訊息，最多10則避免洗版）
for news in news_list[:10]:
    webhook.content = news
    webhook.execute()
    time.sleep(1)  # 避免太快被限流

# 永遠發一則總結（就算今天沒新聞也會報到）
summary = f"【每日微國家新聞總結】\n今天共找到 {sent_count} 則新消息\n機器人完全正常運行中～"
webhook.content = summary
webhook.execute()

# 儲存已發連結
with open(seen_file, "w") as f:
    f.write("\n".join(seen))

print(f"完成！今天發送 {sent_count} 則微國家新聞")
