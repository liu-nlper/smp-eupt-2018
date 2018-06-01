#! /usr/bin/python
# -*- coding: utf-8 -*-
# @Time    : 5/12/18 11:26 PM
# @Author  : HouJP
# @Email   : houjp1992@gmail.com

import json
import random
from absl import logging
from bin.experiment.runner import Runner
from bin.experiment.singlerun import SingleRun
from bin.model.model import Model
from bin.featwheel.io import read_csv, write_csv
from bin.featwheel.ml_math import mode
from bin.analysis.label import Label


class CrossValidation(Runner):

    def __init__(self, conf):
        Runner.__init__(self, conf)

    def run_offline(self, enable_online=False):
        cv_num = self.params['cv_num']
        eval_metric = self.params['eval_metric']

        score = dict()
        score_sum = 0.
        for cv_id in range(cv_num):
            per_run = SingleRun(self.conf)
            per_run.run_offline(cv_id=cv_id, cv_num=cv_num)
            if enable_online:
                per_run.run_online(cv_id=cv_id, cv_num=cv_num)
            score['cv_{}_{}'.format(cv_id, cv_num)] = per_run.params['score']
            score_sum += per_run.params['score'][eval_metric]
        score['ave_{}'.format(eval_metric)] = score_sum / cv_num
        self.params['score'] = score
        self.conf.set(self.get_config_section_name(),
                      self.get_config_field_name(),
                      str(json.dumps(self.params, indent=4)))
        logging.info('validation score [ave_{}={}]'.format(eval_metric, score['ave_{}'.format(eval_metric)]))

        # save config
        self.save_conf()

    def merge_outs(self):
        label_cn2id = Label.cn2id
        label_id2cn = {v: k for k, v in label_cn2id.iteritems()}

        cv_num = self.params['cv_num']
        outs = list()
        for cv_id in range(cv_num):
            preds_name = '{}/{}_{}_{}.{}.preds'.format(self.run_path,
                                                      self.conf.get(Model.get_config_section_name(), 'type'),
                                                      cv_id,
                                                      cv_num,
                                                      'test')
            outs.append(read_csv(preds_name))

        raw_path = self.conf.get('PATH', 'raw')
        csv_name = '{}/raw.test.csv'.format(raw_path)
        raw = read_csv(csv_name)

        out_merged = dict()
        out_merged['id'] = list()
        out_merged['标签'] = list()
        for index_id in range(len(raw['id'])):
            out_merged['id'].append(raw['id'][index_id])
            preds = list()
            for cv_id in range(cv_num):
                preds.append(float(outs[cv_id]['label_id_pred'][index_id]))
            label_id_pred = random.sample(mode(preds)[0], 1)[0]
            label = label_id2cn[int(label_id_pred)]
            out_merged['标签'].append(label)

        out_name = '{}/{}_{}.{}.preds.csv'.format(self.run_path,
                                                  self.conf.get(Model.get_config_section_name(), 'type'),
                                                  cv_num,
                                                  'test')
        out_file = open(out_name, 'w')
        for index_id in range(len(raw['id'])):
            out_file.write('{},{}\n'.format(out_merged['id'][index_id], out_merged['标签'][index_id]))
        out_file.close()

    def run_online(self):
        cv_num = self.params['cv_num']
        for cv_id in range(cv_num):
            per_run = SingleRun(self.conf)
            per_run.run_online(cv_id=cv_id, cv_num=cv_num)
        self.merge_outs()

    def run(self):
        enable_online = (self.params['enable_online'] == 'true')

        self.run_offline(enable_online=enable_online)
        if enable_online:
            self.merge_outs()
