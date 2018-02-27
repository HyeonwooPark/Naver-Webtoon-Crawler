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
import time
# 변수 입력 
# ---------------------------------------------------------------------------------

titleID = 183559  
title = "신의 탑"
weekday = "mon"
episode_number = 5     # 화 (에피소드)
# 세팅 (변경 X)
# ---------------------------------------------------------------------------------
storage = f'{os.path.dirname(os.path.realpath(__file__))}\\{title}'
if os.path.isdir(storage):
    shutil.rmtree(storage)
    shutil.rmtree(storage + "_raw")
os.makedirs(storage)
os.makedirs(storage + "_raw")

f = codecs.open('%s\\log.txt' % storage, 'w', 'utf-8')

header = {'User-agent':'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.84 Safari/537.36'}


async def search(EPISODE_NUMBER):
    loop = asyncio.get_event_loop()
    for i in range(episode_number) :
        url = f"http://comic.naver.com/webtoon/detail.nhn?titleId={titleID}&no={(i+1)}&weekday={weekday}" 
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as res:
                page = await res.text()
                soup = bs(page, "lxml")
                wt_viewer = soup.find(class_="wt_viewer")
                imgs = wt_viewer.find_all("img")
                srcs = [img.get("src") for img in imgs]

            async with session.get([src for src in await srcs], headers=header) as res:
                with open(f'{storage + "_raw"}\\{EPISODE_NUMBER}-{i}.png', 'wb') as outfile:
                    outfile.write(res.content)

            

if __name__ == "__main__":
    
    loop = asyncio.get_event_loop()
    try:
        loop.run_until_complete(search(episode_number))
    finally: 
        loop.close()