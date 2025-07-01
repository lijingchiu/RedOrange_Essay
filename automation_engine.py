import logging
from datetime import datetime
from typing import List, Dict, Any
from src.config import config
from src.services.notion_service import NotionService
from src.services.instagram_service import InstagramService
from src.services.facebook_service import FacebookService
from src.services.threads_service import ThreadsService
from src.services.line_service import LineService
from src.services.media_processor import MediaProcessor

# 設定日誌
logging.basicConfig(
    level=getattr(logging, config.LOG_LEVEL),
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(config.LOG_FILE),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)

class AutomationEngine:
    """自動化發文引擎"""
    
    def __init__(self):
        self.notion_service = NotionService()
        self.instagram_service = InstagramService()
        self.facebook_service = FacebookService()
        self.threads_service = ThreadsService()
        self.line_service = LineService()
        self.media_processor = MediaProcessor()
    
    def run(self) -> None:
        """執行自動化流程"""
        logger.info("開始執行自動化發文流程")
        
        try:
            # 驗證設定
            if not config.validate():
                logger.error("設定驗證失敗，停止執行")
                return
            
            # 獲取待發布的貼文
            pending_posts = self.notion_service.get_pending_posts()
            
            if not pending_posts:
                logger.info("沒有待發布的貼文")
                return
            
            # 處理每個待發布的貼文
            for post in pending_posts:
                self._process_post(post)
            
            # 清理暫存檔案
            self.media_processor.cleanup_temp_files()
            
            logger.info("自動化發文流程執行完成")
            
        except Exception as e:
            logger.error(f"執行自動化流程時發生錯誤: {str(e)}")
    
    def _process_post(self, post: Dict[str, Any]) -> None:
        """處理單個貼文"""
        post_id = post.get('id')
        title = post.get('title', '')
        content = post.get('content', '')
        media_type = post.get('media_type', '')
        media_url = post.get('media_url', '')
        target_platforms = post.get('target_platforms', [])
        
        logger.info(f"開始處理貼文: {title}")
        
        try:
            # 準備發布內容
            publish_content = self._prepare_content(post)
            if not publish_content:
                self._handle_post_failure(post_id, "內容準備失敗")
                return
            
            # 發布到各個平台
            success_platforms = []
            failed_platforms = []
            
            for platform in target_platforms:
                success = self._publish_to_platform(platform, publish_content)
                if success:
                    success_platforms.append(platform)
                else:
                    failed_platforms.append(platform)
            
            # 更新發布狀態
            if success_platforms:
                if failed_platforms:
                    # 部分成功
                    status = "部分發布"
                    error_msg = f"失敗平台: {', '.join(failed_platforms)}"
                    self.notion_service.update_post_status(post_id, status, error_msg)
                else:
                    # 全部成功
                    self.notion_service.update_post_status(post_id, "已發布")
                
                # 發送成功通知
                self._send_success_notification(post, success_platforms)
            else:
                # 全部失敗
                self._handle_post_failure(post_id, f"所有平台發布失敗: {', '.join(failed_platforms)}")
            
        except Exception as e:
            logger.error(f"處理貼文時發生錯誤: {str(e)}")
            self._handle_post_failure(post_id, str(e))
    
    def _prepare_content(self, post: Dict[str, Any]) -> Dict[str, Any]:
        """準備發布內容"""
        try:
            media_type = post.get('media_type', '')
            media_url = post.get('media_url', '')
            title = post.get('title', '')
            content = post.get('content', '')
            
            # 組合文字內容
            text_content = f"{title}\n\n{content}".strip()
            
            result = {
                'text': text_content,
                'media_type': media_type,
                'media_url': media_url
            }
            
            # 如果有媒體，下載並處理
            if media_url and media_type in ['圖片', '影片']:
                # 下載媒體檔案
                downloaded_file = self.media_processor.download_media(media_url)
                if not downloaded_file:
                    logger.error("媒體檔案下載失敗")
                    return None
                
                result['local_media_path'] = downloaded_file
                
                # 如果是圖片，進行處理
                if media_type == '圖片':
                    # 為不同平台處理圖片
                    instagram_image = self.media_processor.process_image_for_instagram(downloaded_file)
                    facebook_image = self.media_processor.process_image_for_facebook(downloaded_file)
                    
                    result['instagram_image'] = instagram_image
                    result['facebook_image'] = facebook_image
                    result['threads_image'] = instagram_image  # Threads 使用與 Instagram 相同的規格
            
            return result
            
        except Exception as e:
            logger.error(f"準備內容時發生錯誤: {str(e)}")
            return None
    
    def _publish_to_platform(self, platform: str, content: Dict[str, Any]) -> bool:
        """發布到指定平台"""
        try:
            media_type = content.get('media_type', '')
            text = content.get('text', '')
            
            if platform == 'Instagram':
                return self._publish_to_instagram(content)
            elif platform == 'Facebook':
                return self._publish_to_facebook(content)
            elif platform == 'Threads':
                return self._publish_to_threads(content)
            else:
                logger.warning(f"不支援的平台: {platform}")
                return False
                
        except Exception as e:
            logger.error(f"發布到 {platform} 時發生錯誤: {str(e)}")
            return False
    
    def _publish_to_instagram(self, content: Dict[str, Any]) -> bool:
        """發布到 Instagram"""
        try:
            media_type = content.get('media_type', '')
            text = content.get('text', '')
            
            if media_type == '圖片':
                image_path = content.get('instagram_image')
                if image_path:
                    # 需要上傳圖片到可公開存取的 URL
                    image_url = self.media_processor.upload_to_temporary_hosting(image_path)
                    if image_url:
                        return self.instagram_service.publish_image(image_url, text)
            elif media_type == '影片':
                video_path = content.get('local_media_path')
                if video_path:
                    # 需要上傳影片到可公開存取的 URL
                    video_url = self.media_processor.upload_to_temporary_hosting(video_path)
                    if video_url:
                        return self.instagram_service.publish_video(video_url, text)
            else:
                # 純文字內容，Instagram 不支援純文字貼文
                logger.warning("Instagram 不支援純文字貼文")
                return False
            
            return False
            
        except Exception as e:
            logger.error(f"發布到 Instagram 時發生錯誤: {str(e)}")
            return False
    
    def _publish_to_facebook(self, content: Dict[str, Any]) -> bool:
        """發布到 Facebook"""
        try:
            media_type = content.get('media_type', '')
            text = content.get('text', '')
            
            if media_type == '圖片':
                image_path = content.get('facebook_image')
                if image_path:
                    # 需要上傳圖片到可公開存取的 URL
                    image_url = self.media_processor.upload_to_temporary_hosting(image_path)
                    if image_url:
                        return self.facebook_service.publish_image_post(image_url, text)
            elif media_type == '影片':
                video_path = content.get('local_media_path')
                if video_path:
                    # 需要上傳影片到可公開存取的 URL
                    video_url = self.media_processor.upload_to_temporary_hosting(video_path)
                    if video_url:
                        return self.facebook_service.publish_video_post(video_url, text)
            else:
                # 純文字貼文
                return self.facebook_service.publish_text_post(text)
            
            return False
            
        except Exception as e:
            logger.error(f"發布到 Facebook 時發生錯誤: {str(e)}")
            return False
    
    def _publish_to_threads(self, content: Dict[str, Any]) -> bool:
        """發布到 Threads"""
        try:
            media_type = content.get('media_type', '')
            text = content.get('text', '')
            
            if media_type == '圖片':
                image_path = content.get('threads_image')
                if image_path:
                    # 需要上傳圖片到可公開存取的 URL
                    image_url = self.media_processor.upload_to_temporary_hosting(image_path)
                    if image_url:
                        return self.threads_service.publish_image_post(image_url, text)
            elif media_type == '影片':
                video_path = content.get('local_media_path')
                if video_path:
                    # 需要上傳影片到可公開存取的 URL
                    video_url = self.media_processor.upload_to_temporary_hosting(video_path)
                    if video_url:
                        return self.threads_service.publish_video_post(video_url, text)
            else:
                # 純文字貼文
                return self.threads_service.publish_text_post(text)
            
            return False
            
        except Exception as e:
            logger.error(f"發布到 Threads 時發生錯誤: {str(e)}")
            return False
    
    def _send_success_notification(self, post: Dict[str, Any], platforms: List[str]) -> None:
        """發送成功通知"""
        try:
            # 發送詳細的成功通知
            success = self.line_service.send_detailed_success_notification(post, platforms)
            
            # 更新 Line 通知狀態
            status = "已發送" if success else "發送失敗"
            self.notion_service.update_line_notification_status(post.get('id'), status)
            
        except Exception as e:
            logger.error(f"發送成功通知時發生錯誤: {str(e)}")
    
    def _handle_post_failure(self, post_id: str, error_message: str) -> None:
        """處理貼文失敗"""
        try:
            # 更新 Notion 狀態
            self.notion_service.update_post_status(post_id, "發布失敗", error_message)
            
            # 發送失敗通知
            self.line_service.send_failure_notification("貼文", [], error_message)
            
        except Exception as e:
            logger.error(f"處理貼文失敗時發生錯誤: {str(e)}")

def main():
    """主函數"""
    engine = AutomationEngine()
    engine.run()

if __name__ == "__main__":
    main()

