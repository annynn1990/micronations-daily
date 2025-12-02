from discord_webhook import DiscordWebhook
import feedparser
import os

# 你的 webhook 網址（記得放進 Railway Variables）
WEBHOOK_URL = os.environ.get("WEBHOOK_URL")
if not WEBHOOK_URL:
    print("錯誤：請設定 WEBHOOK_URL")
    exit()

# 所有微國家來源
FEEDS = [
    "https://www.google.com/alerts/feeds/06026802446385447276/13935726808984734935",
    "https://reddit.com/r/micronations/.rss",
    "https://micronations.wiki/feed/",
    "https://www.micronationworld.com/feed/"
]

# 記錄已發過的連結
SEEN_FILE = "/tmp/seen_links.txt"
seen = set()
if os.path.exists(SEEN_FILE):
    with open(SEEN_FILE) as f:
        seen = set(line.strip() for line in f)

webhook = DiscordWebhook(url=WEBHOOK_URL)
news = []

for url in FEEDS:
    feed = feedparser.parse(url)
    for entry in feed.entries:
        link = entry.link.strip()
        if link in seen:
            continue
        title = entry.title
        if any(k in title.lower() for k in ["micronation", "sealand", "molossia", "seborga", "ladonia", "hutt river"]):
            news.append(f"• {title}")
            seen.add(link)

# 存檔
with open(SEEN_FILE, "w") as f:
    f.write("\n".join(seen))

# 發送結果
if news:
    content = "【今日微國家新聞】\n\n" + "\n\n".join(news)
else:
    content = "【今日微國家新聞】\n\n今天暫無新消息～機器人正常運行中"

webhook.content = content
response = webhook.execute()

print(f"成功發送！共 {len(news)} 則新聞")
