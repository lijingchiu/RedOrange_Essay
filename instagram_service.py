import requests
import logging
import time
from typing import Dict, Any, Optional
from config import config

logger = logging.getLogger(__name__)

class InstagramService:
    """Instagram API 服務類別"""
    
    def __init__(self):
        self.access_token = config.INSTAGRAM_ACCESS_TOKEN
        self.user_id = config.INSTAGRAM_USER_ID
        self.base_url = "https://graph.facebook.com/v23.0"
    
    def publish_image(self, image_url: str, caption: str = "") -> bool:
        """發布圖片到 Instagram"""
        try:
            # 步驟 1: 創建媒體容器
            container_id = self._create_image_container(image_url, caption)
            if not container_id:
                return False
            
            # 步驟 2: 發布容器
            return self._publish_container(container_id)
            
        except Exception as e:
            logger.error(f"發布 Instagram 圖片時發生錯誤: {str(e)}")
            return False
    
    def publish_video(self, video_url: str, caption: str = "", cover_url: str = "") -> bool:
        """發布影片到 Instagram (Reels)"""
        try:
            # 步驟 1: 創建影片容器
            container_id = self._create_video_container(video_url, caption, cover_url)
            if not container_id:
                return False
            
            # 步驟 2: 等待影片處理完成
            if not self._wait_for_video_processing(container_id):
                return False
            
            # 步驟 3: 發布容器
            return self._publish_container(container_id)
            
        except Exception as e:
            logger.error(f"發布 Instagram 影片時發生錯誤: {str(e)}")
            return False
    
    def _create_image_container(self, image_url: str, caption: str) -> Optional[str]:
        """創建圖片容器"""
        try:
            url = f"{self.base_url}/{self.user_id}/media"
            
            params = {
                'image_url': image_url,
                'caption': caption,
                'access_token': self.access_token
            }
            
            response = requests.post(url, params=params)
            response.raise_for_status()
            
            data = response.json()
            container_id = data.get('id')
            
            logger.info(f"成功創建 Instagram 圖片容器: {container_id}")
            return container_id
            
        except Exception as e:
            logger.error(f"創建 Instagram 圖片容器時發生錯誤: {str(e)}")
            return None
    
    def _create_video_container(self, video_url: str, caption: str, cover_url: str = "") -> Optional[str]:
        """創建影片容器 (Reels)"""
        try:
            url = f"{self.base_url}/{self.user_id}/media"
            
            params = {
                'media_type': 'REELS',
                'video_url': video_url,
                'caption': caption,
                'access_token': self.access_token
            }
            
            if cover_url:
                params['cover_url'] = cover_url
            
            response = requests.post(url, params=params)
            response.raise_for_status()
            
            data = response.json()
            container_id = data.get('id')
            
            logger.info(f"成功創建 Instagram 影片容器: {container_id}")
            return container_id
            
        except Exception as e:
            logger.error(f"創建 Instagram 影片容器時發生錯誤: {str(e)}")
            return None
    
    def _wait_for_video_processing(self, container_id: str, max_wait_time: int = 300) -> bool:
        """等待影片處理完成"""
        try:
            url = f"{self.base_url}/{container_id}"
            start_time = time.time()
            
            while time.time() - start_time < max_wait_time:
                params = {
                    'fields': 'status_code',
                    'access_token': self.access_token
                }
                
                response = requests.get(url, params=params)
                response.raise_for_status()
                
                data = response.json()
                status_code = data.get('status_code')
                
                if status_code == 'FINISHED':
                    logger.info(f"Instagram 影片處理完成: {container_id}")
                    return True
                elif status_code == 'ERROR':
                    logger.error(f"Instagram 影片處理失敗: {container_id}")
                    return False
                
                # 等待 10 秒後再次檢查
                time.sleep(10)
            
            logger.error(f"Instagram 影片處理超時: {container_id}")
            return False
            
        except Exception as e:
            logger.error(f"等待 Instagram 影片處理時發生錯誤: {str(e)}")
            return False
    
    def _publish_container(self, container_id: str) -> bool:
        """發布容器"""
        try:
            url = f"{self.base_url}/{self.user_id}/media_publish"
            
            params = {
                'creation_id': container_id,
                'access_token': self.access_token
            }
            
            response = requests.post(url, params=params)
            response.raise_for_status()
            
            data = response.json()
            media_id = data.get('id')
            
            logger.info(f"成功發布 Instagram 媒體: {media_id}")
            return True
            
        except Exception as e:
            logger.error(f"發布 Instagram 容器時發生錯誤: {str(e)}")
            return False
    
    def get_account_info(self) -> Optional[Dict[str, Any]]:
        """獲取帳號資訊"""
        try:
            url = f"{self.base_url}/{self.user_id}"
            
            params = {
                'fields': 'account_type,username,media_count',
                'access_token': self.access_token
            }
            
            response = requests.get(url, params=params)
            response.raise_for_status()
            
            return response.json()
            
        except Exception as e:
            logger.error(f"獲取 Instagram 帳號資訊時發生錯誤: {str(e)}")
            return None

