import os
from telegraph import Telegraph
import requests

def send_to_telegram(md_path, mp3_path, market_name):
    token = os.getenv("TELEGRAM_BOT_TOKEN")
    chat_id = os.getenv("TELEGRAM_CHAT_ID")
    
    with open(md_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # --- [Step 1: 建立 Telegraph 文章] ---
    tg = Telegraph()
    tg.create_account(short_name='LazyNewsAI')
    
    # 將 Markdown 簡單轉成 HTML (Telegraph 只吃 HTML)
    # 這裡建議在 analyzer.py 產出時就稍微控制格式
    html_content = content.replace('\n', '<br>')
    
    response = tg.create_page(
        title=f"{market_name} 每日財經精華",
        html_content=f"<p>{html_content}</p>",
        author_name="AI 分析師"
    )
    report_url = response['url']

    # --- [Step 2: 發送 Telegram 訊息] ---
    # 這裡我們傳送一個精美的導引文字加連結
    message = f"📊 <b>{market_name} 市場深度分析報告</b>\n\n內容已生成，請點擊下方連結閱讀即時預覽：\n{report_url}"
    
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    requests.post(url, data={
        'chat_id': chat_id, 
        'text': message, 
        'parse_mode': 'HTML'
    })

    # --- [Step 3: 發送音檔] ---
    url_audio = f"https://api.telegram.org/bot{token}/sendAudio"
    with open(mp3_path, 'rb') as audio:
        requests.post(url_audio, data={'chat_id': chat_id, 'caption': f"🎧 {market_name} 語音導讀"}, files={'audio': audio})

    print(f"✅ {market_name} 報告已發佈至 Telegraph 並推播成功！")