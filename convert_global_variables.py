#!/usr/bin/python3
# -*- coding: utf-8 -*-

import os
import sys

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(BASE_DIR)
from global_variables import *

global_variables_m_file = open('./global_variables.m', 'w')
global_variables_m_file.write('g_lfd_cropping_thread_num = %d;\n' %(g_lfd_cropping_thread_num))
global_variables_m_file.write('g_lfd_rendering_folder = \'%s\';\n' %(g_lfd_rendering_folder))
global_variables_m_file.write('g_lfd_cropping_folder = \'%s\';\n' %(g_lfd_cropping_folder))
global_variables_m_file.write('\n');
global_variables_m_file.close();
