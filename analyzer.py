# 導入自己的 database 模組
import database

import google.generativeai as genai
import textwrap
from datetime import datetime
from zoneinfo import ZoneInfo
import os
from dotenv import load_dotenv
import boto3
import sys
import argparse

# --- [全域常數] ---
S3_BUCKET_NAME = 'ai-news-podcast-output-andy-1102'

# --- [函數定義區] ---
def upload_to_s3(file_path, bucket_name, object_name):
    s3_client = boto3.client('s3')
    try:
        s3_client.upload_file(file_path, bucket_name, object_name)
        print(f"檔案已成功上傳至 S3: s3://{bucket_name}/{object_name}")
        return True
    except Exception as e:
        print(f"S3 上傳失敗: {e}")
        return False

def main():
    parser = argparse.ArgumentParser(description="分析指定市場的新聞並產生報告。")
    parser.add_argument("--market", type=str, required=True, choices=['TW', 'US'])
    args = parser.parse_args()
    market = args.market
    market_name = "台股" if market == "TW" else "美股"

    load_dotenv()
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        print("錯誤：找不到 GOOGLE_API_KEY 環境變數。")
        sys.exit(1) # 使用非 0 的 exit code 代表錯誤
        return

    try:
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('gemini-flash-latest')
    except Exception as e:
        print(f"AI 設定失敗: {e}")
        sys.exit(1) # 使用非 0 的 exit code 代表錯誤
        return

    print("AI 分析師已上線，正在調閱所有情報...")
    articles = database.get_all_articles_for_analysis(market)
    if not articles:
        print(f"知識庫中沒有 {market_name} 市場的新聞可供分析。")
        sys.exit(1) # 使用非 0 的 exit code 代表錯誤
        return

    print(f"成功調閱 {len(articles)} 篇新聞，正在整理成報告...")
    full_text_content = ""
    for article in articles:
        full_text_content += f"--- 新聞標題: {article['headline']} ---\n{article['content']}\n\n"

    prompt = f"""
    你是一位頂尖的{market_name}財經分析師。你的任務是閱讀以下所有從網路爬取來的{market_name}財經新聞。

    ---
    寫作規則:
    撰寫一份**目標長度約為3000個繁體中文字，不要超過5000個繁體中文字**的專業分析報告。
    請不要在報告中包含任何關於「報告撰寫」、「數據基礎」或「撰寫日期」的欄位。
    你的報告應該直接從「摘要」開始。
    有日期的話，請用中文格式，例如:10月16號，不要寫10/16。
    不要出現沒必要的重複翻譯中文的英文。
    不要給標題。
    不要有表格，如果要放表格內容，請轉成文字描述。
    請在文章的第一句話寫"大家好，以下為24小時內{market_name}新聞重點摘要"
    請在文章的最後一句話寫"本集內容由 AI 自動生成，資訊來源為網路上{market_name}相關新聞，不構成任何投資建議，僅供參考，謝謝收聽"
    ---

    請基於這些資訊，為我提供一份全面、深入的{market_name}市場動態摘要報告。
    報告段落如下，不要新增或減少段落：
    1.  **市場摘要整理**：總結這段時間內{market_name}市場的整體氣氛和主要指數的表現，以及有哪些重大事項。
    2.  **焦點板塊與題材**：哪些產業或概念股是這段時間內的{market_name}市場焦點？為什麼？
    3.  **關鍵公司動態**：提及至少三家在這批新聞中最重要的{market_name}公司，並說明它們發生了什麼關鍵事件（如財報、法說會、重大消息等）。
    4.  **未來關注產業**：針對目前的新聞資訊，分析並給出一到三個未來值得關注的產業，有機會成為下一個市場的焦點。
    4.  **分析與展望**：綜合所有資訊，提出你對短期{market_name}市場走勢的專業見解或潛在的觀察重點。

    請確保你的分析完全基於我提供的文本，並以專業、客觀、條理分明的口吻撰寫，不過可以以有趣活潑的方法來敘事。

    --- 以下為新聞全文 ---
    {full_text_content}
    """
    
    print("報告已發送給 Gemini AI，分析需要一點時間...")
    try:
        request_options = {"timeout": 300}
        response = model.generate_content(prompt, request_options=request_options)
        ai_summary = response.text
        
        print("\n分析完成，正在將報告存入知識庫...")
        database.add_summary(ai_summary, len(articles), market)
        
        # 產出 .md 檔案並上傳到 S3
        tz_taipei = ZoneInfo("Asia/Taipei")
        file_timestamp = datetime.now(tz_taipei).strftime('%Y%m%d_%H')
        filename = f"summary_{market}_{file_timestamp}.md"
        with open(filename, "w", encoding="utf-8") as f:
            f.write(ai_summary)
        
        upload_to_s3(filename, S3_BUCKET_NAME, f"{market}_reports/{filename}")
        os.remove(filename) # 上傳後刪除本地暫存檔

        print("\n\n========== Gemini AI 財經摘要報告 ========== \n")
        print(textwrap.fill(ai_summary.replace('*', ''), width=80))
        print("\n==================== 報告結束 ====================")
    except Exception as e:
        print(f"AI 分析或存檔過程中發生錯誤: {e}")
        sys.exit(1) # 使用非 0 的 exit code 代表錯誤

# --- [程式總開關] ---
if __name__ == "__main__":
    main()