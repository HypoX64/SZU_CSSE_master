import os
import csv
import numpy as np
# import matplotlib.pyplot as plt

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
print('Description length:',description_length)



descriptions = []
for i in range(len(colon_indexs)-1):
    mapping = {}
    description_title = description_txt[colon_indexs[i]]
    interspace = colon_indexs[i+1]-colon_indexs[i]-2 #two space line
    if interspace == 0:
        mapping['Just_num'] = 'None'
        descriptions.append(mapping)
    else:
        for j in range(interspace-1): #del low space line
            line = description_txt[colon_indexs[i]+j+2]
            mapping_key = line[:line.find('\t')]
            #data_description.txt is wrong here
            if mapping_key == 'NA ':
                mapping_key = 'NA'
            if mapping_key == 'WD ':
                mapping_key = 'WD'
            if mapping_key == 'BrkComm' or mapping_key =='Brk Cmn':
                mapping_key = 'BrkCmn'
            mapping[mapping_key] = j
        descriptions.append(mapping)
# print(descriptions)


def normlize(npdata):
    _min = np.min(npdata)
    _max = np.max(npdata)
    return (npdata-_min)/(_max-_min)

def convert2price(tensor):
    return tensor*(755000.0-34900.0)+34900


def fix_key(key):
    #csv is wrong here
    if key == 'Wd Shng':
        key='WdShing'
    if key == '2fmCon':
        key='2FmCon'
    if key == 'NAmes':
        key='Names'
    if key == 'Duplex':
        key='Duplx'
    if key == 'CmentBd':
        key='CemntBd'
    if key == 'C (all)':
        key='C'
    if key == 'Twnhs':
        key='TwnhsI'
    if key == 'Brk Cmn' or key =='BrkComm':
        key='BrkCmn'
    else:
        key = key
    return key

def load_train():
    ##load train csv
    csv_data = []
    reader = csv.reader(open('./datasets/train.csv'))
    for line in reader:
        csv_data.append(line)
    id_length = len(csv_data)-1

    data = np.zeros((id_length,description_length+1))
    for i in range(id_length):
        for j in range(description_length+1):
            key = csv_data[i+1][j+1]
            key = fix_key(key)
            if j == description_length:
                data[i][j] = float(key)
            else:
                if key in descriptions[j]: #SalePrice
                    data[i][j] = float(descriptions[j][key])
                else:#just num here
                    # print(i,j)
                    if key == 'NA':
                        key = 0;
                    data[i][j] = float(key)
    return data

def load_test():
    ##load train csv
    csv_data = []
    reader = csv.reader(open('./datasets/test.csv'))
    for line in reader:
        csv_data.append(line)
    id_length = len(csv_data)-1

    data = np.zeros((id_length,description_length))
    for i in range(id_length):
        for j in range(description_length):
            key = csv_data[i+1][j+1]
            key = fix_key(key)
            if j == description_length:
                data[i][j] = float(key)
            else:
                if key in descriptions[j]: #SalePrice
                    data[i][j] = float(descriptions[j][key])
                else:#just num here
                    # print(i,j)
                    if key == 'NA':
                        key = 0;
                    data[i][j] = float(key)
    return data

def load_all():
    train_desc = load_train()[:,:79]
    train_price = load_train()[:,79]
    test_desc = load_test()
    desc_all = np.concatenate((train_desc,test_desc),axis=0)
    for i in range(description_length):
        desc_all[:,i] = normlize(desc_all[:,i])
    train_price = normlize(train_price)
    train_desc = desc_all[:1460]
    test_desc = desc_all[1460:]
    return train_desc.astype(np.float32),train_price.astype(np.float32),test_desc.astype(np.float32)

def write_csv(prices,path):
    csvFile = open(path, "w",newline='')  
    writer = csv.writer(csvFile)          
    writer.writerow(["Id","SalePrice"])
    for i in range(len(prices)):
        writer.writerow([str(i+1461),prices[i]])
    csvFile.close()

def main():
    train_desc,train_price,test_desc = load_all()
    print(train_price)
    write_csv(train_price, './result.csv')
    # print(data)
    # plt.plot(data[1])
    # plt.show()
if __name__ == '__main__':
    main()

