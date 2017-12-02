# -*- coding:utf-8 -*-
'''
    @author: miaomu(2017/01/08)
'''
import json
import qq_process_conf
from base.req_op import RbtRequests
rbt_requests = RbtRequests()

class SendMsg():
    def __init__(self, cookies):
        self.cookies = cookies
        self.timeout = 120

    def send_msg(self, user_id, msg):
        req = {
            "to": 'user_id',
            "content": [
                msg,
                [
                    "font",
                    {
                        "name": "宋体",
                        "size": 10,
                        "style": [
                            0,
                            0,
                            0
                        ],
                        "color": "000000"
                    }
                ]
            ].to_string(),
            "face": 522,
            "clientid": 53999199,
            "msg_id": 65890001,
            "psessionid": self.cookies['psessionid']
        }
        data = {'r': json.dumps(req)}
        print data
        resp = rbt_requests.post(
            url = qq_process_conf.URL_SEND,
            refer = qq_process_conf.REFER_SEND,
            cookies = self.cookies,
            data = data,
            timeout = self.timeout
        )
        if resp.status_code == 200 and resp.json()['errCode'] == 0:
            print "send ok"
            return True
        else:
            return False

if __name__ == '__main__':
    cookies = ''
    user_id = None
    msg = ''
    s = SendMsg(cookies)
    if s.send_msg(user_id, msg):
        print 'hahaha'
