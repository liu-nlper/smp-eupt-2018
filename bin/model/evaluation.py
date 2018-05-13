#! /usr/bin/python
# -*- coding: utf-8 -*-
# @Time    : 5/12/18 3:27 PM
# @Author  : HouJP
# @Email   : houjp1992@gmail.com

from absl import logging


def ave_f1(labels, preds, class_num, enable_log=True):
    assert len(labels) == len(preds), '[len(labels)={}] [len(preds)={}]'.format(len(labels), len(preds))

    score = dict()
    sum_f1 = 0.
    for class_id in range(class_num):
        tp = 0
        tp_fp = 0
        tp_fn = 0
        for i in range(len(labels)):
            if labels[i] == preds[i] and labels[i] == class_id:
                tp += 1
            if preds[i] == class_id:
                tp_fp += 1
            if labels[i] == class_id:
                tp_fn += 1
        p = 1. * tp / tp_fp
        r = 1. * tp / tp_fn
        f1 = 2. * p * r / (p + r)
        score['p_{}'.format(class_id)] = p
        score['r_{}'.format(class_id)] = r
        score['f1_{}'.format(class_id)] = f1
        sum_f1 += f1
    score['ave_f1'] = sum_f1 / class_num
    if enable_log:
        logging.info('[score={}]'.format(score))

    return score
