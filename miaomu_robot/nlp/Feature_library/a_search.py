# -*- coding: utf-8 -*-
'''
@author: kexh
@update: 2017/12/02
'''
from miaomu_robot.util.es_op import es

def a_search(search_input):
    result_list = es.search(search_input)