import numpy as np
import torch
import dataloader
import model
import evaluation
from torch import nn, optim
import time
import transformer
import matplotlib.pyplot as plt


#parameter
LR = 0.0002
EPOCHS = 5000
BATCHSIZE = 64
CONTINUE = False
use_gpu = True
Dimension = 128
#load data
train_desc,train_price,test_desc = dataloader.load_all(Dimension)
train_desc.tolist()
train_price.tolist()

#def network
net = model.Linear(Dimension)
# net = model.Residual_linear(Dimension)
print(net)

if CONTINUE:
    net.load_state_dict(torch.load(dir_checkpoint+'last.pth'))
if use_gpu:
    net.cuda()
    torch.backends.cudnn.benchmark = True

optimizer = torch.optim.Adam(net.parameters(), lr=LR )
criterion = nn.MSELoss()

test_loss_list = []
train_loss_list = []
for epoch in range(EPOCHS):
    print('Epoch {}/{}.'.format(epoch + 1, EPOCHS))
    
    t1 = time.time()
    net.train()
    price_pres = []
    price_trues = []

    transformer.match_random(train_desc, train_price)
    train_desc = np.array(train_desc)
    train_price = np.array(train_price)
    # train_desc = transformer.random_transform(train_desc, 0.02)
    # train_price = transformer.random_transform(train_price, 0.02)
    for i in range(int(len(train_desc)/BATCHSIZE)):
        desc = np.zeros((BATCHSIZE,Dimension), dtype=np.float32)
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
            price_trues.append(transformer.convert2price(train_price[i*BATCHSIZE+j]))
            price_pres.append(transformer.convert2price(price_pre.cpu().detach().numpy()[j][0]))
    train_loss = evaluation.RMSE(price_trues,price_pres)
    train_loss_list.append(train_loss)

    net.eval()
    price_pres = []
    for i in range(len(test_desc)):
        desc = (test_desc[i]).reshape(1,Dimension)
        desc = torch.from_numpy(desc).cuda()
        price_pre = net(desc)
        price_pres.append(transformer.convert2price(price_pre.cpu().detach().numpy()[0][0]))

    test_loss = evaluation.eval_test(price_pres)
    test_loss_list.append(test_loss)
    dataloader.write_csv(price_pres, './result/result_epoch'+str(epoch+1)+'.csv')

    t2 = time.time()
    print('--- Epoch train_loss:','%.6f'%train_loss,' test_loss:','%.6f'%test_loss,' cost time:','%.3f'%(t2-t1),'s')
    t1 = time.time()
    ##save module
    if epoch>10:
        if test_loss_list[epoch]<min(test_loss_list[:epoch-1]): 
            torch.save(net.cpu().state_dict(),'./checkpoints/'+'epoch'+str(epoch+1)+'.pth')
        if use_gpu:
            net.cuda()

min_loss = min(test_loss_list)
best_epoch = test_loss_list.index(min_loss)
print('\nmin_loss:',min_loss,'epoch:',best_epoch+1)

#####plot
plt.plot(train_loss_list)
plt.plot(test_loss_list)
plt.ylim((0.020,0.050))
plt.legend(['train','test'])
plt.xlabel('epoch')
plt.ylabel('loss')
plt.title('loss of model_1')
plt.savefig('./images/'+'%.6f'%min_loss+'_'+str(best_epoch+1)+'_model_1.png')
plt.show()