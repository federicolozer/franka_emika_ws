#!/usr/bin/env python3
# coding=utf-8

import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import Dataset, DataLoader, random_split
import numpy as np

model_path = "/home/lozer/franka_emika_ws/src/neural_network/data/model/NN_model.pth"



class NN(nn.Module):
    def __init__(self):
        super(NN, self).__init__()
        self.fc1 = nn.ReLU(7, 5)
        self.fc2 = nn.Linear(5, 1)

        self.criterion = nn.MSELoss(reduction = 'mean')
        self.optimizer = optim.SGD(self.parameters(), lr=0.001)

    def forward(self, x):
        x = torch.relu(self.fc1(x))
        x = self.fc2(x)
        return x



class DS(Dataset): 
    def __init__(self, batch): 
        global dataset_path

        data = np.loadtxt(dataset_path, delimiter=',', dtype=np.float32, skiprows=1) 

        self.inputs = torch.from_numpy(data[:, 0:7]) 
        self.outputs = torch.from_numpy(data[:, [7]]) 
        self.n_samples = data.shape[0] 
        self.create_dataset(batch)
      
    def getitem(self, index): 
        return self.inputs[index], self.outputs[index] 

    def __len__(self): 
        return self.n_samples 

    def create_dataset(self, batch):
        sz = int(0.2*len(self))
        test_data, eval_data, train_data = random_split(self, [sz, sz, len(self)-2*sz])
        self.test_dataloader = DataLoader(dataset=test_data, batch_size=batch, shuffle=True) 
        self.eval_dataloader = DataLoader(dataset=eval_data, batch_size=batch, shuffle=True)
        self.train_dataloader = DataLoader(dataset=train_data, batch_size=batch, shuffle=True)



def neural_network(mod, inputData):
    model = mod    

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
