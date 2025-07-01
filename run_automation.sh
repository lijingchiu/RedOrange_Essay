#!/bin/bash

# 社群媒體自動化執行腳本
# 此腳本用於 Cron Job 定期執行自動化流程

# 設定專案目錄
PROJECT_DIR="/home/ubuntu/social-media-automation"
LOG_DIR="$PROJECT_DIR/logs"
VENV_DIR="$PROJECT_DIR/venv"

# 建立日誌目錄
mkdir -p "$LOG_DIR"

# 設定日誌檔案
TIMESTAMP=$(date +"%Y%m%d_%H%M%S")
LOG_FILE="$LOG_DIR/automation_$TIMESTAMP.log"

# 記錄開始時間
echo "$(date): 開始執行自動化流程" >> "$LOG_FILE"

# 切換到專案目錄
cd "$PROJECT_DIR" || {
    echo "$(date): 錯誤 - 無法切換到專案目錄: $PROJECT_DIR" >> "$LOG_FILE"
    exit 1
}

# 啟動虛擬環境
source "$VENV_DIR/bin/activate" || {
    echo "$(date): 錯誤 - 無法啟動虛擬環境: $VENV_DIR" >> "$LOG_FILE"
    exit 1
}

# 執行自動化引擎
python src/automation_engine.py >> "$LOG_FILE" 2>&1

# 記錄執行結果
EXIT_CODE=$?
if [ $EXIT_CODE -eq 0 ]; then
    echo "$(date): 自動化流程執行成功" >> "$LOG_FILE"
else
    echo "$(date): 自動化流程執行失敗，退出代碼: $EXIT_CODE" >> "$LOG_FILE"
fi

# 清理舊日誌檔案（保留最近 30 天）
find "$LOG_DIR" -name "automation_*.log" -mtime +30 -delete

# 記錄結束時間
echo "$(date): 自動化流程執行完成" >> "$LOG_FILE"

exit $EXIT_CODE

