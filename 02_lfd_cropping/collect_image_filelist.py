#!/usr/bin/python3
# -*- coding: utf-8 -*-


import os
import sys

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(BASE_DIR))
from global_variables import *

image_filelist = []
for root, dirs, files in os.walk(g_dataset_folder):
    for filename in files:
        if filename.endswith('.png'):
            filepath = os.path.join(root, filename)
            image_filelist.append(filepath)
print(len(image_filelist), 'images are rendered!')

with open(g_lfd_rendering_filelist, 'w') as filelist:
    for image_filename in image_filelist:
        filelist.write(image_filename+'\n')
