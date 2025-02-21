import csv
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


def default_wordcloud(content):
    # 去掉不需要显示的词
    stopword = {"我", "你", "她", "的", "是", "了", "哈", "就", "都", "这", "贾玲"}
    wc = wordcloud.WordCloud(
        font_path="C://Windows//Fonts//msyh.ttc",
        width=1000,
        height=700,
        background_color='white',
        max_words=100,
        stopwords=stopword
    )
    # msyh.ttc电脑本地字体，写可以写成绝对路径
    wc.generate(content)  # 加载词云文本
    wc.to_file("李焕英.png")  # 保存词云文件

def diy_wordcloud(content):
    # 生成对象
    img = Image.open("20230302.jpg")  # 打开遮罩图片
    mask = np.array(img)  # 将图片转换为数组

    stopword = {"我", "你", "她", "的", "是", "了", "在", "也", "和", "就", "都", "这", "贾玲"}
    wc = wordcloud.WordCloud(
        font_path="msyh.ttc",
        mask=mask,
        width=1000,
        height=700,
        background_color='white',
        max_words=100,
        stopwords=stopword
    )
    wc.generate(content)
    # 显示词云
    plt.imshow(wc, interpolation='bilinear')  # 用plt显示图片
    plt.axis("off")  # 不显示坐标轴
    plt.show()  # 显示图片
    # 保存到文件
    wc.to_file("李焕英2.png")

# range函数的第二个参数是最后一页的数字再加上20，运行此程序前务必检查此参数
urls = ['https://movie.douban.com/subject/34841067/comments?start={}&limit=20&status=P&sort=new_score'.format(str(i))
        for i in range(0, 100, 20)]  # 通过观察的url翻页的规律，使用for循环得到10个链接，保存到urls列表中
# print(urls)
dic_h = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,"
              "image/avif,image/webp,image/apng,"
              "*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
    "text/html": "charset=utf-8",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/"
                  "537.36 (KHTML, like Gecko) Chrome/99.0.4844.84 Safari"
                  "/537.36 HBPC/12.1.1.300",
    "Cookie": "bid=%s" % "".join(random.sample(string.ascii_letters + string.digits, 11))
}
comments_list = []  # 初始化用于保存短评的列表
## 创建文件对象
f = open('你好李焕英短评.csv', 'w', encoding='utf-8-sig', newline="")
csv_write = csv.DictWriter(f, fieldnames=['评论者', '评论日期', '点赞数', '评论内容'])
csv_write.writeheader() # 写入文件头

for url in urls:  # 使用for循环分别获取每个页面的数据，保存到comments_list列表
    r = requests.get(url=url, headers=dic_h,timeout=2)
    print(str(r.status_code)+'  '+url)
    soup = BeautifulSoup(r.text, 'lxml')
    ul = soup.find('div', id="comments")
    ls_comments_items=ul.find_all('div',attrs={'class': 'comment'})
    for item in ls_comments_items:
        # 获取点赞数字段
        vote_count = item.find('span',attrs={'class': 'votes vote-count'}).get_text()
        # 获取评论者字段
        reviewer=item.find('span',attrs={'class': 'comment-info'}).find('a').text
        # 获取评论日期字段
        comment_date=item.find('span',attrs={'class': 'comment-time'}).text
        # 获取评论内容字段
        comment_content=item.find('span',attrs={'class': 'short'}).text
        comments_list.append(comment_content)
        data_dict = {'评论者': reviewer, '评论日期': comment_date,
                     '点赞数': vote_count, '评论内容': comment_content}
        csv_write.writerow(data_dict)
        # 设置睡眠时间间隔，防止频繁访问网站
        time.sleep(random.randint(0,3))
    with open('lhy_comments.txt', 'w', encoding='utf-8') as f:  # 使用with open()新建对象f
        # 将列表中的数据循环写入到文本文件中
        for i in comments_list:
            f.write(i + "\n")  # 写入数据

if __name__ == '__main__':
    # 打开文本
    with open("lhy_comments.txt", encoding="utf-8") as f:
        s = f.read()
    # 基于精确模式的中文分词
    # ls=jieba.lcut(s)
    # 基于搜索引擎模式的中文分词
    ls=jieba.lcut_for_search(s)
    text = ' '.join(ls)
    # print(text)
    default_wordcloud(text)
    diy_wordcloud(text)



