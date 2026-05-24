# Lazy News AI - Daily AI-Automated Financial News Telegram Bot

**Lazy News AI** is a cloud-native, fully automated system designed for busy investors. The system runs on a self-hosted Linux server with cron scheduling, delivering financial news summaries and weekly outlooks via **Telegram Bot push notifications**.

Lazy News AI 是一個專為繁忙投資者設計的全自動化系統，運行於自架 Linux Server，透過 cron 排程每日定時執行。系統會自動抓取台股與美股的財經新聞，利用 **Google Gemini AI** 進行深度分析，透過 **Azure TTS** 生成語音導讀，並推播至 **Telegram** 頻道。每週另有一份整合週報，聚焦未來產業趨勢。

## ✨ Features

* **🌍 Dual Market Coverage**: Automated news processing for both **Taiwan Stocks (TW)** and **US Stocks (US)**.
* **📥 Two-Phase Crawling**: Crawls news in two batches per day to maximize coverage — first batch is stored, second batch merges with the first before analysis, preventing data loss from page auto-cleanup.
* **🧠 AI-Powered Daily Report**: Integrates **Google Gemini AI** (`gemini-2.5-flash`) to generate structured daily reports covering sector focus, key company updates, and market analysis.
* **📅 Weekly Outlook Report**: Every Sunday, generates a weekly trend report using the past two weeks of daily summaries with a **3:2 weighting** (current week weighted higher). Focuses on emerging industries and future outlook.
* **📢 Telegram Delivery**: Uses **Telegraph** to generate clean web reading pages and pushes both the article link and MP3 audio file to a Telegram channel.
* **🗣️ Audio Generation**: Integrates **Azure AI Speech** to convert reports into natural MP3 audio guides.
* **🛡️ Reliability**: Features smart scrolling with retry mechanisms for stable Selenium-based scraping.

## 🚀 How It Works

### Daily Report（每日流程）

**台股 (TW)**
1. **19:30** — `crawl_only`：爬取新聞存入 SQLite
2. **07:30** — `crawl_and_report`：再次爬取並合併，AI 分析生成報告，TTS 語音，推播 Telegram，清空文章

**美股 (US)**
1. **08:00** — `crawl_only`：爬取新聞存入 SQLite
2. **20:00** — `crawl_and_report`：再次爬取並合併，AI 分析生成報告，TTS 語音，推播 Telegram，清空文章

### Weekly Report（週報流程）

**每週日 21:00** — 讀取過去兩週的每日摘要，以 3:2 加權（當週權重較高）生成未來產業展望週報，推播 Telegram

### Daily Report Structure

1. **焦點產業** — 本日市場焦點產業與原因
2. **關鍵公司動態** — 至少三家重要公司的關鍵事件
3. **市場重點分析** — 整體氣氛、指數表現與當日核心主軸

### Weekly Report Structure

1. **本週市場回顧** — 綜合兩週走勢
2. **持續發燒產業** — 跨週持續受關注的產業
3. **新興訊號** — 當週才出現的新題材
4. **未來值得關注的產業** — 下週重點追蹤方向
5. **小結** — 核心主軸總結

## 🛠️ Tech Stack

| Category | Technology |
| --- | --- |
| **Core** | Python 3.11 |
| **Web Scraper** | Selenium (Headless Chrome), BeautifulSoup4 |
| **Database** | SQLite (news deduplication, 14-day summary retention) |
| **AI Services** | Google Gemini API `gemini-2.5-flash` (Analysis), Azure AI Speech (TTS) |
| **Automation** | Linux cron (self-hosted server) |
| **Messaging** | Telegram Bot API, Telegraph |

## ⚙️ Quick Start

### 1. Environment Setup

Create a `.env` file in the root directory:

```env
GOOGLE_API_KEY=your_gemini_key
AZURE_SPEECH_KEY=your_azure_key
AZURE_SPEECH_REGION=your_azure_region
TELEGRAM_BOT_TOKEN=your_bot_token
TELEGRAM_CHAT_ID=your_chat_or_channel_id
```

### 2. Install Dependencies

```bash
# Install Chrome
wget -q -O - https://dl.google.com/linux/linux_signing_key.pub | gpg --dearmor -o /usr/share/keyrings/google-chrome.gpg
echo "deb [arch=amd64 signed-by=/usr/share/keyrings/google-chrome.gpg] http://dl.google.com/linux/chrome/deb/ stable main" > /etc/apt/sources.list.d/google-chrome.list
apt update && apt install -y google-chrome-stable

# Install Python packages
pip install -r requirements.txt
```

### 3. Run Manually

```bash
# 只爬蟲存入 DB（第一次）
python3 run_all.py --market TW --mode crawl_only
python3 run_all.py --market US --mode crawl_only

# 爬蟲 + 分析 + 推播（第二次）
python3 run_all.py --market TW --mode crawl_and_report
python3 run_all.py --market US --mode crawl_and_report

# 生成週報
python3 weekly_report.py --market TW
python3 weekly_report.py --market US
```

### 4. Setup Cron (Linux Server)

```bash
# 修改 setup_cron.sh 內的 PROJECT_DIR 後執行
bash setup_cron.sh
```

## ⏰ Cron Schedule (UTC)

| Task | UTC | 台北時間 |
| --- | --- | --- |
| TW crawl_only | 11:30 | 19:30 |
| TW crawl_and_report | 23:30 | 07:30 |
| US crawl_only | 00:00 | 08:00 |
| US crawl_and_report | 12:00 | 20:00 |
| Weekly TW | Sun 13:00 | Sun 21:00 |
| Weekly US | Sun 13:30 | Sun 21:30 |

---

*Disclaimer: All content is AI-generated for informational purposes only and does not constitute financial or investment advice.*
