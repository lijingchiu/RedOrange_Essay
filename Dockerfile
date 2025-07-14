FROM python:3.11-slim

# 設定工作目錄
WORKDIR /app

# 安裝系統依賴
RUN apt-get update && apt-get install -y \
    curl \
    libjpeg-dev \
    zlib1g-dev \
    && rm -rf /var/lib/apt/lists/*

# 複製需求檔案
COPY requirements.txt .

# 安裝 Python 依賴
RUN pip install --no-cache-dir -r requirements.txt

# 複製應用程式程式碼
COPY . .

# 建立必要目錄
RUN mkdir -p /tmp/media logs

# 設定環境變數
ENV PYTHONPATH=/app
ENV FLASK_APP=main.py

# 暴露端口
EXPOSE 5000

# 啟動命令
CMD ["python", "main.py"]

