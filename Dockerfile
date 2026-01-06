# --- 第一階段：Builder ---
# 專門用來安裝 Python 套件
FROM python:3.11-slim AS builder

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt \
    # 將套件安裝到一個指定資料夾，而不是系統
    --target /app/packages

# --- 第二階段：Final ---
# 這是我們最終要運行的映像檔
FROM python:3.11-slim

WORKDIR /app

# 關閉 Python 的輸出緩衝，讓 print() 能即時出現在 CloudWatch Logs
ENV PYTHONUNBUFFERED=1

# --- 安裝系統依賴 (Chrome 瀏覽器) [核心修正點] ---
# 更新套件列表並安裝必要的工具 (ca-certificates, gnupg, wget)
RUN apt-get update && apt-get install -y \
    tini \
    ca-certificates \
    gnupg \
    wget \
    # 建立存放金鑰的資料夾
    && install -m 0755 -d /etc/apt/keyrings \
    # 下載 Google 的安全金鑰，並存放到推薦的位置
    && wget -q -O - https://dl.google.com/linux/linux_signing_key.pub | gpg --dearmor -o /etc/apt/keyrings/google-chrome.gpg \
    # 新增 Google Chrome 的軟體來源，並明確指定要用哪個金鑰驗證
    && echo "deb [arch=amd64 signed-by=/etc/apt/keyrings/google-chrome.gpg] http://dl.google.com/linux/chrome/deb/ stable main" > /etc/apt/sources.list.d/google-chrome.list \
    # 再次更新套件列表，讓系統知道有 Chrome 可以安裝了
    && apt-get update \
    # 安裝 Google Chrome 穩定版
    && apt-get install -y google-chrome-stable \
    # 清理安裝快取，讓我們的映像檔小一點
    && rm -rf /var/lib/apt/lists/*

# --- 安裝 Python 依賴 ---
COPY --from=builder /app/packages /usr/local/lib/python3.11/site-packages

# --- 複製我們的程式碼 ---
COPY *.py ./

ENTRYPOINT ["/usr/bin/tini", "--"]

# --- 設定啟動指令 ---
CMD ["python", "run_all.py", "--market", "TW"]