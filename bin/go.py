#! /usr/bin/python
# -*- coding: utf-8 -*-
# @Time    : 5/8/18 9:16 PM
# @Author  : HouJP
# @Email   : houjp1992@gmail.com

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from six.moves import configparser
from absl import app
from absl import flags

FLAGS = flags.FLAGS

flags.DEFINE_string('package', 'bin.demo', 'specify the package path to be run')
flags.DEFINE_string('object', 'HelloWorld', 'specify the class name to be run')
flags.DEFINE_string('func', 'run', 'specify the function name to be run')
flags.DEFINE_string('conf', 'conf/template.conf', 'specify the path of config file')

# For feature word document frequency
flags.DEFINE_string('unit', 'word', 'specify the unit for word document frequency, e.g. word/2gram/3gram/...')
flags.DEFINE_string('enable_set', 'true', 'specify whether enable set for words')
flags.DEFINE_integer('min_doc_frequency', 50, 'specify the minimum document frequency')


def main(_):
    conf = configparser.ConfigParser()
    conf.read(FLAGS.conf)
    getattr(getattr(__import__(FLAGS.package, fromlist=["*"]), FLAGS.object)(conf), FLAGS.func)()


if __name__ == '__main__':
    app.run(main)
