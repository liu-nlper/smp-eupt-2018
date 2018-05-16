#! /usr/bin/python
# -*- coding: utf-8 -*-
# @Time    : 5/9/18 8:58 AM
# @Author  : HouJP
# @Email   : houjp1992@gmail.com

import csv


class Analyzer(object):

    def __init__(self, conf):
        self.conf = conf

    def analyze_row(self, row):
        assert False, 'Please override function: Analyzer.analyze_row'

    def aggregate(self, vecs):
        assert False, 'Please override function: Analyzer.aggregate'

    def analyze(self, data_name, data_type):
        vecs = list()
        with open('{}/{}.{}.csv'.format(self.conf.get('PATH', 'raw'), data_name, data_type)) as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                vec = self.analyze_row(row)
                vecs.append(vec)
        self.aggregate(vecs)

    def run(self):
        self.analyze('raw', 'train')
