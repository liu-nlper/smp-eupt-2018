#! /usr/bin/python
# -*- coding: utf-8 -*-
# @Time    : 5/9/18 12:22 AM
# @Author  : HouJP
# @Email   : houjp1992@gmail.com

import csv
from absl import logging


def write_csv(file_name, data):
    """
    Writes data in csv format.
    :param file_name: file name
    :param data: data
    :return: none
    """
    with open(file_name, 'w') as csvfile:
        fieldnames = data.keys()
        assert len(fieldnames) > 0, 'fields is null'

        data_len = len(data[fieldnames[0]])
        logging.info('data_len={}'.format(data_len))
        for field_name in fieldnames:
            assert len(data[field_name]) == data_len, 'len(%s)=%d' % (field_name, len(data[field_name]))

        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for i in range(data_len):
            row = {}
            for field_name in fieldnames:
                row[field_name] = data[field_name][i]
            writer.writerow(row)
        logging.info('write csv done [{}]'.format(file_name))
