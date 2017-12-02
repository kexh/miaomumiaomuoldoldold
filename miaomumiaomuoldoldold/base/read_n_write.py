# -*- coding:utf-8 -*-
import os
import pickle
import os.path
import sys
import time

'''
usage:
from read_n_write import (oex, od, oj, oif)
'''

oex = os.path.exists
oif = os.path.isfile
od = os.path.dirname
oj = os.path.join


def read_cookies(file_cookies):
    try:
        with open(file_cookies, 'rb') as f:
            cookies = pickle.load(f)
    except (IOError, EOFError):
        print "no a cookies file here"
        exit(1)



def write_cookies(file_cookies, cookies):
    try:
        with open(file_cookies, 'wb') as f:
            pickle.dump(cookies, f)
    except :
        os.mknod(file_cookies)
        with open(file_cookies, 'wb') as f:
            pickle.dump(cookies, f)


