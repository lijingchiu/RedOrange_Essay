#!/bin/bash

# Cron Job 設定腳本
# 此腳本用於設定自動化排程任務

PROJECT_DIR="/home/ubuntu/social-media-automation"
SCRIPT_PATH="$PROJECT_DIR/scripts/run_automation.sh"

echo "設定社群媒體自動化 Cron Job..."

# 檢查腳本是否存在
if [ ! -f "$SCRIPT_PATH" ]; then
    echo "錯誤: 找不到執行腳本 $SCRIPT_PATH"
    exit 1
fi

# 檢查腳本是否有執行權限
if [ ! -x "$SCRIPT_PATH" ]; then
    echo "設定腳本執行權限..."
    chmod +x "$SCRIPT_PATH"
fi

# 顯示可用的排程選項
echo ""
echo "請選擇自動化執行頻率："
echo "1) 每小時執行一次"
echo "2) 每天早上 9 點執行"
echo "3) 每天早上 9 點和下午 6 點執行"
echo "4) 每 30 分鐘執行一次"
echo "5) 自訂 Cron 表達式"
echo "6) 移除現有的 Cron Job"
echo ""

read -p "請輸入選項 (1-6): " choice

case $choice in
    1)
        CRON_EXPR="0 * * * *"
        DESCRIPTION="每小時執行一次"
        ;;
    2)
        CRON_EXPR="0 9 * * *"
        DESCRIPTION="每天早上 9 點執行"
        ;;
    3)
        CRON_EXPR="0 9,18 * * *"
        DESCRIPTION="每天早上 9 點和下午 6 點執行"
        ;;
    4)
        CRON_EXPR="*/30 * * * *"
        DESCRIPTION="每 30 分鐘執行一次"
        ;;
    5)
        read -p "請輸入 Cron 表達式 (例如: 0 9 * * *): " CRON_EXPR
        DESCRIPTION="自訂排程: $CRON_EXPR"
        ;;
    6)
        echo "移除現有的 Cron Job..."
        crontab -l | grep -v "$SCRIPT_PATH" | crontab -
        echo "Cron Job 已移除"
        exit 0
        ;;
    *)
        echo "無效的選項"
        exit 1
        ;;
esac

# 建立新的 Cron Job
echo "設定 Cron Job: $DESCRIPTION"

# 備份現有的 crontab
crontab -l > /tmp/crontab_backup 2>/dev/null || touch /tmp/crontab_backup

# 移除舊的相同任務（如果存在）
grep -v "$SCRIPT_PATH" /tmp/crontab_backup > /tmp/new_crontab

# 添加新的 Cron Job
echo "$CRON_EXPR $SCRIPT_PATH" >> /tmp/new_crontab

# 安裝新的 crontab
crontab /tmp/new_crontab

# 清理暫存檔案
rm -f /tmp/crontab_backup /tmp/new_crontab

echo ""
echo "✅ Cron Job 設定完成！"
echo "排程: $DESCRIPTION"
echo "腳本: $SCRIPT_PATH"
echo ""
echo "目前的 Cron Jobs:"
crontab -l | grep -E "(automation|$SCRIPT_PATH)" || echo "沒有找到相關的 Cron Job"
echo ""
echo "💡 提示："
echo "- 可以使用 'crontab -l' 查看所有 Cron Jobs"
echo "- 可以使用 'crontab -e' 手動編輯 Cron Jobs"
echo "- 日誌檔案將儲存在 $PROJECT_DIR/logs/ 目錄中"

