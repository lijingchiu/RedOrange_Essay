import requests
import logging
from typing import Dict, Any, List
from config import config

logger = logging.getLogger(__name__)

class LineService:
    """Line Messaging API 服務類別"""
    
    def __init__(self):
        self.channel_access_token = config.LINE_CHANNEL_ACCESS_TOKEN
        self.user_id = config.LINE_USER_ID
        self.base_url = "https://api.line.me/v2/bot"
        self.headers = {
            "Authorization": f"Bearer {self.channel_access_token}",
            "Content-Type": "application/json"
        }
    
    def send_text_message(self, message: str) -> bool:
        """發送文字訊息"""
        try:
            url = f"{self.base_url}/message/push"
            
            payload = {
                "to": self.user_id,
                "messages": [
                    {
                        "type": "text",
                        "text": message
                    }
                ]
            }
            
            response = requests.post(url, headers=self.headers, json=payload)
            response.raise_for_status()
            
            logger.info("成功發送 Line 文字訊息")
            return True
            
        except Exception as e:
            logger.error(f"發送 Line 文字訊息時發生錯誤: {str(e)}")
            return False
    
    def send_success_notification(self, post_title: str, platforms: List[str], publish_time: str) -> bool:
        """發送發布成功通知"""
        try:
            platforms_text = "、".join(platforms)
            message = f"""🎉 發布成功通知

📝 標題: {post_title}
📱 平台: {platforms_text}
⏰ 發布時間: {publish_time}

您的內容已成功發布到指定的社群媒體平台！"""
            
            return self.send_text_message(message)
            
        except Exception as e:
            logger.error(f"發送發布成功通知時發生錯誤: {str(e)}")
            return False
    
    def send_failure_notification(self, post_title: str, platforms: List[str], error_message: str) -> bool:
        """發送發布失敗通知"""
        try:
            platforms_text = "、".join(platforms)
            message = f"""❌ 發布失敗通知

📝 標題: {post_title}
📱 平台: {platforms_text}
🚫 錯誤訊息: {error_message}

請檢查設定或聯繫技術支援。"""
            
            return self.send_text_message(message)
            
        except Exception as e:
            logger.error(f"發送發布失敗通知時發生錯誤: {str(e)}")
            return False
    
    def send_flex_message(self, alt_text: str, flex_content: Dict[str, Any]) -> bool:
        """發送 Flex 訊息"""
        try:
            url = f"{self.base_url}/message/push"
            
            payload = {
                "to": self.user_id,
                "messages": [
                    {
                        "type": "flex",
                        "altText": alt_text,
                        "contents": flex_content
                    }
                ]
            }
            
            response = requests.post(url, headers=self.headers, json=payload)
            response.raise_for_status()
            
            logger.info("成功發送 Line Flex 訊息")
            return True
            
        except Exception as e:
            logger.error(f"發送 Line Flex 訊息時發生錯誤: {str(e)}")
            return False
    
    def send_detailed_success_notification(self, post_data: Dict[str, Any], platforms: List[str]) -> bool:
        """發送詳細的發布成功通知 (使用 Flex Message)"""
        try:
            flex_content = {
                "type": "bubble",
                "header": {
                    "type": "box",
                    "layout": "vertical",
                    "contents": [
                        {
                            "type": "text",
                            "text": "🎉 發布成功",
                            "weight": "bold",
                            "color": "#1DB446",
                            "size": "lg"
                        }
                    ],
                    "backgroundColor": "#E8F5E8",
                    "paddingAll": "md"
                },
                "body": {
                    "type": "box",
                    "layout": "vertical",
                    "contents": [
                        {
                            "type": "text",
                            "text": post_data.get('title', '無標題'),
                            "weight": "bold",
                            "size": "md",
                            "wrap": True
                        },
                        {
                            "type": "separator",
                            "margin": "md"
                        },
                        {
                            "type": "box",
                            "layout": "vertical",
                            "margin": "md",
                            "contents": [
                                {
                                    "type": "box",
                                    "layout": "baseline",
                                    "contents": [
                                        {
                                            "type": "text",
                                            "text": "平台:",
                                            "color": "#666666",
                                            "size": "sm",
                                            "flex": 1
                                        },
                                        {
                                            "type": "text",
                                            "text": "、".join(platforms),
                                            "wrap": True,
                                            "color": "#333333",
                                            "size": "sm",
                                            "flex": 3
                                        }
                                    ]
                                },
                                {
                                    "type": "box",
                                    "layout": "baseline",
                                    "margin": "sm",
                                    "contents": [
                                        {
                                            "type": "text",
                                            "text": "類型:",
                                            "color": "#666666",
                                            "size": "sm",
                                            "flex": 1
                                        },
                                        {
                                            "type": "text",
                                            "text": post_data.get('media_type', '未知'),
                                            "wrap": True,
                                            "color": "#333333",
                                            "size": "sm",
                                            "flex": 3
                                        }
                                    ]
                                },
                                {
                                    "type": "box",
                                    "layout": "baseline",
                                    "margin": "sm",
                                    "contents": [
                                        {
                                            "type": "text",
                                            "text": "時間:",
                                            "color": "#666666",
                                            "size": "sm",
                                            "flex": 1
                                        },
                                        {
                                            "type": "text",
                                            "text": post_data.get('publish_date', '現在'),
                                            "wrap": True,
                                            "color": "#333333",
                                            "size": "sm",
                                            "flex": 3
                                        }
                                    ]
                                }
                            ]
                        }
                    ]
                }
            }
            
            return self.send_flex_message("發布成功通知", flex_content)
            
        except Exception as e:
            logger.error(f"發送詳細發布成功通知時發生錯誤: {str(e)}")
            return False
    
    def get_profile(self) -> Dict[str, Any]:
        """獲取 Bot 資訊"""
        try:
            url = f"{self.base_url}/info"
            
            response = requests.get(url, headers=self.headers)
            response.raise_for_status()
            
            return response.json()
            
        except Exception as e:
            logger.error(f"獲取 Line Bot 資訊時發生錯誤: {str(e)}")
            return {}

