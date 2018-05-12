#! /usr/bin/python
# -*- coding: utf-8 -*-
# @Time    : 5/12/18 11:07 AM
# @Author  : HouJP
# @Email   : houjp1992@gmail.com

import csv
import json
from absl import logging
from bin.analysis.label import Label


def load_txt(file_path):
    data = dict()
    with open(file_path, 'r') as f:
        for line in f:
            instance = json.loads(line)
            for key in instance:
                key_encode = key.encode('utf-8')
                data[key_encode] = data.get(key_encode, list())
                if isinstance(instance[key], unicode):
                    data[key_encode].append(instance[key].encode('utf-8'))
                else:
                    data[key_encode].append(instance[key])
    return data


def load_label_id(file_path):
    labels = list()
    with open(file_path) as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            label = row['标签']
            label = Label.cn2id[label]
            labels.append(label)
    logging.info('Load IDs for labels done [path={}]'.format(file_path))
    return labels


def get_data_size(file_path):
    data_size = 0
    with open(file_path) as csvfile:
        reader = csv.DictReader(csvfile)
        for _ in reader:
            data_size += 1
    return data_size
