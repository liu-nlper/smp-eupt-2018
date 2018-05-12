#! /usr/bin/python
# -*- coding: utf-8 -*-
# @Time    : 5/12/18 12:15 AM
# @Author  : HouJP
# @Email   : houjp1992@gmail.com

import os
import time
from absl import logging
from bin.featwheel.base import Base


class Runner(Base):

    def __init__(self, conf):
        Base.__init__(self, conf, enable_params=True)

        self.run_path = self.__init_run_dir()
        self.save_conf()

    def __init_run_dir(self):
        """
        If tag is empty, create tag & directory for this run.

        :return: the path of this run
        """
        if self.conf.get('RUN', 'tag') != '':
            run_tag = self.conf.get('RUN', 'tag')
        else:
            run_tag = time.strftime("%Y-%m-%d_%H-%M-%S", time.localtime(time.time()))
            self.conf.set('RUN', 'tag', run_tag)

            # generate run dir
            run_path = '%s/%s/' % (self.conf.get('PATH', 'out'), run_tag)
            if os.path.exists(run_path):
                raise ValueError('Run path already exist [path={}]'.format(run_path))
            else:
                os.mkdir(run_path)
            logging.info('Create run path [path={}]'.format(run_path))

        run_path = '%s/%s/' % (self.conf.get('PATH', 'out'), run_tag)
        return run_path

    def save_conf(self):
        self.conf.write(open(self.run_path + 'featwheel.conf', 'w'))

    def run_offline(self):
        assert False, 'Please override Runner.run_offline'

    def run_online(self):
        assert False, 'Please override Runner.run_online'
