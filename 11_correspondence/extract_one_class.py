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

parser = argparse.ArgumentParser(description="Extract one class.")
parser.add_argument('-l', '--label', help='Label of the class to be extracted', type=int, required=True)
parser.add_argument('-p', '--pool_size', help='Parallel processing pool size', type=int, required=True)
parser.add_argument('-b', '--batch_size', help='Batch processing size', type=int, required=True)
args = parser.parse_args()

def _update_label(feature_label):
  datum = caffe.proto.caffe_pb2.Datum()
  datum.ParseFromString(feature_label[0])
  datum.label = feature_label[1]
  return datum.SerializeToString()

datasets = ['val', 'train']
perturbs = ['_perturbed', '']
features = ['pool5']

pool = Pool(args.pool_size)

for dataset in datasets:
  for perturb in perturbs:
    image_labels_filename = os.path.join(g_imgdb_building_folder, '%s_view_00_id.txt'%(dataset+perturb))
    image_labels = [int(line.strip()) for line in open(image_labels_filename, 'r')]
    for feature in features:
      lmdb_folder_input = os.path.join(g_feature_extraction_folder, '%s_%s_lmdb'%(dataset+perturb,feature))
      lmdb_size = get_lmdb_size(lmdb_folder_input)
      print lmdb_size, len(image_labels)
      assert(lmdb_size == len(image_labels))
      env_input = lmdb.open(lmdb_folder_input, readonly=True)

      lmdb_folder_output = os.path.join(g_feature_extraction_folder, '%s_%02d_%s_lmdb'%(dataset+perturb,args.label,feature))
      env_output = lmdb.open(lmdb_folder_output, map_size=int(1e12))

      with env_input.begin() as txn_input:
        cursor = txn_input.cursor()
        idx = 0
        count = 0
        feature_label_list = []
        for _, value in cursor:
          if image_labels[idx] == args.label:
            feature_label_list.append((value, count)) 
            count = count + 1
          if len(feature_label_list) == args.batch_size or idx == len(image_labels)-1:
            print datetime.datetime.now().time(), "Captured %d samples of the specified class..."%(len(feature_label_list))
            datum_strings = pool.map(_update_label, feature_label_list)
            with env_output.begin(write=True) as txn_output:
              for i in range(len(datum_strings)):
                txn_output.put('{:0>10d}'.format(count-len(datum_strings)+i), datum_strings[i]) 
            feature_label_list = []
          if idx%1000 == 0:
            print datetime.datetime.now().time(), "Processed %d of %d..."%(idx, len(image_labels))
          idx = idx + 1

      env_input.close()
      env_output.close()
