#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import sys

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(os.path.dirname(BASE_DIR)))
from global_variables import *

train_batch_size = 1024
test_batch_size = 512
view_num = 12
perturbs = ['', '_perturbed']
for perturb in perturbs:
    view_prototxt_in = os.path.join(BASE_DIR, 'view.prototxt.in')
    view_prototxt_in_lines = [line for line in open(view_prototxt_in, 'r')]
    lines = []
    for i in range(view_num):
        lines.extend([line.replace('view_xx', 'view_%02d'%(i)) for line in view_prototxt_in_lines])
    view_aggregation_prototxt = os.path.join(BASE_DIR, 'view_aggregation.prototxt')
    lines.extend([line for line in open(view_aggregation_prototxt, 'r')])
    
    path_to_train_lmdb = os.path.join(g_feature_extraction_folder, 'train%s'%(perturb)) 
    path_to_test_lmdb = os.path.join(g_feature_extraction_folder, 'val%s'%(perturb))
    prototxt_folder = os.path.join(g_view_aggregation_folder, 'pooling_early', 'fine_tuning%s'%(perturb))
    if not os.path.exists(prototxt_folder):
        os.makedirs(prototxt_folder)
    prototxt_filename = os.path.join(prototxt_folder, 'train_val.prototxt')
    with open(prototxt_filename, 'w') as prototxt_file:
        prototxt_file.write('name: \"view_aggregation\"\n')
        for line in lines:
            line = line.replace('PATH_TO_TRAIN_LMDB', path_to_train_lmdb)
            line = line.replace('PATH_TO_TEST_LMDB', path_to_test_lmdb)
            line = line.replace('TRAIN_BATCH_SIZE', str(train_batch_size))
            line = line.replace('TEST_BATCH_SIZE', str(test_batch_size))
            prototxt_file.write(line)
      
