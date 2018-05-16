#! /usr/bin/python
# -*- coding: utf-8 -*-
# @Time    : 5/10/18 10:11 PM
# @Author  : HouJP
# @Email   : houjp1992@gmail.com

import csv
import sys
import jieba
from bin.feature.extractor import Extractor
import bin.featwheel.string as string

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
        self.draw_hist(x_max=10000)
        self.draw_kernel_density(x_max=10000)


class WordNum(Extractor):

    def __init__(self, conf):
        Extractor.__init__(self, conf)

    def get_feature_size(self):
        return 1

    def extract_row(self, row):
        content = row['内容']
        return [len(list(jieba.cut(content)))]

    def visual(self):
        self.draw_hist(x_max=1500)
        self.draw_kernel_density(x_max=1500)


class WordSetNum(Extractor):

    def __init__(self, conf):
        Extractor.__init__(self, conf)

    def get_class_name(self):
        return '{}_3'.format(string.title2underline(self.__class__.__name__))

    def get_feature_size(self):
        return 1

    def extract_row(self, row):
        content = row['jieba']
        words = content.split('#_#')
        words = set([word for word in words if len(word) > 3])
        return [len(words)]

    def run(self):
        self.extract(data_name='jieba_cutter')

    def visual(self):
        self.draw_hist(x_max=600)
        self.draw_kernel_density(x_max=600)


class ChineseCharRatio(Extractor):

    def __init__(self, conf):
        Extractor.__init__(self, conf)

    def get_feature_size(self):
        return 1

    def extract_row(self, row):
        content = row['内容']
        return [string.cal_cn_ratio(content)]

    def visual(self):
        self.draw_hist(x_max=1.)
        self.draw_kernel_density(x_max=1., bandwidth=0.005)


class DigitCharRatio(Extractor):

    def __init__(self, conf):
        Extractor.__init__(self, conf)

    def get_feature_size(self):
        return 1

    def extract_row(self, row):
        content = row['内容']
        return [string.cal_digit_ratio(content)]

    def visual(self):
        self.draw_hist(x_max=.3)
        self.draw_kernel_density(x_max=0.3, bandwidth=0.005)


class EnglishCharRatio(Extractor):

    def __init__(self, conf):
        Extractor.__init__(self, conf)

    def get_feature_size(self):
        return 1

    def extract_row(self, row):
        content = row['内容']
        return [string.cal_en_ratio(content)]

    def visual(self):
        self.draw_hist(x_max=.2)
        self.draw_kernel_density(x_max=0.2, bandwidth=0.005)


class CharSetRatio(Extractor):
    def __init__(self, conf):
        Extractor.__init__(self, conf)

    def get_feature_size(self):
        return 1

    def extract_row(self, row):
        content = row['内容'].decode('utf-8')
        return [1. * len(set(content)) / len(content) if len(content) > 0 else 0.]

    def visual(self):
        self.draw_hist(x_max=1.)
        self.draw_kernel_density(x_max=1., bandwidth=0.005)


class WordRatio(Extractor):

    def __init__(self, conf):
        Extractor.__init__(self, conf)

    def get_class_name(self):
        return '{}_3'.format(string.title2underline(self.__class__.__name__))

    def get_feature_size(self):
        return 1

    def extract_row(self, row):
        content = row['内容']
        words = [word.encode('utf-8') for word in list(jieba.cut(content)) if len(word) > 1]

        content_len = len(content)
        words_len = sum([len(word) for word in words])

        return [(1. * words_len / content_len) if content_len > 0 else 0.]

    def test(self):
        self.extract_test(line_id=18772)

    def visual(self):
        self.draw_hist(x_max=1.)
        self.draw_kernel_density(x_max=1., bandwidth=0.005)


class AveChineseContinuousLength(Extractor):

    def __init__(self, conf):
        Extractor.__init__(self, conf)

    def get_feature_size(self):
        return 1

    def extract_row(self, row):
        content = row['内容']
        return [string.ave_continuous_cn_length(content)]

    def visual(self):
        self.draw_hist(x_max=30.)
        self.draw_kernel_density(x_max=30., bandwidth=0.2)


class SpaceNum(Extractor):

    def __init__(self, conf):
        Extractor.__init__(self, conf)

    def get_feature_size(self):
        return 1

    def extract_row(self, row):
        content = row['内容']
        space_num = 0
        for c in content.decode('utf-8'):
            if c == ' ':
                space_num += 1
        return [space_num]

    def visual(self):
        self.draw_hist(x_max=100., bin_num=100)
        self.draw_kernel_density(x_max=100., bandwidth=0.5)


class SpaceRatio(Extractor):

    def __init__(self, conf):
        Extractor.__init__(self, conf)

    def get_feature_size(self):
        return 1

    def extract_row(self, row):
        content = row['内容'].decode('utf-8')
        space_num = 0
        for c in content:
            if c == ' ':
                space_num += 1
        return [1. * space_num / len(content) if len(content) > 0 else 0.]

    def visual(self):
        self.draw_hist(x_max=0.06)
        self.draw_kernel_density(x_max=0.06, bandwidth=0.0005)


class LastCharIsDot(Extractor):

    def __init__(self, conf):
        Extractor.__init__(self, conf)

    def get_feature_size(self):
        return 1

    def extract_row(self, row):
        content = row['内容'].decode('utf-8')
        last_ch = content[-1] if len(content) > 0 else '#_#'
        return [1. if last_ch == '。'.decode('utf-8') else 0.]

    def visual(self):
        self.draw_hist(x_max=2., bin_num=4)
        self.draw_kernel_density(x_max=1., bandwidth=0.2)


class LastCharIsChinese(Extractor):

    def __init__(self, conf):
        Extractor.__init__(self, conf)

    def get_feature_size(self):
        return 1

    def extract_row(self, row):
        content = row['内容'].decode('utf-8')
        last_ch = content[-1] if len(content) > 0 else None
        return [1. if (last_ch and string.is_cn(last_ch)) else 0.]

    def visual(self):
        self.draw_hist(x_max=2., bin_num=4)
        self.draw_kernel_density(x_max=1., bandwidth=0.2)
