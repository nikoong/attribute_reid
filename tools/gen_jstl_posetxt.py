#-*- coding:utf-8 -*-

#将多个数据集的txt，合并成一个的txt。id累加
#jstl只需要train.txt和val.txt
import random
import os

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

#疑问：val应该是train的一个子集，
#

#得到id的set
#将原id和新id用dic一一对应

#for
#将原id转成新id
#if dont have ,del

max_id ={}
for dataset in datasets:
    data = 0;
    files, personids = read_dataset(pose_path+dataset+'/up/train.txt')
    data = len(set(personids))    
    max_id[dataset]=data
#print max_id

#['prid','viper','3dpes','ilids','cuhk01','cuhk03']
#将原id和新id用dic一一对应
add = {}
add['cuhk03'] = max_id['prid'] + max_id['viper'] + max_id['3dpes'] + max_id['ilids'] +max_id['cuhk01']
add['cuhk01'] = max_id['prid'] + max_id['viper'] + max_id['3dpes'] + max_id['ilids']
add['ilids'] = max_id['prid'] + max_id['viper'] + max_id['3dpes']
add['3dpes'] = max_id['prid'] + max_id['viper'] 
add['viper'] = max_id['prid'] 
add['prid'] = 0

print add

datasetid = {}
for dataset in datasets:
    old2new={}
    files, personids = read_dataset(pose_path+dataset+'/up/train.txt')
    personids = list(set(personids))
    personids.sort()
    for i in range(len(personids)):
        old2new[personids[i]]=i + add[dataset]
    datasetid[dataset] = old2new



    
#train.txt
for part in parts:
    savepath = pose_path +'jstl/'+ part +'/train.txt'
    newtxtlist=[]
    for dataset in datasets:    	
    	files, personids = read_dataset(pose_path + dataset +'/'+ part +'/train.txt')
    	for i in range(len(personids)):
    		newid = str(datasetid[dataset][personids[i]])
    		newtxtlist.append(files[i]+' '+ newid)
    #newtxtlist.sort()
    random.shuffle(newtxtlist)
    list2txt(newtxtlist,savepath)	

#val.txt
for part in parts:
    savepath = pose_path +'jstl/'+ part +'/val.txt'
    newtxtlist=[]
    for dataset in datasets:    	
    	files, personids = read_dataset(pose_path + dataset +'/'+ part +'/val.txt')
    	for i in range(len(personids)):
    		if datasetid[dataset].has_key(personids[i]):
    		    newid = str(datasetid[dataset][personids[i]])
    		    newtxtlist.append(files[i]+' '+ newid)
    		else:
    			print dataset,personids[i]
    #newtxtlist.sort()
    random.shuffle(newtxtlist)
    list2txt(newtxtlist,savepath)	


#因为原全身图片数据集的id和jstl_up数据集id不相同
#所以从up数据集生成新的全身数据集

for dataset in ['prid','viper','3dpes','ilids','cuhk01','cuhk03']:
    whole_dir = txtpath = pose_path + dataset +'/whole_body'
    if not os.path.exists(whole_dir):
        os.makedirs(whole_dir)
    for file in ['test_gallery.txt','test_probe.txt','train.txt','val.txt']:
        up_txt_path = pose_path + dataset +'/up/'+ file
        whole_txt_path = pose_path + dataset +'/whole_body/'+ file
        uplist = txt2list(up_txt_path)
        wholelist = []
        for line in uplist:
            oldstr = 're-id_pose/'+ dataset +'/up/' 
            newstr = 're-id/'+ dataset +'/'        
            wholelist.append(line.replace(oldstr,newstr))
        list2txt(wholelist,whole_txt_path)

for dataset in ['jstl']:
    whole_dir = txtpath = pose_path + dataset +'/whole_body'
    if not os.path.exists(whole_dir):
        os.makedirs(whole_dir)
    for file in ['train.txt','val.txt']:
        up_txt_path = pose_path + dataset +'/up/'+ file
        whole_txt_path = pose_path + dataset +'/whole_body/'+ file
        uplist = txt2list(up_txt_path)
        wholelist = []
        for line in uplist:
            newline = line.replace('re-id_pose','re-id')
            newline = newline.replace('up/','')           
            wholelist.append(newline)
        list2txt(wholelist,whole_txt_path)