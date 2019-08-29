import requests
from lxml import etree
import json
import fake_useragent
import hashlib
import re
import random
import traceback
import time
import random


def start(url):
    times = 1

    while True:
        try:
            headers = randomUA()
            proxies = get_proxies()
            try:
                response = requests.get(url, headers=headers, proxies=proxies)
            except Exception as x:
                response = None


            if not response:
                print ('response is None')
            else:
                print (response.status_code)
                if response.status_code == 200:
                    html = etree_html(response)
                    if html:
                        return html

            if times == 1:
                time.sleep(1)
            elif times > 1 and times <= 5:
                time.sleep(2)
            elif times > 5 and times <=20:
                time.sleep(10)
            elif times > 20:
                print('retry 20 times, break!')
                return None

            print('try times:%d'%times)
            times += 1
        except Exception as x:
            err = traceback.format_exc()
            print (err)

def get_proxies():
    if random.randint(1,2)==1:
        proxyUser="H8S586W474G3005D"
        proxyPass="F516EB80A1F0EC9F"

    else:
        proxyUser = "H3MEE66JK209K76D"
        proxyPass = "E5A0C876B366FC47"
    proxies=randomproxies(proxyUser,proxyPass)
    print(proxies)
    return proxies



def lxml_to_string(data):
    data = etree.tostring(data, encoding='utf-8')
    data = str(data, encoding='utf-8')
    return data

def randomproxies(proxyUser,proxyPass):
    # 代理服务器
    # 代理服务器
    proxyHost = "http-dyn.abuyun.com"
    proxyPort = "9020"

    # 代理隧道验证信息
    proxyUser = proxyUser
    proxyPass = proxyPass

    proxyMeta = "http://%(user)s:%(pass)s@%(host)s:%(port)s" % {
        "host": proxyHost,
        "port": proxyPort,
        "user": proxyUser,
        "pass": proxyPass,
    }


    proxies = {
        "http": proxyMeta,
        "https": proxyMeta,

    }
    return proxies

def randomUA():
    ua=fake_useragent.FakeUserAgent()
    headers={
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Cache-Control': 'ax-age=0',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent':ua.random}
    print(headers)
    return headers


def etree_html(response):
    try:
        html = response.text
        html = etree.HTML(html)
        return html
    except Exception as x:
        err =  traceback.format_exc()
        print(err)
        return None


def md5(data):
    data=hashlib.md5(data.encode(encoding='UTF-8')).hexdigest()
    return data



def download_img(url,name):
    response=requests.get(url)
    img=response.content
    path='./img/{}.jpg'.format(name)
    with open(path,'wb') as f:
        f.write(img)
    return path



def send_post(url,data,headers):
    # headers=randomUA_phases()
    try:
        times=0
        while True:
            # proxies = get_proxies()
            response=requests.post(url=url,data=data,headers=headers)
            print(response.status_code)
            print(response.raise_for_status())
            if response.status_code==200:
                return response
            else:
                time.sleep(1)
            times+=1
            print('第%s次请求'%times)

            if times==30:
                print('请求30次，break!')
                return None
    except Exception as x:
        err = traceback.format_exc()
        print(err)
