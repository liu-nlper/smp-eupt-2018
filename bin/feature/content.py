#! /usr/bin/python
# -*- coding: utf-8 -*-
# @Time    : 5/10/18 10:11 PM
# @Author  : HouJP
# @Email   : houjp1992@gmail.com

import csv
import sys
import jieba
import numpy as np
from bin.feature.extractor import Extractor
from bin.featwheel.string import title2underline

csv.field_size_limit(sys.maxsize)


class ContentLength(Extractor):

    def __init__(self, conf):
        Extractor.__init__(self, conf)

    def get_feature_size(self):
        return 1

    def extract_row(self, row):
        content = row['内容']
        return [len(content)]

    def visual(self):
        bins = np.arange(0, 1e4, 2 * 1e2)
        self.draw_hist(bins=bins)


class WordNum(Extractor):

    def __init__(self, conf):
        Extractor.__init__(self, conf)

    def get_feature_size(self):
        return 1

    def extract_row(self, row):
        content = row['内容']
        return [len(list(jieba.cut(content)))]


class WordSetNum(Extractor):

    def __init__(self, conf):
        Extractor.__init__(self, conf)

    def get_class_name(self):
        return '{}_3'.format(title2underline(self.__class__.__name__))

    def get_feature_size(self):
        return 1

    def extract_row(self, row):
        content = row['jieba']
        words = content.split('#_#')
        words = set([word for word in words if len(word) > 3])
        return [len(words)]

    def run(self):
        self.extract(data_name='jieba_cutter')
