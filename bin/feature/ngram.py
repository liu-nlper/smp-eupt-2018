#! /usr/bin/python
# -*- coding: utf-8 -*-
# @Time    : 5/20/18 9:44 AM
# @Author  : HouJP
# @Email   : houjp1992@gmail.com

import csv
import math
import sys
from bin.analysis.label import Label
from bin.feature.extractor import Extractor
from bin.featwheel.io import csv2dict, read_csv
from bin.featwheel.string import ngram

csv.field_size_limit(sys.maxsize)


class NGramEntropy(Extractor):

    def __init__(self, conf):
        Extractor.__init__(self, conf, True)

    def get_config_section_name(self):
        return 'EXTRACTOR'

    def get_date_name(self):
        return '{}_n{}_mdf{}'.format(self.get_config_field_name(),
                                     self.params['n'],
                                     self.params['min_doc_frequency'])

    def get_feature_size(self):
        return 1

    def load_pre_data(self):
        word_entropy = read_csv('{}/n_gram_entropy_n2_mdf100.train.csv'.format(self.conf.get('PATH', 'raw')))
        word_entropy = csv2dict(word_entropy, key='word')
        return {'word_entropy': word_entropy}

    def cal_entropy(self, row):
        word_entropy_sum = 0.
        word_count = 0.
        word_entropy = self.pre_data['word_entropy']
        n = int(self.params['n'])
        min_doc_frequency = float(self.params['min_doc_frequency'])
        content = row['内容']
        words = ngram(content, n)
        for word in words:
            if word not in word_entropy:
                continue
            f = float(word_entropy[word]['total'])
            e = float(word_entropy[word]['entropy'])
            if f < min_doc_frequency:
                continue
            word_entropy_sum += e
            word_count += 1
        return word_entropy_sum, word_count


class NGramEntropySummary(NGramEntropy):

    def __init__(self, conf):
        NGramEntropy.__init__(self, conf)

    def extract_row(self, row):
        word_entropy_sum, _ = self.cal_entropy(row)
        return [word_entropy_sum]

    def visual(self):
        self.draw_hist(x_max=2000)
        self.draw_kernel_density(x_max=2000)


class NGramEntropyAverage(NGramEntropy):

    def __init__(self, conf):
        NGramEntropy.__init__(self, conf)

    def extract_row(self, row):
        word_entropy_sum, word_count = self.cal_entropy(row)
        return [1. * word_entropy_sum / word_count if word_count > 0 else 0.]

    def visual(self):
        self.draw_hist(x_min=1., x_max=2.)
        self.draw_kernel_density(x_min=1., x_max=2., bandwidth=0.002)
