#!/usr/bin/env bash
# Experiments of joint single task learning (JSTL)

# Change to the project root directory. Assume this file is at scripts/.
cd $(dirname ${BASH_SOURCE[0]})/../
#source scripts/routines.sh



exp='baseline'
log_name=market
solver=/home/nikoong/Algorithm_test/attribute/models/${exp}/solver.prototxt


log=logs/${exp}/${log_name}-`date +%Y-%m-%d-%H-%M`.log
GLOG_logtostderr=1  external/caffe/build/tools/caffe train \
    -solver ${solver} -gpu 0 2>&1 | tee ${log}