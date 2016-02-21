#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import sys
import lmdb
import datetime

#https://github.com/BVLC/caffe/issues/861#issuecomment-70124809
import matplotlib 
matplotlib.use('Agg')   

def extract_cnn_features(prototxt, caffemodel, feat_name, label_name, output_lmdb, sample_num, caffe_path=None, gpu_index=0, pool_size=8):   
    if caffe_path:
        sys.path.append(os.path.join(caffe_path, 'python'))
    import caffe
    
    # INIT NETWORK
    caffe.set_mode_gpu()
    caffe.set_device(gpu_index)
    net = caffe.Net(prototxt, caffemodel, caffe.TEST)  
         
    env = lmdb.open(output_lmdb, map_size=int(1e12))
    with env.begin(write=True) as txn:
        count = 0
        while True:
            net.forward()
            feat_array = net.blobs[feat_name].data
            print 'Shape of \"%s\" is' % (feat_name), feat_array.shape 
            label_array = net.blobs[label_name].data
            idx_in_batch = 0
            num_in_batch = feat_array.shape[0]
            len_feature = feat_array.shape[1]
            while count < sample_num and idx_in_batch < num_in_batch:
                feature = feat_array[idx_in_batch].reshape(len_feature, 1, 1).astype(float)
                label = label_array[idx_in_batch].astype(int)
                datum = caffe.io.array_to_datum(feature, label)
                txn.put('{:0>10d}'.format(count), datum.SerializeToString())
                count = count + 1
                idx_in_batch = idx_in_batch + 1
            print datetime.datetime.now().time(), "Processing %d of %d..."%(count, sample_num)
            if count >= sample_num:
                break
    env.close()
    
def get_lmdb_size(lmdb_folder):
    env = lmdb.open(lmdb_folder, readonly=True)
    with env.begin() as txn:
        lmdb_size = sum(1 for _ in txn.cursor())
    env.close()
    return lmdb_size
