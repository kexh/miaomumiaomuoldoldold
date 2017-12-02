# -*- coding:utf-8 -*-
'''
    @author: miaomu(2017/01/04)
'''
import os
import time
import json
import pickle
import p_conf
from PIL import Image
try:
    from StringIO import StringIO
except ImportError:
    from io import StringIO
from base.rbtRequests import RbtRequests
from base.read_n_write import (read_cookies, write_cookies)
rbt_requests = RbtRequests()


file_cookies = '../att/login_cookies.txt'
img_tdc = '../att/tdc_' + str(time.time()) + '.jpeg'




def img_save(content):
    print img_tdc
    i = Image.open(StringIO(content))
    i.save(img_tdc)
    # with open(img_tdc, 'wb') as f:
    #     for chunk in imgcontent:
    #         f.write(chunk)

class Login():
    def __init__(self):
        self.cookies = {}
        self.timeout = 120

    def login_main(self):
        '''
        将cookies保存至文件,避免每次都是需要扫二维码登录。
        :return:
        '''
        read_cookies(file_cookies)
        while self.verifyLogin() == False:
            print('Login with cookies failed... Login with QR code now...')
            self.getQR()
            addr = self.getScanState()
            if self.fetchCookiePT(addr):
                if self.fetchCookieVF():
                    if self.fetchCookiePN():
                        write_cookies(file_cookies, self.cookies)
                    else:
                        continue
                else:
                    continue
            else:
                continue

        print('Login successed...')
        return self.cookies

    def verifyLogin(self):
        if 'psessionid' in self.cookies and 'vfwebqq' in self.cookies:
            payload = {
                'vfwebqq': self.cookies['vfwebqq'],
               'clientid': 53999199,
               'psessionid': self.cookies['psessionid'],
               't': 0.1
            }
            resp = rbt_requests.get(
                url = p_conf.GET_ONLINE,
                refer = p_conf.REFERER_OL,
                cookies = self.cookies,
                params = payload,
                timeout = self.timeout
            )
            if resp.status_code == 200 and resp.json()['retcode'] == 0:
                return True
            else:
                return False

        else:
            return False

    # ok
    def getQR(self):
        payload = {'appid': '501004106',
                   'e': 0,
                   'l': 'M',
                   's': 5,
                   'd': 72,
                   'v': 4,
                   't': 0.1}

        resp = rbt_requests.get(
            url = p_conf.GET_QR,
            refer = '',
            params = payload,
            cookies = self.cookies,
            timeout = self.timeout
        )

        self.cookies.update({'qrsig': resp.cookies['qrsig']})
        img_save(resp.content)

    # ok
    def getScanState(self):
        payload = {'webqq_type': 10,
                   'remember_uin': 1,
                   'login2qq': 1,
                   'aid': 501004106,
                   'u1': 'http://w.qq.com/proxy.html?login2qq=1&webqq_type=10',
                   'ptredirect': 0,
                   'ptlang': 2052,
                   'daid': 164,
                   'from_ui': 1,
                   'pttype': 1,
                   'dumy': '',
                   'fp': 'loginerroralert',
                   'action': '0-0-157510',
                   'mibao_css': 'm_webqq',
                   't': 1,
                   'g': 1,
                   'js_type': 0,
                   'js_ver': 10143,
                   'login_sig': '',
                   'pt_randsalt': 0}
        while 1:
            time.sleep(2)
            resp = rbt_requests.get(
                url = p_conf.SCAN_STATE,
                refer = p_conf.SCAN_STATE_REFERER,
                cookies = self.cookies,
                params = payload,
                timeout = self.timeout
            )
            if resp.status_code != 200:
                print('HTTP request error...retrying...')
            else:
                if u'二维码已失效' in resp.text:
                    print('QR expired, downloading it again...')
                    self.getQR()
                if u'二维码认证中' in resp.text:
                    print('Auth ing...')
                    time.sleep(1)
                if u'二维码未失效' in resp.text:
                    print('Please scan the QR code...')
                if 'http://ptlogin4.web2.qq.com' in resp.text:
                    self.cookies['ptwebqq'] = resp.cookies['ptwebqq']
                    self.cookies['ptisp'] = resp.cookies['ptisp']
                    addr = eval(resp.text.strip()[6:-1])[2]
                    print('updated cookies and get loginAddr')
                    return addr

    def fetchCookiePT(self, addr):
        resp = rbt_requests.get(
            url = addr,
            refer = p_conf.REFERER_PT,
            cookies = self.cookies,
            timeout = self.timeout
        )
        if resp.status_code == 200 or resp.status_code == 302:
            self.cookies.update({'pt4_token': resp.history[0].cookies['pt4_token']})
            self.cookies.update({'p_skey': resp.history[0].cookies['p_skey']})
            self.cookies.update({'skey': resp.history[0].cookies['skey']})
            self.cookies.update({'p_uin': resp.history[0].cookies['p_uin']})
            self.cookies.update({'uin': resp.history[0].cookies['uin']})
            self.cookies.update({'pt2gguin': resp.history[0].cookies['pt2gguin']})
            return True
        else:
            return self.login_main()
    # ok
    def fetchCookieVF(self):
        self.cookies.pop('qrsig')
        payload = {
            'ptwebqq': self.cookies['ptwebqq'],
            'clientid': 53999199,
            'psessionid': '',
            't': 0.1
        }
        resp = rbt_requests.get(
            url = p_conf.FETCH_VF,
            refer = p_conf.REFERER_VF,
            params = payload,
            cookies = self.cookies,
            timeout = self.timeout
        )
        if resp.status_code == 200 and resp.json()['retcode'] == 0:
            self.cookies.update({'vfwebqq': resp.json()['result']['vfwebqq']})
            return True
        else:
            return False

    # ok
    def fetchCookiePN(self):
        req = {'ptwebqq': self.cookies['ptwebqq'],
               'clientid': 53999199,
               'psessionid': '',
               'status': 'online'}
        data = {'r': json.dumps(req)}
        resp = rbt_requests.post(
            url = p_conf.FETCH_PN,
            refer = p_conf.REFERER_PN,
            cookies = self.cookies,
            data = data,
            timeout = self.timeout
        )
        if resp.status_code == 200 and resp.json()['retcode'] == 0:
            self.cookies.update({'psessionid': resp.json()['result']['psessionid']})
            self.cookies.update({'uin': self.cookies['p_uin']})
            return True
        else:
            return False
# ptwebqq, psessionid)


if __name__ == '__main__':
    lg = Login()
    sth_return = lg.login_main()