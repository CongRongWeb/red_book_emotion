# -*- coding: utf-8 -*-
import datetime
import urllib
import jieba
import requests
import json
import jieba.analyse as analyse
import time
from cnsenti import Sentiment,Emotion
import os
import codecs
from fake_useragent import UserAgent
import pymysql
from matplotlib import pyplot as plt    #绘图，数据可视化
from numpy import random
from wordcloud import WordCloud         #词云
from PIL import Image                   #图片处理
import numpy as np                      #矩阵运算
import urllib3  # 导入urllib3模块
from flask import Flask, render_template, request, jsonify, make_response
import json
import re

def get_comment(url,title,id,headers):
    try:
        wb_data = requests.get(url, headers=headers)

        wb_data.encoding='utf-8'
        jsondata = wb_data.json()

        datas = jsondata.get('data').get('data')
        for data in datas:
            created_at = data.get("created_at")
            like_counts = data.get("like_counts")
            source = data.get("source")
            username = data.get("user").get("screen_name")
            comment = data.get("text")
            pattern = re.compile(r'<[^>]+>', re.S)
            comment2 = pattern.sub('', comment)
            cop = re.compile("[^\u4e00-\u9fa5^a-z^A-Z^0-9]")  # 匹配不是中文、大小写、数字的其他字符

            comment1 = cop.sub('', comment2)  # 将string1中匹配到的字符替换成空字符
            sql = "insert into news (news_title,news_id,username,comment,like_counts,source,created_at) values('%s','%s','%s','%s','%s','%s','%s')" % (
            title, id, username, comment1, like_counts, source,created_at)
            db = pymysql.connect(host="localhost", user="root", password="root", database="python_emotion_check", port=3306, charset="utf8")
            cursor = db.cursor()
            cursor.execute(sql)
            cursor.close()
            db.commit()
            db.close()
    except KeyError:
        pass





def sp(cookie,title,id):
  ua = UserAgent()
  headers = {
    'authority': 's.weibo.com',
    'method': 'GET',
    'scheme': 'https',
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'accept-encoding': 'gzip, deflate, br',
    'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8',
    'cache-control': 'no-cache',
    'cookie':cookie,
    'pragma': 'no-cache',
    'referer': 'https://weibo.com/',
    'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="102", "Google Chrome";v="102"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'document',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-site': 'same-site',
    'sec-fetch-user': '?1',
    'upgrade-insecure-requests': '1',
    'user-agent': ua.random,
    "Cookies": cookie,
   }
  url_comment = ['https://m.weibo.cn/api/comments/show?id={}&page={}'.format(id,str(i)) for i in range(1, 1000)]
  for url in url_comment:
    get_comment(url,title,id,headers)
    time.sleep(2)


# cookie='SUB=_2A25JNl91DeThGeNK7FYZ8yrJwziIHXVq2WE9rDV6PUJbktAGLRThkW1NSTc5ZhEfPiB2yYqyP6s-CLRPcds0tEKy; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9W5syz4f4nqnApe3clfQ8CM15NHD95QfShMX1heXSKnXWs4Dqcj6i--Xi-zRiKn7i--ciKL8iKL2i--4iK.Ni-iWi--RiKLhiKLhi--fiKnNi-iWi--fi-2EiK.4i--ciKL2i-2f; SSOLoginState=1681010469; WEIBOCN_FROM=1110006030; __bid_n=187654031832a8f8b54207; FPTOKEN=X0OoXrgg1pohnYZcNKh8qHNk+SKhJZalDbezxE7PyQ/d3p+rmDLkz/cehJ044NS11GfbaWmKZxXRpHHaIf+dUeJFU1p8bvDfjhyPbH2grOLYGjePs8upAUSRE0P+7eRh8PtTpLyui59658QkLC4wV/1wdVNX/s0SlJl53dG/wLBnSXArPL6Wv1F/oijUefAZ49VCC9MVcFW+9ynFE4sDISPG706P9L1R2AT3xfGgGRlfYQb4iigQ3XcoTjFWt0bOttztzyIy9lVuIglD2QEiH1w21ZOU/QxEaNWwsdcMTuEYZizzNhPKjdR9P00ZWkIEikd0KnGiEGX8j/R5XKrXuNIO14h77q8x1CX6JlrLhTPqMoxZoOdl5pkUGDQ/XoI8rvqeIqbULyQxS19n9KWj1A==|WCUS5nZsFd6N61pWQUyY82VKOQtfazmDH6Cq6nRiqDM=|10|d320f4b5749b62adf02d232b9fd7ce83; _T_WM=32522284107; MLOGIN=1; XSRF-TOKEN=fddc16; M_WEIBOCN_PARAMS=luicode%3D20000174%26uicode%3D20000061%26fid%3D4888283618218019%26oid%3D4888283618218019'
# title='测试'
# id='4887273528887623'
#sp(cookie,title,id)



