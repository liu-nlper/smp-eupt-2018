#! /usr/bin/python
# -*- coding: utf-8 -*-
# @Time    : 6/3/18 6:35 PM
# @Author  : HouJP
# @Email   : houjp1992@gmail.com

import sys
import re
import csv
from absl import flags, logging
from bin.statistics.counter import Counter
from bin.analysis.label import Label
from bin.featwheel.ml_math import entropy
from bin.featwheel.string import ngram

csv.field_size_limit(sys.maxsize)

FLAGS = flags.FLAGS


class WordDF(Counter):
    """
    Calculates document frequency for words.
    """

    def __init__(self, conf):
        Counter.__init__(self, conf, False)
        logging.info('[name={}] [unit={}, min_doc_frequency={}]'.format(self.__class__.__name__,
                                                                        FLAGS.unit,
                                                                        FLAGS.min_doc_frequency))

    @staticmethod
    def get_config_section_name():
        return 'STATISTICS'

    def get_config_field_name(self):
        return 'word_df'

    def get_data_name(self):
        return '{}_df_{}'.format(FLAGS.unit,
                                 FLAGS.min_doc_frequency)

    def count_row(self, row):
        label = row['标签']
        label_id = Label.cn2id[label]

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

        data = dict()
        for word in words:
            data[(word, label_id)] = 1
        return data

    def aggregate(self, rows):
        data = dict()
        words = set()
        for row in rows:
            for word_label in row:
                words.add(word_label[0])
                data[word_label] = data.get(word_label, 0.) + row[word_label]

        csv_data = {'word': list()}
        for label_id in Label.cn2id.values():
            csv_data['df#{}'.format(label_id)] = list()
        csv_data['total_df'] = list()
        csv_data['df_entropy'] = list()

        for word in words:
            total = 0.
            for label_id in Label.cn2id.values():
                total += data.get((word, label_id), 0.)
            if total < FLAGS.min_doc_frequency:
                continue

            csv_data['word'].append(word)
            for label_id in Label.cn2id.values():
                csv_data['df#{}'.format(label_id)].append(data.get((word, label_id), 0.))
            csv_data['total_df'].append(total)

            nums = [0.] * len(Label.cn2id.values())
            for label_id in Label.cn2id.values():
                nums[label_id] = float(data.get((word, label_id), 0.))
            p_list = [1. * num / total for num in nums]
            e = entropy(p_list)
            csv_data['df_entropy'].append(e)
        return csv_data

    def run(self):
        unit = FLAGS.unit
        if unit == 'word':
            self.count('jieba_cutter', 'train')
        elif unit.endswith('gram'):
            self.count('raw', 'train')
        else:
            assert False, 'Wrong unit found in configuration'
