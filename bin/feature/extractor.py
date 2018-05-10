#! /usr/bin/python
# -*- coding: utf-8 -*-
# @Time    : 5/10/18 9:41 PM
# @Author  : HouJP
# @Email   : houjp1992@gmail.com

import csv
from absl import logging
from bin.featwheel.feature import save_vector


class Extractor(object):

    def __init__(self, conf):
        self.conf = conf
        # set feature name
        self.feature_name = self.__class__.__name__
        # load data
        self.pre_data = self.load_pre_data()

    def load_pre_data(self):
        return {}

    def extract_row(self, row):
        assert False, 'Please override function: Extractor.extract_row'

    def get_feature_size(self):
        assert False, 'Please override function: Extractor.get_feature_num'

    def get_data_size(self, data_name):
        data_size = 0
        with open('{}/{}.csv'.format(self.conf.get('PATH', 'raw'), data_name)) as csvfile:
            reader = csv.DictReader(csvfile)
            for _ in reader:
                data_size += 1
        return data_size

    def extract(self, data_name):
        data_size = self.get_data_size(data_name)
        feat_size = self.get_feature_size()

        feat_file_path = '{}/{}.{}.smat'.format(self.conf.get('PATH', 'feature'),
                                                self.feature_name,
                                                data_name)
        feat_file = open(feat_file_path, 'w')
        feat_file.write('{} {}\n'.format(data_size, feat_size))

        with open('{}/{}.csv'.format(self.conf.get('PATH', 'raw'), data_name)) as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                vec = self.extract_row(row)
                assert len(vec) == self.get_feature_size(), 'len(vec)=%d' % len(vec)
                save_vector(feat_file, vec)

        feat_file.close()
        logging.info('Save feature done [name={}] [path={}]'.format(self.feature_name, feat_file_path))

    def run(self):
        self.extract('train')
