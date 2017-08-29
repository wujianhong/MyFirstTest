#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@version: 001
@author: jianpan
@file: ProxyProvider.py
@time: 2017/6/11 17:17
"""
import random
import threading
import requests
import pprint
import json
from Proxy import Proxy
class ProxyProvider:
    def __init__(self, min_proxies=200):
        self._bad_proxies = {}
        self._minProxies = min_proxies
        self.lock = threading.RLock()
        self.get_list()
        self.index = 0
        #print(self._proxies)

    def get_list(self):
        # r = requests.get("https://jsonblob.com/api/jsonBlob/31bf2dc8-00e6-11e7-a0ba-e39b7fdbe78b", timeout=10)
        # proxies = json.loads(r.text)
        with open('/usr/local/mobike/conf/data2', 'r') as f:
            result = f.readlines()
            result = map(lambda x: "http://"+x.strip(),result)
            proxies = result
        self._proxies = list(map(lambda p: Proxy(p), proxies))

    def remove_proxy(self, url):
        self._proxies.remove(Proxy(url))

    def pick(self):
        # pprint.pprint(self._proxies)
        with self.lock:
            #self._proxies.sort(key=lambda p: p.score, reverse=True)
            #proxy_len = len(self._proxies)
            #max_range = 50 if proxy_len < 50 else proxy_len
            #proxy = self._proxies[random.randrange(1, max_range)]
            if self.index < len(self._proxies):
                proxy = self._proxies[self.index]
            else:
                self.index = 0
                proxy = self._proxies[0]
            self.index += 1
            proxy.used()
            return proxy

if __name__ == "__main__":
    pro = ProxyProvider()
    r = []
    for i in range(800):
        res = pro.pick()
        print(res.url)
        r.append(res.url)
    print("==========================")
    print(len(set(r)))

