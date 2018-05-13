#! /usr/bin/python
# -*- coding: utf-8 -*-
# @Time    : 5/10/18 10:11 PM
# @Author  : HouJP
# @Email   : houjp1992@gmail.com

import jieba
from bin.feature.extractor import Extractor


class ContentLength(Extractor):

    def __init__(self, conf):
        Extractor.__init__(self, conf)

    def get_feature_size(self):
        return 1

    def extract_row(self, row):
        content = row['内容']
        return [len(content)]


class WordNum(Extractor):

    def __init__(self, conf):
        Extractor.__init__(self, conf)

    def get_feature_size(self):
        return 1

    def extract_row(self, row):
        content = row['内容']
        return [len(list(jieba.cut(content)))]
