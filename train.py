import numpy as np
import torch
import dataloader
import model
from torch import nn, optim

#parameter
LR = 0.0001
EPOCHS = 5
BATCHSIZE = 12
CONTINUE = False
use_gpu = True
SAVE_FRE = 5
MOD = 'dev'
print('MOD:', MOD)


#train 0:1200    dev 1200:1460    test 1460: 2919
#load data
train_desc,train_price,test_desc = dataloader.load_all()

#def network
net = model.Linear(79,256,1)
print(net)

if CONTINUE:
    net.load_state_dict(torch.load(dir_checkpoint+'last.pth'))
if use_gpu:
    net.cuda()
    # cudnn.benchmark = True

optimizer = torch.optim.Adam(net.parameters(), lr=LR )
# criterion = nn.L1Loss()
criterion = nn.MSELoss()



if MOD == 'dev':
    dev_avg_loss = []
    for epoch in range(EPOCHS):
        print('Epoch {}/{}.'.format(epoch + 1, EPOCHS))
        net.train()
        epoch_loss_train = 0
        for i in range(1200):
            desc = (train_desc[i]).reshape(1,79)
            price = (np.array(train_price[i])).reshape(1,1)
            desc = torch.from_numpy(desc).cuda()
            price = torch.from_numpy(price).cuda()

            price_pre = net(desc)
            loss = criterion(price_pre, price)
            epoch_loss_train += loss.item()

            optimizer.zero_grad()
            loss.backward()
            optimizer.step()

        net.eval()
        epoch_loss_dev = 0
        for i in range(1200,1460):
            desc = (train_desc[i]).reshape(1,79)
            price = (np.array(train_price[i])).reshape(1,1)
            desc = torch.from_numpy(desc).cuda()
            price = torch.from_numpy(price).cuda()

            price_pre = net(desc)
            loss = criterion(price_pre, price)
            epoch_loss_dev += loss.item()
            # if epoch == 0:
            #     print(dataloader.convert2price(price_pre.cpu().detach().numpy()))

        print('--- Epoch train_loss:',epoch_loss_train/1200,'dev_loss:',epoch_loss_dev/260)
    #     if epoch>=10:
    #         dev_avg_loss.append(epoch_loss_dev/260)
    # print('dev_avg_loss:',np.mean(dev_avg_loss))

elif MOD == 'test':
    dev_avg_loss = []
    for epoch in range(EPOCHS):
        print('Epoch {}/{}.'.format(epoch + 1, EPOCHS))
        net.train()
        epoch_loss_train = 0
        for i in range(1460):
            desc = (train_desc[i]).reshape(1,79)
            price = (np.array(train_price[i])).reshape(1,1)
            desc = torch.from_numpy(desc).cuda()
            price = torch.from_numpy(price).cuda()

            price_pre = net(desc)
            loss = criterion(price_pre, price)
            epoch_loss_train += loss.item()

            optimizer.zero_grad()
            loss.backward()
            optimizer.step()

        net.eval()
        epoch_loss_dev = 0
        price_pres = []
        for i in range(1459):
            desc = (test_desc[i]).reshape(1,79)
            desc = torch.from_numpy(desc).cuda()
            price_pre = net(desc)
            price_pres.append(dataloader.convert2price(price_pre.cpu().detach().numpy()[0][0]))
        dataloader.write_csv(price_pres, './result_epoch'+str(epoch+1)+'.csv')

        print('--- Epoch train_loss:',epoch_loss_train/1460)

