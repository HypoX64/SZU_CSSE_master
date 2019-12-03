import numpy as np
import torch
import dataloader
import model
import evaluation
from torch import nn, optim

#parameter
LR = 0.0001
EPOCHS = 100
BATCHSIZE = 1
CONTINUE = False
use_gpu = True
SAVE_FRE = 5


#train 0:1200    dev 1200:1460    test 1460: 2919
#load data
train_desc,train_price,test_desc = dataloader.load_all()

#def network
net = model.Linear(79,1024,1)
print(net)

if CONTINUE:
    net.load_state_dict(torch.load(dir_checkpoint+'last.pth'))
if use_gpu:
    net.cuda()
    # cudnn.benchmark = True

# optimizer = torch.optim.SGD(net.parameters(), lr=LR )
optimizer = torch.optim.Adam(net.parameters(), lr=LR )
criterion = nn.MSELoss()


for epoch in range(EPOCHS):
    print('Epoch {}/{}.'.format(epoch + 1, EPOCHS))
    
    net.train()
    price_pres = []
    price_trues = []
    for i in range(int(len(train_desc)/BATCHSIZE)):
        desc = np.zeros((BATCHSIZE,79), dtype=np.float32)
        price = np.zeros((BATCHSIZE,1), dtype=np.float32)
        for j in range(BATCHSIZE):   
            desc[j]=train_desc[i*BATCHSIZE+j:i*BATCHSIZE+j+1]
            price[j]=train_price[i*BATCHSIZE+j:i*BATCHSIZE+j+1]

        desc = torch.from_numpy(desc).cuda()
        price = torch.from_numpy(price).cuda()

        price_pre = net(desc)
        loss = criterion(price_pre, price)

        optimizer.zero_grad()
        loss.backward()
        optimizer.step()

        for j in range(BATCHSIZE):   
            price_trues.append(dataloader.convert2price(train_price[i*BATCHSIZE+j]))
            price_pres.append(dataloader.convert2price(price_pre.cpu().detach().numpy()[j][0]))
    train_loss = evaluation.RMSE(price_trues,price_pres)



    net.eval()
    price_pres = []
    for i in range(len(test_desc)):
        desc = (test_desc[i]).reshape(1,79)
        desc = torch.from_numpy(desc).cuda()
        price_pre = net(desc)
        price_pres.append(dataloader.convert2price(price_pre.cpu().detach().numpy()[0][0]))

    test_loss = evaluation.eval_test(price_pres)

    dataloader.write_csv(price_pres, './result_epoch'+str(epoch+1)+'.csv')

    print('--- Epoch train_loss:',train_loss,' test_loss:',test_loss)

