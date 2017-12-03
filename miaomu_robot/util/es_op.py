# -*- coding: utf-8 -*-
'''
@author: kexh
@update: 2017/12/02
'''
import time
import random
import datetime
from elasticsearch.helpers import bulk
from elasticsearch import Elasticsearch
from miaomu_robot.main_conf import *

class ES():
    # http://elasticsearch-py.readthedocs.io/en/master/api.html
    # http://blog.csdn.net/mydeman/article/details/54808267
    # https://www.elastic.co/guide/cn/elasticsearch/guide/cn/denormalization.html
    def __init__(self):
        self._es = Elasticsearch(es_host)

    def exists_or_create(self):
        if self._es.indices.exists(index=es_index) is not True:
            self._es.indices.create(index=es_index, body=es_index_mapping)

    def _index(self):
        input_data = {
                "title": "上海滩",
                "singer": "周润发",
                "lyric": " 浪奔 浪流 万里涛涛江水永不休 淘尽了世间事 混作滔滔一片潮流 是喜 是愁 浪里分不清欢笑悲忧 成功 失败 浪里看不出有未有 爱你恨你问君知否 似大江一发不收 转千弯转千滩 亦未平复此中争斗 又有喜又有愁 就算分不清欢笑悲忧 仍愿翻百千浪 在我心中起伏够 爱你恨你问君知否 似大江一发不收 转千弯转千滩 亦未平复此中争斗 又有喜又有愁 就算分不清欢笑悲忧 仍愿翻百千浪 在我心中起伏够 仍愿翻百千浪 在我心中起伏够"
                }
        _inputed = self._es.index(index=es_index, doc_type=es_type, refresh=True, body=input_data)
        # {u'_type': u'1202_type', u'created': True, u'_shards': {u'successful': 1, u'failed': 0, u'total': 2}, u'_version': 1, u'_index': u'1202_index', u'_id': u'AWAZ7HTOYvR6BEYHUVSe'}
        print (_inputed)

    def _bulk(self):
        # package = []
        # for i in range(10):
        #     row = {
        #         "@timestamp": time.strftime("%Y-%m-%dT%H:%M:%S.000+0800"),
        #         "http_code": "404",
        #         "count": random.randint(1, 100)
        #     }
        #     package.append(row)
        #
        # actions = [
        #     {
        #         '_op_type': 'index',
        #         '_index': "http_code",
        #     '_type': "error_code",
        # '_source': d
        # }
        # for d in package
        # ]
        # body = [
        #     {
        #         "title": "上海滩",
        #         "singer": "周润发",
        #         "lyric": " 浪奔 浪流 万里涛涛江水永不休 淘尽了世间事 混作滔滔一片潮流 是喜 是愁 浪里分不清欢笑悲忧 成功 失败 浪里看不出有未有 爱你恨你问君知否 似大江一发不收 转千弯转千滩 亦未平复此中争斗 又有喜又有愁 就算分不清欢笑悲忧 仍愿翻百千浪 在我心中起伏够 爱你恨你问君知否 似大江一发不收 转千弯转千滩 亦未平复此中争斗 又有喜又有愁 就算分不清欢笑悲忧 仍愿翻百千浪 在我心中起伏够 仍愿翻百千浪 在我心中起伏够"
        #     },
        #     {
        #         "title": "上海滩",
        #         "singer": "周润发",
        #         "lyric": " 浪奔 浪流 万里涛涛江水永不休 淘尽了世间事 混作滔滔一片潮流 是喜 是愁 浪里分不清欢笑悲忧 成功 失败 浪里看不出有未有 爱你恨你问君知否 似大江一发不收 转千弯转千滩 亦未平复此中争斗 又有喜又有愁 就算分不清欢笑悲忧 仍愿翻百千浪 在我心中起伏够 爱你恨你问君知否 似大江一发不收 转千弯转千滩 亦未平复此中争斗 又有喜又有愁 就算分不清欢笑悲忧 仍愿翻百千浪 在我心中起伏够 仍愿翻百千浪 在我心中起伏够"
        #     }
        # ]
        actions = { '_index': es_index, '_type': es_type, '_id': 42, '_parent': 5, '_ttl': '1d', '_source': { "title": "Hello World!", "body": "..." }}


