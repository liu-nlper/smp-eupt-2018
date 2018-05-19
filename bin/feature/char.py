#! /usr/bin/python
# -*- coding: utf-8 -*-
# @Time    : 5/19/18 2:00 PM
# @Author  : HouJP
# @Email   : houjp1992@gmail.com

import csv
import sys
import jieba
from bin.feature.extractor import Extractor
from bin.featwheel.io import csv2dict, read_csv

csv.field_size_limit(sys.maxsize)


class CharEntropy(Extractor):

    def __init__(self, conf):
        Extractor.__init__(self, conf, True)
        self.feature_name = '{}_{}'.format(self.get_class_name(), self.params['min_doc_frequency'])

    def get_section_name(self):
        return 'EXTRACTOR'

    def get_feature_size(self):
        return 1

    def load_pre_data(self):
        char_entropy = read_csv('{}/char_entropy.train.csv'.format(self.conf.get('PATH', 'raw')))
        char_entropy = csv2dict(char_entropy, key='char')
        return {'char_entropy': char_entropy}

    def cal_entropy(self, row):
        char_entropy_sum = 0.
        char_count = 0.
        char_entropy = self.pre_data['char_entropy']
        min_doc_frequency = float(self.params['min_doc_frequency'])
        content = row['内容'].decode('utf-8')
        chars = set(content)
        for char in chars:
            char_utf8 = char.encode('utf-8')
            if char_utf8 not in char_entropy:
                continue
            f = float(char_entropy[char_utf8]['total'])
            e = float(char_entropy[char_utf8]['entropy'])
            if f < min_doc_frequency:
                continue
            char_entropy_sum += e
            char_count += 1
        return char_entropy_sum, char_count


class CharEntropySummary(CharEntropy):

    def __init__(self, conf):
        CharEntropy.__init__(self, conf)

    def extract_row(self, row):
        char_entropy_sum, _ = self.cal_entropy(row)
        return [char_entropy_sum]

    def visual(self):
        self.draw_hist(x_max=2000)
        self.draw_kernel_density(x_max=2000)


class CharEntropyAverage(CharEntropy):

    def __init__(self, conf):
        CharEntropy.__init__(self, conf)

    def extract_row(self, row):
        char_entropy_sum, char_count = self.cal_entropy(row)
        return [1. * char_entropy_sum / char_count if char_count > 0 else 0.]

    def visual(self):
        self.draw_hist(x_min=1., x_max=2.)
        self.draw_kernel_density(x_min=1., x_max=2., bandwidth=0.002)
