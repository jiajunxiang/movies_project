#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#获取所有正在上映电影的电影词云（数据清洗版本）
import string
import re
import random
import time
import jieba.analyse
import numpy as np
from PIL import Image
import requests
import wordcloud
from matplotlib import pyplot as plt
from bs4 import BeautifulSoup


proxies = {
    'http':'',
    'https':''
}
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

def spider():
     url='https://movie.douban.com/cinema/nowplaying/linyi/'
     movie_data=requests.get(url,headers=header,proxies=proxies, timeout=3).content
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

########提取每一个热映电影的短评数据
def getComments(movieId,pageNum):
     eachComments = []
     if pageNum>0:
         start=(pageNum-1)*20
     else:
         return False

     comments_url='https://movie.douban.com/subject/'+movieId+'/comments?'+\
                  'start='+str(start)+'&limit=20&status=P&sort=new_score'
     comments_data=requests.get(comments_url,headers=header).content
     comments_soup=BeautifulSoup(comments_data,'lxml')
     comments_lists=comments_soup.find_all('p',class_='comment-content')

     for i in comments_lists:
         short_comment = i.find_all('span')[0].text
         if short_comment is not None:
             eachComments.append(short_comment)
             time.sleep(random.randint(0, 1))  # 暂停0~1秒
     # print(eachComments)
     return eachComments

def main():
    movie = dict()
    NowPlayingMovie = spider()
    for movieCount in range(len(NowPlayingMovie)):
        commentList = []
        movie['name'] = NowPlayingMovie[movieCount]['name']
        print(movie['name'])
        for i in range(2):
            num = i + 1
            commentList_temp = getComments(NowPlayingMovie[movieCount]['id'], num)
            commentList.append(commentList_temp)
        # print(commentList)
        ##########数据清洗
        comments = ''
        for j in range(len(commentList)):
            comments += (str(commentList[j])).strip()
        ##########使用正则表达式去掉标点符号
        pattern = re.compile(r'[\u4e00-\u9fa5]+')
        filterdata = re.findall(pattern, comments)
        cleaned_comments = ''.join(filterdata)
        print(cleaned_comments)
        movie['comments'] = cleaned_comments
        ##########使用jieba分词进行中文分词
        result = jieba.analyse.textrank(cleaned_comments, topK=50, withWeight=True)
        keywords = dict()
        for i in result:
            keywords[i[0]] = i[1]
        print("删除停用词前:", keywords)
        # 设置停用词
        stopwords = ["我", "你", "她", "的", "是", "了", "在", "也", "和", "就", "都", "这", "没有", "电影"]
        keywords = {x: keywords[x] for x in keywords if x not in stopwords}
        print("删除停用词后", keywords)
        # 生成对象
        img = Image.open("20221024.png")  # 打开遮罩图片
        mask = np.array(img)  # 将图片转换为数组
        # ###########用词云进行显示
        wc = wordcloud.WordCloud(
            font_path="simkai.ttf",
            mask=mask,
            width=1000,
            height=700,
            background_color='white',
            max_words=200,
            stopwords=stopwords)
        word_frequence = keywords
        myword = wc.fit_words(word_frequence)
        wc.to_file("hotMovie/{}.png".format(movie['name']))
        # 显示词云
        plt.imshow(myword, interpolation='bilinear')
        plt.axis("off")
        plt.show()


if __name__ == '__main__':
    main()