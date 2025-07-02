import requests
import logging
from typing import List, Dict, Any, Optional
from datetime import datetime
from config import config

logger = logging.getLogger(__name__)

class NotionService:
    """Notion API 服務類別"""
    
    def __init__(self):
        self.api_key = config.NOTION_API_KEY
        self.database_id = config.NOTION_DATABASE_ID
        self.base_url = "https://api.notion.com/v1"
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Notion-Version": "2022-06-28",
            "Content-Type": "application/json"
        }
    
    def get_pending_posts(self) -> List[Dict[str, Any]]:
        """獲取待發布的貼文"""
        try:
            url = f"{self.base_url}/databases/{self.database_id}/query"
            
            # 查詢條件：發布狀態為「待發布」且發布日期小於等於現在
            filter_condition = {
                "and": [
                    {
                        "property": "發布狀態",
                        "select": {
                            "equals": "待發布"
                        }
                    },
                    {
                        "property": "發布日期",
                        "date": {
                            "on_or_before": datetime.now().isoformat()
                        }
                    }
                ]
            }
            
            payload = {
                "filter": filter_condition
            }
            
            response = requests.post(url, headers=self.headers, json=payload)
            response.raise_for_status()
            
            data = response.json()
            posts = []
            
            for page in data.get('results', []):
                post_data = self._extract_post_data(page)
                if post_data:
                    posts.append(post_data)
            
            logger.info(f"找到 {len(posts)} 個待發布的貼文")
            return posts
            
        except Exception as e:
            logger.error(f"獲取待發布貼文時發生錯誤: {str(e)}")
            return []
    
    def _extract_post_data(self, page: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """從 Notion 頁面中提取貼文資料"""
        try:
            properties = page.get('properties', {})
            
            # 提取標題
            title_prop = properties.get('標題', {})
            title = ""
            if title_prop.get('type') == 'title':
                title_array = title_prop.get('title', [])
                if title_array:
                    title = title_array[0].get('text', {}).get('content', '')
            
            # 提取內容
            content_prop = properties.get('內容', {})
            content = ""
            if content_prop.get('type') == 'rich_text':
                content_array = content_prop.get('rich_text', [])
                if content_array:
                    content = content_array[0].get('text', {}).get('content', '')
            
            # 提取媒體類型
            media_type_prop = properties.get('媒體類型', {})
            media_type = ""
            if media_type_prop.get('type') == 'select':
                select_obj = media_type_prop.get('select')
                if select_obj:
                    media_type = select_obj.get('name', '')
            
            # 提取媒體URL
            media_url_prop = properties.get('媒體URL', {})
            media_url = ""
            if media_url_prop.get('type') == 'url':
                media_url = media_url_prop.get('url', '')
            
            # 提取目標平台
            target_platforms_prop = properties.get('目標平台', {})
            target_platforms = []
            if target_platforms_prop.get('type') == 'multi_select':
                platforms = target_platforms_prop.get('multi_select', [])
                target_platforms = [platform.get('name', '') for platform in platforms]
            
            # 提取發布日期
            publish_date_prop = properties.get('發布日期', {})
            publish_date = None
            if publish_date_prop.get('type') == 'date':
                date_obj = publish_date_prop.get('date')
                if date_obj:
                    publish_date = date_obj.get('start')
            
            return {
                'id': page.get('id'),
                'title': title,
                'content': content,
                'media_type': media_type,
                'media_url': media_url,
                'target_platforms': target_platforms,
                'publish_date': publish_date
            }
            
        except Exception as e:
            logger.error(f"提取貼文資料時發生錯誤: {str(e)}")
            return None
    
    def update_post_status(self, page_id: str, status: str, error_message: str = "") -> bool:
        """更新貼文狀態"""
        try:
            url = f"{self.base_url}/pages/{page_id}"
            
            properties = {
                "發布狀態": {
                    "select": {
                        "name": status
                    }
                }
            }
            
            if error_message:
                properties["錯誤訊息"] = {
                    "rich_text": [
                        {
                            "text": {
                                "content": error_message
                            }
                        }
                    ]
                }
            
            payload = {
                "properties": properties
            }
            
            response = requests.patch(url, headers=self.headers, json=payload)
            response.raise_for_status()
            
            logger.info(f"成功更新貼文狀態: {page_id} -> {status}")
            return True
            
        except Exception as e:
            logger.error(f"更新貼文狀態時發生錯誤: {str(e)}")
            return False
    
    def update_line_notification_status(self, page_id: str, status: str) -> bool:
        """更新 Line 通知狀態"""
        try:
            url = f"{self.base_url}/pages/{page_id}"
            
            payload = {
                "properties": {
                    "Line通知狀態": {
                        "select": {
                            "name": status
                        }
                    }
                }
            }
            
            response = requests.patch(url, headers=self.headers, json=payload)
            response.raise_for_status()
            
            logger.info(f"成功更新 Line 通知狀態: {page_id} -> {status}")
            return True
            
        except Exception as e:
            logger.error(f"更新 Line 通知狀態時發生錯誤: {str(e)}")
            return False

