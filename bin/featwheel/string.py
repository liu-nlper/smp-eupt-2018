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


def is_cn(c):
    return u'\u4e00' <= c <= u'\u9fff'


def cal_cn_ratio(s):
    cn_num = 0
    all_num = 0
    for c in s.decode('utf-8'):
        if is_cn(c):
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


def cal_digit_ratio(s):
    d_num = 0
    all_num = 0
    for c in s.decode('utf-8'):
        if u'\u0030' <= c <= u'\u0039':
            d_num += 1
        all_num += 1
    return 1. * d_num / all_num if all_num > 0 else 0.


def test_cal_digit_ratio():
    s = '123是'
    assert cal_digit_ratio(s) == 3. / 4.

    s = '123$'
    assert cal_digit_ratio(s) == 3. / 4.

    s = '0123456789a'
    assert cal_digit_ratio(s) == 10. / 11.

    s = '0123456789；'
    assert cal_digit_ratio(s) == 10. / 11.


def cal_en_ratio(s):
    en_num = 0
    all_num = 0
    for c in s.decode('utf-8'):
        if u'\u0041' <= c <= u'\u005a' or u'\u0061' <= c <= u'\u007a':
            en_num += 1
        all_num += 1
    return 1. * en_num / all_num if all_num > 0 else 0.


def test_cal_en_ratio():
    s = '123azAZ'
    assert cal_en_ratio(s) == 4. / 7.


def ave_continuous_cn_length(s):
    len_sum = 0
    len_num = 0
    l = 0
    for c in s.decode('utf-8'):
        if is_cn(c):
            l += 1
        else:
            if l > 0:
                len_sum += l
                len_num += 1
            l = 0
    if l > 0:
        len_sum += l
        len_num += 1
    return 1. * len_sum / len_num if len_num > 0 else 0.


def test_ave_continuous_cn_length():
    s = '$我爱你123哈哈、a我们'
    assert ave_continuous_cn_length(s) == 1. * (3 + 2 + 2) / 3


if __name__ == '__main__':
    test_title2underline()
    test_cal_cn_ratio()
    test_cal_digit_ratio()
    test_cal_en_ratio()
    test_ave_continuous_cn_length()
