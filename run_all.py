import subprocess
import sys
import argparse
import os
import analyzer
import podcaster
import notifier
import database

def run_news_hunter(market):
    """執行爬蟲腳本"""
    print(f"\n--- 1. 正在執行 News Hunter (市場: {market}) ---")
    result = subprocess.run([sys.executable, "news_hunter.py", "--market", market])
    if result.returncode != 0:
        print("❌ 爬蟲失敗，終止任務。")
        return False
    return True

def main():
    parser = argparse.ArgumentParser(description="Lazy News AI 自動化流程")
    parser.add_argument("--market", type=str, required=True, choices=['TW', 'US'])
    parser.add_argument("--mode", type=str, required=True, choices=['crawl_only', 'crawl_and_report'],
                        help="crawl_only: 只爬蟲存入DB / crawl_and_report: 爬蟲+分析+推播+清空文章")
    args = parser.parse_args()
    market = args.market
    mode = args.mode
    market_name = "台股" if market == "TW" else "美股"

    print(f"======================================")
    print(f"   🚀 {market_name} 任務啟動 (模式: {mode})")
    print(f"======================================")

    # Step 1: 爬蟲（兩種模式都要執行）
    if not run_news_hunter(market):
        sys.exit(1)

    if mode == 'crawl_only':
        print(f"\n✅ {market_name} 爬蟲完成，新聞已存入資料庫，等待下次分析。")
        return

    # 以下只有 crawl_and_report 模式才執行

    # Step 2: AI 分析
    try:
        print("\n--- 2. 啟動 AI 分析師 ---")
        md_file = analyzer.main(market=market)
    except Exception as e:
        print(f"❌ AI 分析失敗: {e}")
        sys.exit(1)

    # Step 3: 語音合成
    try:
        print("\n--- 3. 啟動 AI 播音員 ---")
        mp3_file = podcaster.main(market=market)
    except Exception as e:
        print(f"❌ 語音合成失敗: {e}")
        sys.exit(1)

    # Step 4: Telegram 推播
    try:
        print(f"\n--- 4. 發送至 Telegram ({market_name}) ---")
        notifier.send_to_telegram(md_file, mp3_file, market_name)
    except Exception as e:
        print(f"❌ Telegram 發送失敗: {e}")

    # Step 5: 清空文章、刪除 MD 與 MP3
    print(f"\n--- 5. 清理檔案與資料庫 ---")
    database.clear_articles(market)
    for f in [md_file, mp3_file]:
        if f and os.path.exists(f):
            os.remove(f)
            print(f"已刪除 {f}")

    print(f"\n✨ {market_name} 任務順利完成！")

if __name__ == "__main__":
    main()
