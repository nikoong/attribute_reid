#!/usr/bin/env bash
# Change to the project root directory. Assume this file is at scripts/.


EXP_DIR=external/exp
RESULTS_DIR=$EXP_DIR/results
Data_DIR=$EXP_DIR/dataset
MODELS_DIR=models
CAFFE_DIR=external/caffe


get_result_dir() {
  local exp=$1
  local dataset=$2
  local trained_model=$3
  if [[ $# -eq 4 ]]; then
    local blob=$4
  else
    local blob=fc7_bn
  fi

  local weights_name=$(basename ${trained_model})
  local weights_name="${weights_name%%.*}"
  local result_dir=${RESULTS_DIR}/${exp}/${dataset}_${weights_name}_${blob}
  echo ${result_dir}
}

extract_features() {
  local exp=$1
  local dataset=$2
  local trained_model=$3
  if [[ $# -eq 4 ]]; then
    local blob=$4
  else
    local blob=fc7_bn
  fi
  #local result_dir=${RESULTS_DIR}/${exp}/${dataset}_${weights_name}_${blob}
  local result_dir=$(get_result_dir ${exp} ${dataset} ${trained_model})
  rm -rf ${result_dir}
  mkdir -p ${result_dir}
  # Extract train, val, test probe, and test gallery features.
  for subset in train test_probe test_gallery; do
    echo "Extracting ${dataset}/${subset} set"
    local num_samples=$(wc -l ${Data_DIR}/${dataset}/${subset}.txt | awk '{print $1}')
    local num_samples=$((num_samples + 1))
    local num_iters=$(((num_samples + 99) / 100))
    local model=$(mktemp)
    sed -e "s/\${dataset}/${dataset}/g; s/\${subset}/${subset}/g" \
      ${MODELS_DIR}/${exp}/exfeat_template.prototxt > ${model}
    echo ${model}
    echo "exfeat_template" ${MODELS_DIR}/${exp}/exfeat_template.prototxt
    ${CAFFE_DIR}/build/tools/extract_features \
      ${trained_model} ${model} ${blob},label \
      ${result_dir}/${subset}_features_lmdb,${result_dir}/${subset}_labels_lmdb \
      ${num_iters} lmdb GPU 0
    python2 tools/convert_lmdb_to_numpy.py \
      ${result_dir}/${subset}_features_lmdb ${result_dir}/${subset}_features.npy \
      --truncate ${num_samples}
    python2 tools/convert_lmdb_to_numpy.py \
      ${result_dir}/${subset}_labels_lmdb ${result_dir}/${subset}_labels.npy \
      --truncate ${num_samples}
  done
}


cd $(dirname ${BASH_SOURCE[0]})/../
exp='baseline'
trained_model=/home/nikoong/Algorithm_test/attribute/external/exp/snapshots/baseline/DUCK_iter_30000.caffemodel


# Extract features on all datasets
for dataset in DukeMTMC-reID; do
  extract_features ${exp} ${dataset} ${trained_model}
done

# Evaluate performance
for dataset in DukeMTMC-reID; do
  result_dir=$(get_result_dir ${exp} ${dataset} ${trained_model})
  echo ${dataset}
  python2 eval/metric_learning.py ${result_dir}
  echo
done


