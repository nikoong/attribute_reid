#-*- coding:utf-8 -*-
#生成带完整路径的txt
#源：dgd_person_reid/external/exp/datasets/3dpes/train.txt
#目的：dgd_person_reid/external/exp/datasets/3dpes/txt/train.txt

import os

def txt2list(txt_path):
    txt_list = []
    with open(txt_path) as f :
        for line in f:
            txt_list.append(line.split('\n')[0])
    return txt_list

def list2txt(txt_list,txt_path):
    with open(txt_path,'w') as f :
        for line in txt_list:
            f.write(line+'\n')

def read_dataset(txt_path):
    files = []
    ids = []
    data = txt2list(txt_path)
    for line in data:
        personid = int(line.split(' ')[-1])
        onefile = line.split(' ')[0]
        ids.append(personid)
        files.append(onefile)
    return files,ids

datasets = ['prid','viper','3dpes','ilids','cuhk01','cuhk03']
subsets = ['train','val','test_gallery','test_probe']
origin_path = '/home/nikoong/Algorithm_test/dgd_person_reid/external/exp/datasets/'


for dataset in datasets:
    new_path = os.path.join(origin_path , dataset ,'txt')
    if not os.path.exists(new_path):
        os.mkdir(new_path)
    for subset in subsets:
        old_path = os.path.join(origin_path,dataset,subset)
        data = txt2list(old_path+'.txt')
        new_data = []
        for line in data:
            new_line = os.path.join(origin_path,dataset)+'/'+line
            new_data.append(new_line)
        list2txt(new_data,new_path+'/'+subset+'.txt')
        #print new_path+'/'+subset+'.txt'





