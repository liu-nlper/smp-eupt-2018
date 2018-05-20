#! /usr/bin/python
# -*- coding: utf-8 -*-
# @Time    : 5/19/18 7:57 AM
# @Author  : HouJP
# @Email   : houjp1992@gmail.com

import csv
from bin.featwheel.base import Base
from bin.featwheel.io import write_csv


class Counter(Base):

    def __init__(self, conf, enable_params=False):
        Base.__init__(self, conf, enable_params=enable_params)

    def count_row(self, row):
        assert False, 'Please override function: Counter.count_row'

    def aggregate(self, rows):
        assert False, 'Please override function: Counter.aggregate'

    def count(self, data_name, data_type):
        rows = list()
        with open('{}/{}.{}.csv'.format(self.conf.get('PATH', 'raw'), data_name, data_type)) as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                rows.append(self.count_row(row))
        data = self.aggregate(rows)
        file_name = '{}/{}.{}.csv'.format(self.conf.get('PATH', 'raw'), self.get_date_name(), data_type)
        write_csv(file_name, data)

    def run(self):
        self.count('raw', 'train')
