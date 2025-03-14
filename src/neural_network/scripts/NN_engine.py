#!/usr/bin/env python3
# coding=utf-8

import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import Dataset, DataLoader, random_split
import numpy as np
import rospkg

model_path = rospkg.RosPack().get_path("neural_network") + "/data/model/NN_model.pth"
dataset_path = rospkg.RosPack().get_path("neural_network") + "/data/dataset/humanPoses.csv"



class NN_new(nn.Module):
    def __init__(self, n1, n2, criterion, optimizer):
        super(NN, self).__init__()
        if n2 == None:
            self.layer1 = nn.Linear(7, n1)
            self.layer2 = nn.Linear(n1, 1)
        else:
            self.layer1 = nn.Linear(7, n1)
            self.layer2 = nn.Linear(n1, n2)
            self.layer3 = nn.Linear(n2, 1)

        self.criterion = criterion
        self.optimizer = optimizer

    def forward(self, x):
        x = torch.relu(self.layer1(x))
        x = self.layer2(x)
        return x

class NN(nn.Module):
    def __init__(self, n1):
        super(NN, self).__init__()
        self.layer1 = nn.Linear(7, n1)
        self.layer2 = nn.Linear(n1, 1)

        self.criterion = nn.MSELoss(reduction = 'mean')
        self.optimizer = optim.SGD(self.parameters(), lr=0.001)

    def forward(self, x):
        x = torch.relu(self.layer1(x))
        x = self.layer2(x)
        return x
    


    


class DS(Dataset): 
    def __init__(self, batch): 
        global dataset_path

        data = np.loadtxt(dataset_path, delimiter=',', dtype=np.float32, skiprows=1) 

        self.inputs = torch.from_numpy(data[:, 0:7]) 
        self.outputs = torch.from_numpy(data[:, [7]]) 
        self.n_samples = data.shape[0] 
        self.create_dataset(batch)
      
    def __getitem__(self, index): 
        return self.inputs[index], self.outputs[index] 

    def __len__(self): 
        return self.n_samples 

    def create_dataset(self, batch):
        sz = int(0.2*len(self))
        test_data, eval_data, train_data = random_split(self, [sz, sz, len(self)-2*sz])
        self.test_dataloader = DataLoader(dataset=test_data, batch_size=batch, shuffle=True) 
        self.eval_dataloader = DataLoader(dataset=eval_data, batch_size=batch, shuffle=True)
        self.train_dataloader = DataLoader(dataset=train_data, batch_size=batch, shuffle=True)



def neural_network(model, inputData):
    global model_path

    torch.set_default_dtype(torch.float32)
    IN_data = torch.tensor(inputData, dtype=torch.float32)
    sol = None

    if model_path:
        model.load_state_dict(torch.load(model_path, weights_only=False))
        model.eval()
        with torch.no_grad():
            sol = model(IN_data)
    else:
        raise ValueError('wrong neural network model path')
        
    return sol
