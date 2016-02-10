#!/usr/bin/python3
# -*- coding: utf-8 -*-


import os
import sys
import datetime
from functools import partial
from multiprocessing.dummy import Pool
from subprocess import call

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(BASE_DIR))
from global_variables import *

report_step = 100

if __name__ == '__main__':
    if not os.path.exists(g_lfd_images_folder):
        os.mkdir(g_lfd_images_folder) 

    shape_list = []
    lfd_folders = []
    for root, dirs, files in os.walk(g_dataset_folder):
        for filename in files:
            if filename.endswith('.obj'):
                filepath = os.path.join(root, filename)
                shape_list.append(filepath)
                lfd_folder = os.path.dirname(filepath.replace(g_dataset_folder, g_lfd_rendering_folder))
                lfd_folders.append(os.path.abspath(lfd_folder))
    print(len(shape_list), 'shapes are going to be rendered!')

    print('Generating rendering commands...', end = '')
    commands = []
    for i in range(len(shape_list)):
        command = '%s ../blank.blend --background --python render_lfd_single_shape.py -- %s %s ' % (g_blender_executable_path, shape_list[i], lfd_folders[i])
        if len(shape_list) > 32:
            command = command + ' > /dev/null 2>&1'
        commands.append(command)
    print('done(%d commands)'%(len(commands)))

    print('Rendering, it takes long time...')
    pool = Pool(g_lfd_rendering_thread_num)
    for idx, return_code in enumerate(pool.imap(partial(call, shell=True), commands)):
        if idx % report_step == 0:
            print('[%s] Rendering command %d of %d' % (datetime.datetime.now().time(), idx, len(shape_list)))
        if return_code != 0:
            print('Rendering command %d of %d (\"%s\") failed' % (idx, len(shape_list), commands[idx]))
