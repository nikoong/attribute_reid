#!/usr/bin/env bash
# Experiments of joint single task learning (JSTL)

# Change to the project root directory. Assume this file is at scripts/.
cd $(dirname ${BASH_SOURCE[0]})/../


external/caffe/build/tools/extract_features \
      /home/nikoong/Algorithm_test/attribute/external/exp/snapshots/baseline/DUCK_iter_30000.caffemodel /home/nikoong/Algorithm_test/attribute/models/baseline/exfeat_template_test.prototxt fc7_bn,label\
      external/exp/results/baseline/DukeMTMC-reID_DUCK_iter_30000_fc7_bn/train_features_lmdb,external/exp/results/baseline/DukeMTMC-reID_DUCK_iter_30000_fc7_bn/train_labels_lmdb \
      166 lmdb GPU 0

