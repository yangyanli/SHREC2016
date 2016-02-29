#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import sys

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(BASE_DIR))
from global_variables import *

datasets = ['train', 'val', 'test']
for dataset in datasets:
    path_file = os.path.join(g_imgdb_building_folder, '%s_view_00_path_subid.txt'%(dataset))
    model_list = [line.split('_00.png')[0][-6:] for line in open(path_file, 'r')]
    model_list_filename = os.path.join(g_shape_retrieval_folder, 'model_list_%s.txt'%(dataset))
    with open(model_list_filename, 'w') as model_list_file:
        for model in model_list:
            model_list_file.write(model+'\n')

