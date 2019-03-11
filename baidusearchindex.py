import csv
import random
import time
from urllib.parse import urlencode

import execjs
import pymysql
import requests
import json
import re

from Cookies import COOKIES


def get_index(name):
        headers = {
            'Host': 'index.baidu.com',
            #'Connection': 'keep-alive',
            #'X-Requested-With': 'XMLHttpRequest',
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36',
            'Cookie': random.choice(COOKIES)
        }
        #proxies = {"http": "{}".format(proxy), "https": "{}".format(proxy)}
        #print(proxies)

        time.sleep(random.randint(2,3))
        if name:
            keyword = str(name).strip().strip('\t')
            keyword = name.strip()
            print('keyword:',keyword)
            get_uqi_parmas={
                'area': '0',
                'word': keyword,
                'days':'30'
            }
            get_uqi_url ='https://index.baidu.com/api/SearchApi/index?'+urlencode(get_uqi_parmas)
            #print(get_uqi_url)
            res = requests.get(get_uqi_url,headers=headers)
            #print(res.text)
            try:
                uniqid = json.loads(res.text)['data']['uniqid']
                #print('uniqid:',uniqid)
                #print(res.text)
                for info in  json.loads(res.text)['data']['userIndexes']:
                    all_e = info['all']['data']
                    pc_e =info['pc']['data']
                    mobile_e=info['wise']['data']
                print('all_e:',all_e)
                t_url = 'https://index.baidu.com/Interface/ptbk?uniqid={}'.format(uniqid)
                res = requests.get(t_url,headers=headers)
                t_p = json.loads(res.text)['data']
                print('t_p:',t_p)
                data =getSign(t_p,all_e).split(',')
                data2 =getSign(t_p,pc_e).split(',')
                data3 =getSign(t_p,mobile_e).split(',')

                now = int(time.time()) * 1000

                for i,(total,pc,mobile) in enumerate(zip(data,data2,data3)):
                    item={}
                    item['total'] = fullnull(total)
                    item['pc'] =fullnull(pc)
                    item['mobile'] =fullnull(mobile)
                    item['keyword'] = keyword
                    lastday = now - 60 * 60 * 24 * (30-i) * 1000
                    # print(lastday)
                    last = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(lastday / 1000))
                    # print(last)
                    item['day'] = last.split(' ')[0]
                    print(item)
                #print('耗时：',time.time()*1000-start_time)
                    #save_csv('baiduindex.csv', item)
                    # cursor.execute('replace into tbl_baiduindex(keyword, total,mobile,pc, day) values(%s,%s,%s,%s,%s)',
                    #                (item['keyword'], item['total'], item['mobile'], item['pc'], item['day']))
                    # conn.commit()
            except Exception as e:
                print(e)
                with open('baiduindexmiss.txt', 'a+', encoding='utf-8') as f:
                    f.write(keyword)
                    f.write('\n')

if __name__ == '__main__':

    def getSign(key, data):
        a = {}
        r = []
        for i in range(len(key) // 2):
            a[key[i]] = key[len(key) // 2 + i]
        for j in range(len(data)):
            r.append(a[data[j]])
        return ''.join(r)
    def fullnull(s):
        if s:
            data=s
        else:
            data=0
        return data


    def save_csv(filename, data):
        with open(filename, 'a', newline='', errors='ignore', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(data.values())


    # conn = pymysql.connect(
    #         user='********',
    #         passwd='****',
    #         db='newmedia_db',
    #         host='*********',
    #         charset="utf8",
    #         use_unicode=True
    #     )
    # cursor = conn.cursor()

    t_url = 'https://index.baidu.com/Interface/ptbk?uniqid={}'
    get_uqi = 'https://index.baidu.com/api/FeedSearchApi/getFeedIndex?'
    with open(r'D:\Projects\myspiders\demo\keyword.txt', 'r',
              encoding='utf-8') as f:
        keywords = f.readlines()
    # cursor.execute("SELECT keyword FROM `tbl_baiduindex` WHERE `day`='2019-01-27' AND keyword not in (SELECT `keyword` FROM tbl_baiduindex WHERE `day`='2019-02-12');")
    # keywords = cursor.fetchall()
    # print(keywords)

    start_time = time.time()*1000
    count = 0
    for name in keywords:
        get_index(name)