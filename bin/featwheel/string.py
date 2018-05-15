#! /usr/bin/python
# -*- coding: utf-8 -*-
# @Time    : 5/12/18 12:23 PM
# @Author  : HouJP
# @Email   : houjp1992@gmail.com


def title2underline(title):
    underline = ''
    for kv in enumerate(title):
        i = kv[0]
        c = kv[1]
        if c.isupper() and i:
            underline += '_'
        underline += c.lower()
    return underline


def test_title2underline():
    assert title2underline('ContentLength') == 'content_length'


def cal_cn_ratio(s):
    cn_num = 0
    all_num = 0
    for c in s.decode('utf-8'):
        if u'\u4e00' <= c <= u'\u9fff':
            cn_num += 1
        all_num += 1
    return 1. * cn_num / all_num if all_num > 0 else 0.


def test_cal_cn_ratio():
    s = '我们love您'
    assert cal_cn_ratio(s) == 3. / 7.

    s = '我爱你，'
    assert cal_cn_ratio(s) == 3. / 4.

    s = '5爱你'
    assert cal_cn_ratio(s) == 2. / 3.

    s = '我爱你$'
    assert cal_cn_ratio(s) == 3. / 4.


if __name__ == '__main__':
    test_title2underline()
    test_cal_cn_ratio()
