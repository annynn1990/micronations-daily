import feedparser
import requests
import datetime
import os

WEBHOOK_URL = os.environ.get('WEBHOOK_URL')
if not WEBHOOK_URL:
    print("錯誤：沒找到 WEBHOOK_URL")
    exit()

FEEDS = [
    "https://www.google.com/alerts/feeds/06026802446385447276/13935726808984734935",
    "https://reddit.com/r/micronations/.rss",
    "https://micronations.wiki/feed/",
    "https://www.micronationworld.com/feed/"
]

SEEN_FILE = "/tmp/seen.txt"

def load_seen():
    if os.path.exists(SEEN_FILE):
        with open(SEEN_FILE) as f:
            return set(f.read().splitlines())
    return set()

def save_seen(seen):
    with open(SEEN_FILE, "w") as f:
        f.write("\n".join(seen))

def send(title, url, source):
    embed = {
        "title": title[:250],
        "url": url,
        "description": f"來源：{source}",
        "color": 3447003,
        "timestamp": datetime.datetime.utcnow().isoformat(),
        "footer": {"text": "每日微國家快訊"}
    }
    try:
        requests.post(WEBHOOK_URL, json={"embeds": [embed], "username": "微國家小喇叭"})
        print(f"已發送：{title}")
    except:
        print("發送失敗")

seen = load_seen()
new_seen = seen.copy()

for feed_url in FEEDS:
    feed = feedparser.parse(feed_url)
    source = feed.feed.get("title", "未知來源")
    for entry in feed.entries[:10]:
        link = entry.link
        if link in seen: continue
        title = entry.title
        if "micronation" in title.lower() or "sealand" in title.lower() or "molossia" in title.lower():
            send(title, link, source)
            new_seen.add(link)

save_seen(new_seen)
print("今日微國家新聞推送完成！")

# 強制發送測試訊息（不管有沒有新聞都會發）
requests.post(
    WEBHOOK_URL,
    json={
        "content": "**微國家新聞機器人啟動成功！**",
        "embeds": [{
            "title": "測試訊息",
            "description": "如果您看到這則訊息，代表一切設定正確！\n每天 16:00 會自動發送最新微國家新聞～",
            "color": 5814783,
            "footer": {"text": "GitHub Actions + Discord"}
        }]
    }
)
print("測試訊息已強制發送！")
