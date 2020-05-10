import numpy as np
import torch
import torch.utils.data as Data
from torch import nn, optim
from torch.autograd import Variable
import torch.nn.functional as F

##model1##
class Linear(nn.Module):
    def __init__(self, n_feature):
        super(Linear, self).__init__()
        self.fc = nn.Sequential(
            nn.Linear(n_feature, 256),
            nn.Sigmoid(),
            nn.Dropout(0.2)
        )
        self.output = nn.Linear(256, 1)   

    def forward(self, x):
        x = self.fc(x)
        x = self.output(x) 
        return x


class Residual_linear(nn.Module):
    def __init__(self, n_feature):
        super(Residual_linear, self).__init__()
        self.fc = nn.Sequential(
            nn.Linear(n_feature, 256),
            nn.ReLU(inplace=True),
            nn.Linear(256, 1024),
            nn.ReLU(inplace=True),
            nn.Linear(1024, 128),
            nn.ReLU(inplace=True),
            nn.Dropout(0.2)
        )
        self.shortcut = nn.Sequential(
            nn.Linear(n_feature, 128)
        )
        self.output = nn.Sequential(
            nn.Linear(128, 1)
        )


    def forward(self, x):
        x_shortcut = self.shortcut(x)
        x = self.fc(x)
        x = x+x_shortcut
        x = torch.sigmoid(x)
        x = self.output(x)
        return x



