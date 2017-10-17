#-*-coding:utf-8-*- 
import numpy as np
from PIL import Image
import os
import cv2
import random
from keras.preprocessing.image import ImageDataGenerator, array_to_img, img_to_array, load_img

'''
#解析train.txt文件，返回文件名列表和label列表
def Parsetxt(txt_path):
    file_list=[]
    label_list=[]
    with open(txt_path,'r') as f:
        for line in f:
            file_list.append(line.split(' ')[0])
            label_list.append(int(line.split(' ')[1]))
        return file_list, label_list 
'''

#value是类型名，mul是这个类型一个样例要生成几个,output_path是新图片路径
def DataAugmentation(input_txt,output_path,value,mul):
    imagelist,labellist = Parsetxt(input_txt)
    for i in range(len(labellist)):
        if labellist[i]==value:
            new_name = imagelist[i].split('/')[-1]
            newimage(imagelist[i],output_path,mul,new_name)
    
               
    

#生成数据集
def newimage(input_image_path,output_path,output_image_amount,output_image_name):
    datagen = ImageDataGenerator(

        rotation_range=0.2,
        width_shift_range=0.2,
        height_shift_range=0.2,
        shear_range=0.2,
        zoom_range=0.2,
        horizontal_flip=False,
        fill_mode='nearest')
    img =  Image.open(input_image_path) #this is a PIL image
    x = img_to_array(img) 
    x = x.reshape((1,) + x.shape)
     
    i = 0
    for batch in datagen.flow(x, batch_size=1,
                          save_to_dir=output_path, save_prefix=output_image_name, save_format='jpg'):
        i += 1
        if i >= output_image_amount:
            break 


#增加样例到 highlevel(n×1000)+  
def increase_samples(txt_list,lowlevel,sourse_path):
    all_label_num = []
    need_increase_num = []
    increase_label = []
    for i in range(10):
        num = count_list(txt_list,i)
        all_label_num.append(num)
    for i in range(10):
        if all_label_num[i]<lowlevel:
            increase_label.append(i)
            need_increase_num.append((lowlevel-all_label_num[i])/1000*1000 + 1000)    
    increase_num = [elem * 0 for elem in need_increase_num]  
    sourse_list = txt2list(sourse_path)
    for i in range(len(increase_label)):
        for j in range(len(sourse_list)):
            if need_increase_num[i] <= increase_num[i]: break
            elif int(sourse_list[j].split(' ')[1])==increase_label[i]:
                txt_list.append(sourse_list[j])
                increase_num[i] =  increase_num[i] + 1
    random.shuffle(txt_list)
    return txt_list



#减少样例到 lowlevel(n×1000)+
def reduce_samples(txt_list,highlevel):
    all_label_num = []
    need_reduce_num = []
    reduce_label = []
    for i in range(10):
        num = count_list(txt_list,i)
        all_label_num.append(num)
    for i in range(10):
        if all_label_num[i]>highlevel:
            reduce_label.append(i)
            need_reduce_num.append( (all_label_num[i] - highlevel)/1000*1000 )
    random.shuffle(txt_list)
    reduce_num = [elem * 0 for elem in need_reduce_num]
    for i in range(len(reduce_label)):
        for j in range(len(txt_list)):
            if need_reduce_num[i] <= reduce_num[i]: break
            elif int(txt_list[j].split(' ')[1])==reduce_label[i]: 
                del txt_list[j]
                reduce_num[i]=reduce_num[i]+1
    return txt_list


#根据label排序
def sort_txt(txt_list):
    value_list = []
    for line in txt_list:
        value = int(line.split(' ')[1])
        value_list.append(value)
    value_list = np.array(value_list) 
    txt_list = np.array(txt_list)     
    index_list = np.argsort(value_list)
    txt_list =txt_list[index_list]
    return txt_list


#txt to list
def txt2list(txt_path):
    txt_list = []
    with open(txt_path) as f :
        for line in f:
            txt_list.append(line.split('\n')[0])
    return txt_list


#list to txt
def list2txt(txt_list,txt_path):
    with open(txt_path,'w') as f :
        for line in txt_list:
            f.write(line+'\n')


#求个类别数量
def count_list(list,value):
    num = 0
    for line in list:
        label = line.split(' ')[1].split('\n')[0]
        if str(value) == label: num = num + 1
    return num




#txt_name 不是完成路径，是一个标记，比如wrong，会在txt文件下生成一个wrong子
def gen_single_txt(data_path,txt_name,is_random):
    txt_path = os.path.join('/home/nikoong/Algorithm_test/handwritting/data/txt')
    txt = os.path.join(txt_path,txt_name+'.txt')
    all_files = []
    for root, dirs,files in os.walk(data_path,topdown=False):
        for name in files:
            filename = os.path.join(root,name)
            all_files.append(filename)
    if is_random:
        random.shuffle(all_files)
    with open(txt,'w') as f:
        for filename in all_files:
            f.write(filename+' '+filename.split('Value')[1].split('.jpg')[0]+'\n')






