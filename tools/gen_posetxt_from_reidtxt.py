#-*- coding:utf-8 -*-

#有的图片检测不出posepoint，称为无效图片
#删除reid数据集txt包含的无效图片名字，生成pose_reid数据集的txt

import os
import json as js
import numpy as np
data_path = '/home/nikoong/Algorithm_test/dgd_person_reid/external/exp/datasets/'
pose_path = '/home/nikoong/dataset/re-id_pose/'
datasets = ['prid','viper','3dpes','ilids','cuhk01','cuhk03']
subsets = ['train','val','test_gallery','test_probe']
parts = ['up','down']


#得到一个文件夹里所有文件路径的列表，未排序
def getfiles(data_path):
    all_files = []
    for root,dirs,files in os.walk(data_path,topdown=False):
        for name in files:
            filename = os.path.join(root,name)
            all_files.append(filename)
    return all_files

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

#生成无效图片的图片名
for dataset in datasets:
    delimages = []    
    for cam in ['/cam_0','/cam_1']:
        cam_path = data_path + dataset + cam
        json_path = pose_path + dataset +'/json'+ cam
        all_image_files = getfiles(cam_path);
        all_json_files = getfiles(json_path);
        all_image_files.sort()
        all_json_files.sort()
        #print dataset,cam,"img number is",len(all_image_files)
        for i in range(len(all_image_files)):
            picname = all_image_files[i].split('/')[-2] + '/' +all_image_files[i].split('/')[-1]
            with open(all_json_files[i],"r") as f:
                data = js.load(f)
                people = data['people']
                if(len(people) == 1):
                    pose = np.array(people[0]['body_parts'])
                    pose = pose.reshape(18,3)
                    hip_y = (pose[8][1] + pose[11][1])/2
                    hip_y = int(hip_y)
                    if(hip_y == 0):
                        delimages.append(picname)  
                                                                 
                else:
                    delimages.append(picname)

    #删除无效图片后存入newlist               
    for subset in subsets:
        reidtxt = data_path + dataset +'/'+ subset+'.txt'
        originlist = txt2list(reidtxt)
        newlist =[]    
        for i in range(len(originlist)):
            newlist.append(originlist[i].split(' ')[0])
            #print newlist[i]
        for delimage in delimages:
            if(newlist.count(delimage) > 0 and newlist.count(delimage) <= 1):
                newlist.remove(delimage)
            elif(newlist.count(delimage) > 1):
                print "Error!there are two same image in",dataset,",which is",delimage  
        for part in parts:
            txt = []
            partpath = pose_path + dataset +'/'+ part +'/'
            txtpath = partpath + subset+'.txt' 
            print txtpath
            for i in range(len(newlist)):
                personid = int(newlist[i].split('/')[-1].split('_')[0])
                txt.append(partpath + newlist[i] +' '+str(personid))
            list2txt(txt,txtpath)
            

                
           
    
    
    
  



