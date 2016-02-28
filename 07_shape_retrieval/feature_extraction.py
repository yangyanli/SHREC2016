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
features = ['fc_feature', 'fc_id', 'fc_subid']
networks = ['pooling_early', 'concatenate', 'pooling_late']
batch_size = 512
view_num = 12

for network in networks:
    for perturb in perturbs:
        for dataset in datasets:
            view_prototxt_in = os.path.join(BASE_DIR, network, 'view.prototxt.in')
            view_prototxt_in_lines = [line for line in open(view_prototxt_in, 'r')]
            lines = []
            for i in range(view_num):
                lines.extend([line.replace('view_xx', 'view_%02d'%(i)) for line in view_prototxt_in_lines])
            view_aggregation_prototxt = os.path.join(BASE_DIR, network, 'view_aggregation.prototxt')
            lines.extend([line for line in open(view_aggregation_prototxt, 'r')])
            
            path_to_lmdb = os.path.join(g_feature_extraction_folder, '%s%s'%(dataset,perturb)) 
            prototxt_folder = os.path.join(g_shape_retrieval_folder, network, '%s%s'%(dataset,perturb))
            if not os.path.exists(prototxt_folder):
                os.makedirs(prototxt_folder)
            prototxt_filename = os.path.join(prototxt_folder, 'feature_extraction.prototxt')
            with open(prototxt_filename, 'w') as prototxt_file:
                prototxt_file.write('name: \"view_aggregation\"\n')
                for line in lines:
                    line = line.replace('PATH_TO_LMDB', path_to_lmdb)
                    line = line.replace('BATCH_SIZE', str(batch_size))
                    prototxt_file.write(line)
