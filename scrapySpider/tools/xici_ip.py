#!/usr/bin/env python3
# -*- encoding: utf-8 -*-
'''
@File : xici_ip.py
@Time : 2019/04/16 14:27:02
@Author : FanZehua
@Version : 1.0
@Contact : 316679581@qq.com
@License : (C)Copyright 2017-2018, Liugroup-NLPR-CASIA
@Desc : None
'''

# here put the import lib
import requests
from scrapy.selector import Selector
import pymongo
from scrapy.conf import settings
import random

client = pymongo.MongoClient(
    host=settings['MONGO_HOST'], port=settings['MONGO_PORT'])
db = client[settings['MONGO_DB']]  # 获得数据库句柄
coll = db['ip_pool']  # 获得collection的句柄
# 数据库登录需要密码
db.authenticate(settings['MONGO_USER'], settings['MONGO_PSW'])


def crawl_ips():
    headers = {
        'User-Agent':
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36',
    }
    for i in range(10)[1:]:
        re = requests.get(
            'https://www.xicidaili.com/nn/{0}'.format(i), headers=headers)

        selector = Selector(text=re.text)
        all_trs = selector.css('#ip_list tr')

        ip_list = []
        for tr in all_trs[1:]:
            speed_str = tr.css('.bar::attr(title)').extract_first()
            if speed_str:
                speed = float(speed_str.split('秒')[0])
            all_texts = tr.css('td::text').extract()
            ip = all_texts[0]
            port = all_texts[1]
            proxy_type = all_texts[5]

            ip_list.append((ip, port, proxy_type, speed))
            for ip_info in ip_list:
                ip_dict = dict(
                    ip=ip_info[0],
                    port=ip_info[1],
                    proxy_type=ip_info[2],
                    speed=ip_info[3])
                coll.save(ip_dict)


class GetIP(object):

    def delete_ip(self, ip):
        # 从数据库中删除无效ip
        coll.delete_one({'ip': ip})
        return True

    def judge_ip(self, ip, port, proxy_type):
        # 判断ip是否可用
        http_url = 'http://www.baidu.com'
        proxy_url = '{2}://{0}:{1}'.format(ip, port, proxy_type)
        proxy_dict = {proxy_type: proxy_url}
        try:
            response = requests.get(http_url, proxies=proxy_dict)
        except Exception:
            print('invalid ip and port')
            self.delete_ip(ip)
            return False
        else:
            code = response.status_code
            if code <= 200 and code < 300:
                print('effective ip')
                return True
            else:
                print('invalid ip and port')
                self.delete_ip(ip)
                return False

    def get_random_ip(self):
        # 从数据库中随机获取一个可用的ip
        ip_list = coll.find()
        ip_list_count = coll.find().count()
        ip_info = ip_list[random.randint(0, ip_list_count - 1)]
        if self.judge_ip(ip_info['ip'], ip_info['port'], ip_info['proxy_type']):
            return '{2}://{0}:{1}'.format(ip_info['ip'], ip_info['port'],
                                          ip_info['proxy_type'])
        else:
            return self.get_random_ip()


# print(GetIP().get_random_ip())
if __name__ == "__main__":
    get_ip = GetIP()
    get_ip.get_random_ip()