#将多级目录下的所有图片文件,生成txt/txt_name/trian.txt val test
def gen_tri_txt(data_path,txt_name,is_random):
    txt_path = os.path.join('/home/nikoong/Algorithm_test/handwritting/data/txt',txt_name)
    os.mkdir(txt_path)
    train_txt = os.path.join(txt_path,'train.txt')
    val_txt = os.path.join(txt_path,'val.txt')
    test_txt = os.path.join(txt_path,'test.txt')
    all_files = []
    for root, dirs,files in os.walk(data_path,topdown=False):
        for name in files:
            filename = os.path.join(root,name)
            all_files.append(filename)
    if is_random:
        random.shuffle(all_files)
    leng = len(all_files)
    train_len = int(leng*0.5)
    val_len = int(leng*0.8)
    test_len = leng
    train_file =all_files[0:train_len]
    val_file =all_files[train_len+1:val_len]
    test_file =all_files[val_len+1:-1]
    with open(train_txt,'w') as f:
        for filename in train_file:
            f.write(filename+' '+filename.split('Value')[1].split('.jpg')[0]+'\n')

    with open(val_txt,'w') as f:
        for filename in val_file:
            f.write(filename+' '+filename.split('Value')[1].split('.jpg')[0]+'\n')

    with open(test_txt,'w') as f:
        for filename in test_file:
            f.write(filename+' '+filename.split('Value')[1].split('.jpg')[0]+'\n')



#解析train.txt文件，返回文件名列表和label列表
def Parsetxt(txt_path):
    file_list=[]
    label_list=[]
    with open(txt_path,'r') as f:
        for line in f:
            file_list.append(line.split(' ')[0])
            label_list.append(int(line.split(' ')[1]))
        return file_list, label_list   




#生成文件列表
def Makefilelist(data_path):
    filelist=[]
    files= os.listdir(data_path)
    for filename in files:
        fullfilename = os.path.join(data_path,filename)
        filelist.append(fullfilename)
    return filelist,files



#二值化
def Binaryzation(input_image):
    bi_img = input_image
    (thresh, bi_img) = cv2.threshold(bi_img, 128, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
    return bi_img



#反色
def Inverse(input_image):
    img = input_image
    inverse_img = 255-img
    return inverse_img


#闭操作
def Close(input_image,kernel_width,kernel_height):
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT,(kernel_width, kernel_height))
    closed_img = cv2.morphologyEx(input_image, cv2.MORPH_CLOSE, kernel)  
    return closed_img



#膨胀
def Dilate(input_image,kernel_width,kernel_height):
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT,(kernel_width, kernel_height))
    dilated_img = cv2.dilate(input_image,kernel)
    return dilated_img
     


#腐蚀
def Erode (input_image,kernel_width,kernel_height):
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT,(kernel_width, kernel_height))
    eroded_img = cv2.erode(input_image,kernel)
    return eroded_img



#去黑边
def Rm_Blackborder(input_image):
    img = input_image
    #上边
    while np.sum(img[0]) == 0:
        img = img[1:]
    #左边
    while np.sum(img[:,0]) == 0:
        img = img[:,1:]
    w,h = img.shape
    if (w==1 or h==1):return img
    #下边
    while np.sum(img[-1]) == 0:
        img = img[:-1]
    #右边
    w,h = img.shape
    if (w==1 or h==1):return img
    while np.sum(img[:,:-1]) == 0:
        img = img[:,:-1]
    return img

        

#resize
def Resize(input_image,n):
    img = input_image
    h,w = img.shape
    if max(w,h)>n:
        max_ = float(max(w,h))
        ratio = max_/n
        new_w = int(w/ratio)
        new_h = int(h/ratio)
        img = cv2.resize(img,(new_w,new_h))
    return img




#补边函数，补0到20*20，再补到28*28
def MakeBorder (input_image):
    h,w = input_image.shape
    img = input_image
    if((20-h)%2==0):
        top = (20-h)/2;
        bottom = (20-h)/2;
    else:
        top = (20-h)/2+1;
        bottom = (20-h)/2;
    if((20-w)%2==0):
        left = (20-w)/2;
        right = (20-w)/2;
    else:
        left = (20-w)/2+1;
        right = (20-w)/2;
    img_20 = cv2.copyMakeBorder(img, top, bottom, left, right, cv2.BORDER_CONSTANT,value=0)
    img_28 = cv2.copyMakeBorder(img_20, 4, 4, 4, 4, cv2.BORDER_CONSTANT,value=0)
    return img_28



#打印
def Print_img(input_img):
    for i in range(input_img.shape[0]):
        print '\n' 
        for j in  range(input_img.shape[1]):
            print input_img[i][j],' ',



#检测&保存
def Save_img(input_img,save_path):
    input_img = Image.fromarray(input_img)
    input_img.save(save_path)
