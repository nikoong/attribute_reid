
txtname_list = ["train","val","test_gallery","test_probe"]
dataset_list=["3dpes","cuhk01","cuhk03","ilids","prid","viper"]

for dataset in dataset_list:
    for txtname in txtname_list:
        file1 = open("/home/nikoong/Algorithm_test/dgd_person_reid/external/exp/datasets/"+dataset+"/"+txtname+".txt") 
        file2 = open("/home/nikoong/Algorithm_test/dgd_person_reid/external/exp/datasets/"+dataset+"/txt/"+txtname+".txt","a")
        for line in file1.readlines():
            line1 = "/home/nikoong/Algorithm_test/dgd_person_reid/external/exp/datasets/"+dataset+"/" + line
            file2.write(line1)
       
file1.close() 
file2.close() 
