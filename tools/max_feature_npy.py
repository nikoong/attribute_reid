import numpy as np
import os
import shutil

######edit#######################################
#parts = ["up_jstl","down_jstl"]
#new_npy_dir = "up&down_poly_max"
#iters_part1 = "_jstl_poly_iter_30000_fc7_bn/"
#iters_part2 = "_jstl_poly_iter_30000_fc7_bn/"
#iters_new = "_jstl_poly_iter_30000_fc7_bn/"



#results dir
parts = ["up&down_poly_max","whole_body_jstl"]
new_npy_dir = "whole&up&down_poly_max"
iters_part1 = "_jstl_poly_iter_30000_fc7_bn/"
iters_part2 = "_jstl_iter_30000_fc7_bn/"
iters_new = "_jstl_poly_iter_30000_fc7_bn/"  
###############################################


datasets = ["prid","viper",'3dpes','ilids','cuhk01','cuhk03']
features = ['train_features.npy','val_features.npy','test_probe_features.npy','test_gallery_features.npy']
labels =['test_gallery_labels.npy','test_probe_labels.npy','train_labels.npy','val_labels.npy']
result_dir = "/home/nikoong/Algorithm_test/dgd_person_reid/external/exp/results/"
for dataset in datasets:
    print dataset
    for label in labels:
        label1 = result_dir + parts[0]+ "/" + dataset + iters_part1 +label
        new_label =  result_dir + new_npy_dir +"/" + dataset + iters_new +label
        if not os.path.exists(result_dir + new_npy_dir +"/" + dataset + iters_new):
            os.makedirs(result_dir + new_npy_dir +"/" + dataset + iters_new)
        shutil.copyfile(label1,new_label)
    for feature in features:
        print feature
        src_dir_1 = result_dir + parts[0]+ "/" + dataset + iters_part1
        src_dir_2 = result_dir + parts[1]+"/" + dataset + iters_part2
        new_dir = result_dir + new_npy_dir +"/" + dataset + iters_new 
        src1 = np.load(os.path.join(src_dir_1, feature))
        src2 = np.load(os.path.join(src_dir_2, feature))
        src1 = list(src1)
        src2 = list(src2)
        new = []    
        if len(src1) == len(src2):    
            for i in range(len( src1)):
                a = src1[i]
                b = src2[i]
                new.append(np.maximum(a,b))           
        else: print "erroe! len(src1) != len(src2)"
        new = np.array(new)
              
        if not os.path.exists(new_dir):
            os.makedirs(new_dir)
        np.save(os.path.join(new_dir, feature),new)


#print TX[1]   
#print type(TX[1])
 
        
