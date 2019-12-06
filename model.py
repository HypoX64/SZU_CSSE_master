import numpy as np
import torch
import torch.utils.data as Data
from torch import nn, optim
from torch.autograd import Variable
import torch.nn.functional as F


class Linear(nn.Module):
    def __init__(self, n_feature, n_hidden, n_output):
        super(Linear, self).__init__()
        self.fc1 = torch.nn.Linear(n_feature, n_hidden)   # hidden layer
        self.relu = nn.ReLU(inplace=True)
        self.dropout = nn.Dropout(0.2)
        self.fc2 = torch.nn.Linear(n_hidden, n_output)   # output layer

    def forward(self, x):
        x = self.fc1(x)
        x = self.relu(x)
        x = self.dropout(x)
        x = self.fc2(x)
        return x
