import random
import time
from urllib.parse import urlencode

import execjs
import pymysql
import requests
import json
import re
import csv


from zz_proxies import get_ip


# conn = pymysql.connect(
#         user='****',
#         passwd='****',
#         db='newmedia_db',
#         host='****',
#         charset="utf8",
#         use_unicode=True
#     )
# cursor = conn.cursor()



iplist = get_ip.get_iplist()
proxy = random.choice(iplist)


def save_csv(filename,data):
    with open(filename, 'a',newline='', errors='ignore',encoding='utf-8') as f:
        writer =csv.writer(f)
        writer.writerow(data.values())
def getSign(t,e):
    with open("baiduindex.js") as f:
        jsData = f.read()

    js = execjs.compile(jsData)
    sign = js.call('decrypt',t,e)
    return sign





t_url ='https://index.baidu.com/Interface/ptbk?uniqid={}'
get_uqi ='https://index.baidu.com/api/FeedSearchApi/getFeedIndex?'
with open(r'D:\Projects\myspiders\demo\baidusuccess.txt', 'r',
          encoding='utf-8') as f:
    keywords = f.readlines()
for name in ['侯凯文']:
    headers = {
        'Host': 'index.baidu.com',
        'Connection': 'keep-alive',
        'X-Requested-With': 'XMLHttpRequest',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36',
        'Cookie': random.choice(COOKIES)
    }
    proxies = {"http": "{}".format(proxy), "https": "{}".format(proxy)}
    #print(proxies)

    time.sleep(random.randint(2,3))
    if name:
        keyword = str(name).strip().strip('\t')
        get_uqi_parmas={
            'area': '0',
            'word': keyword,
            'days':'30'
        }
        get_uqi_url = 'https://index.baidu.com/api/FeedSearchApi/getFeedIndex?'+urlencode(get_uqi_parmas)
        print(headers['Cookie'])
        res = requests.get(get_uqi_url,headers=headers)

        message = json.loads(res.text)['message']
        print(message,':',keyword)
        if message == 'success':
            with open('baidusuccess.txt', 'a+', encoding='utf-8') as f:
                f.write(name)
                f.write('\n')
            uniqid = json.loads(res.text)['data']['uniqid']

            for i in json.loads(res.text)['data']['index']:
                newsindex = i['data']

            t_url = 'https://index.baidu.com/Interface/ptbk?uniqid={}'.format(uniqid)
            response = requests.get(t_url,headers=headers)
            t_p = json.loads(res.text)['data']

            now = int(time.time()) * 1000

            t = json.loads(response.text)['data']

            datas =getSign(t,newsindex).split(',')
            #print(datas)
            if datas == ['']:
                datas=[0]*30
            else:
                datas = datas

            for i,data in enumerate(datas):
                item={}
                lastday = now - 60 * 60 * 24 * (30-i) * 1000
                # print(lastday)
                last = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(lastday / 1000))
                # print(last)
                item['day'] = last.split(' ')[0]
                #print(data)
                if data=='':
                    i=0
                else:
                    i=data

                item['mediaindex'] = i
                item['keyword'] = keyword
                print(item)
                #save_csv('baidunewsindex.csv',item)
                # cursor.execute(
                #     'INSERT INTO `tbl_baiduindex` (`keyword`, `mediaindex`, `day`) VALUES (%s, %s ,%s) ON DUPLICATE KEY UPDATE mediaindex=VALUES(mediaindex)',
                #     (item['keyword'], item['mediaindex'], item['day']),
                #
                # )
                # conn.commit()
        elif 'not login' or 'request block' in message:
            with open('baidu.txt', 'a+', encoding='utf-8') as f:
                f.write(name)
                f.write('\n')
