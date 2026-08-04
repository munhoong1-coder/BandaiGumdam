import requests
import os
from datetime import datetime


# 从 GitHub Secrets 获取
TOKEN = os.getenv("TELEGRAM_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")


def send_telegram(message):

    print("======================")
    print("Telegram Debug")
    print("======================")

    # 检查 Secret 有没有传进来
    if TOKEN:
        print("TOKEN: OK")
    else:
        print("TOKEN: MISSING")

    print("CHAT_ID:", CHAT_ID)


    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"


    data = {
        "chat_id": CHAT_ID,
        "text": message
    }


    try:

        response = requests.post(
            url,
            data=data
        )


        print("Telegram API Response:")
        print(response.text)


    except Exception as e:

        print("ERROR:")
        print(e)



# 测试讯息

message = f"""
🤖 Shopee Restock Bot Test

Status:
GitHub Actions Connected ✅

Time:
{datetime.now()}
"""


send_telegram(message)
