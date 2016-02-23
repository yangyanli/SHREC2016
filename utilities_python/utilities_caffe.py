#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import sys
import lmdb
import datetime
from subprocess import call
from google.protobuf import text_format

#https://github.com/BVLC/caffe/issues/861#issuecomment-70124809
import matplotlib 
matplotlib.use('Agg')   

def extract_features(prototxt, caffemodel, features, output_lmdbs, sample_num, caffe_path=None, gpu_index=0):
    # get batch_size
    if caffe_path:
        sys.path.append(os.path.join(caffe_path, 'python'))
    import caffe
    net_parameter = caffe.proto.caffe_pb2.NetParameter()
    text_format.Merge(open(prototxt, 'r').read(), net_parameter)
    if not net_parameter.layer:
        batch_size = net_parameter.layers[0].data_param.batch_size
    else:
        batch_size = net_parameter.layer[0].data_param.batch_size
    num_mini_batches = (sample_num+batch_size-1)/batch_size
    print 'Batch size is %d, and requires %d mini batches to process %d samples!'%(batch_size, num_mini_batches, sample_num)
        
    # extract features
    executable_path = os.path.join(caffe_path, 'bin', 'extract_features')
    args = [executable_path, caffemodel, prototxt, ','.join(features), ','.join(output_lmdbs), num_mini_batches, 'LMDB', 'GPU', 'DEVICE_ID=%d'%(gpu_index)]
    call(args)
    
    # crop lmdbs to length of sample_num
    num_cropping = batch_size*num_mini_batches-sample_num
    if num_cropping != 0:
        print datetime.datetime.now().time(), "Cropping LMDBS %s..."%(' and '.join(output_lmdbs))
        num_cropping = batch_size*num_mini_batches-sample_num
        for output_lmdb in output_lmdbs:
            env = lmdb.open(output_lmdb, reverse_key=True)
            with env.begin(write=True) as txn:
                cursor = txn.cursor()
                key = cursor.get('key')
                print 'Deleting item with key: %s...'%(key)
                lmdb.delete(key)
            env.close()
    
def get_lmdb_size(lmdb_folder):
    env = lmdb.open(lmdb_folder, readonly=True)
    with env.begin() as txn:
        lmdb_size = sum(1 for _ in txn.cursor())
    env.close()
    return lmdb_size
