import requests
import logging
import time
from typing import Dict, Any, Optional
from src.config import config

logger = logging.getLogger(__name__)

class ThreadsService:
    """Threads API 服務類別"""
    
    def __init__(self):
        self.access_token = config.THREADS_ACCESS_TOKEN
        self.user_id = config.THREADS_USER_ID
        self.base_url = "https://graph.threads.net/v1.0"
    
    def publish_text_post(self, text: str) -> bool:
        """發布文字貼文到 Threads"""
        try:
            # 步驟 1: 創建媒體容器
            container_id = self._create_text_container(text)
            if not container_id:
                return False
            
            # 步驟 2: 發布容器
            return self._publish_container(container_id)
            
        except Exception as e:
            logger.error(f"發布 Threads 文字貼文時發生錯誤: {str(e)}")
            return False
    
    def publish_image_post(self, image_url: str, text: str = "") -> bool:
        """發布圖片貼文到 Threads"""
        try:
            # 步驟 1: 創建媒體容器
            container_id = self._create_image_container(image_url, text)
            if not container_id:
                return False
            
            # 步驟 2: 發布容器
            return self._publish_container(container_id)
            
        except Exception as e:
            logger.error(f"發布 Threads 圖片貼文時發生錯誤: {str(e)}")
            return False
    
    def publish_video_post(self, video_url: str, text: str = "") -> bool:
        """發布影片貼文到 Threads"""
        try:
            # 步驟 1: 創建媒體容器
            container_id = self._create_video_container(video_url, text)
            if not container_id:
                return False
            
            # 步驟 2: 等待影片處理完成
            if not self._wait_for_video_processing(container_id):
                return False
            
            # 步驟 3: 發布容器
            return self._publish_container(container_id)
            
        except Exception as e:
            logger.error(f"發布 Threads 影片貼文時發生錯誤: {str(e)}")
            return False
    
    def _create_text_container(self, text: str) -> Optional[str]:
        """創建文字容器"""
        try:
            url = f"{self.base_url}/{self.user_id}/threads"
            
            params = {
                'media_type': 'TEXT',
                'text': text,
                'access_token': self.access_token
            }
            
            response = requests.post(url, params=params)
            response.raise_for_status()
            
            data = response.json()
            container_id = data.get('id')
            
            logger.info(f"成功創建 Threads 文字容器: {container_id}")
            return container_id
            
        except Exception as e:
            logger.error(f"創建 Threads 文字容器時發生錯誤: {str(e)}")
            return None
    
    def _create_image_container(self, image_url: str, text: str) -> Optional[str]:
        """創建圖片容器"""
        try:
            url = f"{self.base_url}/{self.user_id}/threads"
            
            params = {
                'media_type': 'IMAGE',
                'image_url': image_url,
                'text': text,
                'access_token': self.access_token
            }
            
            response = requests.post(url, params=params)
            response.raise_for_status()
            
            data = response.json()
            container_id = data.get('id')
            
            logger.info(f"成功創建 Threads 圖片容器: {container_id}")
            return container_id
            
        except Exception as e:
            logger.error(f"創建 Threads 圖片容器時發生錯誤: {str(e)}")
            return None
    
    def _create_video_container(self, video_url: str, text: str) -> Optional[str]:
        """創建影片容器"""
        try:
            url = f"{self.base_url}/{self.user_id}/threads"
            
            params = {
                'media_type': 'VIDEO',
                'video_url': video_url,
                'text': text,
                'access_token': self.access_token
            }
            
            response = requests.post(url, params=params)
            response.raise_for_status()
            
            data = response.json()
            container_id = data.get('id')
            
            logger.info(f"成功創建 Threads 影片容器: {container_id}")
            return container_id
            
        except Exception as e:
            logger.error(f"創建 Threads 影片容器時發生錯誤: {str(e)}")
            return None
    
    def _wait_for_video_processing(self, container_id: str, max_wait_time: int = 300) -> bool:
        """等待影片處理完成"""
        try:
            url = f"{self.base_url}/{container_id}"
            start_time = time.time()
            
            while time.time() - start_time < max_wait_time:
                params = {
                    'fields': 'status',
                    'access_token': self.access_token
                }
                
                response = requests.get(url, params=params)
                response.raise_for_status()
                
                data = response.json()
                status = data.get('status')
                
                if status == 'FINISHED':
                    logger.info(f"Threads 影片處理完成: {container_id}")
                    return True
                elif status == 'ERROR':
                    logger.error(f"Threads 影片處理失敗: {container_id}")
                    return False
                
                # 等待 10 秒後再次檢查
                time.sleep(10)
            
            logger.error(f"Threads 影片處理超時: {container_id}")
            return False
            
        except Exception as e:
            logger.error(f"等待 Threads 影片處理時發生錯誤: {str(e)}")
            return False
    
    def _publish_container(self, container_id: str) -> bool:
        """發布容器"""
        try:
            url = f"{self.base_url}/{self.user_id}/threads_publish"
            
            params = {
                'creation_id': container_id,
                'access_token': self.access_token
            }
            
            response = requests.post(url, params=params)
            response.raise_for_status()
            
            data = response.json()
            thread_id = data.get('id')
            
            logger.info(f"成功發布 Threads 貼文: {thread_id}")
            return True
            
        except Exception as e:
            logger.error(f"發布 Threads 容器時發生錯誤: {str(e)}")
            return False
    
    def get_user_info(self) -> Optional[Dict[str, Any]]:
        """獲取用戶資訊"""
        try:
            url = f"{self.base_url}/{self.user_id}"
            
            params = {
                'fields': 'id,username,threads_profile_picture_url,threads_biography',
                'access_token': self.access_token
            }
            
            response = requests.get(url, params=params)
            response.raise_for_status()
            
            return response.json()
            
        except Exception as e:
            logger.error(f"獲取 Threads 用戶資訊時發生錯誤: {str(e)}")
            return None
    
    def get_user_threads(self, limit: int = 10) -> Optional[Dict[str, Any]]:
        """獲取用戶的 Threads"""
        try:
            url = f"{self.base_url}/{self.user_id}/threads"
            
            params = {
                'fields': 'id,media_type,text,timestamp',
                'limit': limit,
                'access_token': self.access_token
            }
            
            response = requests.get(url, params=params)
            response.raise_for_status()
            
            return response.json()
            
        except Exception as e:
            logger.error(f"獲取 Threads 用戶貼文時發生錯誤: {str(e)}")
            return None

