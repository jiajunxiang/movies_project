#-*- coding:utf-8 -*-

import requests
import random
import string
from lxml import etree

#这里导入时间模块，以免豆瓣封你IP
import time




url ='https://movie.douban.com/subject/26942674/'
headers = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36",
    "Cookie":"bid=%s" % "".join(random.sample(string.ascii_letters+string.digits,11))}
data = requests.get(url,headers=headers).text

s=etree.HTML(data)
#给定url并用requests.get()方法来获取页面的text，用etree.HTML()

#来解析下载的页面数据“data”。

####1.获取电影名称。
film_name=s.xpath('//*[@id="content"]/h1/span[1]/text()')#电影名
director=s.xpath('//*[@id="info"]/span[1]/span[2]/a/text()')#编剧
actor=s.xpath('//*[@id="info"]/span[3]/span[2]/a/text()')#主演
movie_time=s.xpath('//*[@id="info"]/span[13]/text()')#片长

#由于导演有时候不止一个人，所以我这里以列表的形式输出
ds = []
for d in director:
    ds.append(d)

#由于演员不止一个人，所以我这里以列表的形式输出
acs = []
for a in actor:
    acs.append(a)

print ('电影名:',film_name)

print ('导演:',ds)

print ('主演:',acs)

print ('片长:',movie_time)