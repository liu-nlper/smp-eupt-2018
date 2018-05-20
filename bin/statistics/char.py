#! /usr/bin/python
# -*- coding: utf-8 -*-
# @Time    : 5/19/18 8:42 AM
# @Author  : HouJP
# @Email   : houjp1992@gmail.com

from bin.statistics.counter import Counter
from bin.analysis.label import Label
from bin.featwheel.ml_math import entropy


class CharDF(Counter):
    """
    Calculates document frequency for chars.
    """

    def __init__(self, conf):
        Counter.__init__(self, conf)

    def get_class_name(self):
        return 'char_df'

    def count_row(self, row):
        label = row['标签']
        content = row['内容'].decode('utf-8')

        label_id = Label.cn2id[label]
        chars = set(content)

        data = dict()
        for char in chars:
            data[(char.encode('utf-8'), label_id)] = 1
        return data

    def aggregate(self, rows):
        data = dict()
        chars = set()
        for row in rows:
            for char_label in row:
                chars.add(char_label[0])
                data[char_label] = data.get(char_label, 0.) + row[char_label]

        csv_data = {'char': list()}
        for label_id in Label.cn2id.values():
            csv_data[label_id] = list()
        for char in chars:
            csv_data['char'].append(char)
            for label_id in Label.cn2id.values():
                csv_data[label_id].append(data.get((char, label_id), 0.))
        return csv_data


class CharEntropy(Counter):

    def __init__(self, conf):
        Counter.__init__(self, conf, True)

    def get_section_name(self):
        return 'STATISTICS'

    def count_row(self, row):
        char = row['char']
        nums = list()
        for label_id in Label.cn2id.values():
            nums.append(float(row[str(label_id)]))
        total = sum(nums)
        p_list = [1. * num / total for num in nums]
        e = entropy(p_list)

        data = dict()
        data['char'] = char
        data['total'] = total
        data['entropy'] = e
        return data

    def aggregate(self, rows):
        data = {'char': list(), 'total': list(), 'entropy': list()}
        for row in rows:
            data['char'].append(row['char'])
            data['total'].append(row['total'])
            data['entropy'].append(row['entropy'])
        return data

    def run(self):
        self.count(data_name='char_df', data_type='train')
