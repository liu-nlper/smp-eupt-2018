#! /usr/bin/python
# -*- coding: utf-8 -*-
# @Time    : 5/9/18 12:22 AM
# @Author  : HouJP
# @Email   : houjp1992@gmail.com

import csv
from enum import Enum
from absl import logging


class ValidType(Enum):
    STR = 'str'
    INT = 'int'
    FLOAT = 'float'


def save_vector(file_name, vec, mode):
    """
    Save vector on disk
    :param file_name: vector file path
    :param vec: a vector in List type
    :param mode: mode of writing file
    :return: none
    """
    f = open(file_name, mode)
    for value in vec:
        f.write(str(value) + "\n")
    f.close()


def load_vector(file_name, ele_type):
    """
    Load vector from disk
    :param file_name: vector file path
    :param ele_type: element type in vector
    :return: a vector in List type
    """
    ele_type = eval(ele_type.value.lower())
    vec = []
    f = open(file_name)
    for line in f:
        value = ele_type(line.strip())
        vec.append(value)
    f.close()
    logging.info('Load vector done [len={}] [path={}]'.format(len(vec), file_name))
    return vec


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


def read_csv(file_name):
    data = {}
    with open(file_name) as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            for key in row:
                if key in data:
                    data[key].append(row[key])
                else:
                    data[key] = [row[key]]
        logging.info('read csv done [{}]'.format(file_name))
    return data


def csv2dict(data, key):
    data_dict = dict()
    data_len = len(data[data.keys()[0]])
    for data_id in range(data_len):
        data_dict[data[key][data_id]] = dict()
        for field_name in data:
            if field_name == key:
                continue
            else:
                data_dict[data[key][data_id]][field_name] = data[field_name][data_id]
    return data_dict


def csv2dict_test():
    data = {'f1': [1, 2], 'f2': [3, 4], 'f3': [5, 6]}
    data_dict = csv2dict(data, key='f1')

    assert data_dict == {1: {'f2': 3,
                             'f3': 5},
                         2: {'f2': 4,
                             'f3': 6}}


if __name__ == '__main__':
    csv2dict_test()
