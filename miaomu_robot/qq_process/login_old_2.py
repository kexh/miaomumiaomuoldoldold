# -*- coding:utf-8 -*-

from __future__ import unicode_literals
import os
import json
import base64
import binascii
from Crypto.Cipher import AES
# from base import read_n_write
from util import req_op# import RbtRequests
rbt_requests = req_op.RbtRequests()
file_cookies = '../att/necm_login_cookies.txt'
file_html = '../att/necm_search_result.html'
file_html_2 = '../att/necm_search_result_2.html'
default_timeout = 10

# def for_cookies():
#     url = 'http://music.163.com/'
#     headers = {
#         'Host': 'music.163.com',
#         'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:50.0) Gecko/20100101 Firefox/50.0',
#
#     }

# def for_search_page():
#     url = 'http://music.163.com/search/'
#     headers = {
#         'Referer': 'http://music.163.com/',
#         'Host': 'music.163.com'
#     }

# ********************************** RSA in NeCM ******************************************
modulus = ('00e0b509f6259df8642dbc35662901477df22677ec152b5ff68ace615bb7'
           'b725152b3ab17a876aea8a5aa76d2e417629ec4ee341f56135fccf695280'
           '104e0312ecbda92557c93870114af6c9d05c4f7f0c3685b7a46bee255932'
           '575cce10b424d813cfe4875d3e82047b97ddef52741d546b8e289dc6935b'
           '3ece0462db0a22b8e7')
nonce = '0CoJUm6Qyw8W8jud'
pubKey = '010001'

def createSecretKey(size):
    r = os.urandom(size)
    return binascii.hexlify(r)[:16]

def aesEncrypt(text, secKey):
    pad = 16 - len(text) % 16
    text = text + chr(pad) * pad
    encryptor = AES.new(secKey, 2, '0102030405060708')
    ciphertext = encryptor.encrypt(text)
    ciphertext = base64.b64encode(ciphertext).decode('utf-8')
    return ciphertext

def rsaEncrypt(text, pubKey, modulus):
    # secKey is text here.
    text = text[::-1]
    rs = pow(int(binascii.hexlify(text), 16), int(pubKey, 16)) % int(modulus, 16)
    return format(rs, 'x').zfill(256)

# 加密算法, 基于https://github.com/stkevintan/nw_musicbox脚本实现
def encrypted_request(text):
    text = json.dumps(text)
    secKey = createSecretKey(16)
    encText = aesEncrypt(aesEncrypt(text, nonce), secKey)
    encSecKey = rsaEncrypt(secKey, pubKey, modulus)
    data = {'params': encText, 'encSecKey': encSecKey}
    return data

# ZaKUGSPB93apS4BtZTHUkzICClCep5cYiqFCpt6HnfkR6aQ7aPiKBtiz+/SpFABitTFowtkVuqRHqSjf7ERg9qEHgq2XQ5W3KvU8Uf/ihrIUqddpavSbKbV6LDM71a7EdyChrK7LM7e/Lt+NhUBZRMfgNcxILw02+newOAH//yr8JA26bC5Vy5cyYxxZvF3jZ4LvL/qQD2X0U+ctNKLcmm/hYe+OSxCSB5njPTlbDjdyfJrTvew1MJQLepBMr/+Lc/fJAPCrZJQ85EGfdz7fTg==
# 8UDT88z6Jl0g1ATUxdu7S20KeOThKXvtK1PLBM45gP/aYQ5Gf1mFYIN5le+9coXtkI318cn9qZVO5TR95CHoQqrlHPBfYx4CjGU13ncdNMyAiOcXX95enHQWaJ0wHSfMFkFofPYwstsiuAuN+3buI31Je9KAI/e3nQE7s7VbYKBKO7u09raUEQXvbLlZYYPxKuswLWqATXqfwW4m8qfh88rGAjdvfJ288HZHL2UP39f31AC6mnfqZvUyZ+2BStRNJxhsEn0KKOjU+AmLx5dHPw==
# 3980ce75945fabd6de0c448776895441bcdd26c9bfda8dfd422f632424c3fa98b450a3abdc23229ba0d2e9241daa79e8340625eb6db8e9146d9dfafef97e19d3ded8b84ea825ddfe709fa2acf87d8c4c1c9231695a8d2f80d2c6ac5845a9402332ce34a2113f442002f82b9ef940f9ad8c113b21dc9dbf700cd2719b994c521c
# bf7712a9c02026ad825430c73c96defba29853c0a8e669847429d97ef21b59a05fa3c33770265ae2430738359b1272b14f848c1484a8f2274f372fac83c9d1caa2836824330241d2a1946b90a1df898623ea572115563c98db8ee2c59b60174bbe5a4d4275ba84fe7d605cc9e25e96763960b14e0988007689111d925da87a7e


