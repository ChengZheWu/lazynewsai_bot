#!/bin/bash
# 執行前請先修改 PROJECT_DIR 為你的實際專案路徑
# 例如：PROJECT_DIR="/home/ubuntu/lazynewsai_bot"

PROJECT_DIR="/home/ubuntu/lazynewsai_bot"
PYTHON="/usr/bin/python3"
LOG_DIR="$PROJECT_DIR/logs"

mkdir -p "$LOG_DIR"

crontab -l 2>/dev/null | grep -v 'lazynewsai' > /tmp/current_cron

cat >> /tmp/current_cron << EOF

# ===== LazyNewsAI =====

# 台股：晚上 19:30 爬蟲存起來 (UTC 11:30)
30 11 * * * cd $PROJECT_DIR && $PYTHON run_all.py --market TW --mode crawl_only >> $LOG_DIR/tw_crawl.log 2>&1

# 台股：早上 07:30 爬蟲+分析+推播 (UTC 23:30)
30 23 * * * cd $PROJECT_DIR && $PYTHON run_all.py --market TW --mode crawl_and_report >> $LOG_DIR/tw_report.log 2>&1

# 美股：早上 08:00 爬蟲存起來 (UTC 00:00)
0 0 * * * cd $PROJECT_DIR && $PYTHON run_all.py --market US --mode crawl_only >> $LOG_DIR/us_crawl.log 2>&1

# 美股：晚上 20:00 爬蟲+分析+推播 (UTC 12:00)
0 12 * * * cd $PROJECT_DIR && $PYTHON run_all.py --market US --mode crawl_and_report >> $LOG_DIR/us_report.log 2>&1

# 週報：每週日晚上 21:00 台股+美股 (UTC 13:00)
0 13 * * 0 cd $PROJECT_DIR && $PYTHON weekly_report.py --market TW >> $LOG_DIR/weekly_tw.log 2>&1
30 13 * * 0 cd $PROJECT_DIR && $PYTHON weekly_report.py --market US >> $LOG_DIR/weekly_us.log 2>&1

# ===== End LazyNewsAI =====
EOF

crontab /tmp/current_cron
rm /tmp/current_cron

echo "✅ Cron 設定完成！目前排程："
crontab -l
