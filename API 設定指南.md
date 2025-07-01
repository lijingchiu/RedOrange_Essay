# API 設定指南

本指南將詳細說明如何設定各個社群媒體平台的 API，以便使用自動化發文系統。

## 目錄

1. [Notion API 設定](#notion-api-設定)
2. [Instagram API 設定](#instagram-api-設定)
3. [Facebook API 設定](#facebook-api-設定)
4. [Threads API 設定](#threads-api-設定)
5. [Line Messaging API 設定](#line-messaging-api-設定)
6. [環境變數設定](#環境變數設定)

---

## Notion API 設定

### 步驟 1: 建立 Notion 整合

1. 前往 [Notion Developers](https://developers.notion.com/)
2. 點擊「My integrations」
3. 點擊「New integration」
4. 填寫整合資訊：
   - **Name**: 輸入整合名稱（例如：社群媒體自動化）
   - **Logo**: 可選擇上傳 Logo
   - **Associated workspace**: 選擇您的工作區
5. 點擊「Submit」

### 步驟 2: 獲取 API 金鑰

1. 在整合頁面中，複製「Internal Integration Token」
2. 這就是您的 `NOTION_API_KEY`

### 步驟 3: 建立資料庫

1. 在 Notion 中建立新的資料庫
2. 添加以下欄位：

| 欄位名稱 | 類型 | 說明 |
|---------|------|------|
| 標題 | 標題 | 文章標題或貼文標題 |
| 內容 | 富文本 | 文章正文或貼文文字內容 |
| 媒體類型 | 選擇 | 選項：文章、圖片、影片 |
| 媒體URL | URL | 圖片或影片的 URL |
| 發布狀態 | 選擇 | 選項：草稿、待發布、已發布、發布失敗 |
| 發布日期 | 日期 | 預計發布日期和時間 |
| 目標平台 | 多選 | 選項：Instagram、Facebook、Threads |
| Line通知狀態 | 選擇 | 選項：未發送、已發送、發送失敗 |
| 錯誤訊息 | 富文本 | 記錄發布失敗時的錯誤訊息 |

### 步驟 4: 分享資料庫給整合

1. 在資料庫頁面中，點擊右上角的「Share」
2. 點擊「Add connections」
3. 搜尋並選擇您剛建立的整合
4. 點擊「Invite」

### 步驟 5: 獲取資料庫 ID

1. 複製資料庫頁面的 URL
2. URL 格式：`https://www.notion.so/DATABASE_ID?v=VIEW_ID`
3. 提取 `DATABASE_ID` 部分（32 個字元的字串）
4. 這就是您的 `NOTION_DATABASE_ID`

---

## Instagram API 設定

### 前置條件

- Instagram 商業帳號或創作者帳號
- 連結到 Facebook 專頁的 Instagram 帳號
- Facebook 開發者帳號

### 步驟 1: 建立 Facebook 應用程式

1. 前往 [Facebook for Developers](https://developers.facebook.com/)
2. 點擊「My Apps」→「Create App」
3. 選擇「Business」類型
4. 填寫應用程式資訊：
   - **App Name**: 輸入應用程式名稱
   - **App Contact Email**: 輸入聯絡信箱
5. 點擊「Create App」

### 步驟 2: 添加 Instagram Basic Display

1. 在應用程式儀表板中，點擊「Add Product」
2. 找到「Instagram Basic Display」，點擊「Set Up」
3. 點擊「Create New App」
4. 填寫必要資訊並儲存

### 步驟 3: 設定 Instagram Graph API

1. 在應用程式儀表板中，添加「Instagram Graph API」產品
2. 在「Instagram Graph API」設定中：
   - 添加 Instagram 商業帳號
   - 設定權限：`instagram_basic`, `instagram_content_publish`, `pages_read_engagement`

### 步驟 4: 獲取存取權杖

1. 使用 Graph API Explorer 或程式碼獲取長期存取權杖
2. 確保權杖具有必要的權限
3. 這就是您的 `INSTAGRAM_ACCESS_TOKEN`

### 步驟 5: 獲取 Instagram 用戶 ID

1. 使用以下 API 呼叫獲取用戶 ID：
   ```
   GET https://graph.facebook.com/v23.0/me/accounts?access_token=YOUR_ACCESS_TOKEN
   ```
2. 找到對應的 Instagram 商業帳號 ID
3. 這就是您的 `INSTAGRAM_USER_ID`

---

## Facebook API 設定

### 步驟 1: 使用現有的 Facebook 應用程式

如果您已經為 Instagram 建立了 Facebook 應用程式，可以使用同一個應用程式。

### 步驟 2: 添加 Pages API

1. 在應用程式儀表板中，添加「Facebook Login」和「Pages API」產品
2. 設定必要的權限：`pages_manage_posts`, `pages_read_engagement`

### 步驟 3: 獲取專頁存取權杖

1. 使用 Graph API Explorer 獲取專頁存取權杖
2. 選擇您要發布內容的 Facebook 專頁
3. 獲取長期的專頁存取權杖
4. 這就是您的 `FACEBOOK_ACCESS_TOKEN`

### 步驟 4: 獲取專頁 ID

1. 在 Facebook 專頁設定中找到專頁 ID
2. 或使用 Graph API 呼叫：
   ```
   GET https://graph.facebook.com/v23.0/me/accounts?access_token=YOUR_ACCESS_TOKEN
   ```
3. 這就是您的 `FACEBOOK_PAGE_ID`

---

## Threads API 設定

### 前置條件

- Threads 帳號（連結到 Instagram 商業帳號）
- 已設定的 Instagram Graph API

### 步驟 1: 啟用 Threads API

1. 在 Facebook 應用程式中，添加「Threads API」產品
2. 確保您的 Instagram 商業帳號已連結到 Threads

### 步驟 2: 獲取 Threads 存取權杖

1. 使用與 Instagram 相同的存取權杖
2. 確保權杖具有 Threads 相關權限
3. 這就是您的 `THREADS_ACCESS_TOKEN`

### 步驟 3: 獲取 Threads 用戶 ID

1. 使用以下 API 呼叫：
   ```
   GET https://graph.threads.net/v1.0/me?access_token=YOUR_ACCESS_TOKEN
   ```
2. 這就是您的 `THREADS_USER_ID`

---

## Line Messaging API 設定

### 步驟 1: 建立 Line 開發者帳號

1. 前往 [Line Developers](https://developers.line.biz/)
2. 使用 Line 帳號登入
3. 建立新的 Provider（如果還沒有）

### 步驟 2: 建立 Messaging API Channel

1. 在 Provider 中點擊「Create a new channel」
2. 選擇「Messaging API」
3. 填寫 Channel 資訊：
   - **Channel name**: 輸入頻道名稱
   - **Channel description**: 輸入描述
   - **Category**: 選擇適當的類別
   - **Subcategory**: 選擇子類別
4. 同意條款並建立 Channel

### 步驟 3: 設定 Channel

1. 在 Channel 設定中：
   - 啟用「Use webhooks」（如果需要）
   - 設定「Auto-reply messages」為停用
   - 設定「Greeting messages」為停用

### 步驟 4: 獲取 Channel Access Token

1. 在「Messaging API」標籤中
2. 找到「Channel access token」
3. 點擊「Issue」生成權杖
4. 這就是您的 `LINE_CHANNEL_ACCESS_TOKEN`

### 步驟 5: 獲取用戶 ID

1. 將 Line Bot 加為好友
2. 發送訊息給 Bot
3. 使用 Webhook 或其他方式獲取您的用戶 ID
4. 或使用 Line 官方工具獲取
5. 這就是您的 `LINE_USER_ID`

---

## 環境變數設定

### 建立 .env 檔案

在專案根目錄建立 `.env` 檔案，並填入所有獲取的 API 金鑰：

```bash
# Notion API 設定
NOTION_API_KEY=secret_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
NOTION_DATABASE_ID=xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx

# Instagram API 設定
INSTAGRAM_ACCESS_TOKEN=IGQVJxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
INSTAGRAM_USER_ID=17841xxxxxxxxxx

# Facebook API 設定
FACEBOOK_ACCESS_TOKEN=EAAxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
FACEBOOK_PAGE_ID=10158xxxxxxxxxx

# Threads API 設定
THREADS_ACCESS_TOKEN=IGQVJxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
THREADS_USER_ID=17841xxxxxxxxxx

# Line Messaging API 設定
LINE_CHANNEL_ACCESS_TOKEN=xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
LINE_USER_ID=Uxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx

# 媒體處理設定
TEMP_MEDIA_DIR=/tmp/media
MAX_IMAGE_SIZE_MB=8
MAX_VIDEO_SIZE_MB=300

# 日誌設定
LOG_LEVEL=INFO
LOG_FILE=automation.log
```

### 安全性注意事項

1. **絕對不要**將 `.env` 檔案提交到版本控制系統
2. 確保 `.env` 檔案已加入 `.gitignore`
3. 定期更新 API 金鑰
4. 使用最小權限原則設定 API 權限
5. 監控 API 使用情況

### 驗證設定

使用系統提供的測試功能驗證所有 API 設定：

```bash
# 啟動 Flask 應用程式
python src/main.py

# 在另一個終端機中測試
curl -X POST http://localhost:5000/api/automation/test-services
```

---

## 常見問題

### Q: Instagram API 權限被拒絕

**A**: 確保您的 Instagram 帳號是商業帳號或創作者帳號，並且已正確連結到 Facebook 專頁。

### Q: Notion API 無法存取資料庫

**A**: 確保您已將資料庫分享給 Notion 整合，並且資料庫 ID 正確。

### Q: Line Bot 無法發送訊息

**A**: 確保您已將 Bot 加為好友，並且用戶 ID 正確。

### Q: Facebook 專頁權限不足

**A**: 確保您是專頁的管理員，並且存取權杖具有必要的權限。

### Q: API 呼叫頻率限制

**A**: 各平台都有 API 呼叫頻率限制，請參考官方文件並適當調整呼叫頻率。

---

## 參考資源

- [Notion API 文件](https://developers.notion.com/docs)
- [Instagram Graph API 文件](https://developers.facebook.com/docs/instagram-api)
- [Facebook Graph API 文件](https://developers.facebook.com/docs/graph-api)
- [Threads API 文件](https://developers.facebook.com/docs/threads)
- [Line Messaging API 文件](https://developers.line.biz/en/docs/messaging-api/)

如有任何問題，請參考官方文件或聯繫技術支援。

