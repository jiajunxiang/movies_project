#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#获取所有正在上映电影的电影词云（无数据清洗）
import string
import requests
from bs4 import BeautifulSoup
import time
import random
import jieba
import wordcloud
from PIL import Image
import numpy as np
from matplotlib import pyplot as plt


header = {
          "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,"
                    "image/avif,image/webp,image/apng,"
                    "*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
          "text/html":"charset=utf-8",
          "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/"
                        "537.36 (KHTML, like Gecko) Chrome/99.0.4844.84 Safari"
                        "/537.36 HBPC/12.1.1.300",
          "Cookie":"bid=%s" % "".join(random.sample(string.ascii_letters+string.digits,11))
}


def nowPlaying():
     url='https://movie.douban.com/cinema/nowplaying/linyi/'
     movie_data=requests.get(url,headers=header, timeout=3).content
     #将网页源码构造成BeautifulSoup对象，方便操作
     soup=BeautifulSoup(movie_data,'lxml')
     ##########提取热映电影的数据
     """从＜div id= 'nowplaying>标签开始是想要的数据，里面有电影的名称、 主演等信息"""
     nowplaying_movie=soup.find_all('div',id='nowplaying')
     #nowp aying movie ist 是所有电影信息的一个列表
     nowplaying_movie_list=nowplaying_movie[0].find_all('li',class_='list-item')
     movie_list=[]
     for i in nowplaying_movie_list:
          movie_dict={}
          movie_dict['id']=i['id']
          for tag in i.find_all('img') :
               movie_dict['name']=tag['alt']
               movie_list.append(movie_dict)
     return  movie_list


def getComments(movieID):
    urls = ['https://movie.douban.com/subject/'+str(movieID)+'/comments?start={}&limit=20&status=P&sort=new_score'.format(str(i))
        for i in range(0, 200, 20)]  # 通过观察的url翻页的规律，使用for循环得到10个链接，保存到urls列表中
    #print(urls)
    dic_h = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36",
    "Cookie":"bid=%s" % "".join(random.sample(string.ascii_letters+string.digits,11))}
    comments=''# 初始化用于保存短评的字符串
    for url in urls:  # 使用for循环分别获取每个页面的数据，保存到comments字符串
        r = requests.get(url=url, headers=dic_h).text

        soup = BeautifulSoup(r, 'lxml')
        ul = soup.find('div', id="comments")
        lis = ul.find_all('p')

        for li in lis:
            comments+=li.find('span').string
        time.sleep(random.randint(0, 2))  # 暂停0~2秒
    return comments
    """
    # 读取文本
    with open("lhy_comments.txt",encoding="utf-8") as f:
        s = f.read()
    ls = jieba.lcut(s) # 生成分词列表
    text = ' '.join(ls) # 连接成字符串
    
    
    stopwords = ["的","是","了"] # 去掉不需要显示的词
    
    wc = wordcloud.WordCloud(font_path="C://Windows//Fonts//msyh.ttc",
                             width = 1000,
                             height = 700,
                             background_color='white',
                             max_words=100,stopwords=s)
    # msyh.ttc电脑本地字体，写可以写成绝对路径
    wc.generate(text) # 加载词云文本
    wc.to_file("李焕英.png") # 保存词云文件
    """
def main():
    movie=dict()
    NowPlayingMovie = nowPlaying()
    for i in range(len(NowPlayingMovie)):
        movie['name'] = NowPlayingMovie[i]['name']
        print(movie['name'])

        comments=getComments(NowPlayingMovie[i]['id'])

        #中文分词
        text = ' '.join(jieba.cut(comments))
        # 生成对象
        img = Image.open("20221024.png") # 打开遮罩图片
        mask = np.array(img) #将图片转换为数组

        stopwords = ["我","你","她","的","是","了","在","也","和","就","都","这","贾玲","电影"]
        wc = wordcloud.WordCloud(font_path="msyh.ttc",
                           mask=mask,
                           width = 1000,
                           height = 700,
                           background_color='white',
                           max_words=400,
                           stopwords=stopwords)
        wc.generate(text)

        # 显示词云
        plt.imshow(wc, interpolation='bilinear')# 用plt显示图片
        plt.axis("off")  # 不显示坐标轴
        plt.show() # 显示图片

        # 保存到文件
        wc.to_file("hotMovie/{}.png".format(movie['name']))

if __name__ == '__main__':
        main()
