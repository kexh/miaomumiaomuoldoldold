# -*- coding:utf-8 -*-

from __future__ import unicode_literals

'''
每个点大概做两天，在此之前最好先把接口调通。
【输入】string
【需求】
1. 根据string_1获取对应爬虫结果，目前数据源网站包括以下几个：
http://music.163.com/#/search/
http://music.baidu.com/
2. 根据string_2获取本地数据库结果：数据库计划包括以下几个库：
唐宋诗词，元曲，文学名著中的名句or简介。
3. 根据string_3做自然语言处理，并将解析结果传入相关查询算法，
再获取数据库结果；另外，需要调取学习算法，将string_3做学习，存入数据库。
这两个可能是不同的数据库，因为语料库cropus数据库其实是“标签”or“value”分类用的数据库；
返回结果的数据库则是包含完整语义和信息的数据库，除非有算法将“标签”和“value”转成句子。
【输出】string

'''

if __name__ == '_main__':
    pass