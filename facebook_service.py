import requests
import logging
from typing import Dict, Any, Optional
from config import config

logger = logging.getLogger(__name__)

class FacebookService:
    """Facebook API 服務類別"""
    
    def __init__(self):
        self.access_token = config.FACEBOOK_ACCESS_TOKEN
        self.page_id = config.FACEBOOK_PAGE_ID
        self.base_url = "https://graph.facebook.com/v23.0"
    
    def publish_text_post(self, message: str) -> bool:
        """發布文字貼文到 Facebook"""
        try:
            url = f"{self.base_url}/{self.page_id}/feed"
            
            params = {
                'message': message,
                'access_token': self.access_token
            }
            
            response = requests.post(url, params=params)
            response.raise_for_status()
            
            data = response.json()
            post_id = data.get('id')
            
            logger.info(f"成功發布 Facebook 文字貼文: {post_id}")
            return True
            
        except Exception as e:
            logger.error(f"發布 Facebook 文字貼文時發生錯誤: {str(e)}")
            return False
    
    def publish_image_post(self, image_url: str, message: str = "") -> bool:
        """發布圖片貼文到 Facebook"""
        try:
            url = f"{self.base_url}/{self.page_id}/photos"
            
            params = {
                'url': image_url,
                'caption': message,
                'access_token': self.access_token
            }
            
            response = requests.post(url, params=params)
            response.raise_for_status()
            
            data = response.json()
            photo_id = data.get('id')
            
            logger.info(f"成功發布 Facebook 圖片貼文: {photo_id}")
            return True
            
        except Exception as e:
            logger.error(f"發布 Facebook 圖片貼文時發生錯誤: {str(e)}")
            return False
    
    def publish_video_post(self, video_url: str, description: str = "") -> bool:
        """發布影片貼文到 Facebook"""
        try:
            url = f"{self.base_url}/{self.page_id}/videos"
            
            params = {
                'file_url': video_url,
                'description': description,
                'access_token': self.access_token
            }
            
            response = requests.post(url, params=params)
            response.raise_for_status()
            
            data = response.json()
            video_id = data.get('id')
            
            logger.info(f"成功發布 Facebook 影片貼文: {video_id}")
            return True
            
        except Exception as e:
            logger.error(f"發布 Facebook 影片貼文時發生錯誤: {str(e)}")
            return False
    
    def publish_link_post(self, link: str, message: str = "") -> bool:
        """發布連結貼文到 Facebook"""
        try:
            url = f"{self.base_url}/{self.page_id}/feed"
            
            params = {
                'link': link,
                'message': message,
                'access_token': self.access_token
            }
            
            response = requests.post(url, params=params)
            response.raise_for_status()
            
            data = response.json()
            post_id = data.get('id')
            
            logger.info(f"成功發布 Facebook 連結貼文: {post_id}")
            return True
            
        except Exception as e:
            logger.error(f"發布 Facebook 連結貼文時發生錯誤: {str(e)}")
            return False
    
    def get_page_info(self) -> Optional[Dict[str, Any]]:
        """獲取專頁資訊"""
        try:
            url = f"{self.base_url}/{self.page_id}"
            
            params = {
                'fields': 'name,category,fan_count,talking_about_count',
                'access_token': self.access_token
            }
            
            response = requests.get(url, params=params)
            response.raise_for_status()
            
            return response.json()
            
        except Exception as e:
            logger.error(f"獲取 Facebook 專頁資訊時發生錯誤: {str(e)}")
            return None
    
    def get_page_posts(self, limit: int = 10) -> Optional[Dict[str, Any]]:
        """獲取專頁貼文"""
        try:
            url = f"{self.base_url}/{self.page_id}/posts"
            
            params = {
                'fields': 'id,message,created_time,type',
                'limit': limit,
                'access_token': self.access_token
            }
            
            response = requests.get(url, params=params)
            response.raise_for_status()
            
            return response.json()
            
        except Exception as e:
            logger.error(f"獲取 Facebook 專頁貼文時發生錯誤: {str(e)}")
            return None

