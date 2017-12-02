# -*- coding:utf-8 -*-
'''
    @author: miaomu(2017/01/08)
'''

import json
import p_conf
from base.rbtRequests import RbtRequests
rbt_requests = RbtRequests()

class RecMsg():
    def __init__(self, cookies):
        self.cookies = cookies
        self.timeout = 120

    def rec_msg(self):
        req = {
            "ptwebqq": self.cookies['ptwebqq'],
            "clientid": 53999199,
            "psessionid": self.cookies['psessionid'],
            "key": ""
        }
        data = {'r': json.dumps(req)}
        resp = rbt_requests.post(
            url = p_conf.URL_REC,
            refer = p_conf.REFER_REC,
            cookies = self.cookies,
            data = data,
            timeout = self.timeout
        )
        if resp.status_code == 200:
            msg = resp.json()['result'][0]['value']['content']#[1]
            return msg
        else:#ReadTimeout
            return None

if __name__ == '__main__':
    r = RecMsg()
    while True:
        msg = r.rec_msg()
        if msg != None:
            print msg