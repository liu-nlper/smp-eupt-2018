#! /usr/bin/python
# -*- coding: utf-8 -*-
# @Time    : 5/19/18 9:24 AM
# @Author  : HouJP
# @Email   : houjp1992@gmail.com

from bin.analysis.analyzer import Analyzer


class CharNum(Analyzer):

    def __init__(self, conf):
        Analyzer.__init__(self, conf)

    def analyze_row(self, row):
        content = row['内容'].decode('utf-8')
        return set(content)

    def aggregate(self, vecs):
        chars = set()
        for vec in vecs:
            chars = chars | vec
        # len(chars)=8569
        print('len(chars)={}'.format(len(chars)))
