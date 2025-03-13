#!/usr/bin/env python3
# coding=utf-8

import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import Dataset, DataLoader, random_split
import sys
import numpy as np
import os


model = None
dataset = None
model_path = "/home/lozer/franka_emika_ws/src/neural_network/data/model/NN_model.pth"
dataset_path = "/home/lozer/franka_emika_ws/src/neural_network/data/dataset/humanPoses.csv"



class NN(nn.Module):
    def __init__(self):
        super(NN, self).__init__()
        self.fc1 = nn.Linear(7, 5)  #relu 
        self.fc2 = nn.Linear(5, 1)

        self.criterion = nn.MSELoss(reduction = 'mean')
        self.optimizer = optim.SGD(self.parameters(), lr=0.001)

    def forward(self, x):
        x = torch.relu(self.fc1(x))
        x = self.fc2(x)
        return x



class DS(Dataset): 
    def __init__(self): 
        global dataset_path

        data = np.loadtxt(dataset_path, delimiter=',', dtype=np.float32, skiprows=1) 

        self.inputs = torch.from_numpy(data[:, 0:7]) 
        self.outputs = torch.from_numpy(data[:, [7]]) 
        self.n_samples = data.shape[0]  
        self.create_dataset()
      
    def __getitem__(self, index): 
        return self.inputs[index], self.outputs[index] 

    def __len__(self): 
        return self.n_samples 

    def create_dataset(self):
        test_data, eval_data, train_data = random_split(self, [len(self)-10, 10])
        self.train_dataloader = DataLoader(dataset=train_data, batch_size=int(len(self)/n_cpu), shuffle=True, num_workers=os.cpu_count()) 
        self.eval_dataloader = DataLoader(dataset=eval_data, batch_size=10, shuffle=True) 



def training(n_epoch, dataloader):
    global model

    prev_loss = 1
    for epoch in range(n_epoch):
        model.train()
        for IN_data, OUT_data in dataloader: 
            outputs = model(IN_data)
            loss = model.criterion(outputs, OUT_data)
            
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
        for IN_data, OUT_data in dataloader: 
            outputs = model(IN_data)
            loss = model.criterion(outputs, OUT_data)

            if print_out == True:
                print("\nINPUTS")
                print(IN_data)

            print("\nOUTPUTS")
            print("------------------")
            print(f'Predictions:\n{torch.transpose(outputs, 0, 1)}')
            print("------------------")
            print(f'Real data:\n{torch.transpose(OUT_data, 0, 1)}')



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




if __name__ == "__main__":
    model = NN()
    dataset = DS() 


    quit()

    try:
        mode = sys.argv[1]
        if mode == "--train":
            n_epoch = 10000
            training(n_epoch, dataset.train_dataloader)
            torch.save(model.state_dict(), model_path)
        elif mode == "--eval":
            if not model_path:
                raise ValueError('wrong neural network model path')
            else:
                model.load_state_dict(torch.load(model_path, weights_only=False))
                evaluation(dataset.eval_dataloader, print_out=True)
        else:
            raise ValueError('wrong argument')
    except:
        raise ValueError('argument required')

