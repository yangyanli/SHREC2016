#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import sys
from subprocess import call
from subprocess import Popen

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(BASE_DIR))
from global_variables import *

datasets = ['train', 'val']
perturbs = ['', '_perturbed']
for dataset in datasets:
  for perturb in perturbs:
    input_folder = os.path.join(g_lfd_cropping_folder, dataset+perturb)
    annotations = os.path.join(g_dataset_folder, dataset+'.csv')
    call(['./build_image_list.py', '-i', input_folder, '-a', annotations])

shuffles = ['_shuffle', '']
for dataset in datasets:
  for perturb in perturbs:
    for shuffle in shuffles:
      image_filelist = os.path.join(g_lfd_cropping_folder, 'filelist_'+dataset+perturb+shuffle+'.txt')
      record_filename = os.path.join(g_imgdb_building_folder, dataset+perturb+shuffle+'.rec')
      args = [g_im2rec_executable_path, image_filelist, '/', record_filename, 'color=1', 'resize=227', 'force_square=1', 'label_width=2']
      log_filename = os.path.join(g_imgdb_building_folder, dataset+perturb+shuffle+'.rec.txt')
      with open(log_filename, 'w') as log_file:
        Popen(args, stdout=log_file, stderr=log_file)
