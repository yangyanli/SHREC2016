#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import sys
import shutil
import fileinput

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(BASE_DIR))
from global_variables import *
sys.path.append(os.path.dirname(BASE_DIR))
sys.path.append(os.path.join(os.path.dirname(BASE_DIR), 'utilities_python'))
from utilities_caffe import *

datasets = ['train', 'val', 'test']
perturbs = ['', '_perturbed']

view_num = 12
for i in range(view_num):
  for dataset in datasets:
    for perturb in perturbs:
      imagedb_folder = os.path.join(g_imgdb_building_folder, '%s_view_%02d_lmdb' % (dataset+perturb, i))
      lmdb_folder = os.path.join(g_feature_extraction_folder, '%s_view_%02d_lmdb' % (dataset+perturb, i))
      prototxt_in = os.path.join(BASE_DIR, 'feature_extraction.prototxt')
      prototxt_file = os.path.join(g_feature_extraction_folder, '%s_view_%02d_lmdb.prototxt' % (dataset+perturb, i))
      shutil.copyfile(prototxt_in, prototxt_file)
      for line in fileinput.input(prototxt_file, inplace=True):
        print line.replace('PATH_TO_LMDB', imagedb_folder),
      caffemodel_file = os.path.join(g_fine_tuning_folder, 'fine_tuning%s' % (perturb), 'best_per_view.caffemodel')
      print 'Extracting features from %s...' % (imagedb_folder)
      extract_cnn_features(prototxt=prototxt_file,
                           caffemodel=caffemodel_file,
                           feat_name='fc7',
                           label_name='subid',
                           output_lmdb=lmdb_folder,
                           sample_num=get_lmdb_size(imagedb_folder),
                           caffe_path=g_caffe_installation_path,
                           gpu_index=6)
