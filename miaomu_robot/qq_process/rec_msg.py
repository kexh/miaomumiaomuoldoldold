# -*- coding:utf-8 -*-
'''
    @author: miaomu(2017/01/08)
'''

import json
import qq_process_conf
from base.req_op import RbtRequests
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
            url = qq_process_conf.URL_REC,
            refer = qq_process_conf.REFER_REC,
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