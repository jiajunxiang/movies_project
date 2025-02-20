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
from faker import Faker


urls = ['https://movie.douban.com/subject/34841067/comments?start={}&limit=20&status=P&sort=new_score'.format(str(i))
        for i in range(0, 200, 20)]  # 通过观察的url翻页的规律，使用for循环得到10个链接，保存到urls列表中
print(urls)
dic_h = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36",
    "Cookie":"bid=%s" % "".join(random.sample(string.ascii_letters+string.digits,11))}
comments_list = []  # 初始化用于保存短评的列表

for url in urls:  # 使用for循环分别获取每个页面的数据，保存到comments_list列表
    r = requests.get(url=url, headers=dic_h).text

    soup = BeautifulSoup(r, 'lxml')
    ul = soup.find('div', id="comments")
    lis = ul.find_all('p')

    list2 = []
    for li in lis:
        list2.append(li.find('span').string)
    # print(list2)
    comments_list.extend(list2)
    time.sleep(random.randint(0, 3))  # 暂停0~3秒

with open('lhy_comments.txt', 'w', encoding='utf-8') as f:  # 使用with open()新建对象f
    # 将列表中的数据循环写入到文本文件中
    for i in comments_list:
        f.write(i + "\n")  # 写入数据
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
# 打开文本
with open("lhy_comments.txt",encoding="utf-8") as f:
    s = f.read()
print(type(s))
# 中文分词
text = ' '.join(jieba.cut(s))
print(text)
# 生成对象
img = Image.open("19.png") # 打开遮罩图片
mask = np.array(img) #将图片转换为数组

stopwords = ["我","你","她","的","是","了","在","也","和","就","都","这","贾玲"]
wc = wordcloud.WordCloud(font_path="msyh.ttc",
               mask=mask,
               width = 1000,
               height = 700,
               background_color='white',
               max_words=200,
               stopwords=stopwords)
print(type(text))
wc.generate(text)

# 显示词云
plt.imshow(wc, interpolation='bilinear')# 用plt显示图片
plt.axis("off")  # 不显示坐标轴
plt.show() # 显示图片

# 保存到文件
wc.to_file("李焕英2.png")