app = Flask(__name__)
UPLOAD_FOLDER = 'upload'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
class DateEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime.datetime):
            return obj.strftime('%Y-%m-%d %H:%M:%S')
        elif isinstance(obj, date):
            return obj.strftime("%Y-%m-%d")
        else:
            return json.JSONEncoder.default(self, obj)


basedir = os.path.abspath(os.path.dirname(__file__))
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'JPG', 'PNG', 'gif', 'GIF','MP4'])


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

import datetime
import random
class Pic_str:
    def create_uuid(self): #生成唯一的图片的名称字符串，防止图片显示时的重名问题
        nowTime = datetime.datetime.now().strftime("%Y%m%d%H%M%S");  # 生成当前时间
        randomNum = random.randint(0, 100);  # 生成的随机整数n，其中0<=n<=100
        if randomNum <= 10:
            randomNum = str(0) + str(randomNum);
        uniqueNum = str(nowTime) + str(randomNum);
        return uniqueNum;


@app.route('/show/<string:filename>', methods=['GET'])
def show_photo(filename):
    file_dir = os.path.join(basedir, app.config['UPLOAD_FOLDER'])
    if request.method == 'GET':
        if filename is None:
            pass
        else:
            image_data = open(os.path.join(file_dir, '%s' % filename), "rb").read()
            response = make_response(image_data)
            response.headers['Content-Type'] = 'image/png'
            return response
    else:
        pass


def wordtowords(string):
  finalStr = ""
  for i in range(len(string)):  # 遍历每个字符
    try:
      if string[i - 1] == " " and string[i + 1] == " ":  # 若此字符前后都为空白，则判断为单字符，丢弃
        continue
    except Exception as e:  # 第一个和最后一个字符的判断会越界
      print(e)
    finalStr += string[i]  # 保存通过判断的字符
  return finalStr


@app.route('/insertNews',methods=['post'])
def insertNews():
    data = request.get_json()
    cookie = data['cookie']
    title = data['title']
    id = data['id']
    sp(cookie,title,id)
    return jsonify({"flag": True, "message": '操作成功'})



@app.route('/getNews',methods=['post'])
def getNews():
    data = request.get_json()
    name = data['name']
    db = pymysql.connect(host="localhost", user="root", password="root", database="python_emotion_check", port=3306, charset="utf8")
    cursor = db.cursor()
    sql = "select any_value(news_id),any_value(news_title) from news where news_title like '%{}%' group by news_title ".format(name)
    cursor.execute(sql)
    results=cursor.fetchall()
    cursor.close()
    db.commit()
    db.close()
    return jsonify({"flag": True, "data": results,"message":'操作成功'})

@app.route('/getComment',methods=['post'])
def getComment():
    data = request.get_json()
    comment = data['comment']
    news_title = data['news_title']
    db = pymysql.connect(host="localhost", user="root", password="root", database="python_emotion_check", port=3306, charset="utf8")
    cursor = db.cursor()
    sql = "select * from news where news_title like '%{}%' and comment like '%{}%' ".format(news_title,comment)
    cursor.execute(sql)
    results=cursor.fetchall()
    cursor.close()
    db.commit()
    db.close()
    return jsonify({"flag": True, "data": results,"message":'操作成功'})


@app.route('/getCloudImgOrSave',methods=['post'])
def getCloudImgOrSave():
    data = request.get_json()
    comment = data['comment']
    cut = jieba.cut(comment)
    string = ' '.join(cut)
    words = wordtowords(string)
    img = Image.open(r'.\upload\movie_spider_tree.jpg')  # 打开遮罩图片
    img_array = np.array(img)  # 将图片转换为数组
    wc = WordCloud(
        background_color='white',
        mask=img_array,
        font_path="msyh.ttc"  # 字体所在位置：C:\Windows\Fonts
    )
    wc.generate_from_text(words)

    # 绘制图片
    fig = plt.figure(1)
    plt.imshow(wc)
    plt.axis('off')  # 是否显示坐标轴
    nowTime = datetime.datetime.now().strftime("%Y%m%d%H%M%S");  # 生成当前时间
    randomNum = random.randint(0, 100);  # 生成的随机整数n，其中0<=n<=100
    if randomNum <= 10:
        randomNum = str(0) + str(randomNum);
    uniqueNum = str(nowTime) + str(randomNum);
    # 输出词云图片到文件
    plt.savefig( './upload/{}.jpg'.format(uniqueNum) ,dpi=500)
    return jsonify({"flag": True,"imgurl":'http://localhost:5003/show/' + uniqueNum+'.jpg', "message": '操作成功'})

senti = Sentiment( merge=True, encoding='utf-8')
emotion = Emotion()

@app.route('/getEmotion',methods=['post'])
def getEmotion():
    data = request.get_json()
    comment = data['comment']
    result1 = emotion.emotion_count(comment)
    result2 = senti.sentiment_calculate(comment)
    return {"result1":result1,"pos":int(result2['pos']),'neg':int(result2['neg'])}





