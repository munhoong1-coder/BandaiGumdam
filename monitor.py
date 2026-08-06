import os
import requests

# 需要监控的 Shopee 商品列表
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
    
    for item in ITEMS:
        api_url = f"https://shopee.com.my/api/v4/item/get?itemid={item['itemid']}&shopid={item['shopid']}"
        try:
            res = requests.get(api_url, headers=headers, timeout=10)
            data = res.json().get("data", {})
            
            stock = data.get("stock", 0)
            title = data.get("title", item["name"])
            item_url = f"https://shopee.com.my/product/{item['shopid']}/{item['itemid']}"
            
            print(f"[{title}] 当前库存: {stock}")
            
            # 如果存在子规格 (models)，也可以单独检查具体型号库存
            models = data.get("models", [])
            available_models = [m['name'] for m in models if m.get("stock", 0) > 0] if models else []

            if stock > 0:
                msg = f"🚨 *Shopee 补货通知！*\n\n*商品名称:* {title}\n*总库存:* {stock}\n"
                if available_models:
                    msg += f"*可用规格:* {', '.join(available_models)}\n"
                msg += f"\n[👉 立即点击购买]({item_url})"
                
                send_telegram_notification(msg)
        except Exception as e:
            print(f"检查商品 {item['itemid']} 出错: {e}")

if __name__ == "__main__":
    check_stock()

