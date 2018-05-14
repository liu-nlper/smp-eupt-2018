#! /usr/bin/python
# -*- coding: utf-8 -*-
# @Time    : 5/10/18 9:41 PM
# @Author  : HouJP
# @Email   : houjp1992@gmail.com

import csv
from absl import logging
import matplotlib.pyplot as plt
from bin.featwheel.feature import save_vector, load
from bin.featwheel.base import Base
from bin.featwheel.io import read_csv
from bin.analysis.label import Label

class Extractor(Base):

    def __init__(self, conf):
        Base.__init__(self, conf)
        # set feature name
        self.feature_name = self.get_class_name()
        # load data
        self.pre_data = self.load_pre_data()

    def load_pre_data(self):
        return {}

    def extract_row(self, row):
        assert False, 'Please override function: Extractor.extract_row'

    def get_feature_size(self):
        assert False, 'Please override function: Extractor.get_feature_num'

    def get_data_size(self, data_name, data_type):
        data_size = 0
        with open('{}/{}.{}.csv'.format(self.conf.get('PATH', 'raw'), data_name, data_type)) as csvfile:
            reader = csv.DictReader(csvfile)
            for _ in reader:
                data_size += 1
        return data_size

    def extract(self, data_name='raw', data_type='train'):
        data_size = self.get_data_size(data_name, data_type)
        feat_size = self.get_feature_size()

        feat_file_path = '{}/{}.{}.smat'.format(self.conf.get('PATH', 'feature'),
                                                self.feature_name,
                                                data_type)
        feat_file = open(feat_file_path, 'w')
        feat_file.write('{} {}\n'.format(data_size, feat_size))

        with open('{}/{}.{}.csv'.format(self.conf.get('PATH', 'raw'), data_name, data_type)) as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                vec = self.extract_row(row)
                assert len(vec) == self.get_feature_size(), 'len(vec)=%d' % len(vec)
                save_vector(feat_file, vec)

        feat_file.close()
        logging.info('Save feature done [name={}] [path={}]'.format(self.feature_name, feat_file_path))

    def draw_hist(self, f_id=0, bins=10, data_name='raw', data_type='train'):
        raw_path = self.conf.get('PATH', 'raw')
        feature_path = self.conf.get('PATH', 'feature')

        f_name = '%s/%s.%s.smat' % (feature_path, self.get_class_name(), data_type)
        f_vecs = load(f_name).toarray()

        labels = read_csv('{}/{}.{}.csv'.format(raw_path, data_name, data_type))['标签']

        data = dict()
        for i in range(len(labels)):
            label = labels[i]
            c_len = f_vecs[i][f_id]
            data[label] = data.get(label, list())
            data[label].append(c_len)

        for label in Label.cn2en:
            label_data = data[label]
            plt.hist(label_data, label=Label.cn2en[label], alpha=0.5, bins=bins)

        plt.title('{} Analysis'.format(self.get_class_name()))
        plt.xlabel(self.get_class_name())
        plt.ylabel('Count')

        plt.tick_params(top='off', right='off')
        plt.legend()
        plt.show()

    def run(self):
        self.extract()

    def visual(self):
        assert False, 'Please override function: Extractor.visual'

