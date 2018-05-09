#! /usr/bin/python
# -*- coding: utf-8 -*-
# @Time    : 5/9/18 8:33 AM
# @Author  : HouJP
# @Email   : houjp1992@gmail.com

import numpy as np
from absl import logging
from bin.analysis.analyzer import Analyzer


class ContentLen(Analyzer):

    def __init__(self, conf):
        Analyzer.__init__(self, conf)

    def analyze_row(self, row):
        content = row['内容']
        if len(content) == 0:
            print(row['id'])
        return len(content)

    def aggregate(self, vecs):
        # max=101487, min=0, med=1096.0, ave=1872.12172434
        logging.info('max={}, min={}, med={}, ave={}'.format(np.max(vecs),
                                                             np.min(vecs),
                                                             np.median(vecs),
                                                             np.average(vecs)))
        # len(content)=0:
        #   * id=83445  机器作者
        #   * id=118318 机器作者
