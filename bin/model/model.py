#! /usr/bin/python
# -*- coding: utf-8 -*-
# @Time    : 5/12/18 12:56 PM
# @Author  : HouJP
# @Email   : houjp1992@gmail.com

from enum import Enum
from bin.featwheel.base import Base


class ModelType(Enum):
    XGB = 'xgb'


class Model(Base):

    def __init__(self, conf):
        Base.__init__(self, conf, enable_params=True)

        self.model = None

    @staticmethod
    def get_config_section_name():
        return 'MODEL'

    def get_config_field_name(self):
        return self.conf.get(self.get_config_section_name(), 'type')

    @staticmethod
    def new(conf):
        model_type = ModelType(conf.get(Model.get_config_section_name(), 'type'))
        exec ("from %s import %s" % (model_type.value, model_type.name))
        return eval(model_type.name)(conf)

    def fit(self, data_set, cv_id, cv_num):
        assert False, 'Please override function: Model.fit'

    def save(self, file_path):
        assert False, 'Please override function: Model.save'

    def load(self, file_path):
        assert False, 'Please override function: Model.load'

    def predict(self, f_vecs, cv_id, cv_num, labels=None):
        assert False, 'Please override function: Model.predict'
