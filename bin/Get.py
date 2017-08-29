#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@version: 001
@author: jianpan
@file: test.py
@time: 2017/6/6 22:04
"""

import urllib
import urllib.parse
import json
import pandas as pd
import time
import numpy as np
from multiprocessing import Process
import gevent.pool
from gevent import monkey;monkey.patch_all()
import time
import threading
from ProxyProvider import ProxyProvider
import pprint
import logging
import logging.config

logging.config.fileConfig("/usr/local/test/mobike_1/conf/logger.conf")
logger = logging.getLogger("example02")

class Crawler:
    def __init__(self):
        self.start_time = time.time()
        self.proxyProvider = ProxyProvider()
        self.headers = [{
                'Content-Type': 'application/x-www-form-urlencoded',
                'Host': 'api.mobike.com',
                'mobileNo': '13729009386',
                'eption': 'a7eab',
                'lang': 'zh',
                'uuid': '78c8a7eecf9ba3ef7f2bca96e59fbe4c',
                'citycode': '0755',
                'accesstoken': 'bc6066bdb5ab2bff2b9c942d0add4089'
        },
            {
'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
'Host': 'api.mobike.com',
'Accept-Encoding': 'gzip',
'platform': '1',
'eption': '99d25',
'citycode': '0755',
'os': '23',
'lang': 'zh',
'version': '5.4.1',
'uuid': '3d6bc5f57fbe14a14c846bfe7091993c'}

        ]
        self.result_success = []
        self.index = 0
        self.result_fail = []
        self.req_index = 0

    def get_nearby_bikes(self, args):
        url = 'https://api.mobike.com/mobike-api/rent/v2/nearbyBikesInfo.do'
        self.req_index +=1

        reqdata = [{
            'cityCode': '0755',
            'biketype': '0',
            'latitude': str(args[0]),
            'scope': '500',
            'sign': '68bb54c96acc635edc9fd95eb72b42a0',
            'userid': '72182150542387824640362706',
            'client_id': 'android',
            'longitude': str(args[1])
        },
            {
                'cityCode': '0755',
                                'biketype': '0',
                                            'latitude': str(args[0]),
        'scope': '500',
        'sign': '67a80df315dc26738ba002cbfa920e26',
        'client_id': 'android',
        'longitude': str(args[1])
            }
        ]
        # print(reqdata)
        i = self.req_index % 2
        data = urllib.parse.urlencode(reqdata[i]).encode('utf-8')
        self.get_request(url, self.headers[i], data, args)

    def get_request(self, url, headers, data, args):
        proxy = self.proxyProvider.pick()
        try:
            proxies = {'http': proxy.url}
            # print(proxies)
            proxy_support = urllib.request.ProxyHandler(proxies)
            opener = urllib.request.build_opener(proxy_support)
            urllib.request.install_opener(opener)
            a = urllib.request.Request(url=url, headers=headers, data=data)
            r = urllib.request.urlopen(a).read()
            tmp = json.loads(r)
            # print(tmp)
            result = pd.DataFrame.from_dict(tmp['bike'])
            self.result_success.append(result)
        except Exception as ex:
            #print(ex)
            proxy.fatal_error()
            self.result_fail.append("{0}, {1}, {2}, {3}" .format(args[0], args[1],proxy.url, ex))
        finally:
            self.index += 1
            #if self.index % 100 == 0:
            #    print(self.index)

    def gevent_fun(self,locate_list, pool_num):
        from gevent import monkey
        monkey.patch_all(socket=True, select=True)
        from gevent.pool import Pool
        gevent_pool = Pool(pool_num)
        gevent_pool.map(self.get_nearby_bikes, locate_list)

    def thread_fun(self, locate_list, pool_num):
        import threadpool
        thread_pool = threadpool.ThreadPool(pool_num)
        requestsx = threadpool.makeRequests(self.get_nearby_bikes, locate_list)
        [thread_pool.putRequest(req) for req in requestsx]
        thread_pool.wait()


    def process_start(self, locate_list, PoolNum):
        pool = gevent.pool.Pool(PoolNum)
        data_list = pool.map(self.get_nearby_bikes, locate_list)
        result = []
        for i in data_list:
            if type(i) != str:
                result.append(i)
                time.strftime()

    # def process_start(self, locate_list):
    #     for locate in locate_list:
    #         self.get_nearby_bikes(locate)

    def init_start(self, PoolNum, now):
        left = 22.55
        top = 113.80
        right = 22.85
        bottom = 114.20
        offset = 0.002
        lat_range = np.arange(left, right, offset)
        lon_range = np.arange(top, bottom, offset)
        locate_range = np.transpose([np.tile(lat_range, len(lon_range)), np.repeat(lon_range, len(lat_range))])
        print(len(locate_range))
        # self.thread_fun(locate_range, PoolNum)
        self.gevent_fun(locate_range, PoolNum)
        with open("/usr/local/test/mobike_1/data/{0}_fail.txt".format(t), 'w') as f:
            f.write('\n'.join(self.result_fail))
        pd_result = pd.concat(self.result_success)
        #pd_result = self.result_success[0]
        #for i in self.result_success:
        #    pd_result.append(i, ignore_index=True)
        print(len(self.result_fail))
        #pd_result = pd_result.drop_duplicates(['bikeIds'])
        t = time.strftime('%Y%m%d%H%M%S', now)
        print(len(pd_result))

        pd_result.to_csv('/usr/local/test/mobike_1/data/{0}_success.csv'.format(t),header=True,index=False)

if __name__ == "__main__":
    time_start = time.time()
    
    logger.info(' ####################################')
    logger.info(' ####################################')
    logger.info(' ############## START ###############')
    now = time.localtime()
    c = Crawler()
    c.init_start(40, now)
    time_end = time.time()
    print(time_end-time_start)
    logger.info(' ##############  END  ############### ')
    logger.info(' ####################################')
    logger.info(' ####################################')
