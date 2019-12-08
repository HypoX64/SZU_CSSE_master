import os
import csv
import numpy as np
import random
from sklearn.decomposition import PCA 
import evaluation
from description_map import value_map,fix_key,fix_miss,add_future,fix_LotFrontage

# load description_txt
description_txt = []
colon_indexs = []
for i,line in enumerate(open('./datasets/data_description.txt'),0):
    line = line.strip()
    if(':' in line[0:20]):
        colon_indexs.append(i)
    description_txt.append(line)
colon_indexs.append(524)#the end of description
description_length = len(colon_indexs)-1


Full_map = {}
desc_keys = []
for i in range(len(colon_indexs)-1):
    ori_map = {}
    my_map = {}
    desc_key = description_txt[colon_indexs[i]]
    desc_key = desc_key[:desc_key.find(':')]
    desc_keys.append(desc_key)
    # print(desc_key)
    interspace = colon_indexs[i+1]-colon_indexs[i]-2 #two space line

    if interspace == 0:
        ori_map['Just_num'] = 'None'
        Full_map[desc_key]=ori_map
    else:
        for j in range(interspace-1): #del low space line
            line = description_txt[colon_indexs[i]+j+2]
            key = line[:line.find('\t')]
            #data_description.txt is wrong here
            if key == 'NA ':
                key = 'NA'
            if key == 'WD ':
                key = 'WD'
            if key == 'BrkComm' or key =='Brk Cmn':
                key = 'BrkCmn'
            if desc_key in value_map:
                my_map[key] = value_map[desc_key][key]
                Full_map['my_'+desc_key]=my_map
            ori_map[key] = interspace-j-1 #change word to vector
            Full_map[desc_key]=ori_map


def normlize(npdata,justprice = False):
    _min = np.min(npdata)
    _max = np.max(npdata)
    if justprice:       
        _min = 34900.0
        _max = 755000.0
    return (npdata-_min)/(_max-_min)


def convert2price(tensor):
    return tensor*(755000.0-34900.0)+34900

def load_train():
    
    desc_map = {}
    price_map = {}
    csv_data = []
    #train_del_1299_524.csv
    reader = csv.reader(open('./datasets/train.csv'))
    for line in reader:
        csv_data.append(line)
    id_length = len(csv_data)-1

    for i in range(80):
        arr = np.zeros(id_length)
        my_arr = np.zeros(id_length)
        for j in range(id_length):
            key = csv_data[j+1][i+1]
            key = fix_key(key)
            if i == 79:
                arr[j] = float(key)
            else:
                #my map
                if desc_keys[i] in value_map:
                    if key == 'NA':
                        my_arr[j] = fix_miss(desc_keys[i])
                    else:
                        my_arr[j] = Full_map['my_'+desc_keys[i]][key]
                #auto map
                if key in Full_map[desc_keys[i]]:
                    arr[j] = Full_map[desc_keys[i]][key]
                else:
                    if key == 'NA':
                        arr[j] = fix_miss(desc_keys[i])
                    else:
                        arr[j] = float(key)
        if i == 79:        
            price_map['price']=arr
        else:
            if desc_keys[i] in value_map:
                desc_map['my_'+desc_keys[i]] = my_arr
            # else:
            desc_map[desc_keys[i]] = arr
    return desc_map,price_map

def load_test():
    desc_map = {}
    csv_data = []
    reader = csv.reader(open('./datasets/test.csv'))
    for line in reader:
        csv_data.append(line)
    id_length = len(csv_data)-1

    for i in range(79):
        arr = np.zeros(id_length)
        my_arr = np.zeros(id_length)
        for j in range(id_length):
            key = csv_data[j+1][i+1]
            key = fix_key(key)

            #my map
            if desc_keys[i] in value_map:
                if key == 'NA':
                    my_arr[j] = fix_miss(desc_keys[i])
                else:
                    my_arr[j] = Full_map['my_'+desc_keys[i]][key]

            #auto map
            if key in Full_map[desc_keys[i]]:
                arr[j] = Full_map[desc_keys[i]][key]
            else:
                if key == 'NA':
                    arr[j] = fix_miss(desc_keys[i])
                else:
                    arr[j] = float(key)

        if desc_keys[i] in value_map:
            desc_map['my_'+desc_keys[i]] = my_arr
        # else:
        desc_map[desc_keys[i]] = arr
    return desc_map
# for i,word in enumerate(wordlist,0):

def dict2numpy(dict_data):
    value_0 = list(dict_data.values())[0]
    np_data = np.zeros((len(value_0),len(dict_data)))
    for i,key in  enumerate(dict_data.keys(),0):
        np_data[:,i] = np.array(dict_data[key])
    return np_data

def load_all(dimension):

    train_desc_map,train_price_map = load_train()
    test_desc_map = load_test()
    desc_map = {}
    train_length = len(list(train_desc_map.values())[0])

    for key in train_desc_map.keys():
        desc_map[key] = np.concatenate((train_desc_map[key],test_desc_map[key]),axis=0)
        # desc_map[key] = normlize(desc_map[key])

    desc_map['LotFrontage'] = fix_LotFrontage(desc_map)
    desc_map['YearBuilt'] = (desc_map['YearBuilt']-1800)/10
    desc_map['YearRemodAdd'] = (desc_map['YearRemodAdd']-1800)/10
    desc_map = add_future(desc_map)

    for key in desc_map.keys():
        desc_map[key] = normlize(desc_map[key])

    desc_all = dict2numpy(desc_map)

    pca=PCA(n_components=dimension)     #加载PCA算法，设置降维后主成分数目为
    desc_all=pca.fit_transform(desc_all)#对样本进行降维

    train_price = normlize(np.array(train_price_map['price']),True)
    train_desc = desc_all[:train_length]
    test_desc = desc_all[train_length:]

    return train_desc.astype(np.float32),train_price.astype(np.float32),test_desc.astype(np.float32)

def write_csv(prices,path):
    csvFile = open(path, "w",newline='')  
    writer = csv.writer(csvFile)          
    writer.writerow(["Id","SalePrice"])
    for i in range(len(prices)):
        writer.writerow([str(i+1461),prices[i]])
    csvFile.close()

def main():
    load_all(80)

    # dimension = 80
    # train_desc,train_price,test_desc = load_all(dimension)

if __name__ == '__main__':
    main()

