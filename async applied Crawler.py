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
episode_number = 100     # 화 (에피소드)
# 세팅 (변경 X)
# ---------------------------------------------------------------------------------
storage = f'{os.path.dirname(os.path.realpath(__file__))}\\{title}'
if os.path.isdir(storage):
    shutil.rmtree(storage)
    shutil.rmtree(storage + "_raw")
os.makedirs(storage)
os.makedirs(storage + "_raw")

f = codecs.open('%s\\log.txt' % storage, 'w', 'utf-8')


async def get_page_html(url):
    async with aiohttp.ClientSession() as session :
        async with session.get(url) as resp :
            page = await resp.text()
    return page

async def search_src(epi_num):
    url = f"http://comic.naver.com/webtoon/detail.nhn?titleId={titleID}&no={(epi_num+1)}&weekday={weekday}"
    page = await get_page_html(url)
    soup = bs(page, "lxml")
    wt_viewer = soup.find(class_="wt_viewer")
    imgs = wt_viewer.find_all("img")
    srcs = [img.get("src") for img in imgs]

    header = {'User-agent':'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.84 Safari/537.36'}
    header.update({'referer' : url})
    return header, srcs

async def download_image(EPISODE_NUMBER):
    header, srcs = await search_src(EPISODE_NUMBER)
    
    i = 0
    for src in srcs :
        async with aiohttp.ClientSession() as session :
            async with session.get(src, headers=header) as res:
                with open(f'{storage + "_raw"}\\{EPISODE_NUMBER}-{i}.png', 'wb') as outfile:
                    content = await res.content.read()
                    outfile.write(content)
                    i += 1

if __name__ == "__main__" :
    s = time.time()
    tasks = [download_image(x) for x in range(episode_number)]
    loop = asyncio.get_event_loop()    
    try : 
        loop.run_until_complete(asyncio.wait(tasks))
    finally : 
        print(f'{time.time() - s:0.3f}sec')
        loop.close()