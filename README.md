# Lazy News AI - Daily AI-Automated Financial News Telegram Bot

**Lazy News AI** is a cloud-native, fully automated system designed for busy investors. To optimize delivery reliability and reduce maintenance costs, the system has transitioned from traditional newsletters to **Telegram Bot push notifications**.

The system automatically scrapes massive amounts of financial news for both the Taiwan Stock Market (TW) and US Stock Market (US) on a daily schedule. It utilizes **Google Gemini AI** for deep reading and structured summarization, and leverages **Azure TTS** technology to generate audio briefings. Finally, the system publishes the concise report to **Telegraph** (a clean web-based reading page) and pushes the audio file directly to your **Telegram** channel, allowing you to stay on top of the market just by "listening."

Lazy News AI 是一個專為繁忙投資者設計的雲原生全自動化系統。為了優化寄送穩定性並降低維運成本，系統已由傳統的電子報形式轉型為 Telegram 機器人推播。

本系統每日定時自動抓取台股 (TW) 與美股 (US) 的海量財經新聞，利用 Google Gemini AI 進行深度閱讀與結構化摘要，並透過 Azure TTS 技術生成語音導讀。最後，系統會將精華報告發佈至 Telegraph（簡潔的網頁閱讀頁面）並同步推播音檔至您的 Telegram 頻道，讓您隨時隨地用「聽」的也能掌握市場脈動。

## ✨ Features

* **🌍 Dual Market Monitoring**: Supports parameterized settings to automate news processing for both **Taiwan Stocks (TW)** and **US Stocks (US)** simultaneously.
* **🧠 AI-Powered Analysis**: Integrates **Google Gemini API** as a virtual analyst to read and filter dozens of real-time news articles, generating unique, structured market summary reports.
* **📢 Instant Telegram Delivery**: Replaces traditional email limits with a Telegram Bot. It uses **Telegraph** to generate aesthetic web links for quick reading on mobile devices.
* **🗣️ Audio Generation**: Integrates **Azure AI Speech** services to convert text reports into natural-sounding MP3 audio guides, perfect for listening during commutes.
* **☁️ Serverless & Zero Cost**: Runs entirely on **GitHub Actions** with Cron scheduling, achieving full automation without the need for paid server hosting.
* **🛡️ Reliability**: Features "Smart Scrolling" and multiple retry mechanisms to ensure stable web scraping even with dynamic content.

## 🚀 How It Works

1. **News Hunter**: Launches a headless browser via Selenium to crawl the latest financial news from Yahoo Finance and performs precise time filtering.
2. **AI Analyzer**: Sends the filtered news to the Google Gemini model to generate a report covering market overviews, sector focus, key company updates, and future outlooks.
3. **Podcaster**: Converts the generated text report into an MP3 audio file using Azure TTS.
4. **Telegram Notifier**:
* Converts Markdown content to HTML and publishes it as a Telegraph page.
* Sends the reading link and the MP3 file to a designated Telegram channel via the Bot API.



## 🛠️ Tech Stack

| Category | Technology |
| --- | --- |
| **Core** | Python 3.11 |
| **Web Scraper** | Selenium (Headless Chrome), BeautifulSoup4 |
| **Database** | SQLite (for news deduplication and caching) |
| **AI Services** | Google Gemini API (Analysis), Azure AI Speech (TTS) |
| **Automation** | GitHub Actions |
| **Messaging** | Telegram Bot API, Telegraph |

## ⚙️ Quick Start

### 1. Environment Setup

Create a `.env` file in the root directory and fill in the necessary keys:

```env
# AI Services
GOOGLE_API_KEY=your_gemini_key
AZURE_SPEECH_KEY=your_azure_key
AZURE_SPEECH_REGION=your_azure_region

# Telegram
TELEGRAM_BOT_TOKEN=your_bot_token
TELEGRAM_CHAT_ID=your_chat_or_channel_id

```

### 2. Install Dependencies

```bash
pip install -r requirements.txt

```

### 3. Run Locally

```bash
# Run task for Taiwan Stock Market
python run_all.py --market TW

# Run task for US Stock Market
python run_all.py --market US

```

## ⏰ Scheduling

The system is currently configured to run automatically via GitHub Actions:

* **TW Market**: Daily at 08:00 AM (Taipei Time).
* **US Market**: Daily at 20:00 PM (Taipei Time).

---

*Disclaimer: All content is AI-generated for informational purposes only and does not constitute financial or investment advice.*