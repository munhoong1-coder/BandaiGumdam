import json
import os
import requests

ITEMS = [
    {"shopid": 435791627, "itemid": 47515367410, "name": "商品 1"},
    {"shopid": 435791627, "itemid": 50114610930, "name": "商品 2"}
]

TG_BOT_TOKEN = os.environ.get("TG_BOT_TOKEN")
TG_CHAT_ID = os.environ.get("TG_CHAT_ID")

def send_telegram_notification(message):
    if TG_BOT_TOKEN and TG_CHAT_ID:
        url = f"https://api.telegram.org/bot{TG_BOT_TOKEN}/sendMessage"
        payload = {"chat_id": TG_CHAT_ID, "text": message, "parse_mode": "Markdown"}
        requests.post(url, json=payload)

def check_stock():
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Referer": "https://shopee.com.my/"
    }
    
    stock_state = []

    for item in ITEMS:
        api_url = f"https://shopee.com.my/api/v4/item/get?itemid={item['itemid']}&shopid={item['shopid']}"
        try:
            res = requests.get(api_url, headers=headers, timeout=10)
            res_data = res.json().get("data", {})
            
            title = res_data.get("title", item["name"])
            stock = res_data.get("stock", 0)
            models = res_data.get("models", [])
            
            # 判断是否有货（true / false）
            is_in_stock = stock > 0
            
            item_info = {
                "itemid": item["itemid"],
                "shopid": item["shopid"],
                "title": title,
                "in_stock": is_in_stock,  # 有货为 true，没货为 false
                "total_stock": stock,
                "url": f"https://shopee.com.my/product/{item['shopid']}/{item['itemid']}"
            }
            stock_state.append(item_info)

            # 有货时发送通知
            if is_in_stock:
                send_telegram_notification(f"🚨 *Shopee 补货通知！*\n\n*商品:* {title}\n*库存:* {stock}\n\n[👉 点击购买]({item_info['url']})")

        except Exception as e:
            print(f"检查商品 {item['itemid']} 出错: {e}")

    # 保存 JSON 到当前目录
    with open("stock_state.json", "w", encoding="utf-8") as f:
        json.dump(stock_state, f, ensure_ascii=False, indent=2)

if __name__ == "__main__":
    check_stock()
