#! /usr/bin/python
# -*- coding: utf-8 -*-
# @Time    : 5/9/18 9:54 AM
# @Author  : HouJP
# @Email   : houjp1992@gmail.com

from bin.analysis.analyzer import Analyzer


class Label(object):

    cn2en = {
        '人类作者': 'Human Auth',
        '机器翻译': 'Machine Trans',
        '自动摘要': 'Auto Sub',
        '机器作者': 'Machine Auth'
    }

    cn2id = {
        '人类作者': 0,
        '机器翻译': 1,
        '自动摘要': 2,
        '机器作者': 3
    }


class LabelCount(Analyzer):

    def __init__(self, conf):
        Analyzer.__init__(self, conf)

    def analyze_row(self, row):
        label = row['标签']
        return label

    def aggregate(self, vecs):
        label_count = dict()
        for label in vecs:
            label_count[label] = label_count.get(label, 0) + 1
        # 人类作者=48018
        # 机器翻译=36206
        # 自动摘要=31034
        # 机器作者=31163
        for label in label_count:
            print('#{}={}'.format(label, label_count[label]))
