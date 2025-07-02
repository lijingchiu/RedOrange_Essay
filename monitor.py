#!/usr/bin/env python3
"""
社群媒體自動化系統監控腳本
監控系統狀態、日誌檔案和錯誤情況
"""

import os
import sys
import json
import time
import logging
from datetime import datetime, timedelta
from pathlib import Path

# 添加專案路徑
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from config import config
from line_service import LineService

# 設定日誌
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class SystemMonitor:
    """系統監控類別"""
    
    def __init__(self):
        self.project_dir = project_root
        self.log_dir = self.project_dir / "logs"
        self.status_file = self.project_dir / "status.json"
        self.line_service = LineService() if config.LINE_CHANNEL_ACCESS_TOKEN else None
        
        # 建立日誌目錄
        self.log_dir.mkdir(exist_ok=True)
    
    def check_system_health(self):
        """檢查系統健康狀態"""
        health_status = {
            'timestamp': datetime.now().isoformat(),
            'status': 'healthy',
            'issues': [],
            'warnings': []
        }
        
        try:
            # 檢查設定
            if not config.validate():
                health_status['issues'].append('設定不完整')
                health_status['status'] = 'unhealthy'
            
            # 檢查日誌檔案
            log_issues = self._check_log_files()
            if log_issues:
                health_status['issues'].extend(log_issues)
                health_status['status'] = 'unhealthy'
            
            # 檢查磁碟空間
            disk_warnings = self._check_disk_space()
            if disk_warnings:
                health_status['warnings'].extend(disk_warnings)
            
            # 檢查最近的執行狀態
            execution_issues = self._check_recent_executions()
            if execution_issues:
                health_status['issues'].extend(execution_issues)
                health_status['status'] = 'unhealthy'
            
        except Exception as e:
            health_status['status'] = 'error'
            health_status['issues'].append(f'監控檢查失敗: {str(e)}')
        
        return health_status
    
    def _check_log_files(self):
        """檢查日誌檔案"""
        issues = []
        
        try:
            # 檢查是否有錯誤日誌
            log_files = list(self.log_dir.glob("automation_*.log"))
            
            if not log_files:
                issues.append('找不到自動化日誌檔案')
                return issues
            
            # 檢查最近的日誌檔案
            recent_logs = [f for f in log_files if 
                          (datetime.now() - datetime.fromtimestamp(f.stat().st_mtime)).days <= 1]
            
            if not recent_logs:
                issues.append('最近 24 小時內沒有新的日誌檔案')
            
            # 檢查錯誤訊息
            for log_file in recent_logs[-3:]:  # 檢查最近 3 個日誌檔案
                try:
                    with open(log_file, 'r', encoding='utf-8') as f:
                        content = f.read()
                        if 'ERROR' in content or '錯誤' in content:
                            issues.append(f'日誌檔案 {log_file.name} 包含錯誤訊息')
                except Exception as e:
                    issues.append(f'無法讀取日誌檔案 {log_file.name}: {str(e)}')
            
        except Exception as e:
            issues.append(f'檢查日誌檔案時發生錯誤: {str(e)}')
        
        return issues
    
    def _check_disk_space(self):
        """檢查磁碟空間"""
        warnings = []
        
        try:
            import shutil
            
            # 檢查專案目錄的磁碟空間
            total, used, free = shutil.disk_usage(self.project_dir)
            free_percent = (free / total) * 100
            
            if free_percent < 10:
                warnings.append(f'磁碟空間不足，剩餘 {free_percent:.1f}%')
            elif free_percent < 20:
                warnings.append(f'磁碟空間偏低，剩餘 {free_percent:.1f}%')
            
            # 檢查暫存目錄
            temp_dir = Path(config.TEMP_MEDIA_DIR)
            if temp_dir.exists():
                temp_files = list(temp_dir.glob("*"))
                if len(temp_files) > 100:
                    warnings.append(f'暫存目錄檔案過多: {len(temp_files)} 個檔案')
            
        except Exception as e:
            warnings.append(f'檢查磁碟空間時發生錯誤: {str(e)}')
        
        return warnings
    
    def _check_recent_executions(self):
        """檢查最近的執行狀態"""
        issues = []
        
        try:
            # 檢查最近 24 小時內是否有成功執行
            log_files = list(self.log_dir.glob("automation_*.log"))
            recent_success = False
            
            for log_file in log_files:
                file_time = datetime.fromtimestamp(log_file.stat().st_mtime)
                if (datetime.now() - file_time).hours <= 24:
                    try:
                        with open(log_file, 'r', encoding='utf-8') as f:
                            content = f.read()
                            if '執行成功' in content or 'success' in content.lower():
                                recent_success = True
                                break
                    except:
                        continue
            
            if not recent_success:
                issues.append('最近 24 小時內沒有成功執行記錄')
            
        except Exception as e:
            issues.append(f'檢查執行狀態時發生錯誤: {str(e)}')
        
        return issues
    
    def save_status(self, status):
        """儲存狀態到檔案"""
        try:
            with open(self.status_file, 'w', encoding='utf-8') as f:
                json.dump(status, f, ensure_ascii=False, indent=2)
        except Exception as e:
            logger.error(f'儲存狀態檔案失敗: {str(e)}')
    
    def send_alert(self, status):
        """發送警報通知"""
        if not self.line_service:
            logger.warning('Line 服務未設定，無法發送警報')
            return
        
        if status['status'] == 'unhealthy':
            issues_text = '\n'.join([f'• {issue}' for issue in status['issues']])
            message = f"""🚨 系統健康檢查警報

⚠️ 系統狀態: 異常

發現的問題:
{issues_text}

時間: {status['timestamp']}

請檢查系統設定和日誌檔案。"""
            
            try:
                self.line_service.send_text_message(message)
                logger.info('警報通知已發送')
            except Exception as e:
                logger.error(f'發送警報通知失敗: {str(e)}')
        
        elif status['warnings']:
            warnings_text = '\n'.join([f'• {warning}' for warning in status['warnings']])
            message = f"""⚠️ 系統健康檢查警告

系統狀態: 正常但有警告

警告事項:
{warnings_text}

時間: {status['timestamp']}"""
            
            try:
                self.line_service.send_text_message(message)
                logger.info('警告通知已發送')
            except Exception as e:
                logger.error(f'發送警告通知失敗: {str(e)}')
    
    def run_monitor(self, send_alerts=True):
        """執行監控檢查"""
        logger.info('開始系統健康檢查')
        
        status = self.check_system_health()
        self.save_status(status)
        
        logger.info(f'系統狀態: {status["status"]}')
        
        if status['issues']:
            logger.warning(f'發現 {len(status["issues"])} 個問題')
            for issue in status['issues']:
                logger.warning(f'  - {issue}')
        
        if status['warnings']:
            logger.info(f'發現 {len(status["warnings"])} 個警告')
            for warning in status['warnings']:
                logger.info(f'  - {warning}')
        
        if send_alerts and (status['status'] == 'unhealthy' or status['warnings']):
            self.send_alert(status)
        
        logger.info('系統健康檢查完成')
        return status

def main():
    """主函數"""
    import argparse
    
    parser = argparse.ArgumentParser(description='社群媒體自動化系統監控')
    parser.add_argument('--no-alerts', action='store_true', help='不發送警報通知')
    parser.add_argument('--continuous', action='store_true', help='持續監控模式')
    parser.add_argument('--interval', type=int, default=300, help='持續監控間隔（秒）')
    
    args = parser.parse_args()
    
    monitor = SystemMonitor()
    
    if args.continuous:
        logger.info(f'開始持續監控，間隔 {args.interval} 秒')
        try:
            while True:
                monitor.run_monitor(send_alerts=not args.no_alerts)
                time.sleep(args.interval)
        except KeyboardInterrupt:
            logger.info('監控已停止')
    else:
        monitor.run_monitor(send_alerts=not args.no_alerts)

if __name__ == "__main__":
    main()

