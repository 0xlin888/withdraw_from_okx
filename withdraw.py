import json
import random
import time
import requests
import pandas as pd
import hmac
import hashlib
import base64
from datetime import datetime, timezone

API_KEY = ''  # 替换为你的 API KEY
SECRET_KEY = ''  # 替换为你的 API 密钥
PASSPHRASE = ''  # 替换为你的 API Passphrase

# 提现币种（示例：G）
CURRENCY = "G"
CHAIN = "G-Gravity Alpha Mainnet"  # 选择提现链
FEE = "0.000001"  # 提现手续费，具体根据 OKX 规则调整

# 读取 Excel 文件（假设第一列是地址，第二列是金额，第三列是提现状态）
EXCEL_PATH = r"D:\withdraw.xlsx"

# 生成符合 OKX 认证要求的时间戳（ISO 8601 格式）
def get_iso_timestamp():
    return datetime.now(timezone.utc).isoformat(timespec="milliseconds").replace("+00:00", "Z")

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


# 提现
def withdraw(address, amount):
    url = "https://www.okx.com/api/v5/asset/withdrawal"
    request_path = "/api/v5/asset/withdrawal"
    method = "POST"

    body = {
        "ccy": CURRENCY,
        "chain": CHAIN,
        "amt": str(amount),
        "dest": "4",  # 4 代表提现到外部地址
        "toAddr": address,
        "fee": FEE
    }

    body_str = json.dumps(body, separators=(",", ":"))
    headers = generate_headers(API_KEY, SECRET_KEY, PASSPHRASE, method, request_path, body_str)

    try:
        response = requests.post(url, headers=headers, data=body_str)
        response.raise_for_status()
        data = response.json()

        if data.get("code") == "0":
            wd_id = data.get("data")[0]["wdId"]
            return True, wd_id
        else:
            print(f"❌ 提现失败: {data.get('msg')}")
            return False, None
    except requests.exceptions.RequestException as e:
        print(f"❌ 请求失败: {e}")
        return False, None

# 处理 Excel 数据（每次成功提现后立即更新状态）
def process_withdrawals():
    try:
        df = pd.read_excel(EXCEL_PATH)
    except Exception as e:
        print(f"❌ 读取Excel文件失败: {e}")
        return

    # 列数检查
    if df.shape[1] < 3:
        print("❌ Excel 格式错误，请确保至少有3列（地址、金额、提现状态）")
        return

    # 列名处理
    df.columns = list(df.columns[:3]) + list(df.columns[3:])
    df = df.rename(columns={0: "address", 1: "amount", 2: "status"})

    # 添加时间列（如果不存在）
    if "time" not in df.columns:
        df["time"] = ""

    pending_withdrawals = df[df["status"].isna()].copy()  # 选择未提现的
    pending_withdrawals = pending_withdrawals.sample(frac=1).reset_index(drop=True)  # 随机打乱

    for index, row in pending_withdrawals.iterrows():
        address, amount = row["address"], row["amount"]

        print(f"🚀 正在向 {address} 提现 {amount} {CURRENCY}...")
        success, wd_id = withdraw(address, amount)

        if success:
            # 更新 Excel 文件的状态
            df["status"] = df["status"].astype(str)
            df.loc[df["address"] == address, "status"] = "已提现"
            # 确保 'time' 列是字符串类型
            df["time"] = df["time"].astype(str)
            df.loc[df["address"] == address, "time"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            print(f"✅ 提现成功! 提现ID: {wd_id}")

            # 立即保存 Excel 文件
            df.to_excel(EXCEL_PATH, index=False)

        else:
            print(f"⚠️ 提现失败: {address}")

        # 设置随机时间间隔，防止频繁请求
        sleep_time = random.randint(120, 300)
        minutes, seconds = divmod(sleep_time, 60)  # 计算分钟和秒
        for remaining in range(sleep_time, 0, -1):
            mins, secs = divmod(remaining, 60)
            print(f"\r⏳ 等待 {mins} 分 {secs} 秒", end="", flush=True)
            time.sleep(1)

    print("✅ 所有提现处理完成，已更新 Excel！")

if __name__ == "__main__":
    process_withdrawals()
