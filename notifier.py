import os
import re
from telegraph import Telegraph
import requests

def markdown_to_html(md_text):
    """將簡單的 Markdown 語法轉換為 Telegraph 支援的 HTML"""
    # 1. 處理粗體: **文字** -> <b>文字</b>
    html = re.sub(r'\*\*(.*?)\*\*', r'<b>\1</b>', md_text)
    
    # 2. 處理標題 (###): ### 標題 -> <h3>標題</h3>
    # Telegraph 支援 h3 和 h4
    html = re.sub(r'^###\s+(.*)', r'<h3>\1</h3>', html, flags=re.MULTILINE)
    
    # 3. 處理標題 (##): ## 標題 -> <h3>標題</h3>
    html = re.sub(r'^##\s+(.*)', r'<h3>\1</h3>', html, flags=re.MULTILINE)

    # 4. 處理換行: \n -> <br>
    # 注意：Telegraph 的 <br> 處理有時比較嚴格，多個 \n 可以轉成 <p>
    html = html.replace('\n', '<br>')
    
    return html

def send_to_telegram(md_path, mp3_path, market_name):
    token = os.getenv("TELEGRAM_BOT_TOKEN")
    chat_id = os.getenv("TELEGRAM_CHAT_ID")
    
    with open(md_path, 'r', encoding='utf-8') as f:
        md_content = f.read()

    # 語法轉換
    html_content = markdown_to_html(md_content)

    # --- [Step 1: 建立 Telegraph 文章] ---
    tg = Telegraph()
    tg.create_account(short_name='LazyNewsAI')
    
    response = tg.create_page(
        title=f"{market_name}新聞摘要",
        html_content=f"<p>{html_content}</p>",
        author_name="Fin God"
    )
    report_url = response['url']

    # --- [Step 2: 發送 Telegram 訊息] ---
    # 這裡我們傳送一個精美的導引文字加連結
    message = f"📊 <b>LazyNewsAI {market_name}每日新聞摘要</b>\n\n請點擊下方連結閱讀即時預覽：\n{report_url}"
    
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    requests.post(url, data={
        'chat_id': chat_id, 
        'text': message, 
        'parse_mode': 'HTML'
    })

    # --- [Step 3: 發送音檔] ---
    url_audio = f"https://api.telegram.org/bot{token}/sendAudio"
    with open(mp3_path, 'rb') as audio:
        requests.post(url_audio, data={'chat_id': chat_id, 'caption': f"🎧 {market_name}新聞摘要Podcast"}, files={'audio': audio})

    print(f"✅ {market_name} 報告已發佈至 Telegraph 並推播成功！")