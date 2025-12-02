from discord_webhook import DiscordWebhook
import feedparser
import os
from deep_translator import GoogleTranslator   # 超穩免費翻譯

webhook_url = os.environ.get("WEBHOOK_URL")
if not webhook_url:
    print("錯誤：沒找到 WEBHOOK_URL")
    exit()

# 需要翻譯的 RSS 來源
feeds = [
    "https://www.google.com/alerts/feeds/06026802446385447276/13935726808984734935",
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
news_lines = []

for url in feeds:
    feed = feedparser.parse(url)
    source = feed.feed.get("title", "未知來源")
    for entry in feed.entries:
        link = entry.link.strip()
        if link in seen:
            continue

        raw_title = entry.title
        # 關鍵字過濾（更廣泛抓微國家）
        if any(k in raw_title.lower() for k in ["micronation","sealand","molossia","seborga","ladonia","hutt river","asgardia","micro nation","christiania","unrecognized state"]):
            # 自動翻譯成繁體中文
            try:
                zh_title = GoogleTranslator(source='auto', target='zh-TW').translate(raw_title)
            except:
                zh_title = raw_title  # 翻譯失敗就用原文

            news_lines.append(f"• {zh_title} （來源：{source}）")
            seen.add(link)

# 儲存已發連結
with open(seen_file, "w") as f:
    f.write("\n".join(seen))

# 整理成一篇美美的純文字訊息發送
if news_lines:
    content = "【今日微國家新聞速報】\n\n" + "\n\n".join(news_lines) + f"\n\n共 {len(news_lines)} 則新消息"
else:
    content = "【今日微國家新聞】\n\n今天暫無新消息～\n機器人正常運行中"

webhook.content = content
response = webhook.execute()

print(f"發送完成！今日共 {len(news_lines)} 則新聞")
