#!/usr/bin/python
# -*- coding: utf-8 -*-

#------------------------------------------------------------------------------
# Define all the global variables for the project
# Many of the variables are just for organizing the files/folders in a nice
# way. Variables that you should take care of are marked by "[take care!]"
# tags. Good luck!
#------------------------------------------------------------------------------

import os
g_debug = False
ROOT = os.path.dirname(os.path.abspath(__file__))
g_dataset_folder = os.path.abspath(os.path.join(ROOT, 'dataset'))
g_thread_num = 16

##############################################################################
# Paths and urls to executable and data sources
##############################################################################
g_3rd_party_folder = os.path.abspath(os.path.join(ROOT, '3rd_party'))
g_blender_executable_url = 'http://download.blender.org/release/Blender2.75/blender-2.75a-linux-glibc211-x86_64.tar.bz2'
g_blender_executable_path = os.path.abspath(os.path.join(g_3rd_party_folder, 'blender/blender'))
g_matlab_executable_path = os.path.abspath('/usr/local/bin/matlab') # [take care!!!]
g_caffe_installation_path = os.path.abspath(os.path.join(g_3rd_party_folder, 'caffe'))

##############################################################################
# Rendering
##############################################################################
g_lfd_light_num = 4
g_lfd_light_dist = 14.14
g_lfd_camera_dist = 3
g_lfd_view_num = 20 #[take care!] g_lfd_view_num = elevation_num*azimuth_num
g_lfd_rendering_thread_num = g_thread_num #[take care!], try to match with #CPU core
g_lfd_rendering_folder = os.path.abspath(os.path.join(ROOT, 'dataset_lfd_rendering'))
g_lfd_rendering_filelist = os.path.abspath(os.path.join(g_lfd_rendering_folder, 'filelist.txt'))

##############################################################################
# Cropping
##############################################################################
# Consider change the default parfor worker number in matlab by following the instructions here:
# http://www.mathworks.com/help/distcomp/saveprofile.html
g_lfd_cropping_thread_num = g_thread_num # [take care!], try to match with #CPU core
g_lfd_cropping_folder = os.path.abspath(os.path.join(ROOT, 'dataset_lfd_cropping'))

##############################################################################
# ImgDB Building
##############################################################################
g_imgdb_building_thread_num = g_thread_num # [take care!], try to match with #CPU core
g_imgdb_building_folder = os.path.abspath(os.path.join(ROOT, 'dataset_imgdb_building'))
g_imgdb_category_list = os.path.abspath(os.path.join(g_imgdb_building_folder, 'category_list.txt'))
g_imgdb_sub_category_list = os.path.abspath(os.path.join(g_imgdb_building_folder, 'sub_category_list.txt'))

##############################################################################
# Fine Tuning
##############################################################################
g_caffemodel_url = 'http://www.robots.ox.ac.uk/~vgg/software/very_deep/caffe/VGG_ILSVRC_19_layers.caffemodel'
g_fine_tuning_folder = os.path.abspath(os.path.join(ROOT, 'dataset_fine_tuning'))
g_caffemodel_filename = os.path.abspath(os.path.join(g_fine_tuning_folder, 'VGG_ILSVRC_19_layers.caffemodel'))


##############################################################################
# Feature Extraction
##############################################################################
g_feature_extraction_folder = os.path.abspath(os.path.join(ROOT, 'dataset_feature_extraction'))

##############################################################################
# View Aggregation
##############################################################################
g_view_aggregation_folder = os.path.abspath(os.path.join(ROOT, 'dataset_view_aggregation'))

##############################################################################
# Shape Retrieval
##############################################################################
g_shape_retrieval_folder = os.path.abspath(os.path.join(ROOT, 'dataset_shape_retrieval'))