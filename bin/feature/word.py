#! /usr/bin/python
# -*- coding: utf-8 -*-
# @Time    : 6/3/18 6:22 PM
# @Author  : HouJP
# @Email   : houjp1992@gmail.com

import csv
import sys
import math
import numpy as np
import re
from absl import logging, flags
from bin.analysis.label import Label
from bin.feature.extractor import Extractor
from bin.featwheel.io import csv2dict, read_csv
from bin.featwheel.string import ngram

csv.field_size_limit(sys.maxsize)


FLAGS = flags.FLAGS


class AveWordLength(Extractor):
    def __init__(self, conf):
        Extractor.__init__(self, conf)

    def get_feature_size(self):
        return 1

    def extract_row(self, row):
        content = row['jieba']
        words = content.split('#_#')
        ave_word_length = np.average([len(word.decode('utf-8')) for word in words])
        return [ave_word_length]

    def run(self):
        self.extract(data_name='jieba_cutter', data_type='train')
        self.extract(data_name='jieba_cutter', data_type='test')

    def visual(self):
        self.draw_hist(x_min=1., x_max=2.5)
        self.draw_kernel_density(x_min=1., x_max=2.5, bandwidth=0.005)


class WordDFBase(Extractor):
    def __init__(self, conf):
        Extractor.__init__(self, conf)
        logging.info('[name={}] [unit={}, enable_set={}, min_doc_frequency={}]'.format(self.__class__.__name__,
                                                                                       FLAGS.unit,
                                                                                       FLAGS.enable_set,
                                                                                       FLAGS.min_doc_frequency))

    @staticmethod
    def get_config_section_name():
        return 'EXTRACTOR'

    def load_pre_data(self):
        word_df = read_csv('{}/{}_df_{}.train.csv'.format(self.conf.get('PATH', 'raw'),
                                                          FLAGS.unit,
                                                          FLAGS.min_doc_frequency))
        word_df = csv2dict(word_df, key='word')
        return {'word_df': word_df}

    def get_df_info(self, row):
        word_entropy_sum = 0.
        word_p_list = [0.] * 4
        word_count = 0.

        word_df = self.pre_data['word_df']

        unit = FLAGS.unit
        if unit == 'word':
            content = row['jieba']
            words = content.split('#_#')
        elif unit.endswith('gram'):
            content = row['内容']
            n = int(re.match(r'^(\d*)gram', unit).group(1).strip())
            words = ngram(content, n)
        else:
            assert False, 'Wrong unit found in configuration'

        if FLAGS.enable_set == 'true':
            words = set(words)
        for word in words:
            if word not in word_df:
                continue
            f = float(word_df[word]['total_df'])
            e = float(word_df[word]['df_entropy'])
            word_entropy_sum += e
            for label_id in Label.cn2id.values():
                # Correction: p = n / total -> (n + 1) / (total + 4)
                p = (float(word_df[word]['df#{}'.format(label_id)]) + 1) / (f + 4)
                # P(sentence) = p(word_1) * p(word_2) * ...
                word_p_list[label_id] -= math.log(p)

            word_count += 1
        return word_entropy_sum, word_p_list, word_count

    def run(self):
        unit = FLAGS.unit
        if unit == 'word':
            self.extract(data_name='jieba_cutter', data_type='train')
            self.extract(data_name='jieba_cutter', data_type='test')
        elif unit.endswith('gram'):
            self.extract(data_name='raw', data_type='train')
            self.extract(data_name='raw', data_type='test')
        else:
            assert False, 'Wrong unit found in configuration'


class WordDFEntropySum(WordDFBase):
    def __init__(self, conf):
        WordDFBase.__init__(self, conf)

    def get_feature_size(self):
        return 1

    def get_config_field_name(self):
        return 'word_df_entropy_sum'

    def get_data_name(self):
        return '{}_df_entropy_sum_{}_{}'.format(FLAGS.unit,
                                                FLAGS.enable_set,
                                                FLAGS.min_doc_frequency)

    def extract_row(self, row):
        word_entropy_sum, _, _ = self.get_df_info(row)
        return [word_entropy_sum]

    def visual(self):
        self.draw_hist(x_max=2000)
        self.draw_kernel_density(x_max=2000)


