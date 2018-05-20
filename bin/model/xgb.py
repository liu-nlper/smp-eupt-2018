#! /usr/bin/python
# -*- coding: utf-8 -*-
# @Time    : 5/12/18 2:37 PM
# @Author  : HouJP
# @Email   : houjp1992@gmail.com

import json
import xgboost as xgb
from absl import logging
from bin.model.model import Model
from bin.model.evaluation import ave_f1 as eval_ave_f1


class XGB(Model):

    def __init__(self, conf):
        Model.__init__(self, conf)

    def fit(self, data, cv_id, cv_num):
        train_dmatrix = xgb.DMatrix(data['train_f_vecs'], label=data['train_labels'])
        valid_dmatrix = xgb.DMatrix(data['valid_f_vecs'], label=data['valid_labels'])

        watchlist = [(train_dmatrix, 'train'), (valid_dmatrix, 'valid')]

        self.model = xgb.train(self.params,
                               train_dmatrix,
                               self.params['num_round'],
                               watchlist,
                               early_stopping_rounds=self.params['early_stop'],
                               verbose_eval=self.params['verbose_eval'])
        logging.info('[best_ntree_limit_{}_{}={}]'.format(cv_id, cv_num, self.model.best_ntree_limit))

        valid_preds = self.model.predict(valid_dmatrix, ntree_limit=self.model.best_ntree_limit)
        self.params['best_ntree_limit_{}_{}'.format(cv_id, cv_num)] = self.model.best_ntree_limit
        self.conf.set(self.get_config_section_name(),
                      self.get_config_field_name(),
                      str(json.dumps(self.params, indent=4)))
        return valid_preds

    def save(self, file_path):
        self.model.save_model(file_path)

    def load(self, file_path):
        self.model = xgb.Booster(self.params)
        self.model.load_model(file_path)
