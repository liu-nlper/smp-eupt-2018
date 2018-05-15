#! /usr/bin/python
# -*- coding: utf-8 -*-
# @Time    : 5/12/18 11:26 PM
# @Author  : HouJP
# @Email   : houjp1992@gmail.com

import json
from absl import logging
from bin.experiment.runner import Runner
from bin.experiment.singlerun import SingleRun


class CrossValidation(Runner):

    def __init__(self, conf):
        Runner.__init__(self, conf)

    def run_offline(self):
        cv_num = self.params['cv_num']
        eval_metric = self.params['eval_metric']

        score = dict()
        score_sum = 0.
        for cv_id in range(cv_num):
            per_run = SingleRun(self.conf)
            per_run.run_offline(cv_id=cv_id, cv_num=cv_num)
            score['cv_{}_{}'.format(cv_id, cv_num)] = per_run.params['score']
            score_sum += per_run.params['score'][eval_metric]
        score['ave_{}'.format(eval_metric)] = score_sum / cv_num
        self.params['score'] = score
        self.conf.set(self.get_section_name(), self.get_class_name(), str(json.dumps(self.params, indent=4)))
        logging.info('validation score [ave_{}={}]'.format(eval_metric, score['ave_{}'.format(eval_metric)]))

        # save config
        self.save_conf()

    def run(self):
        self.run_offline()
