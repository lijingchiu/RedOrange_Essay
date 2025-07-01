import os
from dataclasses import dataclass
from typing import Optional

@dataclass
class Config:
    """應用程式設定類別"""
    
    # Notion API 設定
    NOTION_API_KEY: Optional[str] = os.getenv('NOTION_API_KEY')
    NOTION_DATABASE_ID: Optional[str] = os.getenv('NOTION_DATABASE_ID')
    
    # Instagram API 設定
    INSTAGRAM_ACCESS_TOKEN: Optional[str] = os.getenv('INSTAGRAM_ACCESS_TOKEN')
    INSTAGRAM_USER_ID: Optional[str] = os.getenv('INSTAGRAM_USER_ID')
    
    # Facebook API 設定
    FACEBOOK_ACCESS_TOKEN: Optional[str] = os.getenv('FACEBOOK_ACCESS_TOKEN')
    FACEBOOK_PAGE_ID: Optional[str] = os.getenv('FACEBOOK_PAGE_ID')
    
    # Threads API 設定
    THREADS_ACCESS_TOKEN: Optional[str] = os.getenv('THREADS_ACCESS_TOKEN')
    THREADS_USER_ID: Optional[str] = os.getenv('THREADS_USER_ID')
    
    # Line Messaging API 設定
    LINE_CHANNEL_ACCESS_TOKEN: Optional[str] = os.getenv('LINE_CHANNEL_ACCESS_TOKEN')
    LINE_USER_ID: Optional[str] = os.getenv('LINE_USER_ID')
    
    # 媒體處理設定
    TEMP_MEDIA_DIR: str = os.getenv('TEMP_MEDIA_DIR', '/tmp/media')
    MAX_IMAGE_SIZE_MB: int = int(os.getenv('MAX_IMAGE_SIZE_MB', '8'))
    MAX_VIDEO_SIZE_MB: int = int(os.getenv('MAX_VIDEO_SIZE_MB', '300'))
    
    # 日誌設定
    LOG_LEVEL: str = os.getenv('LOG_LEVEL', 'INFO')
    LOG_FILE: str = os.getenv('LOG_FILE', 'automation.log')
    
    def validate(self) -> bool:
        """驗證必要的設定是否存在"""
        required_configs = [
            'NOTION_API_KEY',
            'NOTION_DATABASE_ID',
            'LINE_CHANNEL_ACCESS_TOKEN',
            'LINE_USER_ID'
        ]
        
        missing_configs = []
        for config in required_configs:
            if not getattr(self, config):
                missing_configs.append(config)
        
        if missing_configs:
            print(f"缺少必要設定: {', '.join(missing_configs)}")
            return False
        
        return True

# 全域設定實例
config = Config()

