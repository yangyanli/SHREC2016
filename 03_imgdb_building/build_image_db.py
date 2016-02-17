#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import sys
import time
from subprocess import call
from subprocess import Popen

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(BASE_DIR))
from global_variables import *

call(['./build_category_list.py'])

datasets = ['train', 'val', 'test']
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
for i in range(view_num+1):
  for dataset in datasets:
    for perturb in perturbs:
      view_str = '_view_%02d' % (i)
      if i == view_num:
          view_str = ''
      image_filelist = os.path.join(g_imgdb_building_folder, '%s%s_path_subid.txt'%(dataset+perturb, view_str))
      imagedb_folder = os.path.join(g_imgdb_building_folder, '%s%s_lmdb' % (dataset+perturb, view_str))
      args = [convert_imageset_executable_path, '-resize_height', '224', '-resize_width', '224', '/', image_filelist, imagedb_folder]
      log_filename = os.path.join(g_imgdb_building_folder, '%s%s_log.txt'%(dataset+perturb, view_str))
      with open(log_filename, 'w') as log_file:
        processes.append(Popen(args, stdout=log_file, stderr=log_file))
        args_list.append(args)
      while len(processes) >= g_imgdb_building_thread_num:
        for p in processes:
          if p.poll() is not None:
            p_idx = processes.index(p)
            if p.returncode != 0:
              print 'Error: command \'%s\' failed!!' % (' '.join(args_list[p_idx]))
            else:
              print 'Command \'%s\' finished successfully.' % (' '.join(args_list[p_idx]))
            del args_list[p_idx]
            processes.remove(p)
        time.sleep(1)
