#! /usr/bin/python
# -*- coding: utf-8 -*-
# @Time    : 5/12/18 10:20 AM
# @Author  : HouJP
# @Email   : houjp1992@gmail.com

from absl import logging
from bin.featwheel.string import title2underline


class Base(object):

    def __init__(self, conf, enable_params=False):
        self.conf = conf

        if enable_params:
            self.params = eval(self.conf.get(self.get_config_section_name(),
                                             self.get_config_field_name()))
            logging.info('[name={}] [params={}]'.format(self.__class__.__name__, self.params))
        else:
            self.params = {}

    def run(self):
        assert False, 'Please override Base.run'

    @staticmethod
    def get_config_section_name():
        assert False, 'Please override Base.get_config_section_name'

    def get_config_field_name(self):
        return title2underline(self.__class__.__name__)

    def get_data_name(self):
        return title2underline(self.__class__.__name__)
