import subprocess
import sys
import argparse
import analyzer  # 匯入改造後的 analyzer.py
import podcaster # 匯入改造後的 podcaster.py
import notifier  # 你新建立的 telegram 工具

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
    args = parser.parse_args()
    market = args.market
    market_name = "台股" if market == "TW" else "美股"

    print(f"======================================")
    print(f"   🚀 {market_name} 任務啟動 (GitHub Actions) ")
    print(f"======================================")

    # Step 1: 爬蟲 (寫入本地 sqlite)
    if not run_news_hunter(market):
        sys.exit(1)

    # Step 2: AI 分析 (取得 Markdown 檔名)
    try:
        print("\n--- 2. 啟動 AI 分析師 ---")
        md_file = analyzer.main(market=market) # 記得修改 analyzer.py 的 main() 讓他 return 檔名
    except Exception as e:
        print(f"❌ AI 分析失敗: {e}")
        sys.exit(1)

    # Step 3: 語音合成 (取得 MP3 檔名)
    try:
        print("\n--- 3. 啟動 AI 播音員 ---")
        mp3_file = podcaster.main(market=market) # 記得修改 podcaster.py 的 main() 讓他 return 檔名
    except Exception as e:
        print(f"❌ 語音合成失敗: {e}")
        sys.exit(1)

    # Step 4: Telegram 推播
    try:
        print(f"\n--- 4. 發送至 Telegram ({market_name}) ---")
        notifier.send_to_telegram(md_file, mp3_file, market_name)
    except Exception as e:
        print(f"❌ Telegram 發送失敗: {e}")

    print(f"\n✨ {market_name} 任務順利完成！檔案將在 GitHub Runner 結束後自動清理。")

if __name__ == "__main__":
    main()