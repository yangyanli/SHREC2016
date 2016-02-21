#!/usr/bin/python
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
parser.add_argument('-o', '--output_folder', help='Path to output folder', required=True)
args = parser.parse_args()

fileid_to_category = dict()
fileid_to_sub_category = dict()
 
is_testing = True
if os.path.exists(args.annotations):
    is_testing = False
    # Read the annotations
    annotations = [line.strip().split(',') for line in open(args.annotations, 'r')]
    del annotations[0] # remove the header
    
    categories_list = [line.strip() for line in open(g_imgdb_category_list, 'r')]
    sub_categories_list = [line.strip() for line in open(g_imgdb_sub_category_list, 'r')]
    
    categories_dict = dict(zip(categories_list, range(len(categories_list))))
    sub_categories_dict = dict(zip(sub_categories_list, range(len(sub_categories_list))))
    
    for i in range(len(annotations)):
        fileid_to_category[annotations[i][0]] = categories_dict[annotations[i][1]] 
        fileid_to_sub_category[annotations[i][0]] = sub_categories_dict[annotations[i][2]] 

view_num = 12
image_filelist = [[] for i in range(view_num)]
for root, dirs, files in os.walk(args.input_folder):
    for filename in sorted(files):
        if filename.endswith('.png'):
            fileid = root[-6:]
            if is_testing or fileid in fileid_to_category:
                category_id = 0
                sub_category_id = 0
                if not is_testing:
                    category_id = fileid_to_category[fileid]
                    sub_category_id = fileid_to_sub_category[fileid]
                filepath = os.path.join(root, filename)
                view_id = int(filename[-6:-4])
                image_filelist[view_id].append([filepath, category_id, sub_category_id])
print len(image_filelist[0]), 'models!'

shuffle = range(len(image_filelist[0]))
random.seed(9527)
random.shuffle(shuffle)

basename = os.path.basename(args.input_folder)
for i in range(view_num):
    path_subid_filename = '%s/%s_view_%02d_path_subid.txt' % (args.output_folder, basename, i)
    id_filename = '%s/%s_view_%02d_id.txt' % (args.output_folder, basename, i)
    print 'Saving', path_subid_filename, 'and', id_filename, '...'
    with open(path_subid_filename, 'w') as path_subid_file, open(id_filename, 'w') as id_file:
        for j in range(len(shuffle)):
            image_info = image_filelist[i][shuffle[j]]
            path_subid_file.write('%s %d\n' % (image_info[0], image_info[2]))
            id_file.write('%d\n' % (image_info[1]))

if not is_testing:
    image_filelist_all_views = [item for view_list in image_filelist for item in view_list]
    random.seed(9527)
    random.shuffle(image_filelist_all_views)
    path_subid_filename = '%s/%s_path_subid.txt' % (args.output_folder, basename)
    id_filename = '%s/%s_id.txt' % (args.output_folder, basename)
    print 'Saving', path_subid_filename, 'and', id_filename, '...'
    with open(path_subid_filename, 'w') as path_subid_file, open(id_filename, 'w') as id_file:
        for image_info in image_filelist_all_views:
            path_subid_file.write('%s %d\n' % (image_info[0], image_info[2]))
            id_file.write('%d\n' % (image_info[1]))
