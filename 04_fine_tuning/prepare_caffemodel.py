#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import sys
from subprocess import call

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(BASE_DIR))
from global_variables import *

if not os.path.exists(g_fine_tuning_folder):
    os.mkdir(g_fine_tuning_folder) 

# download caffemodel
call(['wget', '-O', g_caffemodel_filename, g_blender_executable_url])