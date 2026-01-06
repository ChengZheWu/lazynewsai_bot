# Lazy News AI - Daily AI-Automated Financial News Newsletter

**Lazy News AI** is a fully automated cloud-native system designed for busy investors. The system automatically scrapes massive amounts of financial news for the Taiwan Stock Market (TW) and US Stock Market (US) on a daily schedule. It utilizes Large Language Models (LLM) to perform deep reading and summarization, and leverages Text-to-Speech (TTS) technology to generate audio files. Finally, it packages the concise text report and audio summary into a newsletter, which is automatically delivered to your inbox.
Stop spending time scrolling through news feeds—let AI organize daily market trends for you, so you can stay on top of the market just by "listening."

**Lazy News AI** 是一個全自動化的雲原生系統，專為繁忙的投資人設計。系統每日定時自動抓取台股 (TW) 與美股 (US) 的海量財經新聞，利用大型語言模型 (LLM) 進行深度閱讀與重點摘要，並透過文字轉語音 (TTS) 技術生成語音檔。最終，將精華的文字報告與語音內容打包成一份電子報，自動寄送至您的信箱。
不用再花時間刷新聞，讓 AI 為您整理每日市場動態，用「聽」的也能掌握股市脈動。

## ✨ Features

* **🌍 Dual Market Monitoring**: Supports parameterized settings to automate news processing for both **Taiwan Stocks (TW)** and **US Stocks (US)** simultaneously.
* **🧠 AI-Powered Analysis**: Integrates **Google Gemini API** as a virtual analyst to read and filter dozens of real-time news articles, generating unique, structured market summary reports.
* **📧 Automated Newsletter**: Integrates **n8n** automated workflows to package the AI-generated text report and audio file, delivering them punctually to subscribers via email every day.
* **🗣️ Audio Generation**: Integrates **Azure AI Speech** services to convert text reports into natural-sounding MP3 audio guides, perfect for listening during commutes or spare time.
* **☁️ Serverless Architecture**: The core computation is deployed on **AWS Fargate**, utilizing a serverless architecture that launches on demand, achieving low cost and high efficiency.
* **⏰ Precision Scheduling**: Uses **Amazon EventBridge Scheduler** to set Cron schedules, automatically triggering tasks based on specific time zones (Asia/Taipei).
* **🛡️ Reliability & Monitoring**: Integrates **Amazon CloudWatch** for log monitoring and includes retry mechanisms at the crawler and API layers to ensure stable system operation.

## 🚀 How It Works

1. **News Hunter**: Launches a headless browser via Selenium to crawl the latest financial news from sources like Yahoo Finance and performs precise time filtering.
2. **AI Analyzer**: Sends the filtered news to the Google Gemini model, requesting a structured financial analysis report (including market overview, sector focus, and key company updates).
3. **Podcaster**: Converts the generated text report into an audio file (MP3) using Azure TTS.
4. **Delivery**: Uploads the final Markdown report and MP3 to AWS S3 and triggers the n8n workflow to send the newsletter.

## 🛠️ Tech Stack

| Category | Technology |
| --- | --- |
| **Core** | Python |
| **Web Scraper** | Selenium, BeautifulSoup, requests |
| **Database** | SQLite (RDBMS) |
| **Local Dev** | Python venv |
| **Containerization** | Docker |
| **Cloud (AWS)** | ECR, ECS Fargate (Serverless), EventBridge, IAM, SNS, CloudWatch, S3, Boto3 |
| **AI** | Google Gemini API (Analysis), Azure AI Speech (TTS), AI-Assisted Dev |
| **Automation** | n8n |
| **Version Control** | Git |

## ⚙️ Quick Start (Local Development)

To run this project locally:

1. **Environment Setup**
Create a `.env` file and fill in the necessary keys:
```env
GOOGLE_API_KEY=your_gemini_key
AZURE_SPEECH_KEY=your_azure_key
AZURE_SPEECH_REGION=your_azure_region
# AWS credentials can be omitted if configured in ~/.aws/credentials

```


2. **Install Dependencies**
```bash
pip install -r requirements.txt

```


3. **Run Tasks**
```bash
# Run task for Taiwan Stock Market
python run_all.py --market TW

# Run task for US Stock Market
python run_all.py --market US

```



## 📈 Future Improvements

* [ ] **Web Frontend**: Build a simple web interface to showcase historical newsletter archives and allow online podcast streaming.
* [ ] **Advanced AI Applications**: Experiment with different LLM models or add features like Sentiment Analysis and Named Entity Recognition (NER) to enrich the newsletter content.