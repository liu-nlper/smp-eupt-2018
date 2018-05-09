#! /usr/bin/python
# -*- coding: utf-8 -*-
# @Time    : 5/9/18 8:33 AM
# @Author  : HouJP
# @Email   : houjp1992@gmail.com

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.mlab as mlab
from bin.analysis.analyzer import Analyzer


class ContentLen(Analyzer):

    def __init__(self, conf):
        Analyzer.__init__(self, conf)

    def analyze_row(self, row):
        content = row['内容']
        if len(content) < 20 or len(content) > 1e5:
            print('id={}, 标签={}, len(content)={}'.format(row['id'], row['标签'], len(content)))
        return len(content)

    def aggregate(self, vecs):
        # max=101487, min=0, med=1096.0, ave=1872.12172434
        print('max={}, min={}, med={}, ave={}'.format(np.max(vecs),
                                                      np.min(vecs),
                                                      np.median(vecs),
                                                      np.average(vecs)))
        # id = 3911, 标签 = 人类作者, len(content) = 101487
        # id = 141703, 标签 = 人类作者, len(content) = 101487
        # id = 83445, 标签 = 机器作者, len(content) = 0
        # id = 118318, 标签 = 机器作者, len(content) = 0


class ContentLenDistribution(Analyzer):
    # How to draw: https://www.kesci.com/apps/home/project/59f6f21bc5f3f511952c2966

    def __init__(self, conf):
        Analyzer.__init__(self, conf)

    def analyze_row(self, row):
        ins = dict()
        ins['标签'] = row['标签']
        ins['len'] = len(row['内容'])
        return ins

    def aggregate(self, vecs):
        data = dict()
        for ins in vecs:
            label = ins['标签']
            c_len = ins['len']
            data[label] = data.get(label, list())
            data[label].append(c_len)

        bins = np.arange(0, 1e4, 2 * 1e2)

        label_cn = ['人类作者', '机器翻译', '自动摘要', '机器作者']
        label_en = ['Human Auth', 'Machine Trans', 'Auto Sub', 'Machine Auth']

        for label in zip(label_cn, label_en):
            label_data = data[label[0]]
            plt.hist(label_data, label=label[1], alpha=0.5, bins=bins)

        plt.rcParams['font.sans-serif'] = ['Microsoft YaHei']
        plt.rcParams['axes.unicode_minus'] = False

        plt.title('Content Length Analysis')
        plt.xlabel('Content Length')
        plt.ylabel('Count')

        plt.tick_params(top='off', right='off')
        plt.legend()
        plt.show()
