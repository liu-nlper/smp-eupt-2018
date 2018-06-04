#! /usr/bin/python
# -*- coding: utf-8 -*-
# @Time    : 5/10/18 9:41 PM
# @Author  : HouJP
# @Email   : houjp1992@gmail.com

import csv
from absl import logging
import numpy as np
from sklearn.neighbors import KernelDensity
from bin.featwheel.feature import save_vector, load
from bin.featwheel.base import Base
from bin.featwheel.io import read_csv
from bin.analysis.label import Label


class Extractor(Base):

    def __init__(self, conf, enable_params=False):
        Base.__init__(self, conf, enable_params=enable_params)
        # load data
        self.pre_data = self.load_pre_data()

    def load_pre_data(self):
        return {}

    @staticmethod
    def get_config_section_name():
        return 'EXTRACTOR'

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
                                                self.get_data_name(),
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
        logging.info('Save feature done [name={}] [path={}]'.format(self.get_data_name(), feat_file_path))

    def extract_test(self, data_name='raw', data_type='train', line_id=0):
        with open('{}/{}.{}.csv'.format(self.conf.get('PATH', 'raw'), data_name, data_type)) as csvfile:
            reader = csv.DictReader(csvfile)
            line_num = 0
            for row in reader:
                if line_num == line_id:
                    self.extract_row(row)
                line_num += 1

    def load_draw_data(self, f_id=0, data_name='raw', data_type='train'):
        raw_path = self.conf.get('PATH', 'raw')
        feature_path = self.conf.get('PATH', 'feature')

        f_name = '%s/%s.%s.smat' % (feature_path, self.get_data_name(), data_type)
        f_vecs = load(f_name).toarray()

        labels = read_csv('{}/{}.{}.csv'.format(raw_path, data_name, data_type))['标签']

        data = dict()
        for i in range(len(labels)):
            label = labels[i]
            c_len = f_vecs[i][f_id]
            data[label] = data.get(label, list())
            data[label].append(c_len)
        return data

    def draw_hist(self, f_id=0, x_min=0., x_max=2000., bin_num=200., data_name='raw', data_type='train'):
        import matplotlib.pyplot as plt

        data = self.load_draw_data(f_id=f_id, data_name=data_name, data_type=data_type)

        bins = np.arange(x_min, x_max, x_max / bin_num)

        for label in Label.cn2en:
            label_data = data[label]
            plt.hist(label_data, label=Label.cn2en[label], alpha=0.5, bins=bins)

        plt.title('{} analysis'.format(self.get_data_name()))
        plt.xlabel(self.get_data_name())
        plt.ylabel('count')

        plt.tick_params(top='off', right='off')
        plt.legend(loc='best')
        plt.show()

    def draw_kernel_density(self,
                            f_id=0,
                            x_min=0.,
                            x_max=2000.,
                            bin_num=200,
                            data_name='raw',
                            data_type='train',
                            bandwidth=0.5):
        import matplotlib.pyplot as plt

        data = self.load_draw_data(f_id=f_id, data_name=data_name, data_type=data_type)

        bins = np.linspace(x_min, x_max, bin_num)[:, np.newaxis]

        for label in Label.cn2en:
            label_data = np.array(data[label])
            kde = KernelDensity(kernel='gaussian', bandwidth=bandwidth).fit(label_data[:, np.newaxis])
            log_dens = kde.score_samples(bins)
            plt.plot(bins[:, 0], np.exp(log_dens), '-', label='{}'.format(Label.cn2en[label]))

        plt.title('{} analysis'.format(self.get_data_name()))
        plt.xlabel(self.get_data_name())
        plt.ylabel('probability density')

        plt.tick_params(top='off', right='off')
        plt.legend(loc='best')
        plt.show()

    def run(self):
        self.extract(data_type='train')
        self.extract(data_type='test')

    def test(self):
        assert False, 'Please override function: Extractor.test'

    def visual(self):
        assert False, 'Please override function: Extractor.visual'

