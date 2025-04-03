import requests
import time
import hmac
import base64
import hashlib
from datetime import datetime, timezone

API_KEY = ''  # 替换为你的 API KEY
SECRET_KEY = ''  # 替换为你的 API 密钥
PASSPHRASE = ''  # 替换为你的 API Passphrase

# 生成符合 OKX 认证要求的时间戳（ISO 8601 格式）
def get_iso_timestamp():
    return datetime.now(timezone.utc).isoformat(timespec='milliseconds').replace("+00:00", "Z")

# 生成 OKX API 请求的认证头部
def generate_headers(api_key, secret_key, passphrase, method, request_path, body=""):
    timestamp = get_iso_timestamp()  
    message = timestamp + method.upper() + request_path + body  
    signature = base64.b64encode(
        hmac.new(secret_key.encode(), message.encode(), hashlib.sha256).digest()
    ).decode()

    headers = {
        "OK-ACCESS-KEY": api_key,
        "OK-ACCESS-SIGN": signature,
        "OK-ACCESS-TIMESTAMP": timestamp,
        "OK-ACCESS-PASSPHRASE": passphrase,
        "Content-Type": "application/json"
    }
    return headers

# 获取 OKX 指定币种的信息
def get_okx_currency(currency_code):
    request_path = f"/api/v5/asset/currencies?ccy={currency_code}"
    url = f"https://www.okx.com{request_path}"  
    method = "GET"

    headers = generate_headers(API_KEY, SECRET_KEY, PASSPHRASE, method, request_path)
    
    try:
        response = requests.get(url, headers=headers)
        # print("Response Status Code:", response.status_code)
        # print("Response Headers:", response.headers)
        # print("Response Body:", response.text)

        response.raise_for_status()
        data = response.json()

        if data.get("code") == "0":
            return data.get("data", [])
        else:
            print(f"Error: {data.get('msg')}")
            return []
    except requests.exceptions.RequestException as e:
        print(f"Request failed: {e}")
        return []

if __name__ == "__main__":
    currency_code = "ETH"  # 你要查询的币种，例如 "BTC", "ETH", "USDT"
    currency_info = get_okx_currency(currency_code)
if currency_info:
    print(f"\n🔹 查询结果（{currency_code}）:\n")
    for currency in currency_info:
        print(f"   🔸 币种: {currency['ccy']}")
        print(f"   🔹 链名: {currency['chain']}")
        print(f"   🔹 最小提现: {currency['minWd']}")
        print(f"   🔹 提现手续费: {currency['fee']}")
        print(f"   🔹 合约地址: {currency['ctAddr'] or '无'}")
        print("-" * 40)
else:
    print(f"❌ 未找到 {currency_code} 的数据")
