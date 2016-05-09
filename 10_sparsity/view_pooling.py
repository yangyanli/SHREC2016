#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import sys
import lmdb
import argparse
import datetime
import numpy as np
from multiprocessing import Pool

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(BASE_DIR))
from global_variables import *
sys.path.append(os.path.dirname(BASE_DIR))
sys.path.append(os.path.join(os.path.dirname(BASE_DIR), 'utilities_python'))
from utilities_caffe import *
sys.path.append(os.path.join(g_caffe_installation_path, 'python'))
import caffe

parser = argparse.ArgumentParser(description="View pooling.")
parser.add_argument('-p', '--pool_size', help='Parallel processing pool size', type=int, required=True)
parser.add_argument('-b', '--batch_size', help='Batch processing size', type=int, required=True)
args = parser.parse_args()

def _view_pooling(view_features):
  array = np.empty([0])
  label = -1
  datum = caffe.proto.caffe_pb2.Datum()
  for value in view_features:
    datum.ParseFromString(value)
    datum_np_array = caffe.io.datum_to_array(datum)
    if array.size == 0:
      label = datum.label 
      array = datum_np_array
    else:
      assert(label == datum.label)
      array = np.maximum(array, datum_np_array)
  datum = caffe.io.array_to_datum(array.astype(float), label)
  return datum.SerializeToString()

datasets = ['val', 'test', 'train']
perturbs = ['_perturbed', '']
features = ['pool5']
view_num = 12

pool = Pool(args.pool_size)

for dataset in datasets:
  for perturb in perturbs:
    for feature in features:
      lmdb_folder = os.path.join(g_feature_extraction_folder, '%s_%s_lmdb'%(dataset+perturb,feature))
      env = lmdb.open(lmdb_folder, map_size=int(1e12))
      env_views = []
      cursor_views = []
      for view_idx in range(view_num):
        lmdb_view_folder = os.path.join(g_feature_extraction_folder, '%s_view_%02d_%s_lmdb'%(dataset+perturb,view_idx,feature))
        env_views.append(lmdb.open(lmdb_view_folder, readonly=True))      
        cursor_views.append(env_views[-1].begin().cursor())
        cursor_views[-1].next()

      lmdb_size = get_lmdb_size(lmdb_view_folder)
      array_idx_list = []
      key_list = []
      for i in range(0, lmdb_size, args.batch_size):
        print datetime.datetime.now().time(), "Processed %d of %d..."%(i, lmdb_size)
        count = args.batch_size
        if i + count > lmdb_size:
          count = lmdb_size-i
        view_features_list = []
        key_list = []

        for j in range(count):
          view_features_list.append([cursor_views[0].value()])
          key_list.append(cursor_views[0].key())
          cursor_views[0].next()
        for view_idx in range(1, view_num):
          for j in range(count):
            view_features_list[j].append(cursor_views[view_idx].value())
            assert(key_list[j] == cursor_views[view_idx].key())
            cursor_views[view_idx].next()
            
        datum_strings = pool.map(_view_pooling, view_features_list)
        with env.begin(write=True) as txn:
          for idx in range(len(datum_strings)):
            #print key_list[idx], len(datum_strings[idx])
            txn.put(key_list[idx], datum_strings[idx])
        view_features_list = []
        key_list = []

      for view_idx in range(view_num):
        cursor_views[view_idx].close()
        env_views[view_idx].close()
      env.close()
