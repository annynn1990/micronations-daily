from discord_webhook import DiscordWebhook
import os

# 這三行是 Railway 自動傳給你的（千萬不要改）
webhook_url = os.environ.get("WEBHOOK_URL")
content = os.environ.get("DISCORD_MESSAGE", "")

# 只要訊息以 !! 開頭就回應
if content.startswith("!!"):
    reply = content[2:].strip() or "你沒說話喔？"
    # 這裡你想怎麼回都行（下面是範例）
    if "法律" in reply or "條例" in reply:
        reply = ("黃名帝國《首都論壇帖務條例》重點：\n"
                 "• 官方語言是中文，所有官方文件必須有書面中文版\n"
                 "• 可以有英文版，但中文才是準據\n"
                 "• 原創貼文版權歸你，但不能刪已回覆的貼文\n"
                 "• 媒體可免費轉載公開內容\n"
                 "（這是微國家法律，現實請找律師喔～）")
    elif "新聞" in reply:
        reply = "今天微國家圈還算平靜～有大八卦我馬上告訴你！"
    else:
        reply = f"收到：{content[2:]}\n\n我聽到啦！有什麼想問的繼續打 !! 開頭～"

    webhook = DiscordWebhook(url=webhook_url, content=reply)
    webhook.execute()
