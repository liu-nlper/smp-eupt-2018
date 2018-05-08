#! /usr/bin/python
# -*- coding: utf-8 -*-
# @Time    : 5/8/18 9:16 PM
# @Author  : HouJP
# @Email   : houjp1992@gmail.com

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from absl import app
from absl import flags

FLAGS = flags.FLAGS

flags.DEFINE_string('package', 'bin.demo', 'specify the package path to be run')
flags.DEFINE_string('object', 'HelloWorld', 'specify the class name to be run')


def main(_):
    getattr(__import__(FLAGS.package, fromlist=["*"]), FLAGS.object).run()


if __name__ == '__main__':
    app.run(main)
