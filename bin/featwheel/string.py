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


if __name__ == '__main__':
    print(title2underline('ContentLength'))
