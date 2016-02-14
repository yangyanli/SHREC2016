#!/usr/bin/python3
# -*- coding: utf-8 -*-


import os
import sys
import random
import argparse

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(BASE_DIR))
from global_variables import *

parser = argparse.ArgumentParser(description="Create image list.")
parser.add_argument('-i', '--input_folder', help='Path to input folder', required=True)
parser.add_argument('-a', '--annotations', help='Path to annotations file', required=True)
args = parser.parse_args()

# Read the annotations
annotations = [line.strip().split(',') for line in open(args.annotations, 'r')]
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

categories_dict = dict(zip(categories_list, range(len(categories_list))))
sub_categories_dict = dict(zip(sub_categories_list, range(len(sub_categories_list))))

image_filelist = []
for root, dirs, files in os.walk(args.input_folder):
    for filename in files:
        if filename.endswith('.png'):
            fileid = root[-6:]
            category_id = categories_dict[fileid]
            sub_category_id = sub_categories_dict[fileid]
            filepath = os.path.join(root, filename)
            image_filelist.append([len(image_filelist), category_id, sub_category_id, filepath])
print len(image_filelist), 'images!'

dirname = os.path.dirname(args.input_folder)
basename = os.path.basename(args.input_folder)

image_filelist_filename = dirname +'filelist_'+basename+'.txt'
print 'Saving', image_filelist_filename, '...'
with open(image_filelist_filename, 'w') as filelist:
    for image_info in image_filelist:
        filelist.write('\t'.join([str(item) for item in image_info])+'\n')
        
image_filelist_filename = dirname +'filelist_'+basename+'_shuffle.txt'
print 'Saving', image_filelist_filename, '...'
with open(image_filelist_filename, 'w') as filelist:
    random.shuffle(image_filelist)
    for image_info in image_filelist:
        filelist.write('\t'.join([str(item) for item in image_info])+'\n')
