import os
import requests
import logging
import tempfile
from typing import Optional, Tuple, Dict, Any
from urllib.parse import urlparse
from config import config

logger = logging.getLogger(__name__)

class MediaProcessor:
    """媒體處理服務類別"""
    
    def __init__(self):
        self.temp_dir = config.TEMP_MEDIA_DIR
        self.max_image_size_mb = config.MAX_IMAGE_SIZE_MB
        self.max_video_size_mb = config.MAX_VIDEO_SIZE_MB
        
        # 確保暫存目錄存在
        os.makedirs(self.temp_dir, exist_ok=True)
    
    def download_media(self, url: str, filename: str = None) -> Optional[str]:
        """下載媒體檔案"""
        try:
            response = requests.get(url, stream=True)
            response.raise_for_status()
            
            # 如果沒有提供檔名，從 URL 中提取
            if not filename:
                parsed_url = urlparse(url)
                filename = os.path.basename(parsed_url.path)
                if not filename:
                    filename = "downloaded_media"
            
            # 建立完整的檔案路徑
            file_path = os.path.join(self.temp_dir, filename)
            
            # 下載檔案
            with open(file_path, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    f.write(chunk)
            
            logger.info(f"成功下載媒體檔案: {file_path}")
            return file_path
            
        except Exception as e:
            logger.error(f"下載媒體檔案時發生錯誤: {str(e)}")
            return None
    
    def process_image_for_instagram(self, image_path: str) -> Optional[str]:
        logger.warning("Pillow 庫未安裝或存在問題，Instagram 圖片處理功能已禁用。將直接使用原始圖片。")
        return image_path

    def process_image_for_facebook(self, image_path: str) -> Optional[str]:
        logger.warning("Pillow 庫未安裝或存在問題，Facebook 圖片處理功能已禁用。將直接使用原始圖片。")
        return image_path

    def get_image_info(self, image_path: str) -> Optional[Dict[str, Any]]:
        logger.warning("Pillow 庫未安裝或存在問題，圖片資訊獲取功能已禁用。")
        return None
    
    def get_video_info(self, video_path: str) -> Optional[Dict[str, Any]]:
        """獲取影片資訊"""
        try:
            file_size = os.path.getsize(video_path)
            
            return {
                'file_size_bytes': file_size,
                'file_size_mb': file_size / (1024 * 1024),
                'file_path': video_path
            }
            
        except Exception as e:
            logger.error(f"獲取影片資訊時發生錯誤: {str(e)}")
            return None
    
    def _get_processed_filename(self, original_path: str, suffix: str) -> str:
        """生成處理後的檔案名稱"""
        base_name = os.path.splitext(os.path.basename(original_path))[0]
        return os.path.join(self.temp_dir, f"{base_name}{suffix}.jpg")
    
    def cleanup_temp_files(self) -> None:
        """清理暫存檔案"""
        try:
            for filename in os.listdir(self.temp_dir):
                file_path = os.path.join(self.temp_dir, filename)
                if os.path.isfile(file_path):
                    os.remove(file_path)
            
            logger.info("成功清理暫存檔案")
            
        except Exception as e:
            logger.error(f"清理暫存檔案時發生錯誤: {str(e)}")
    
    def upload_to_temporary_hosting(self, file_path: str) -> Optional[str]:
        """上傳檔案到暫時託管服務（這裡需要實作實際的上傳邏輯）"""
        # 這裡應該實作上傳到雲端儲存服務的邏輯
        # 例如 AWS S3, Google Cloud Storage, 或其他檔案託管服務
        # 目前返回本地檔案路徑作為示例
        
        try:
            # 實際實作時，這裡應該上傳檔案並返回公開的 URL
            logger.warning("upload_to_temporary_hosting 尚未實作實際的上傳邏輯")
            return f"file://{file_path}"  # 暫時返回本地路徑
            
        except Exception as e:
            logger.error(f"上傳檔案到暫時託管服務時發生錯誤: {str(e)}")
            return None

