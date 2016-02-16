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
    call(['./build_image_list.py', '-i', input_folder, '-a', annotations, '-o', g_imgdb_building_folder])

convert_imageset_executable_path = os.path.join(g_caffe_installation_path, 'bin', 'convert_imageset')

processes = []
args_list = []
view_num = 12
for i in range(view_num):
  for dataset in datasets:
    for perturb in perturbs:
      image_filelist = os.path.join(g_imgdb_building_folder, '%s_view_%02d_path_subid.txt'%(dataset+perturb, i))
      imagedb_folder = os.path.join(g_imgdb_building_folder, '%s_view_%02d' % (dataset+perturb, i))
      args = [convert_imageset_executable_path, '-resize_height', '227', '-resize_width', '227', '/', image_filelist, imagedb_folder]
      log_filename = os.path.join(g_imgdb_building_folder, '%s_view_%02d_log.txt'%(dataset+perturb, i))
      with open(log_filename, 'w') as log_file:
        processes.append(Popen(args, stdout=log_file, stderr=log_file)
      while len(processes) >= g_imgdb_building_thread_num:
        for p in processes:
          if p.poll() is None:
            p_idx = processes.index(p)
            if p.returncode != 0:
              print 'Error: command \'%s\' failed!!' % (args_list[p_idx])   
            del args_list[p_idx]
            processes.remove(p)
        time.sleep(1)
