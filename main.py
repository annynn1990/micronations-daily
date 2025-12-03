from discord_webhook import DiscordWebhook
import feedparser
import os
import time

# 你的 webhook 網址（放進 Railway Variables）
WEBHOOK_URL = os.environ.get("WEBHOOK_URL")
if not WEBHOOK_URL:
    print("錯誤：請設定 WEBHOOK_URL")
    exit()

# 收到訊息的內容（Railway 會傳給你）
message = os.environ.get("DISCORD_MESSAGE", "")

# 如果是以 !! 開頭就觸發回應
if message.startswith("!!"):
    question = message[2:].strip().lower()

    # 簡單關鍵字回應（你可以一直加）
    if "法律" in question or "條例" in question or "英文" in question:
        reply = ("黃名帝國《首都論壇帖務條例》重點整理：\n\n"
                 "• 官方語言是中文，所有官方文件必須有書面中文版\n"
                 "• 可以有英文或其他版本，但中文版才是法律效力來源\n"
                 "• 原創帖文版權歸你，但不能刪除別人回覆的貼文\n"
                 "• 媒體可以免費轉載公開貼文\n"
                 "• 司法文件必須用書面中文\n\n"
                 "（這是微國家法律，現實請找律師喔～）")
    elif "新聞" in question or "微國家" in question:
        reply = "今天微國家圈還沒爆炸性新聞～有新鮮八卦我馬上告訴你！"
    elif "乞丐" in question or "你好帥" in question:
        reply = "對啊我就是自由城最帥的乞丐！今天又撿到一個鋁罐，王國又壯大了～"
    else:
        reply = f"你說：{message[2:]}\n\n我聽到啦！有什麼想問的直接打 !! 開頭，我隨時都在～"

    # 發送回應
    webhook = DiscordWebhook(url=WEBHOOK_URL, content=reply)
    webhook.execute()
    print("已回應：" + reply)
else:
    print("不是 !! 開頭，忽略")
