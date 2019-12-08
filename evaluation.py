import csv
import math
import numpy as np
import dataloader
import transformer

def load_submission(path):
    csv_data = []
    price = []
    reader = csv.reader(open(path))
    for line in reader:
        csv_data.append(line)
    for i in range(len(csv_data)):
        if i != 0:
            price.append(float(csv_data[i][1]))
    return price 

def eval_test(records_predict):
    records_real = load_submission('./datasets/ground_true_submission.csv')
    return RMSE(records_real, records_predict)

def RMSE(records_real,records_predict):
    # records_real = np.log1p(records_real)
    # records_predict = np.log1p(records_predict)
    records_real = dataloader.normlize(np.array(records_real),True)
    records_predict = dataloader.normlize(np.array(records_predict),True)
    if len(records_real) == len(records_predict):
        return math.sqrt(sum([(x - y) ** 2 for x, y in zip(records_real, records_predict)]) / len(records_real))
    else:
        print('error: length !=')
        return None

def main():
    # my_price = load_submission('./datasets/sample_submission.csv')
    my_price = load_submission('./result/keras_untuned.csv')

    print(eval_test(my_price))
if __name__ == '__main__':
    main()