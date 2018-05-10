#! /usr/bin/python
# -*- coding: utf-8 -*-
# @Time    : 5/10/18 10:06 PM
# @Author  : HouJP
# @Email   : houjp1992@gmail.com


def save_vector(f, vec):
    if isinstance(vec, str):
        f.write('{}\n'.format(vec))
    elif isinstance(vec, list):
        vec = ' '.join(['{}:{}'.format(kv[0], kv[1]) for kv in enumerate(vec) if kv[1] != 0])
        f.write('{}\n'.format(vec))
    else:
        raise ValueError('Feature vector has wrong type: %s' % type(vec))
