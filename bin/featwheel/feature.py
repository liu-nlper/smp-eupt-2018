#! /usr/bin/python
# -*- coding: utf-8 -*-
# @Time    : 5/10/18 10:06 PM
# @Author  : HouJP
# @Email   : houjp1992@gmail.com

import hashlib
import random
import numpy as np
from os.path import isfile
from absl import logging
from scipy.sparse import csr_matrix, hstack, vstack


def save_vector(f, vec):
    if isinstance(vec, str):
        f.write('{}\n'.format(vec))
    elif isinstance(vec, list):
        vec = ' '.join(['{}:{}'.format(kv[0], kv[1]) for kv in enumerate(vec) if kv[1] != 0])
        f.write('{}\n'.format(vec))
    else:
        raise ValueError('Feature vector has wrong type: %s' % type(vec))


def load_all(feature_pt, feature_names, rawset_name, cache=False):
    index_begin = 0
    features = None
    for index in reversed(range(1, len(feature_names))):
        f_names_s = '|'.join(feature_names[0:index + 1]) + '|' + rawset_name
        f_names_md5 = hashlib.md5(f_names_s).hexdigest()
        if isfile('%s/md5_%s.smat.npz' % (feature_pt, f_names_md5)):
            index_begin = index
            features = load('%s/md5_%s.smat' % (feature_pt, f_names_md5))
            break
    if index_begin >= 1:
        logging.info('Load {} features: [{}, {}]'.format(rawset_name, feature_names[0], feature_names[index_begin]))
    else:
        features = load('%s/%s.%s.smat' % (feature_pt, feature_names[0], rawset_name))

    for index in range(index_begin + 1, len(feature_names)):
        features = merge_col(features,
                             load('%s/%s.%s.smat' % (feature_pt, feature_names[index], rawset_name)))

    features = features.tocsr()

    if cache and (index_begin < len(feature_names) - 1):
        f_names_s = '|'.join(feature_names) + '|' + rawset_name
        f_names_md5 = hashlib.md5(f_names_s).hexdigest()
        save_npz(features, '%s/md5_%s.smat' % (feature_pt, f_names_md5))
    return features


def load(ft_fp):
    """
    WARNING: the NPZ file is a cache file, be careful of these files
    :param ft_fp: feature file path
    :return: matrix of features
    """
    has_npz = isfile('%s.npz' % ft_fp)
    if has_npz:
        features = load_npz(ft_fp)
    else:
        features = load_smat(ft_fp)
        save_npz(features, ft_fp)
    return features


def load_npz(ft_fp):
    loader = np.load('%s.npz' % ft_fp)
    features = csr_matrix((loader['data'],
                           loader['indices'],
                           loader['indptr']),
                          shape=loader['shape'])
    logging.info('Load npz feature file done [path={}]'.format(ft_fp))
    return features


def save_npz(features, ft_fp):
    """
    save features to disk in binary format
    :param features: matrix of features
    :param ft_fp: feature file path
    :return: none
    """
    np.savez(ft_fp,
             data=features.data,
             indices=features.indices,
             indptr=features.indptr,
             shape=features.shape)
    logging.info('Save npz feature file done [path={}]'.format(ft_fp))


def load_smat(ft_fp):
    """
    load features from disk, the format:
        row_num col_num
        f1_index:f1_value f2_index:f2_value ...
    """
    data = []
    indice = []
    indptr = [0]
    f = open(ft_fp)
    [row_num, col_num] = [int(num) for num in f.readline().strip().split()]
    for line in f:
        line = line.strip()
        subs = line.split()
        for sub in subs:
            [f_index, f_value] = sub.split(":")
            f_index = int(f_index)
            f_value = float(f_value)
            data.append(f_value)
            indice.append(f_index)
        indptr.append(len(data))
    f.close()
    features = csr_matrix((data, indice, indptr), shape=(row_num, col_num), dtype=float)
    logging.info('Load smat feature file done [shape=({}, {})] [path={}]'.format(row_num, col_num, ft_fp))
    return features


def save_smat(features, ft_pt):
    """
    save features to disk in SMAT format
    :param features: the matrix of features
    :param ft_pt: features file path
    :return: none
    """
    (row_num, col_num) = features.shape
    data = features.data
    indice = features.indices
    indptr = features.indptr
    f = open(ft_pt, 'w')
    f.write("%d %d\n" % (row_num, col_num))
    ind_indptr = 1
    begin_line = True
    for ind_data in range(len(data)):
        while ind_data == indptr[ind_indptr]:
            f.write('\n')
            begin_line = True
            ind_indptr += 1
        if (data[ind_data] < 1e-12) and (data[ind_data] > -1e-12):
            continue
        if (not begin_line) and (ind_data != indptr[ind_indptr - 1]):
            f.write(' ')
        f.write("%d:%s" % (indice[ind_data], data[ind_data]))
        begin_line = False
    while ind_indptr < len(indptr):
        f.write("\n")
        ind_indptr += 1
    logging.info('Save smat feature file done [path={}]'.format(ft_pt))
    f.close()


def sample_row(features, indexs):
    features_sampled = features[indexs, :]
    (row_num, col_num) = features_sampled.shape
    logging.info('Row sample done [shape=({},{})]'.format(row_num, col_num))
    return features_sampled


def sample_col(features, indexs):
    features_sampled = features[:, indexs]
    (row_num, col_num) = features_sampled.shape
    logging.info('Col sample done [shape=({},{})]'.format(row_num, col_num))
    return features_sampled


def merge_row(feature_1, feature_2):
    """
    merge features made split by row
    :param feature_1: the first part of features
    :param feature_2: the second part of features
    :return: feature matrix
    """
    features = vstack([feature_1, feature_2])
    (row_num, col_num) = features.shape
    logging.info('Merge row done [shape=({},{})]'.format(row_num, col_num))
    return features


def merge_col(features_1, features_2):
    """
    merge features made split by column
    :param features_1: the first part of features
    :param features_2: the second part of features
    :return: feature matrix
    """
    features = hstack([features_1, features_2])
    (row_num, col_num) = features.shape
    logging.info('Merge col done [shape=({},{})]'.format(row_num, col_num))
    return features
