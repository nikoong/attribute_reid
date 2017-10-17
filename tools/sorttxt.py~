#-*- coding:utf-8 -*-
#将数据集按照id排序
import random

pose_path = '/home/nikoong/dataset/re-id_pose/'
datasets = ['prid','viper','3dpes','ilids','cuhk01','cuhk03']
subsets = ['train','val']
parts = ['up','down']

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


    

savepath = pose_path +'jstl/up/train.txt'
newline = txt2list(savepath)
newline.sort(key =lambda newline : int(newline.split(' ')[1]) )
#random.shuffle(newline)
list2txt(newline,'/home/nikoong/dataset/re-id_pose/jstl/up/train.txt')

    
    	

	
