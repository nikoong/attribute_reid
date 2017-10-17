#-*-coding:utf-8-*-
#从re-id数据集读图片。根据posepoint文件，截取上下半身，分别放到图像路径。


import os
import json as js
import numpy as np
import cv2
data_path = '/home/nikoong/Algorithm_test/dgd_person_reid/external/exp/datasets/'
pose_path = '/home/nikoong/dataset/re-id_pose/'
datasets = ["prid","viper",'3dpes','ilids','cuhk01','cuhk03']
#datasets = ["prid"]



#得到一个文件夹里所有文件路径的列表，未排序
def getfiles(data_path):
    all_files = []
    for root,dirs,files in os.walk(data_path,topdown=False):
        for name in files:
            filename = os.path.join(root,name)
            all_files.append(filename)
    return all_files


for dataset in datasets:    
    for cam in ['/cam_0','/cam_1']:
        delimage = []
        cam_path = data_path + dataset + cam
        json_path = pose_path + dataset +'/json'+ cam
        all_image_files = getfiles(cam_path);
        all_json_files = getfiles(json_path);
        all_image_files.sort()
        all_json_files.sort()
        print dataset,cam,"img number is",len(all_image_files)
        for i in range(len(all_image_files)):
            #print all_image_files[i]
            uppath=pose_path + dataset +'/up'+ cam+'/' + all_image_files[i].split('/')[-1]
            downpath=pose_path + dataset +'/down'+ cam+'/' + all_image_files[i].split('/')[-1]
            #print uppath
            #print downpath
            img = cv2.imread(all_image_files[i])                   
            with open(all_json_files[i],"r") as f:
                data = js.load(f)
                people = data['people']
                if(len(people) == 1):
                    pose = np.array(people[0]['body_parts'])
                    pose = pose.reshape(18,3)
                    hip_y = (pose[8][1] + pose[11][1])/2
                    hip_y = int(hip_y)
                    if (hip_y != 0):
                        img_up = img[0:hip_y,:,:]
                        img_down = img[hip_y:,:,:]
                        #cv2.namedWindow('up',cv2.WINDOW_AUTOSIZE)
                        #cv2.imshow('up',img_up)
                        #cv2.waitKey()  
                        cv2.imwrite(uppath, img_up)
                        cv2.imwrite(downpath, img_down)
'''
                else:
                    delimage.append(all_image_files[i])
        with open(pose_path + dataset +cam+'_del.txt','w') as f :
                for line in delimage:
                    f.write(line+'\n')
'''
  



