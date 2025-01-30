#!/usr/bin/env python3
# coding=utf-8

import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import Dataset, DataLoader, random_split
import sys
import numpy as np
import rospy


model = None
dataset = None
model_path = "/home/lozer/franka_emika_ws/src/neural_network/data/NN_model.pth"
dataset_path = "/home/lozer/franka_emika_ws/src/neural_network/data/dataset/humanPoses.csv"



class NN(nn.Module):
    def __init__(self):
        super(NN, self).__init__()
        self.fc1 = nn.Linear(7, 5)
        self.fc2 = nn.Linear(5, 5)
        self.fc3 = nn.Linear(5, 1)

        self.criterion = nn.MSELoss(reduction = 'mean')
        self.optimizer = optim.Adam(self.parameters(), lr=0.001)

    def forward(self, x):
        x = torch.relu(self.fc1(x))
        x = torch.relu(self.fc2(x))
        x = self.fc3(x)
        return x



class DS(Dataset): 
    def __init__(self, n_eval): 
        global dataset_path

        data = np.loadtxt(dataset_path, delimiter=',', dtype=np.float32, skiprows=1) 

        self.inputs = torch.from_numpy(data[:, 0:7]) 
        self.outputs = torch.from_numpy(data[:, [7]]) 
        self.n_samples = data.shape[0]  
        self.create_dataset(n_eval)
      
    def __getitem__(self, index): 
        return self.inputs[index], self.outputs[index] 

    def __len__(self): 
        return self.n_samples 

    def create_dataset(self, n_eval):
        if len(self) <= n_eval:
            raise ValueError('number of evaluation data bigger or equal than training data')
        else:
            train_data, eval_data = random_split(self, [len(self)-n_eval, n_eval])
            self.train_dataloader = DataLoader(dataset=train_data, batch_size=len(self)-n_eval, shuffle=True) 
            self.eval_dataloader = DataLoader(dataset=eval_data, batch_size=n_eval, shuffle=True) 



def training(n_epoch, dataloader):
    global model

    prev_loss = 1
    for epoch in range(n_epoch):
        model.train()
        for IN_train, OUT_train in dataloader: 
            outputs = model(IN_train)
            loss = model.criterion(outputs, OUT_train)
            
            model.optimizer.zero_grad()
            grad = loss.backward()
            model.optimizer.step()

        if loss.item() <= 0.0001:
            break

        if abs(loss.item() - prev_loss) <= 0.00000001:
            break

        prev_loss = loss.item()

        if (epoch + 1) % 100 == 0:
            print(f'Epoch [{epoch + 1}/{n_epoch}], Loss: {loss.item():.4f}')



def evaluation(dataloader, print_out=False):
    global model

    model.eval()
    with torch.no_grad():
        for IN_eval, OUT_eval in dataloader: 
            outputs = model(IN_eval)
            loss = model.criterion(outputs, OUT_eval)

            if print_out == True:
                print("\nINPUTS")
                print(IN_eval)

            print("\nOUTPUTS")
            print("------------------")
            print(f'Predictions:\n{torch.transpose(outputs, 0, 1)}')
            print("------------------")
            print(f'Real data:\n{torch.transpose(OUT_eval, 0, 1)}')



def solution(dataloader, print_out=False):
    global model

    model.eval()
    with torch.no_grad():
        outputs = model(dataloader)

        print("\nOUTPUTS")
        print("------------------")
        print(f'Solutions:\n{torch.transpose(outputs, 0, 1)}')

        return outputs
            



def neural_network(mod, inputData):
    global model, dataset, model_path

    model = mod    
    torch.set_default_dtype(torch.float32)
    dataloader = torch.tensor(inputData, dtype=torch.float32)
    sol = None

    if not model_path:
        raise ValueError('incorrect neural network model path')
    else:
        model.load_state_dict(torch.load(model_path, weights_only=False))
        sol = solution(dataloader, print_out=True)

    return sol




if __name__ == "__main__":
    model = NN()
    dataset = DS(1) 

    mode = sys.argv[1]
    if mode == "--train":
        n_epoch = 10000
        training(n_epoch, dataset.train_dataloader)
        torch.save(model.state_dict(), model_path)
    elif mode == "--eval":
        if not model_path:
            raise ValueError('incorrect NN model path')
        else:
            model.load_state_dict(torch.load(model_path, weights_only=False))
            evaluation(dataset.eval_dataloader, print_out=True)
    else:
        raise ValueError('argument required or wrong argument')

