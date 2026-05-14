import database
import podcaster
import notifier

import google.generativeai as genai
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo
import os
import textwrap
from dotenv import load_dotenv
import sys
import argparse

THIS_WEEK_DAYS = 7
LAST_WEEK_DAYS = 14


def build_weighted_content(summaries, market_name):
    """
    將兩週摘要依照時間分為當週(權重3)與前一週(權重2)，
    組成給 Gemini 的內容區塊。
    """
    tz_taipei = ZoneInfo("Asia/Taipei")
    now = datetime.now(tz_taipei)
    this_week_cutoff = now - timedelta(days=THIS_WEEK_DAYS)

    this_week, last_week = [], []
    for s in summaries:
        created_at = datetime.fromisoformat(s['created_at']).replace(tzinfo=ZoneInfo("UTC")).astimezone(tz_taipei)
        if created_at >= this_week_cutoff:
            this_week.append(s['summary_text'])
        else:
            last_week.append(s['summary_text'])

    # 3:2 加權：當週重複 3 份，前一週重複 2 份
    weighted_blocks = []
    for i, text in enumerate(this_week):
        for _ in range(3):
            weighted_blocks.append(f"[當週第{i+1}篇]\n{text}")
    for i, text in enumerate(last_week):
        for _ in range(2):
            weighted_blocks.append(f"[前一週第{i+1}篇]\n{text}")

    return "\n\n---\n\n".join(weighted_blocks), len(this_week), len(last_week)


def main(market=None):
    if market is None:
        parser = argparse.ArgumentParser(description="生成指定市場的週報。")
        parser.add_argument("--market", type=str, required=True, choices=['TW', 'US'])
        args = parser.parse_args()
        market = args.market

    market_name = "台股" if market == "TW" else "美股"

    load_dotenv()
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        print("錯誤：找不到 GOOGLE_API_KEY 環境變數。")
        sys.exit(1)

    try:
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('gemini-3.1-flash-lite')
    except Exception as e:
        print(f"AI 設定失敗: {e}")
        sys.exit(1)

    print(f"--- {market_name} 週報生成啟動 ---")
    summaries = database.get_summaries_for_weekly_report(market)
    if not summaries:
        print(f"資料庫中沒有 {market_name} 的每日摘要可供生成週報。")
        sys.exit(1)

    weighted_content, this_week_count, last_week_count = build_weighted_content(summaries, market_name)
    print(f"當週摘要: {this_week_count} 篇，前一週摘要: {last_week_count} 篇（3:2 加權）")

    prompt = f"""
    你是一位頂尖的{market_name}財經週報分析師。
    以下提供你過去兩週的每日{market_name}市場摘要，當週的報告權重較高（標記為「當週」），前一週權重較低（標記為「前一週」）。
    請綜合這些資訊，撰寫一份以「未來展望與產業觀察」為主題的週報。

    ---
    寫作規則:
    撰寫一份**目標長度約為2000個繁體中文字，不要超過3000個繁體中文字**的週報。
    有日期的話，請用中文格式，例如:10月16號，不要寫10/16。
    不要出現沒必要的重複翻譯中文的英文。
    不要給標題。
    不要有表格，如果要放表格內容，請轉成文字描述。
    請在文章的第一句話寫"大家好，以下為本週{market_name}市場展望週報"
    請在文章的最後一句話寫"本集內容由 AI 自動生成，資訊來源為網路上{market_name}相關新聞，不構成任何投資建議，僅供參考，謝謝收聽"
    分析時，當週的資訊應給予更高的參考比重；前一週的資訊作為趨勢對照，若兩週均出現相同趨勢則強調其持續性，若僅當週出現則視為新興訊號。
    ---

    報告段落如下，不要新增或減少段落：
    1.  **本週市場回顧**：綜合兩週資料，以當週為主，簡述整體市場氣氛與走勢變化。
    2.  **持續發燒產業**：哪些產業在兩週內持續受到關注？趨勢是加強還是減弱？
    3.  **新興訊號**：當週才出現、前一週尚未明顯的新產業焦點或題材。
    4.  **未來值得關注的產業**：基於以上分析，給出兩到三個下週或近期最值得追蹤的產業或方向，並說明理由。
    5.  **小結**：三句話內總結本週最核心的市場主軸與下週關注重點。

    --- 以下為兩週每日摘要（依加權排列）---
    {weighted_content}
    """

    print("週報已發送給 Gemini AI，分析需要一點時間...")
    try:
        request_options = {"timeout": 300}
        response = model.generate_content(prompt, request_options=request_options)
        weekly_summary = response.text

        tz_taipei = ZoneInfo("Asia/Taipei")
        file_timestamp = datetime.now(tz_taipei).strftime('%Y%m%d')
        md_filename = f"weekly_{market}_{file_timestamp}.md"
        with open(md_filename, "w", encoding="utf-8") as f:
            f.write(weekly_summary)

        print("\n\n========== 週報 ========== \n")
        print(textwrap.fill(weekly_summary.replace('*', ''), width=80))
        print("\n==================== 週報結束 ====================")

        # 語音合成（直接從檔案讀取，複用 podcaster 邏輯）
        print("\n--- 啟動 AI 播音員（週報）---")
        mp3_filename = podcaster.synthesize_from_text(weekly_summary, market)
        if not mp3_filename:
            print("❌ 語音合成失敗，跳過推播。")
            return

        # Telegram 推播
        weekly_market_name = f"{market_name}週報"
        notifier.send_to_telegram(md_filename, mp3_filename, weekly_market_name)

        return md_filename
    except Exception as e:
        print(f"週報生成過程中發生錯誤: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
