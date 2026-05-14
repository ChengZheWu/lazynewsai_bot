# 導入自己的 database 模組
import database

from datetime import datetime
from zoneinfo import ZoneInfo
import os
import re
from dotenv import load_dotenv
import azure.cognitiveservices.speech as speechsdk
import sys
import argparse

# --- [全域常數] ---
BYTE_LIMIT = 15000

# --- [函數定義區] ---
def create_text_chunks(text):
    chunks, current_chunk = [], ""
    sentences = text.replace('\n', '。').replace('！', '。').replace('？', '。').split('。')
    for sentence in sentences:
        if not sentence: continue
        sentence_with_period = sentence + "。"
        if len((current_chunk + sentence_with_period).encode('utf-8')) > BYTE_LIMIT:
            if current_chunk: chunks.append(current_chunk)
            current_chunk = sentence_with_period
        else:
            current_chunk += sentence_with_period
    if current_chunk: chunks.append(current_chunk)
    return chunks

def synthesize_from_text(text, market, filename=None):
    """將文字合成為 MP3，回傳檔名。可供 main() 和 weekly_report.py 共用。"""
    load_dotenv()
    speech_key = os.getenv("AZURE_SPEECH_KEY")
    speech_region = os.getenv("AZURE_SPEECH_REGION")
    if not all([speech_key, speech_region]):
        print("錯誤：缺少 AZURE_SPEECH_KEY 或 AZURE_SPEECH_REGION 環境變數。")
        return None

    cleaned_text = re.sub(r'#+\s*', '', text).replace('**', '').replace('*', '').replace('---', '').replace('/', '、')

    if filename is None:
        tz_taipei = ZoneInfo("Asia/Taipei")
        file_timestamp = datetime.now(tz_taipei).strftime('%Y%m%d_%H')
        filename = f"podcast_{market}_{file_timestamp}.mp3"

    try:
        speech_config = speechsdk.SpeechConfig(subscription=speech_key, region=speech_region)
        audio_config = speechsdk.audio.AudioOutputConfig(filename=filename)
        voice_name = "zh-TW-YunJheNeural"
        speech_config.speech_synthesis_voice_name = voice_name
        speech_synthesizer = speechsdk.SpeechSynthesizer(speech_config=speech_config, audio_config=audio_config)

        text_chunks = create_text_chunks(cleaned_text)
        print(f"報告已切分成 {len(text_chunks)} 段落，準備使用聲音 '{voice_name}' 進行合成...")
        for i, chunk in enumerate(text_chunks):
            print(f"  - 正在合成第 {i+1}/{len(text_chunks)} 段語音...")
            result = speech_synthesizer.speak_text_async(chunk).get()
            if result.reason == speechsdk.ResultReason.Canceled:
                cancellation_details = result.cancellation_details
                print(f"語音合成被取消: {cancellation_details.reason}")
                if cancellation_details.reason == speechsdk.CancellationReason.Error:
                    print(f"錯誤詳情: {cancellation_details.error_details}")
                return None

        print("\n所有段落語音合成完畢！")
        return filename
    except Exception as e:
        print(f"語音合成過程中發生錯誤: {e}")
        return None


def main(market=None):
    if market is None:
        parser = argparse.ArgumentParser(description="為指定市場的最新報告生成 Podcast。")
        parser.add_argument("--market", type=str, required=True, choices=['TW', 'US'])
        args = parser.parse_args()
        market = args.market

    market_name = "台股" if market == "TW" else "美股"
    load_dotenv()

    print(f"--- AI 播音員 ({market_name}市場版) 啟動 ---")
    latest_summary = database.get_latest_summary(market)
    if not latest_summary:
        print(f"錯誤：資料庫中找不到任何 {market_name} 市場的分析報告。")
        sys.exit(1)
        return

    print("成功讀取報告，準備進行語音合成...")
    filename = synthesize_from_text(latest_summary['summary_text'], market)
    if not filename:
        sys.exit(1)
    return filename

# --- [程式總開關] ---
if __name__ == "__main__":
    main()