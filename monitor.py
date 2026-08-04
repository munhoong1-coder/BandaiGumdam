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
        "text": message,
        "disable_web_page_preview": False
    }

    try:
        response = requests.post(
            url,
            data=data,
            timeout=10
        )

        print("Telegram:")
        print(response.text)

    except Exception as e:
        print("Telegram Error:")
        print(e)



def check_product(product):

    shop_id = product["shop_id"]
    item_id = product["item_id"]


    url = (
        "https://shopee.com.my/api/v4/item/get"
        f"?itemid={item_id}"
        f"&shopid={shop_id}"
    )


    headers = {
        "User-Agent":
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
        "Accept":
        "application/json"
    }


    try:

        response = requests.get(
            url,
            headers=headers,
            timeout=10
        )


        data = response.json()


        item = data["data"]["item"]


        stock = item.get(
            "stock",
            0
        )


        price = item.get(
            "price",
            0
        )


        # Shopee price 是 cents
        price = price / 100000


        print(
            product["name"],
            "Stock:",
            stock,
            "Price:",
            price
        )


        return {
            "available": stock > 0,
            "stock": stock,
            "price": price
        }


    except Exception as e:

        print(
            "Shopee Error:",
            e
        )

        return {
            "available": False,
            "stock": 0,
            "price": 0
        }




# 读取商品列表

with open("products.json") as f:
    products = json.load(f)



for product in products:


    result = check_product(product)


    if result["available"]:


        message = f"""
🚨 SHOPEE RESTOCK ALERT 🚨


商品:
{product['name']}


库存:
{result['stock']} 件


价格:
RM {result['price']:.2f}


时间:
{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}


购买链接:
{product['url']}
"""


        send_telegram(message)

