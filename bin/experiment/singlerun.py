#! /usr/bin/python
# -*- coding: utf-8 -*-
# @Time    : 5/12/18 10:15 AM
# @Author  : HouJP
# @Email   : houjp1992@gmail.com

import json
import numpy as np
from absl import logging
from bin.model.model import Model
from bin.experiment.runner import Runner
from bin.featwheel.io import load_vector, ValidType, write_csv
from bin.preprocess.loader import load_label_id
from bin.featwheel.feature import load_all, sample_row
from bin.model.evaluation import ave_f1


class SingleRun(Runner):

    def __init__(self, conf):
        Runner.__init__(self, conf)

    def load_index(self, cv_id, cv_num):
        index_name = self.conf.get(self.get_config_section_name(), 'index_name')
        index_path = self.conf.get('PATH', 'index')

        train_indexs = list()
        valid_indexs = list()

        for i in range(cv_num):
            file_name = '{}/{}_{}_{}.train.index'.format(index_path, index_name,  i, cv_num)
            index = load_vector(file_name, ValidType.INT)
            if i == cv_id:
                valid_indexs = index
            else:
                train_indexs.extend(index)
        logging.info('[train_size={}] [valid_size={}]'.format(len(train_indexs), len(valid_indexs)))
        return train_indexs, valid_indexs

    @staticmethod
    def generate_data(indexs, labels, f_vecs):
        # sample label
        labels = labels[indexs]
        # sample features
        f_vecs = sample_row(f_vecs, indexs)

        return labels, f_vecs

    def save_valid_preds(self, valid_indexs, valid_preds, model_name, cv_id, cv_num):
        data_preds = dict()
        data_preds['index'] = valid_indexs
        data_preds['label_id_pred'] = valid_preds

        file_name = '{}/{}_{}_{}.{}.preds'.format(self.run_path,
                                                  model_name,
                                                  cv_id,
                                                  cv_num,
                                                  'valid')
        write_csv(file_name, data_preds)

    def save_preds(self, indexs, preds, model_name, data_type, cv_id, cv_num):
        data_preds = dict()
        if indexs:
            data_preds['index'] = indexs
        data_preds['label_id_pred'] = preds

        file_name = '{}/{}_{}_{}.{}.preds'.format(self.run_path,
                                                  model_name,
                                                  cv_id,
                                                  cv_num,
                                                  data_type)
        write_csv(file_name, data_preds)

    def run_offline(self, cv_id=-1, cv_num=-1):
        if cv_id != self.params['cv_id']:
            logging.info('Reset cv_id={}, previous cv_id={}'.format(cv_id, self.params['cv_id']))
            self.params['cv_id'] = cv_id
        if cv_num != self.params['cv_num']:
            logging.info('Reset cv_num={}, previous cv_num={}'.format(cv_num, self.params['cv_num']))
            self.params['cv_num'] = cv_num

        # load feature
        f_vecs = load_all(self.conf.get('PATH', 'feature'),
                          self.conf.get(self.get_config_section_name(), 'feature').split(),
                          'train',
                          False)
        # load label
        labels = np.array(load_label_id('{}/{}.{}.csv'.format(self.conf.get('PATH', 'raw'), 'raw', 'train')))
        # load index
        train_indexs, valid_indexs = self.load_index(cv_id, cv_num)

        # generate data set
        train_labels, train_f_vecs = self.generate_data(train_indexs, labels, f_vecs)
        valid_labels, valid_f_vecs = self.generate_data(valid_indexs, labels, f_vecs)

        # model
        self.model = Model.new(self.conf)
        valid_preds = self.model.fit({'train_labels': train_labels,
                                      'train_f_vecs': train_f_vecs,
                                      'valid_labels': valid_labels,
                                      'valid_f_vecs': valid_f_vecs},
                                     cv_id,
                                     cv_num)
        self.save_preds(valid_indexs, valid_preds, self.model.get_config_field_name(), 'valid', cv_id, cv_num)
        self.model.save('{}/{}_{}_{}.model'.format(self.run_path, self.model.get_config_field_name(), cv_id, cv_num))

        # evaluation
        score = ave_f1(valid_labels, valid_preds, 4, False)
        self.params['score'] = score
        self.conf.set(self.get_config_section_name(), self.get_config_field_name(), str(json.dumps(self.params, indent=4)))
        logging.info('validation score [ave_f1={}]'.format(score['ave_f1']))

        # save config
        self.save_conf()

    def run_online(self, cv_id=-1, cv_num=-1):
        if cv_id != self.params['cv_id']:
            logging.info('Reset cv_id={}, previous cv_id={}'.format(cv_id, self.params['cv_id']))
            self.params['cv_id'] = cv_id
        if cv_num != self.params['cv_num']:
            logging.info('Reset cv_num={}, previous cv_num={}'.format(cv_num, self.params['cv_num']))
            self.params['cv_num'] = cv_num
        # load feature
        f_vecs = load_all(self.conf.get('PATH', 'feature'),
                          self.conf.get(self.get_config_section_name(), 'feature').split(),
                          'test',
                          False)
        # predict
        if not self.model:
            self.model = Model.new(self.conf)
            self.model.load('{}/{}_{}_{}.model'.format(self.run_path,
                                                       self.model.get_config_field_name(),
                                                       cv_id,
                                                       cv_num))
        preds = self.model.predict(f_vecs, cv_id, cv_num)
        self.save_preds(None, preds, self.model.get_config_field_name(), 'test', cv_id, cv_num)

    def run(self):
        self.run_offline(self.params['cv_id'], self.params['cv_num'])
        self.run_online(self.params['cv_id'], self.params['cv_num'])
