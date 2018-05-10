#! /usr/bin/python
# -*- coding: utf-8 -*-
# @Time    : 5/9/18 12:00 AM
# @Author  : HouJP
# @Email   : houjp1992@gmail.com

import json
from bin.featwheel.io import write_csv


class Json2CSV(object):

    def __init__(self, conf):
        self.conf = conf

    def run(self):
        raw_path = self.conf.get('PATH', 'raw')
        txt_path = '{}/train.txt'.format(raw_path)
        data = load_txt(txt_path)

        csv_path = '{}/training.csv'.format(raw_path)
        write_csv(csv_path, data)


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
