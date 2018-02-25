from bs4 import BeautifulSoup as bs
import numpy as np
import requests
import os
import shutil
import PIL
from PIL import Image
import codecs


# 변수 입력 
# ---------------------------------------------------------------------------------

titleId = 697680
title = "선천적 얼간이들"
weekday = "mon"
episode_number = 72     # 화 (에피소드)

# 세팅 (변경 X)
# ---------------------------------------------------------------------------------
dir_path = os.path.dirname(os.path.realpath(__file__))  # 파일 위치 찾기
os.mkdir('{0}\\{1}'.format(dir_path, title + "_임시"))
os.mkdir('{0}\\{1}'.format(dir_path, title))

f = codecs.open('{0}\\{1}\\log.txt'.format(dir_path, title + "_임시"), 'w', 'utf-8')

headers = {'User-agent':'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.84 Safari/537.36'}



def main_crawler():
    for i in range(episode_number):
        page = "http://comic.naver.com/webtoon/detail.nhn?titleId={0}&no={1}&weekday={2}".format(titleId, (i+1), weekday)
        response = requests.get(page)
        soup = bs(response.text, "lxml")
        wt_viewer = soup.find(class_="wt_viewer")
        img = wt_viewer.find_all("img")

        imgs_set = list()
        headers.update({'referer' : page})
        cut_number = 0
        for cut in img:
            src = cut.get("src")
            r = requests.get(src, stream=True, headers=headers)
            with open('{0}\\{1}\\{2:03d}화 {3}.png'.format(dir_path, title + "_임시", i, cut_number), 'wb') as outfile:
                outfile.write(r.content)
                imgs_set.append('{0}\\{1}\\{2:03d}화 {3}.png'.format(dir_path, title + "_임시", i, cut_number))
                # 확장자가 jpg면 raise IOError(encoder error %d when writing image file % s) 에러에 화질 저하 --> 대신 PNG로
            cut_number += 1
        
        try :
            imgs = [PIL.Image.open(i) for i in imgs_set]
            imgs_comb = np.vstack(np.asarray(i) for i in imgs)
            imgs_comb = PIL.Image.fromarray(imgs_comb)
            imgs_comb.save('{0}\\{1}\\{2:03d}화.png'.format(dir_path, title, i))
        except Exception as e:
            #os.mkdir('{0}\\{1}'.format(dir_path, title + "_임시\\{0}".format(i))) # 경로 : _임시 \\ {에러 발생 화} 
            print("Error : %s" % e)
            print("error occured on {0:03d}화 {1}".format(i, cut_number))
            f.write("error occured on {0:03d}화 {1}".format(i, cut_number))

        imgs[:] = []
        imgs_set[:] = []
    f.close()
    #shutil.rmtree('{0}\\{1}'.format(dir_path, title + "_임시"))

if __name__ == "__main__":
    main_crawler()