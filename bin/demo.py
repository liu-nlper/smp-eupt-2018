#! /usr/bin/python
# -*- coding: utf-8 -*-
# @Time    : 5/8/18 10:07 PM
# @Author  : HouJP
# @Email   : houjp1992@gmail.com


class HelloWorld(object):
    """
    This is an example class.
    """

    def __init__(self, conf):
        self.conf = conf

    @staticmethod
    def run():
        print('hello, world!')
