#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import sys
import shutil
import argparse
import fileinput

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(BASE_DIR))
from global_variables import *
sys.path.append(os.path.dirname(BASE_DIR))
sys.path.append(os.path.join(os.path.dirname(BASE_DIR), 'utilities_python'))
from utilities_caffe import *

parser = argparse.ArgumentParser(description="Feature extraction.")
parser.add_argument('-g', '--gpu_index', help='GPU to use', type=int, required=True)
parser.add_argument('-s', '--start_view', help='Start view', type=int, required=True)
parser.add_argument('-e', '--end_view', help='End view', type=int, required=True)
args = parser.parse_args()

datasets = ['train', 'val', 'test']
perturbs = ['', '_perturbed']
features = ['pool5', 'subid']

for i in range(args.start_view, args.end_view):
  for dataset in datasets:
    for perturb in perturbs:
      imagedb_folder = os.path.join(g_imgdb_building_folder, '%s_view_%02d_lmdb' % (dataset+perturb, i))
      prototxt_in = os.path.join(BASE_DIR, 'feature_extraction.prototxt')
      prototxt_file = os.path.join(g_feature_extraction_folder, '%s_view_%02d_lmdb.prototxt' % (dataset+perturb, i))
      shutil.copyfile(prototxt_in, prototxt_file)
      for line in fileinput.input(prototxt_file, inplace=True):
        print line.replace('PATH_TO_LMDB', imagedb_folder),
      caffemodel_file = os.path.join(g_fine_tuning_folder, 'fine_tuning%s' % (perturb), 'best_per_view.caffemodel')
      print 'Extracting features from %s...' % (imagedb_folder)
      
      output_lmdbs = [os.path.join(g_feature_extraction_folder, '%s_view_%02d_%s_lmdb' % (dataset+perturb, i, feature)) for feature in features]
      for output_lmdb in output_lmdbs:
        if os.path.exists(output_lmdb):
          shutil.rmtree(output_lmdb)
      extract_features(prototxt=prototxt_file,
                           caffemodel=caffemodel_file,
                           features=features,
                           output_lmdbs=output_lmdbs,
                           sample_num=get_lmdb_size(imagedb_folder),
                           caffe_path=g_caffe_installation_path,
                           gpu_index=args.gpu_index)
