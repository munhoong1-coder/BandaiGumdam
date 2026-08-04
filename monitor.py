import requests
import json
import os
from datetime import datetime


TOKEN = os.getenv("TELEGRAM_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")


def send_telegram(message):

    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"

    data = {
        "chat_id": CHAT_ID,
        "text": message
    }

    requests.post(url, data=data)



def check_product(product):

    shop_id = product["shop_id"]
    item_id = product["item_id"]

    api = (
        f"https://shopee.com.my/api/v4/item/get?"
        f"itemid={item_id}&shopid={shop_id}"
    )

    try:
        r = requests.get(api,
        headers={
            "User-Agent":
            "Mozilla/5.0"
        })

        data = r.json()

        item = data["data"]["item"]

        stock = item.get("stock",0)

        return stock > 0


    except Exception as e:
        print(e)
        return False



with open("products.json") as f:
    products=json.load(f)



for product in products:

    available = check_product(product)


    if available:

        msg=f"""
🚨 SHOPEE RESTOCK ALERT 🚨

商品:
{product['name']}

状态:
AVAILABLE ✅

时间:
{datetime.now()}

链接:
{product['url']}
"""

        send_telegram(msg)
