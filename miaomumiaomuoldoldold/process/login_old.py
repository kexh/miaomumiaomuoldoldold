# -*-coding:utf-8-*-
import time
import pickle
import os
import json
import old.TBot_github.TBot.src.client
import old.TBot_github.TBot.src.api
import conf


class Login(object):

    def __init__(self):
        self.httpcli = old.TBot_github.TBot.src.client.Client()
        self.cookies = {}
        self.timeout = 120

    def getQR(self):
        payload = {'appid': '501004106',
                   'e': 0,
                   'l': 'M',
                   's': 5,
                   'd': 72,
                   'v': 4,
                   't': 0.1}
        response = self.httpcli.get(uri=old.TBot_github.TBot.src.api.GET_QR, referer='', cookies={}, payload=payload, timeout=self.timeout)
        self.cookies.update({'qrsig': response.cookies['qrsig']})

        with open('s.png', 'wb') as f:
            for chunk in response.iter_content(1):
                f.write(chunk)

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
            response = self.httpcli.get(old.TBot_github.TBot.src.api.SCAN_STATE, old.TBot_github.TBot.src.api.SCAN_STATE_REFERER,
                                        self.cookies, payload, timeout=self.timeout)
            if response.status_code == 200:
                if u'二维码已失效' in response.text:
                    print('QR expired, downloading it again...')
                    self.getQR()
                if u'二维码认证中' in response.text:
                    print('Auth ing...')
                    time.sleep(1)
                if u'二维码未失效' in response.text:
                    print('Please scan the QR code...')
                if 'http://ptlogin4.web2.qq.com' in response.text:
                    loginAddr = eval(response.text.strip()[6:-1])[2]
                    # fetch ptwebqq in cookie
                    self.cookies.update({'ptwebqq': response.cookies['ptwebqq']})
                    self.cookies.update({'ptisp': response.cookies['ptisp']})
                    # self.cookies.update({'RK': response.cookies['RK']})
                    print('Login processing...')
                    return loginAddr
            else:
                print('HTTP request error...retrying...')

    def fetchCookiePT(self, addr):
        response = self.httpcli.get(addr, old.TBot_github.TBot.src.api.REFERER_PT, self.cookies, timeout=self.timeout)
        self.cookies.update({'pt4_token': response.history[0].cookies['pt4_token']})
        self.cookies.update({'p_skey': response.history[0].cookies['p_skey']})
        self.cookies.update({'skey': response.history[0].cookies['skey']})
        self.cookies.update({'p_uin': response.history[0].cookies['p_uin']})
        self.cookies.update({'uin': response.history[0].cookies['uin']})
        self.cookies.update({'pt2gguin': response.history[0].cookies['pt2gguin']})

    def fetchCookieVF(self):
        # fetch vfwebqq in result-json
        self.cookies.pop('qrsig')
        payload = {'ptwebqq': self.cookies['ptwebqq'],
                   'clientid': 53999199,
                   'psessionid': '',
                   't': 0.1}
        addr = 'http://s.web2.qq.com/api/getvfwebqq'
        response = self.httpcli.get(addr, old.TBot_github.TBot.src.api.REFERER_VF, self.cookies, payload, timeout=self.timeout)
        self.cookies.update(response.json()['result'])

    def fetchCookiePN(self):
        req = {'ptwebqq': self.cookies['ptwebqq'],
               'clientid': 53999199,
               'psessionid': '',
               'status': 'online'}
        data = {'r': json.dumps(req)}
        response = self.httpcli.post(old.TBot_github.TBot.src.api.FETCH_PN, old.TBot_github.TBot.src.api.REFERER_PN,
                                     self.cookies, data, timeout=self.timeout)
        print response.text
        self.cookies.update({'psessionid': response.json()['result']['psessionid']})
        self.cookies.update({'uin': self.cookies['p_uin']})

    def verifyLogin(self):
        if 'psessionid' in self.cookies and 'vfwebqq' in self.cookies:
            payload = {'vfwebqq': self.cookies['vfwebqq'],
                       'clientid': 53999199,
                       'psessionid': self.cookies['psessionid'],
                       't': 0.1}
            response = self.httpcli.get(old.TBot_github.TBot.src.api.GET_ONLINE, old.TBot_github.TBot.src.api.REFERER_OL,
                                        self.cookies, payload, timeout=self.timeout)
            if response.json()['retcode'] == 0:
                return True
            else:
                return False
        else:
            return False

    def run(self):
        with open(conf.file_cookies, 'rb') as f:
            self.cookies = pickle.load(f)
        while self.verifyLogin()==False:
            print('Login with cookies failed... Login with QR code now...')
            self.getQR()
            addr = self.getScanState()
            self.fetchCookiePT(addr)
            self.fetchCookieVF()
            self.fetchCookiePN()

            try:
                with open(conf.file_cookies, 'wb') as f:
                    pickle.dump(self.cookies, f)
            except FileNotFoundError:
                os.mknod(conf.file_cookies)
                with open(conf.file_cookies, 'wb') as f:
                    pickle.dump(self.cookies, f)

        print('Login with cookies successed...')
        return self.cookies