# 89af5de8ac8bc48a
# a8992d1a6be0fcf7751c235390959cab54e2123593e75978f3feca1867084048e62b9a4f1f7b3bf136e2753488ff594c7646740171f713fc38db85a769605a986965cf5783b5510b988aaaa02488429ce43f4353c9798d1a2273dea074961fd4768f9406472ed11f4bf211fe0c59cadb81b102a470550a32b624dec112eeddc6




# ***************************************************************************************************


# # 歌曲加密算法, 基于https://github.com/yanunon/NeteaseCloudMusic脚本实现
# def encrypted_id(id):
#     magic = bytearray('3go8&$8*3*3h0k(2)2', 'u8')
#     song_id = bytearray(id, 'u8')
#     magic_len = len(magic)
#     for i, sid in enumerate(song_id):
#         song_id[i] = sid ^ magic[i % magic_len]
#     m = hashlib.md5(song_id)
#     result = m.digest()
#     result = base64.b64encode(result)
#     result = result.replace(b'/', b'_')
#     result = result.replace(b'+', b'-')
#     return result.decode('utf-8')


class NeCMusic(object):
    def __init__(self):
        self.headers = {
            'Accept': '*/*',
            # 'Accept-Encoding': 'gzip,deflate,sdch',
            'Accept-Language': 'zh-CN,zh;q=0.8,gl;q=0.6,zh-TW;q=0.4',
            'Connection': 'keep-alive',
            'Referer': 'http://music.163.com/search/',
            'Content-Type': 'application/x-www-form-urlencoded',
            'Host': 'music.163.com'
        }
        # self.cookies = {'appver': '1.5.2'}
        self.cookies = {}

    def get_search_result(self, data):
        # action = 'https://music.163.com/weapi/login/'
        # query=None, urlencoded=None, callback=None
        # # song -- > resp.content.json()['program']['mainSong']
        # if song['hMusic'] and quality <= 0:
        #     music = song['hMusic']
        #     quality = 'HD'
        # elif song['mMusic'] and quality <= 1:
        #     music = song['mMusic']
        #     quality = 'MD'
        # elif song['lMusic'] and quality <= 2:
        #     music = song['lMusic']
        # song_id = str(music['dfsId'])
        # enc_id = encrypted_id(song_id)


        # 'http://music.163.com/api/search/get'
        url = 'http://music.163.com/weapi/search/suggest/web?csrf_token='
              # % (random.randrange(1, 3),
              #                                         enc_id, song_id)
        # data = {
        #     # 'params': '',
        #     # 'encSecKey': ''
        # }
        # data = encrypted_request(text)
        resp = rbt_requests.post(
            url = url,
            data = data,
            headers = self.headers,
            cookies = self.cookies
        )
        if resp.status_code != 200:
            raise('HTTP request error...')
        else:
            print resp.content
            try:
                with open(file_html, 'wb') as f:
                    f.write(resp.content)
                return resp.json()
            except:
                raise('save error...')

    def get_query(self, j_content):
        result_list = j_content["result"]["albums"]
        return result_list

    def for_lyc(self, result_query):
        # os=osx&id={}&lv=-1&kv=-1&tv=-1
    # lyric http://music.163.com/api/song/lyric?os=osx&id= &lv=-1&kv=-1&tv=-1
        data = encrypted_request(result_query)
        url = 'http://music.163.com/weapi/song/lyric?csrf_token='##?
        self.headers['Referer']= 'http://music.163.com/song?id=' + result_query['id']
        resp = rbt_requests.post(
            url = url,
            data = data,
            headers = self.headers,
            cookies = self.cookies
        )
        if resp.status_code != 200:
            raise('HTTP request error...')
        else:
            print resp.content
            try:
                with open(file_html_2, 'wb') as f:
                    f.write(resp.content)
                return resp.json()
            except:
                raise

def main(text):
    data = encrypted_request(text)
    ncm = NeCMusic()
    j_content = ncm.get_search_result(data)
    result_list = ncm.get_query(j_content)
    for i in result_list:
        result_query = {}
        result_query['id'] = i['id']
        result_query['name'] = i['name']
        result_query['publishTime'] = i['publishTime']
        result_query['copyrightId'] = i['copyrightId']
        lyc_content = ncm.for_lyc(result_query)

if __name__ == '__main__':
    '''
    1. line 368.
    2. 在不同的请求下会有不同的值。这里我只列出它在登录时的值。
    const bl = {
        username: '帐号',
        password: crypto.createHash('md5').update('密码').digest('hex'),
        rememberLogin: true,
        csrf_token: ''
    }
    '''
    query = {
        's': u'开心',
        'type': 1,#song_name(1)，artist_name(100)，albums_name(10)，search_playlist(1000)，用户(1002)
        'offset': 0,
        'total': 'true',
        'limit': 60
             }
    main(query)
