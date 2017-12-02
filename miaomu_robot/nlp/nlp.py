# -*- coding: utf-8 -*-
'''
@author: miaomu
@update: 2017/12/02
'''
from miaomu_robot.nlp.Feature_library.q_search import q_search
from miaomu_robot.nlp.Feature_library.a_search import a_search
'''
根据关键字过滤结果不同,需要走不同的调取数据源的分支:
1. Data_crawler: 直接调爬虫数据(包括实时和非实时的)得到答句的
2. KB_library: 直接从本地知识库获取得到答句的
3. Feature_library: 需要匹配es问句库答句库得到答句的

代码实现次序: 3(格式化存储入es的歌词库) - 2(批量拉下来的歌词库,在1and3用不了的时候备用) - 1(网易云或百度音乐等).
'''


def nlp(sent_ori):
    if sent_ori != "":
        sent_ans = "123"
    else:
        sent_ans = "empty input..."
    return sent_ans


if __name__ == "__main__":
    sent_ori = raw_input("input a sentence for test: ")
    print nlp(sent_ori)


