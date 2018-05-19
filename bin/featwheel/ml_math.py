#! /usr/bin/python
# -*- coding: utf-8 -*-
# @Time    : 5/19/18 1:41 PM
# @Author  : HouJP
# @Email   : houjp1992@gmail.com

import math


def entropy(p_list, base=2):
    ans = 0.
    for p in p_list:
        if p <= 0.:
            continue
        ans -= p * math.log(p, base)
    return ans


def entropy_test():
    p_list = [0.]
    assert entropy(p_list) == 0.

    p_list = [1./2, 1./4, 1./8, 1./8]
    assert entropy(p_list) == 7./4


if __name__ == '__main__':
    entropy_test()
