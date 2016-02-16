#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import sys
import lmdb
import numpy as np

#https://github.com/BVLC/caffe/issues/861#issuecomment-70124809
import matplotlib 
matplotlib.use('Agg')

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(BASE_DIR))
from global_variables import *

sys.path.append(os.path.join(g_caffe_installation_path, 'python'))
import caffe
    
datasets = ['train', 'val']
perturbs = ['', '_perturbed']
view_num = 12
for i in range(view_num+1):
  for dataset in datasets:
    for perturb in perturbs:
      view_str = '_view_%02d' % (i)
      if i == view_num:
          view_str = ''
      id_filename = os.path.join(g_imgdb_building_folder, '%s%s_id.txt'%(dataset+perturb, view_str))
      id_folder = os.path.join(g_imgdb_building_folder, '%s%s_id_lmdb' % (dataset+perturb, view_str))
      print 'Building ID LMDB', id_folder, '...'      
      env = lmdb.open(id_folder, map_size=int(1e12))
      ids = [int(line) for line in open(id_filename, 'r')]
      array = np.zeros([1,1,1])
      with env.begin(write=True) as txn:
        for idx, category_id in enumerate(ids):
          array[0] = category_id
          datum = caffe.io.array_to_datum(array.astype(float), category_id)
          txn.put('{:0>10d}'.format(idx), datum.SerializeToString())
      env.close();
