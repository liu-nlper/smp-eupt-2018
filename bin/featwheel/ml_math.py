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


def mode(nums):
    count = dict()
    for num in nums:
        count[num] = count.get(num, 0) + 1

    max_count = 0
    for num in count.keys():
        if count[num] > max_count:
            max_count = count[num]

    mode_list = list()
    for num in count.keys():
        if count[num] == max_count:
            mode_list.append(num)
    return mode_list, max_count


def mode_test():
    nums = [1., 2., 3., 1., 2., 3., 3., 4., 4., 4.]
    assert mode(nums) == ([3., 4.], 3)

    nums = [1., 2., 3., 1., 2., 3., 3., 4., 4., 4., 3.]
    assert mode(nums) == ([3.], 4)


if __name__ == '__main__':
    entropy_test()
    mode_test()
