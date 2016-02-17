#!/usr/bin/python
# -*- coding: utf-8 -*-


import os
import sys

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(BASE_DIR))
from global_variables import *

# Read the annotations
annotations_filename = os.path.join(g_dataset_folder, 'train.csv')
annotations = [line.strip().split(',') for line in open(annotations_filename, 'r')]
del annotations[0] # remove the header

categories = set()
sub_categories = set()
for i in range(len(annotations)):
    categories.add(annotations[i][1])
    sub_categories.add(annotations[i][2])
    
categories_list = sorted(list(categories))
sub_categories_list = sorted(list(sub_categories))

print len(categories_list), 'categories!'
print len(sub_categories_list), 'sub-categories!'

with open(g_imgdb_category_list, 'w') as category_list_file:
    for category in categories_list:
        category_list_file.write('%d\n' % (category))
        
with open(g_imgdb_sub_category_list, 'w') as sub_category_list_file:
    for sub_category_list_file in sub_categories_list:
        sub_category_list_file.write('%d\n' % (sub_category))