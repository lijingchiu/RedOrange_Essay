from flask import Blueprint, jsonify, request
from automation_engine import AutomationEngine
from config import config
import threading
import logging

logger = logging.getLogger(__name__)

automation_bp = Blueprint('automation', __name__)

@automation_bp.route('/run', methods=['POST'])
def run_automation():
    """手動觸發自動化流程"""
    try:
        # 在背景執行自動化流程
        def run_in_background():
            engine = AutomationEngine()
            engine.run()
        
        thread = threading.Thread(target=run_in_background)
        thread.daemon = True
        thread.start()
        
        return jsonify({
            'success': True,
            'message': '自動化流程已開始執行'
        })
        
    except Exception as e:
        logger.error(f"觸發自動化流程時發生錯誤: {str(e)}")
        return jsonify({
            'success': False,
            'message': f'執行失敗: {str(e)}'
        }), 500

@automation_bp.route('/status', methods=['GET'])
def get_status():
    """獲取系統狀態"""
    try:
        # 檢查設定是否完整
        config_valid = config.validate()
        
        # 檢查各服務狀態
        status = {
            'config_valid': config_valid,
            'services': {
                'notion': bool(config.NOTION_API_KEY and config.NOTION_DATABASE_ID),
                'instagram': bool(config.INSTAGRAM_ACCESS_TOKEN and config.INSTAGRAM_USER_ID),
                'facebook': bool(config.FACEBOOK_ACCESS_TOKEN and config.FACEBOOK_PAGE_ID),
                'threads': bool(config.THREADS_ACCESS_TOKEN and config.THREADS_USER_ID),
                'line': bool(config.LINE_CHANNEL_ACCESS_TOKEN and config.LINE_USER_ID)
            }
        }
        
        return jsonify({
            'success': True,
            'status': status
        })
        
    except Exception as e:
        logger.error(f"獲取系統狀態時發生錯誤: {str(e)}")
        return jsonify({
            'success': False,
            'message': f'獲取狀態失敗: {str(e)}'
        }), 500

@automation_bp.route('/config', methods=['GET'])
def get_config():
    """獲取設定資訊（隱藏敏感資訊）"""
    try:
        safe_config = {
            'notion_configured': bool(config.NOTION_API_KEY),
            'notion_database_id': config.NOTION_DATABASE_ID[:8] + '...' if config.NOTION_DATABASE_ID else None,
            'instagram_configured': bool(config.INSTAGRAM_ACCESS_TOKEN),
            'facebook_configured': bool(config.FACEBOOK_ACCESS_TOKEN),
            'threads_configured': bool(config.THREADS_ACCESS_TOKEN),
            'line_configured': bool(config.LINE_CHANNEL_ACCESS_TOKEN),
            'temp_media_dir': config.TEMP_MEDIA_DIR,
            'max_image_size_mb': config.MAX_IMAGE_SIZE_MB,
            'max_video_size_mb': config.MAX_VIDEO_SIZE_MB,
            'log_level': config.LOG_LEVEL
        }
        
        return jsonify({
            'success': True,
            'config': safe_config
        })
        
    except Exception as e:
        logger.error(f"獲取設定資訊時發生錯誤: {str(e)}")
        return jsonify({
            'success': False,
            'message': f'獲取設定失敗: {str(e)}'
        }), 500

@automation_bp.route('/test-services', methods=['POST'])
def test_services():
    """測試各服務連線"""
    try:
        results = {}
        
        # 測試 Notion
        if config.NOTION_API_KEY and config.NOTION_DATABASE_ID:
            try:
                from notion_service import NotionService
                notion_service = NotionService()
                posts = notion_service.get_pending_posts()
                results['notion'] = {
                    'success': True,
                    'message': f'成功連接，找到 {len(posts)} 個待發布貼文'
                }
            except Exception as e:
                results['notion'] = {
                    'success': False,
                    'message': str(e)
                }
        else:
            results['notion'] = {
                'success': False,
                'message': '設定不完整'
            }
        
        # 測試 Instagram
        if config.INSTAGRAM_ACCESS_TOKEN and config.INSTAGRAM_USER_ID:
            try:
                from instagram_service import InstagramService
                instagram_service = InstagramService()
                account_info = instagram_service.get_account_info()
                if account_info:
                    results['instagram'] = {
                        'success': True,
                        'message': f'成功連接帳號: {account_info.get("username", "未知")}'
                    }
                else:
                    results['instagram'] = {
                        'success': False,
                        'message': '無法獲取帳號資訊'
                    }
            except Exception as e:
                results['instagram'] = {
                    'success': False,
                    'message': str(e)
                }
        else:
            results['instagram'] = {
                'success': False,
                'message': '設定不完整'
            }
        
        # 測試 Facebook
        if config.FACEBOOK_ACCESS_TOKEN and config.FACEBOOK_PAGE_ID:
            try:
                from facebook_service import FacebookService
                facebook_service = FacebookService()
                page_info = facebook_service.get_page_info()
                if page_info:
                    results['facebook'] = {
                        'success': True,
                        'message': f'成功連接專頁: {page_info.get("name", "未知")}'
                    }
                else:
                    results['facebook'] = {
                        'success': False,
                        'message': '無法獲取專頁資訊'
                    }
            except Exception as e:
                results['facebook'] = {
                    'success': False,
                    'message': str(e)
                }
        else:
            results['facebook'] = {
                'success': False,
                'message': '設定不完整'
            }
        
        # 測試 Threads
        if config.THREADS_ACCESS_TOKEN and config.THREADS_USER_ID:
            try:
                from threads_service import ThreadsService
                threads_service = ThreadsService()
                user_info = threads_service.get_user_info()
                if user_info:
                    results['threads'] = {
                        'success': True,
                        'message': f'成功連接帳號: {user_info.get("username", "未知")}'
                    }
                else:
                    results['threads'] = {
                        'success': False,
                        'message': '無法獲取用戶資訊'
                    }
            except Exception as e:
                results['threads'] = {
                    'success': False,
                    'message': str(e)
                }
        else:
            results['threads'] = {
                'success': False,
                'message': '設定不完整'
            }
        
        # 測試 Line
        if config.LINE_CHANNEL_ACCESS_TOKEN:
            try:
                from line_service import LineService
                line_service = LineService()
                bot_info = line_service.get_profile()
                if bot_info:
                    results['line'] = {
                        'success': True,
                        'message': '成功連接 Line Bot'
                    }
                else:
                    results['line'] = {
                        'success': False,
                        'message': '無法獲取 Bot 資訊'
                    }
            except Exception as e:
                results['line'] = {
                    'success': False,
                    'message': str(e)
                }
        else:
            results['line'] = {
                'success': False,
                'message': '設定不完整'
            }
        
        return jsonify({
            'success': True,
            'test_results': results
        })
        
    except Exception as e:
        logger.error(f"測試服務時發生錯誤: {str(e)}")
        return jsonify({
            'success': False,
            'message': f'測試失敗: {str(e)}'
        }), 500

