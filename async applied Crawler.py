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
import concurrent.futures

# 변수 입력 
# ---------------------------------------------------------------------------------

titleID = 183559
title = "신의 탑"
weekday = "mon"
episode_number = 4     # 화 (에피소드)
# 세팅 (변경 X)
# ---------------------------------------------------------------------------------
storage = '{0}\\{1}'.format(os.path.dirname(os.path.realpath(__file__)), title)
if os.path.isdir(storage):
    shutil.rmtree(storage)
    shutil.rmtree(storage + "_raw")
os.makedirs(storage)
os.makedirs(storage + "_raw")

f = codecs.open('%s\\log.txt' % storage, 'w', 'utf-8')

headers = {'User-agent':'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.84 Safari/537.36'}

async def search(titleID, weekday, episode_number):    
    url = "http://comic.naver.com/webtoon/detail.nhn?titleId={0}&no={1}&weekday={2}".format(titleID, (episode_number+1), weekday)
    res = requests.get(url)
    soup = bs(res.text, "lxml")
    wt_viewer = soup.find(class_="wt_viewer")
    imgs = wt_viewer.find_all("img")
    srcs = [{img.get("src") : img.get("id")} for img in imgs]

    return srcs

if __name__ == "__main__":
    with concurrent.futures.ThreadPoolExecutor(max_workers=5) as exe:
        fus = [exe.submit(search, titleID, weekday, i)  for i in range(10)]
        for f in concurrent.futures.as_completed(fus):
            data = f.result()
            print(data)