from discord_webhook import DiscordWebhook
import feedparser
import os
import httpx
from deep_translator import GoogleTranslator

webhook_url = os.environ.get("WEBHOOK_URL")
if not webhook_url:
    print("沒找到 webhook")
    exit()

# 簡單記憶上一次抓到的連結
seen_file = "/tmp/seen.txt"
seen = set(open(seen_file).read().splitlines()) if os.path.exists(seen_file) else set()

# 所有微國家 RSS
feeds = [
    "https://www.google.com/alerts/feeds/06026802446385447276/13935726808984734935",
    "https://reddit.com/r/micronations/.rss",
    "https://micronations.wiki/feed/",
    "https://www.micronationworld.com/feed/"
]

def get_latest_news():
    news = []
    for url in feeds:
        feed = feedparser.parse(url)
        for e in feed.entries[:10]:
            if e.link in seen:
                continue
            title = e.title
            if any(k in title.lower() for k in ["micronation","sealand","molossia","seborga","ladonia","hutt river","asgardia","christiania"]):
                news.append(f"• {title}")
                seen.add(e.link)
    with open(seen_file, "w") as f:
        f.write("\n".join(seen))
    return news if news else ["今天暫時沒抓到新鮮的微國家八卦～"]

# 收到 !! 開頭的訊息就觸發
content = os.environ.get("TRIGGER_MESSAGE", "")
if content.startswith("!!"):
    question = content[2:].strip()

    # 關鍵字觸發微國家新聞
    if any(k in question.lower() for k in ["新聞","動態","最近","micro","micronation","sealand","molossia"]):
        news = get_latest_news()
        reply = "微國家最新情報來啦！\n\n" + "\n\n".join(news)
    else:
        # 其他問題就直接用 Grok 風格回（你現在看到的語氣）
        reply = f"嗯？{question}\n\n哈哈這個問題有點意思啊～\n不過我現在是專職微國家情報員，其他的等我下班再聊啦（逃"

    webhook = DiscordWebhook(url=webhook_url, content=reply)
    webhook.execute()
