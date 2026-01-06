import subprocess
import sys
import argparse

# --- [函數定義區] ---
def run_script(script_name, market):
    """執行一個 Python 腳本，並檢查是否成功。"""
    print(f"\n--- 正在執行 {script_name} (市場: {market}) ---")
    # sys.executable 會確保我們用的是同一個環境下的 python.exe
    result = subprocess.run([sys.executable, script_name, "--market", market])
    if result.returncode != 0:
        print(f"!!! 執行 {script_name} (市場: {market}) 時發生錯誤，中止任務 !!!")
        return False
    print(f"--- {script_name} (市場: {market}) 執行成功 ---\n")
    return True

def main():
    parser = argparse.ArgumentParser(description="執行指定市場的財經 Podcast 自動化流程。")
    parser.add_argument("--market", type=str, required=True, choices=['TW', 'US'], help="要處理的市場 (TW 或 US)")
    args = parser.parse_args()

    market = args.market
    market_name = "台灣" if market == "TW" else "美國"

    print("==============================================")
    print("      每日財經 Podcast 自動化專案啟動 v9      ")
    print("==============================================")
    
    # 步驟一：執行新聞抓取
    if not run_script("news_hunter.py", market):
        return # 如果抓取失敗，就直接結束

    # 步驟二：執行 AI 分析與儲存
    if not run_script("analyzer.py", market):
        return # 如果分析失敗，就直接結束

    # 步驟三：執行 Podcast 生成
    if not run_script("podcaster.py", market):
        return # 如果生成語音失敗，就直接結束
    
    print(f"--- 所有 {market_name} 市場任務執行完畢，專案成功！ ---")

# --- [程式總開關] ---
if __name__ == "__main__":
    main()