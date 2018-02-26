from bs4 import BeautifulSoup as bs
import numpy as np
import requests
import os
import shutil
import PIL
from PIL import Image
import codecs
import asyncio
import aiohttp


# 변수 입력 
# ---------------------------------------------------------------------------------

titleID = 183559
title = "신의 탑"
weekday = "mon"
episode_number = 2     # 화 (에피소드)
# 세팅 (변경 X)
# ---------------------------------------------------------------------------------
dir_path = os.path.dirname(os.path.realpath(__file__))  # 파일 위치 찾기
storage = '{0}\\{1}'.format(dir_path, title)
os.makedirs(storage)
os.makedirs(storage + "_raw")

f = codecs.open('%s\\log.txt' % storage, 'w', 'utf-8')

headers = {'User-agent':'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.84 Safari/537.36'}

async def search(titleID, episode_number, weekday):    
    url = "http://comic.naver.com/webtoon/detail.nhn?titleId={0}&no={1}&weekday={2}".format(titleID, (episode_number+1), weekday)
    res = requests.get(url)
    soup = bs(res.text, "lxml")
    wt_viewer = soup.find(class_="wt_viewer")
    imgs = wt_viewer.find_all("img")
    srcs = [{img.get("src") : img.get("id")} for img in imgs]