class WordDFEntropyAverage(WordDFBase):
    def __init__(self, conf):
        WordDFBase.__init__(self, conf)

    def get_feature_size(self):
        return 1

    def get_config_field_name(self):
        return 'word_df_entropy_average'

    def get_data_name(self):
        return '{}_df_entropy_average_{}_{}'.format(FLAGS.unit,
                                                    FLAGS.enable_set,
                                                    FLAGS.min_doc_frequency)

    def extract_row(self, row):
        word_entropy_sum, _, word_count = self.get_df_info(row)
        return [1. * word_entropy_sum / word_count if word_count > 0 else -1.]

    def visual(self):
        self.draw_hist(x_min=1., x_max=2.)
        self.draw_kernel_density(x_min=1., x_max=2., bandwidth=0.002)


class WordDFProbabilitySum(WordDFBase):
    def __init__(self, conf):
        WordDFBase.__init__(self, conf)

    def get_feature_size(self):
        return 4

    def get_config_field_name(self):
        return 'word_df_probability_sum'

    def get_data_name(self):
        return '{}_df_probability_sum_{}_{}'.format(FLAGS.unit,
                                                    FLAGS.enable_set,
                                                    FLAGS.min_doc_frequency)

    def extract_row(self, row):
        _, word_p_list, _ = self.get_df_info(row)
        return word_p_list

    def visual(self):
        self.draw_hist(x_max=2000)
        self.draw_kernel_density(x_max=2000)


class WordDFProbabilityAve(WordDFBase):
    def __init__(self, conf):
        WordDFBase.__init__(self, conf)

    def get_feature_size(self):
        return 4

    def get_config_field_name(self):
        return 'word_df_probability_ave'

    def get_data_name(self):
        return '{}_df_probability_ave_{}_{}'.format(FLAGS.unit,
                                                    FLAGS.enable_set,
                                                    FLAGS.min_doc_frequency)

    def extract_row(self, row):
        _, word_p_list, word_count = self.get_df_info(row)
        return [1. * p / word_count if word_count > 0 else -1. for p in word_p_list]

    def visual(self):
        self.draw_hist(x_min=0.5, x_max=1.5)
        self.draw_kernel_density(x_min=0.5, x_max=1.5, bandwidth=0.002)


class WordDFProbabilityNorm(WordDFBase):
    def __init__(self, conf):
        WordDFBase.__init__(self, conf)

    def get_feature_size(self):
        return 4

    def get_config_field_name(self):
        return 'word_df_probability_norm'

    def get_data_name(self):
        return '{}_df_probability_norm_{}_{}'.format(FLAGS.unit,
                                                     FLAGS.enable_set,
                                                     FLAGS.min_doc_frequency)

    def extract_row(self, row):
        _, word_p_list, _ = self.get_df_info(row)
        word_p_sum = sum(word_p_list)
        return [p / word_p_sum if word_p_sum > 0 else -1. for p in word_p_list]

    def visual(self):
        self.draw_hist(x_min=0.1, x_max=0.2, f_id=0)
        self.draw_hist(x_min=0.1, x_max=0.3, f_id=1)
        self.draw_hist(x_min=0.35, x_max=0.5, f_id=2)
        self.draw_hist(x_min=0.1, x_max=0.3, f_id=3)


class WordDFProbabilitySumSum(WordDFBase):
    def __init__(self, conf):
        WordDFBase.__init__(self, conf)

    def get_feature_size(self):
        return 1

    def get_config_field_name(self):
        return 'word_df_probability_sum_sum'

    def get_data_name(self):
        return '{}_df_probability_sum_sum_{}_{}'.format(FLAGS.unit,
                                                        FLAGS.enable_set,
                                                        FLAGS.min_doc_frequency)

    def extract_row(self, row):
        _, word_p_list, _ = self.get_df_info(row)
        return [sum(word_p_list)]

    def visual(self):
        self.draw_hist(x_max=2000)
        self.draw_kernel_density(x_max=2000)


class WordDFProbabilityAveSum(WordDFBase):
    def __init__(self, conf):
        WordDFBase.__init__(self, conf)

    def get_feature_size(self):
        return 1

    def get_config_field_name(self):
        return 'word_df_probability_ave_sum'

    def get_data_name(self):
        return '{}_df_probability_ave_sum_{}_{}'.format(FLAGS.unit,
                                                        FLAGS.enable_set,
                                                        FLAGS.min_doc_frequency)

    def extract_row(self, row):
        _, word_p_list, word_count = self.get_df_info(row)
        return [sum([1. * p / word_count if word_count > 0 else -1. for p in word_p_list])]

    def visual(self):
        self.draw_hist(x_min=0.5, x_max=1.5)
        self.draw_kernel_density(x_min=0.5, x_max=1.5, bandwidth=0.002)
