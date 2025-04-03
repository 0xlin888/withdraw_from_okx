# OKX 自动提现脚本 - 小白教程
📢 我的推特

![](https://raw.githubusercontent.com/0xlin888/withdraw_from_okx/refs/heads/main/x.png?raw=true)

🔗[@0x零](https://x.com/0xlin888) 求个关注！如果有任何使用问题，可以通过推特联系我。
## 📌 1. 什么是这个脚本？
这个 Python 脚本可以帮助你自动从 OKX 提现任意的加密货币（前提是OKX支持API提现的币种）到你的钱包地址。它会从 Excel 文件中读取地址和金额，并按照设置的随机时间间隔自动执行提现操作。

---

## 🛠 2. 需要准备什么？

### ✅ 基础要求
- 一台可以运行 Python 的电脑（Windows / Mac / Linux 都可以）
- 安装 Python（建议使用 Python 3.8 及以上）
- 一个 OKX 账户，并获取 API Key
- 一个 Excel 文件，存储提现数据

### ✅ 安装 Python
如果你的电脑没有 Python，可以按照下面的方式安装：
1. **Windows 用户**：
   - 访问 [Python 官网](https://www.python.org/downloads/) 下载最新版本。
   - 安装时勾选“Add Python to PATH”。
   - 安装完成后，在终端（cmd）输入 `python --version`，如果出现 Python 版本号，说明安装成功。

2. **Mac 用户**：
   - 打开“终端”输入：
     ```sh
     brew install python
     ```
   - 安装完成后，输入 `python3 --version` 检查是否成功。

---

## 📦 3. 安装必需的工具

打开终端（Windows 叫“命令提示符” CMD），输入以下命令安装所需的 Python 库：

```sh
pip install requests pandas openpyxl
```

这些库的作用如下：
- `requests`：用于向 OKX API 发送请求
- `pandas`：用于读取和处理 Excel 文件
- `openpyxl`：用于操作 `.xlsx` 格式的 Excel 文件

如果安装成功，你可以输入 `pip list` 来检查它们是否已经安装。

---

## 🔑 4. 获取 OKX API Key

![](https://raw.githubusercontent.com/0xlin888/withdraw_from_okx/refs/heads/main/1.png?raw=true)

1. 登录 OKX 账户。
2. 进入  [API](https://www.okx.com/zh-hans/account/my-api)  页面。
3. 创建新的 API 密钥，确保权限包含“提现”权限。
4. 复制 `API_KEY`、`SECRET_KEY` 和 `PASSPHRASE`，并填写到脚本中对应的位置。

⚠️ **注意**：API Key 请务必保密，不要泄露给他人！

---
## 🛡️ 5. 提现地址加入白名单

![](https://raw.githubusercontent.com/0xlin888/withdraw_from_okx/refs/heads/main/2.png?raw=true)

1. 登录 OKX 账户。
3. 进入  [地址簿](https://www.okx.com/zh-hans/balance/withdrawal-address)  页面。
4. 把需要提现的地址全部加入白名单，提什么链的就加什么链的地址，如提SUI就把SUI地址加入白名单，提ETH就把EVM地址就如白名单。

---

## 📊 6. 准备 Excel 文件

创建一个 Excel 文件，文件格式如下：

| address           | amount    | status   |
|---------------|--------|--------|
| 0x123456789   | 10.5   | （留空）|
| 0x987654321   | 5.2    | （留空）|

- **第一列**（address）：输入接收提现的区块链地址。
- **第二列**（amount）：输入要提现的金额。
- **第三列**（status）：不用填，脚本会自动更新。
- **文件路径**：记下 Excel 文件的路径，填入脚本 `EXCEL_PATH` 变量。

---
## 🪙 7. 查询币种信息

先在info.py中大概第60行修改要查询的币种，如查询SUI
```sh
currency_code = "SUI"
```
然后运行脚本，不会运行脚本看9常见问题
```sh
🔹 查询结果（SUI）:

   🔸 币种: SUI
   🔹 链名: SUI-SUI
   🔹 最小提现: 0.1
   🔹 提现手续费: 0.06
   🔹 合约地址: 无
```
---

## 📜 8. 运行提现脚本

![](https://raw.githubusercontent.com/0xlin888/withdraw_from_okx/refs/heads/main/3.png?raw=true)

修改withdraw.py配置，以SUI为例

找到大概第16行，修改为查询到的币种提现信息

```sh
CURRENCY = "SUI"

CHAIN = "SUI-SUI"  # 选择提现链

FEE = "0.06"  # 提现手续费
```

找到大概第21行，修改为提现地址的excel路径
```sh

EXCEL_PATH = r"D:\withdraw.xlsx"
```

找到大概第126行，修改随机间隔的时间，单位是秒
```sh

sleep_time = random.randint(120, 300)
```

然后运行脚本，然后运行脚本，不会运行脚本看9常见问题

---

## 🧐 9. 常见问题

### ❓ 如何确认 Python 是否安装正确？
打开终端输入：
```sh
python --version
```
如果出现类似 `Python 3.10.5`，说明安装成功。

### ❓ 运行 `pip install` 时出错？
尝试加 `--upgrade` 重新安装：
```sh
pip install --upgrade requests pandas openpyxl
```
### ❓ 如何运行脚本？

**步骤 1: 打开命令行工具**

Windows**：按 `Win + R`，输入 `cmd`，然后按回车。

Mac/Linux**：打开终端（Terminal）。

**步骤 2: 切换到脚本目录**

使用 `cd` 命令切换到存放 Python 脚本的目录。假设你的脚本在桌面上的 `my_project` 文件夹中，可以使用以下命令：

```bash
cd ~/Desktop/my_project
```
**步步骤 3: 运行脚本**
```bash
python3 script.py
```
script改为你要运行的脚本名

### ❓ 提现失败？
- 确保 API Key 填写正确，并具有提现权限。
- 确保 Excel 文件地址正确。
- 确保 OKX 账户有足够余额。

---

## 🛑 10. 免责声明
本脚本仅供学习交流，请自行承担使用风险！使用前请确保了解 OKX 的提现规则。

📌 **有问题？欢迎留言讨论！** 🚀

