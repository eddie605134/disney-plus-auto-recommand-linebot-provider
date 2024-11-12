# disney_bot.py
import os
from dotenv import load_dotenv
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
from linebot import LineBotApi
from linebot.models import TextSendMessage
import time
import re

# 載入 .env 檔案
load_dotenv()

# 取得環境變數
DISNEY_URL = os.getenv('DISNEY_URL')
LINE_CHANNEL_ACCESS_TOKEN = os.getenv('LINE_CHANNEL_ACCESS_TOKEN')
LINE_USER_ID = os.getenv('LINE_USER_ID')

# 設定 LINE Bot
line_bot_api = LineBotApi(LINE_CHANNEL_ACCESS_TOKEN)

def fetch_white_text_from_strong_tags_selenium(url):
    # 初始化 Chrome 瀏覽器 (需要有 chromedriver)
    service = ChromeService(executable_path='/opt/homebrew/bin/chromedriver')  # 替換成 chromedriver 的實際路徑
    driver = webdriver.Chrome(service=service)

    # 打開指定的 URL
    driver.get(url)

    # 等待 JavaScript 加載完成，根據網頁情況適當調整等待時間
    time.sleep(5)

    # 使用 BeautifulSoup 解析最終頁面內容
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    driver.quit()

    # 找到所有的 <strong> 標籤
    strong_tags = soup.find_all('strong')
    if not strong_tags:
        return "未找到任何 <strong> 標籤"

    # 遍歷所有找到的 <strong> 標籤，篩選出符合條件的
    white_text_list = []
    white_color_patterns = [
        r'color:\s*rgb\(\s*255,\s*255,\s*255\s*\)',
        r'color:\s*#ffffff',
        r'color:\s*rgba\(\s*255,\s*255,\s*255,\s*1\s*\)'
    ]

    for tag in strong_tags:
        # 確保 style 存在並且匹配顏色模式
        style = tag.get('style')
        if style and any(re.search(pattern, style, re.IGNORECASE) for pattern in white_color_patterns):
            text = tag.get_text(strip=True)
            white_text_list.append(text)

    if not white_text_list:
        return "未找到符合條件的 <strong> 標籤"

    return '\n'.join(white_text_list)

def send_line_message(message):
    line_bot_api.push_message(LINE_USER_ID, TextSendMessage(text=message))

def job():
    new_releases = fetch_white_text_from_strong_tags_selenium(DISNEY_URL)
    send_line_message(new_releases)