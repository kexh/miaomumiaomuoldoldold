# -*- coding:utf-8 -*-
import requests

# **kwargs默认有refer，url，cookies等key，是不好的，要加判断。
# headers里头可能会有多个值要添加。所以可以对key做是否包含headers的判断。

class RbtRequests():
    # http://music.163.com/#/search/m/?s=%E7%9B%B4%E8%A7%89&type=1
    # post,可以在浏览器被反复访问
    def __init__(self):
        self.userAgent = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.82 Safari/537.36'

    def get(self, **kwargs):
        if ('url' and 'cookies' in kwargs) and (('headers' in kwargs) or ('refer' in kwargs)) == False:
            raise(u'参数不完全')
        if 'headers' in kwargs:
            headers = kwargs['headers']
        else:
            headers = {'User-Agent': self.userAgent, 'Referer': kwargs['refer']}
        url = kwargs['url']
        cookies = kwargs['cookies']
        if kwargs.has_key('timeout'):
            timeout = kwargs['timeout']
        else:
            timeout = 120
        if kwargs.has_key('params'):
            params = kwargs['params']
            resp = requests.get(
                url = url,
                headers = headers,
                params = params,
                cookies = cookies,
                timeout = timeout
            )
        else:
            resp = requests.get(
                url = url,
                headers = headers,
                cookies = cookies,
                timeout = timeout
            )
        return resp

    def post(self, **kwargs):
        if ('url' and 'cookies' in kwargs) and (('headers' in kwargs) or ('refer' in kwargs)) == False:
            raise(u'参数不完全')
        if 'headers' in kwargs:
            headers = kwargs['headers']
        else:
            headers = {'User-Agent': self.userAgent, 'Referer': kwargs['refer']}
        url = kwargs['url']
        cookies = kwargs['cookies']
        if kwargs.has_key('timeout'):
            timeout = kwargs['timeout']
        else:
            timeout = 120
        data = kwargs['data']
        print url
        print headers
        print data
        print cookies
        print timeout
        resp = requests.post(
            url = url,
            headers = headers,
            data = data,
            cookies = cookies,
            timeout = timeout
        )
        return resp


if __name__ == '__main__':
    rbt_requests = RbtRequests()