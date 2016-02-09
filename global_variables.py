#!/usr/bin/python
# -*- coding: utf-8 -*-

#------------------------------------------------------------------------------
# Define all the global variables for the project
# Many of the variables are just for organizing the files/folders in a nice
# way. Variables that you should take care of are marked by "[take care!]"
# tags. Good luck!
#------------------------------------------------------------------------------

import os
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

##############################################################################
# Rendering
##############################################################################
g_lfd_light_num = 4
g_lfd_light_dist = 14.14
g_lfd_camera_dist = 3
g_lfd_view_num = 20 #[take care!] g_lfd_view_num = elevation_num*azimuth_num
g_lfd_rendering_thread_num = g_thread_num #[take care!], try to match with #CPU core
g_lfd_rendering_folder = os.path.abspath(os.path.join(ROOT, 'lfd_rendering'))

##############################################################################
# Cropping
##############################################################################
# Consider change the default parfor worker number in matlab by following the instructions here:
# http://www.mathworks.com/help/distcomp/saveprofile.html
g_lfd_cropping_thread_num = g_thread_num # [take care!], try to match with #CPU core
g_lfd_cropping_folder = os.path.abspath(os.path.join(ROOT, 'lfd_cropping'))