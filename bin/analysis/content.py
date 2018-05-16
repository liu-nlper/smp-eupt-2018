#! /usr/bin/python
# -*- coding: utf-8 -*-
# @Time    : 5/9/18 8:33 AM
# @Author  : HouJP
# @Email   : houjp1992@gmail.com

import numpy as np
from bin.analysis.analyzer import Analyzer


class ContentLen(Analyzer):

    def __init__(self, conf):
        Analyzer.__init__(self, conf)

    def analyze_row(self, row):
        content = row['内容']
        if len(content) < 20 or len(content) > 1e5:
            # id = 3911, 标签 = 人类作者, len(content) = 101487
            # id = 141703, 标签 = 人类作者, len(content) = 101487
            # id = 83445, 标签 = 机器作者, len(content) = 0
            # id = 118318, 标签 = 机器作者, len(content) = 0
            print('id={}, 标签={}, len(content)={}'.format(row['id'], row['标签'], len(content)))
        return len(content)

    def aggregate(self, vecs):
        # max=101487, min=0, med=1096.0, ave=1872.12172434
        print('max={}, min={}, med={}, ave={}'.format(np.max(vecs),
                                                      np.min(vecs),
                                                      np.median(vecs),
                                                      np.average(vecs)))


class ContentLenDistribution(Analyzer):

    def __init__(self, conf):
        Analyzer.__init__(self, conf)

    def analyze_row(self, row):
        ins = dict()
        ins['标签'] = row['标签']
        ins['len'] = len(row['内容'])
        return ins

    def aggregate(self, vecs):
        # How to draw: https://www.kesci.com/apps/home/project/59f6f21bc5f3f511952c2966
        data = dict()
        for ins in vecs:
            label = ins['标签']
            c_len = ins['len']
            data[label] = data.get(label, list())
            data[label].append(c_len)

        # label=人类作者: max=101487, min=105, med=1380.0, ave=2616.42465326
        # label=机器翻译: max=3382, min=371, med=1084.0, ave=1095.47655085
        # label=自动摘要: max=1443, min=65, med=237.0, ave=254.209995489
        # label=机器作者: max=6971, min=0, med=3487.0, ave=3238.79212528
        for label in data:
            print('label={}: max={}, min={}, med={}, ave={}'.format(label,
                                                                    np.max(data[label]),
                                                                    np.min(data[label]),
                                                                    np.median(data[label]),
                                                                    np.average(data[label])))


class LastChar(Analyzer):

    def __init__(self, conf):
        Analyzer.__init__(self, conf)

    def analyze_row(self, row):
        ins = dict()
        last_ch = row['内容'].decode('utf-8')[-1] if len(row['内容']) > 0 else '#_#'
        ins['last_ch'] = last_ch.encode('utf-8')
        return ins

    def aggregate(self, vecs):
        last_chs = set()
        for ins in vecs:
            last_chs.add(ins['last_ch'])
        print('|-|'.join(last_chs))
