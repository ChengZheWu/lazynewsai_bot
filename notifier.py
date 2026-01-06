import requests
import os

def send_to_telegram(md_path, mp3_path, market_name):
    token = os.getenv("TELEGRAM_BOT_TOKEN")
    chat_id = os.getenv("TELEGRAM_CHAT_ID")
    
    if not token or not chat_id:
        print("❌ 錯誤：找不到 TELEGRAM_BOT_TOKEN 或 TELEGRAM_CHAT_ID")
        return

    # 1. 發送文字報告 (Markdown)
    with open(md_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Telegram 訊息有長度限制 (約4096字)，如果太長建議發送檔案
    if len(content) > 4000:
        url = f"https://api.telegram.org/bot{token}/sendDocument"
        files = {'document': open(md_path, 'rb')}
        data = {'chat_id': chat_id, 'caption': f"📊 {market_name} 市場深度分析報告"}
        requests.post(url, data=data, files=files)
    else:
        url = f"https://api.telegram.org/bot{token}/sendMessage"
        data = {'chat_id': chat_id, 'text': content, 'parse_mode': 'Markdown'}
        requests.post(url, data=data)

    # 2. 發送語音檔案 (MP3)
    url = f"https://api.telegram.org/bot{token}/sendAudio"
    files = {'audio': open(mp3_path, 'rb')}
    data = {'chat_id': chat_id, 'caption': f"🎧 {market_name} 財經 Podcast"}
    requests.post(url, data=data, files=files)
    
    print(f"✅ {market_name} 報告與語音已送達 Telegram 群組！")