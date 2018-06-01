#! /usr/bin/python
# -*- coding: utf-8 -*-
# @Time    : 5/9/18 12:00 AM
# @Author  : HouJP
# @Email   : houjp1992@gmail.com

import random
import jieba
from absl import logging
from bin.featwheel.base import Base
from bin.preprocess.loader import load_txt, get_data_size
from bin.featwheel.io import write_csv, save_vector, read_csv


class Json2CSV(Base):

    def __init__(self, conf):
        Base.__init__(self, conf)

    def transform(self, data_type='train'):
        raw_path = self.conf.get('PATH', 'raw')
        txt_path = '{}/{}.txt'.format(raw_path, data_type)
        data = load_txt(txt_path)

        csv_path = '{}/raw.{}.csv'.format(raw_path, data_type)
        write_csv(csv_path, data)

    def run(self):
        self.transform('train')
        self.transform('test')


class IndexGenerator(Base):

    def __init__(self, conf):
        Base.__init__(self, conf, enable_params=True)

    @staticmethod
    def random_split(vec, rates):
        """
        Random split vector with rates
        :param vec: vector
        :param rates: Proportions of each part of the data
        :return: list of subsets
        """
        slices = []
        pre_sum_rates = []
        sum_rates = 0.0
        for rate in rates:
            slices.append([])
            pre_sum_rates.append(sum_rates + rate)
            sum_rates += rate
        for e in vec:
            randn = random.random()
            for i in range(0, len(pre_sum_rates)):
                if randn < pre_sum_rates[i]:
                    slices[i].append(e)
                    break
        n_slices = []
        for slic in slices:
            n_slices.append(len(slic))
        logging.info('Random split vector done [n_vec={}] [n_slices={}]'.format(len(vec), str(n_slices)))
        return slices

    @staticmethod
    def get_config_section_name():
        return 'PRE'

    def run(self):
        cv_num = self.params['cv_num']
        index_name = self.params['index_name']
        index_slices = self.random_split(range(get_data_size('{}/raw.train.csv'.format(self.conf.get('PATH', 'raw')))),
                                         [1.0 / cv_num] * cv_num)
        # r0: [n_slices=[29577, 29177, 29212, 29238, 29217]]
        for kv in enumerate(index_slices):
            cv_id = kv[0]
            index_slice = kv[1]
            file_name = '{}/{}_{}_{}.train.index'.format(self.conf.get('PATH', 'index'), index_name, cv_id, cv_num)
            save_vector(file_name, index_slice, 'w')


class JiebaCutter(Base):

    def __init__(self, conf):
        Base.__init__(self, conf)

    def cut(self, data_type):
        raw_path = self.conf.get('PATH', 'raw')
        data = read_csv('{}/raw.{}.csv'.format(self.conf.get('PATH', 'raw'), data_type))
        jieba_data = {'jieba': list()}
        if '标签' in data.keys():
            jieba_data['标签'] = data['标签']
        for content in data['内容']:
            words = list(jieba.cut(content))
            words = [word.encode('utf8') for word in words]
            jieba_data['jieba'].append('#_#'.join(words))
        write_csv('{}/{}.{}.csv'.format(raw_path, self.get_date_name(), data_type), jieba_data)

    def run(self):
        self.cut('train')
        self.cut('test')
