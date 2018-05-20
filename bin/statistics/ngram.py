#! /usr/bin/python
# -*- coding: utf-8 -*-
# @Time    : 5/20/18 8:31 AM
# @Author  : HouJP
# @Email   : houjp1992@gmail.com

from bin.statistics.counter import Counter
from bin.analysis.label import Label
from bin.featwheel.ml_math import entropy
from bin.featwheel.string import ngram


class NGramDF(Counter):
    """
    Calculates document frequency for n-grams.
    """

    def __init__(self, conf):
        Counter.__init__(self, conf, True)

    @staticmethod
    def get_config_section_name():
        return 'STATISTICS'

    def get_config_field_name(self):
        return 'n_gram_df'

    def get_date_name(self):
        return '{}_n{}_mdf{}'.format(self.get_config_field_name(),
                                     self.params['n'],
                                     self.params['min_doc_frequency'])

    def count_row(self, row):
        label = row['标签']
        content = row['内容']

        label_id = Label.cn2id[label]
        words = ngram(content, self.params['n'])

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
            csv_data[label_id] = list()
        for word in words:
            total = 0.
            for label_id in Label.cn2id.values():
                total += data.get((word, label_id), 0.)
            if total < self.params['min_doc_frequency']:
                continue
            csv_data['word'].append(word)
            for label_id in Label.cn2id.values():
                csv_data[label_id].append(data.get((word, label_id), 0.))
        return csv_data


class NGramEntropy(Counter):

    def __init__(self, conf):
        Counter.__init__(self, conf, True)

    def get_config_section_name(self):
        return 'STATISTICS'

    def get_date_name(self):
        return '{}_n{}_mdf{}'.format(self.get_config_field_name(),
                                     self.params['n'],
                                     self.params['min_doc_frequency'])

    def count_row(self, row):
        word = row['word']
        nums = [0.] * len(Label.cn2id.values())
        for label_id in Label.cn2id.values():
            nums[label_id] = float(row[str(label_id)])
        total = sum(nums)
        p_list = [1. * num / total for num in nums]
        e = entropy(p_list)

        data = dict()
        data['word'] = word
        data['total'] = total
        data['entropy'] = e
        for label_id in Label.cn2id.values():
            data['p{}'.format(label_id)] = p_list[label_id]
        return data

    def aggregate(self, rows):
        data = {'word': list(), 'total': list(), 'entropy': list()}
        for label_id in Label.cn2id.values():
            data['p{}'.format(label_id)] = list()
        for row in rows:
            data['word'].append(row['word'])
            data['total'].append(row['total'])
            data['entropy'].append(row['entropy'])
            for label_id in Label.cn2id.values():
                data['p{}'.format(label_id)].append(row['p{}'.format(label_id)])
        return data

    def run(self):
        self.count(data_name='n_gram_df_n{}_mdf{}'.format(self.params['n'],
                                                          self.params['min_doc_frequency']),
                   data_type='train')