@app.route('/getCloudImgOrSaveAll',methods=['post'])
def getCloudImgOrSaveAll():
    comment=''
    data = request.get_json()
    news_id = data['news_id']
    db = pymysql.connect(host="localhost", user="root", password="root", database="python_emotion_check", port=3306, charset="utf8")
    cursor = db.cursor()
    sql = "select news_title from news where news_id = '{}'".format(news_id,)
    cursor.execute(sql)
    results=cursor.fetchall()
    cursor.close()
    db.commit()
    db.close()
    for i in results:
      comment += i[0].replace('回复','')
    cut = jieba.cut(comment)
    string = ' '.join(cut)
    words = wordtowords(string)
    img = Image.open(r'.\upload\movie_spider_tree.jpg')  # 打开遮罩图片
    img_array = np.array(img)  # 将图片转换为数组
    wc = WordCloud(
        background_color='white',
        mask=img_array,
        font_path="msyh.ttc"  # 字体所在位置：C:\Windows\Fonts
    )
    wc.generate_from_text(words)

    # 绘制图片
    fig = plt.figure(1)
    plt.imshow(wc)
    plt.axis('off')  # 是否显示坐标轴
    nowTime = datetime.datetime.now().strftime("%Y%m%d%H%M%S");  # 生成当前时间
    randomNum = random.randint(0, 100);  # 生成的随机整数n，其中0<=n<=100
    if randomNum <= 10:
        randomNum = str(0) + str(randomNum);
    uniqueNum = str(nowTime) + str(randomNum);
    # 输出词云图片到文件
    plt.savefig( './upload/{}.jpg'.format(uniqueNum) ,dpi=500)
    return jsonify({"flag": True,"imgurl":'http://localhost:5003/show/' + uniqueNum+'.jpg', "message": '操作成功'})



@app.route('/getEmotionAll',methods=['post'])
def getEmotionAll():
    data = request.get_json()
    news_id = data['news_id']
    db = pymysql.connect(host="localhost", user="root", password="root", database="python_emotion_check", port=3306, charset="utf8")
    cursor = db.cursor()
    sql = "select any_value(created_at),any_value(fid) from news where news_id='{}' group by created_at having count(created_at) >2 order by any_value(fid) desc ".format(news_id)
    cursor.execute(sql)
    results=cursor.fetchall()
    cursor.close()
    db.commit()
    db.close()
    return jsonify({"flag": True, "data": results,"message":'操作成功'})


@app.route('/getEmotionAllComment',methods=['post'])
def getEmotionAllComment():
    comment=''
    data = request.get_json()
    created_at = data['created_at']
    news_id = data['news_id']
    db = pymysql.connect(host="localhost", user="root", password="root", database="python_emotion_check", port=3306, charset="utf8")
    cursor = db.cursor()
    sql = "select comment from news where created_at = '{}' and news_id = '{}'".format(created_at,news_id)
    cursor.execute(sql)
    results=cursor.fetchall()
    cursor.close()
    db.commit()
    db.close()
    for i in results:
      comment += i[0].replace('回复','') +'。'
    result2 = senti.sentiment_calculate(comment)
    result1 = emotion.emotion_count(comment)
    percent = int(result2['pos'])/result1['words']
    return jsonify({"flag": True, "percent": percent,"message":'操作成功'})


@app.route('/makeSpider',methods=['post'])
def makeSpider():
    data = request.get_json()
    news_id = data['news_id']
    news_title = data['news_title']
    cookie = data['cookie']
    sp(cookie, news_title, news_id)
    return jsonify({"flag": True,"message":'操作成功'})


@app.route('/getDash',methods=['post'])
def getDash():
    comment=''
    data = request.get_json()
    news_id = data['news_id']
    db = pymysql.connect(host="localhost", user="root", password="root", database="python_emotion_check", port=3306, charset="utf8")
    cursor = db.cursor()
    sql = "select comment from news where  news_id = '{}'".format(news_id)
    cursor.execute(sql)
    results=cursor.fetchall()
    cursor.close()
    db.commit()
    db.close()
    for i in results:
      comment += i[0].replace('回复','') +'。'
    result2 = senti.sentiment_calculate(comment)
    result1 = emotion.emotion_count(comment)
    percent = int(result2['pos'])/result1['words']
    return jsonify({"flag": True, "percent": percent,"message":'操作成功'})


@app.route('/getZhu',methods=['post'])
def getZhu():
    comment=''
    data = request.get_json()
    news_id = data['news_id']
    db = pymysql.connect(host="localhost", user="root", password="root", database="python_emotion_check", port=3306, charset="utf8")
    cursor = db.cursor()
    sql = "select comment from news where  news_id = '{}'".format(news_id)
    cursor.execute(sql)
    results=cursor.fetchall()
    cursor.close()
    db.commit()
    db.close()
    for i in results:
      comment += i[0].replace('回复','') +'。'
    tags=analyse.extract_tags(comment, topK=20, withWeight=True, allowPOS=())
    return jsonify({"flag": True,"message":'操作成功',"result":tags})



if __name__ == "__main__":
    app.run(port=5003)