# { "field1" : "value1" }'''

        bulk(client=self._es, actions=actions, index=es_index, doc_type=es_type)


    def _search(self):
        print('Search all...')
        _query_all = {
            'query': {
                'match_all': {}
            }
        }
        _searched = self._es.search(index=es_index, doc_type=es_type, body=_query_all)
        # u'_index': u'1202_index'}], u'total': 26, u'max_score': 1.0}, u'_shards': {u'successful': 5, u'failed': 0, u'total': 5}, u'took': 6, u'timed_out': False}{u'singer': u'\u540e\u6d77\u5927\u9ca8\u9c7c', u'lyric': u' \u68a6\u662f\u4ec0\u4e48 \u662f\u767d\u8272\u7684\u6ce1\u6cab \u662f\u5564\u9152\u82b1\u91cc\u6211\u4eec\u5410\u51fa\u7684\u91ce\u9a6c \u5e26\u6211\u5728\u8fd9\u4e16\u754c \u95ea\u7535\u822c\u7684\u5954\u8dd1 \u6211\u4eec\u50cf\u91ce\u9a6c\u4e00\u6837\u5728\u8fd9\u4e16\u754c\u4e0a \u4f60\u770b\u5230\u4e86\u4ec0\u4e48 \u57288 \u82f1\u91cc\u7684\u7a7a\u4e2d \u653e\u6d6a\u7684\u65f6\u5149\u603b\u663e\u5306\u5fd9 \u7231\u53ea\u6c38\u6052\u5728\u7535\u89c6\u4e0a \u4ecd\u7136\u653e\u4efb\u81ea\u6d41 \u52c7\u6562\u5230\u6ca1\u6709\u4e86\u65b9\u5411 \u52c7\u6562\u7684\u50cf\u4e00\u53ea\u91ce\u9a6c \u5b83\u6b63\u5728\u95ea\u95ea\u53d1\u5149 \u6211\u4eec\u50cf\u53ea\u91ce\u9a6c\u4e00\u6837\u5728\u8fd9\u57ce\u5e02\u91cc\u6d41\u6dcc \u6d6a\u8d39\u4e86\u592a\u9633\u4e5f\u4ece\u4e0d\u611f\u5230\u60b2\u4f24 \u6211\u4eec\u50cf\u53ea\u91ce\u9a6c\u4e00\u6837\u5728\u57ce\u5e02\u91cc\u6d41\u6dcc \u6d6a\u8d39\u4e86\u592a\u9633\u4e5f\u4ece\u4e0d\u4f1a\u611f\u5230\u60b2\u4f24 \u4f60\u8fd8\u8bb0\u5f97\u4ec0\u4e48 \u5f53\u4e00\u4e2a\u4eba\u5728\u8857\u4e0a\u9192\u6765 \u770b\u72c2\u559c\u7684\u592a\u9633\u4ece\u5929\u9645\u7ebf\u5347\u8d77 \u4f60\u77e5\u9053\u53c8\u662f\u4f60\u81ea\u5df1 \u5f53\u4f60\u4e00\u65e0\u6240\u6709\u65f6 \u518d\u4e5f\u4e0d\u5fc5\u611f\u5230\u5bb3\u6015 \u5410\u51fa\u7684\u90a3\u4e00\u53ea\u91ce\u9a6c \u5728\u8fd9\u4e16\u754c\u4e0a \u6211\u4eec\u50cf\u53ea\u91ce\u9a6c\u4e00\u6837\u5728\u8fd9\u57ce\u5e02\u91cc\u6d41\u6dcc \u6d6a\u8d39\u4e86\u592a\u9633\u4e5f\u4ece\u4e0d\u611f\u5230\u60b2\u4f24 \u6211\u4eec\u50cf\u53ea\u91ce\u9a6c\u4e00\u6837\u5728\u8fd9\u57ce\u5e02\u91cc\u6d41\u6dcc \u591a\u5e0c\u671b\u770b\u5230\u4e0d\u4e00\u6837\u7684\u660e\u5929', u'title': u'\u731b\u72b8'}
        print(_searched)

        # 输出查询到的结果
        for hit in _searched['hits']['hits']:
            # {u'singer': u'\u8c22\u6625\u82b1', u'lyric': u' \u4f5c\u66f2 : \u8c22\u77e5\u975e \u4f5c\u8bcd : \u8c22\u77e5\u975e/\u9526\u5c4f \u7f16\u66f2/\u6df7\u97f3\uff1a\u5c0f\u76ae \u5409\u4ed6 : \u5362\u5c71/\u5c0f\u76ae \u501f\u6211\u5341\u5e74 \u501f\u6211\u4ea1\u547d\u5929\u6daf\u7684\u52c7\u6562 \u501f\u6211\u8bf4\u5f97\u51fa\u53e3\u7684\u65e6\u65e6\u8a93\u8a00 \u501f\u6211\u5b64\u7edd\u5982\u521d\u89c1 \u501f\u6211\u4e0d\u60e7\u78be\u538b\u7684\u9c9c\u6d3b \u501f\u6211\u751f\u731b\u4e0e\u83bd\u649e\u4e0d\u95ee\u660e\u5929 \u501f\u6211\u4e00\u675f\u5149\u7167\u4eae\u9eef\u6de1 \u501f\u6211\u7b11\u989c\u707f\u70c2\u5982\u6625\u5929 \u501f\u6211\u6740\u6b7b\u5eb8\u788c\u7684\u60c5\u6000 \u501f\u6211\u7eb5\u5bb9\u7684\u60b2\u6006\u4e0e\u54ed\u558a \u501f\u6211\u6026\u7136\u5fc3\u52a8\u5982\u5f80\u6614 \u501f\u6211\u5b89\u9002\u7684\u6e05\u6668\u4e0e\u508d\u665a \u9759\u770b\u5149\u9634\u834f\u82d2 \u501f\u6211\u5591\u54d1\u65e0\u8a00 \u4e0d\u7ba1\u4e0d\u987e\u4e0d\u95ee\u4e0d\u8bf4 \u4e5f\u4e0d\u5ff5 \u9759\u770b\u5149\u9634\u834f\u82d2 \u501f\u6211\u5591\u54d1\u65e0\u8a00 \u4e0d\u7ba1\u4e0d\u987e\u4e0d\u95ee\u4e0d\u8bf4 \u4e5f\u4e0d\u5ff5 \u501f\u6211\u5341\u5e74 \u501f\u6211\u4ea1\u547d\u5929\u6daf\u7684\u52c7\u6562 \u501f\u6211\u8bf4\u5f97\u51fa\u53e3\u7684\u65e6\u65e6\u8a93\u8a00 \u501f\u6211\u5b64\u7edd\u5982\u521d\u89c1 \u501f\u6211\u4e0d\u60e7\u78be\u538b\u7684\u9c9c\u6d3b \u501f\u6211\u751f\u731b\u4e0e\u83bd\u649e\u4e0d\u95ee\u660e\u5929 \u501f\u6211\u4e00\u675f\u5149\u7167\u4eae\u9eef\u6de1 \u501f\u6211\u7b11\u989c\u707f\u70c2\u5982\u6625\u5929 \u501f\u6211\u6740\u6b7b\u5eb8\u788c\u7684\u60c5\u6000 \u501f\u6211\u7eb5\u5bb9\u7684\u60b2\u6006\u4e0e\u54ed\u558a \u501f\u6211\u6026\u7136\u5fc3\u52a8\u5982\u5f80\u6614 \u501f\u6211\u5b89\u9002\u7684\u6e05\u6668\u4e0e\u508d\u665a \u9759\u770b\u5149\u9634\u834f\u82d2 \u501f\u6211\u5591\u54d1\u65e0\u8a00 \u4e0d\u7ba1\u4e0d\u987e\u4e0d\u95ee\u4e0d\u8bf4 \u4e5f\u4e0d\u5ff5 \u9759\u770b\u5149\u9634\u834f\u82d2 \u501f\u6211\u5591\u54d1\u65e0\u8a00 \u4e0d\u7ba1\u4e0d\u987e\u4e0d\u95ee\u4e0d\u8bf4 \u4e5f\u4e0d\u5ff5', u'title': u'\u501f\u6211'}
            print(hit['_source'])

es = ES()
es.exists_or_create()
# es._index()
es._bulk()
es._search()




