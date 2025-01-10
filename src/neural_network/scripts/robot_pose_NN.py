#!/usr/bin/env python3
# coding=utf-8

import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import Dataset, DataLoader, random_split
import sys
import numpy as np
import rospy



class NN(nn.Module):
    def __init__(self):
        super(NN, self).__init__()
        self.fc1 = nn.Linear(7, 15)
        self.fc2 = nn.Linear(15, 10)
        self.fc3 = nn.Linear(10, 1)

    def forward(self, x):
        x = torch.relu(self.fc1(x))
        x = torch.relu(self.fc2(x))
        x = self.fc3(x)
        return x




class cDataSet(Dataset): 
    def __init__(self): 
        data = np.loadtxt('/home/lozer/franka_emika_ws/src/neural_network/data/poses.csv', delimiter=',', 
                           dtype=np.float32, skiprows=1) 
        
        self.inputs = torch.from_numpy(data[:, 0:7]) 
        self.outputs = torch.from_numpy(data[:, [7]]) 
        self.n_samples = data.shape[0]  
      

    def __getitem__(self, index): 
        return self.inputs[index], self.outputs[index] 

    def __len__(self): 
        return self.n_samples 



def training(n_epoch, dataloader):
    for epoch in range(n_epoch):
        model.train()
        for IN_train, OUT_train in dataloader: 
            outputs = model(IN_train)
            loss = criterion(outputs, OUT_train)
            
            optimizer.zero_grad()
            grad = loss.backward()
            optimizer.step()

        if loss.item() <= 0.0001:
            break

        if (epoch + 1) % 100 == 0:
            print(f'Epoch [{epoch + 1}/{n_epoch}], Loss: {loss.item():.4f}')



def evaluation(dataloader, print_out=False):
    model.eval()
    with torch.no_grad():
        for IN_train, OUT_train in dataloader: 
            outputs = model(IN_train)
            loss = criterion(outputs, OUT_train)

            if print_out == True:
                print("INPUTS")
                print(IN_train)

            print()
            print("OUTPUTS")
            print("------------------")
            print(f'Predictions:\n{torch.transpose(outputs, 0, 1)}')
            print("------------------")
            print(f'Ground truth:\n{torch.transpose(OUT_train, 0, 1)}')



if __name__ == "__main__":
    #rospy.init_node('NN', anonymous=True)

    model = NN()

    dataset = cDataSet() 
    train_data, eval_data, test_data = random_split(dataset, [1000, 5, 1])
    train_dataloader = DataLoader(dataset=train_data, batch_size=100, shuffle=True) 
    eval_dataloader = DataLoader(dataset=eval_data, batch_size=5, shuffle=True) 
    test_dataloader = DataLoader(dataset=test_data, batch_size=1, shuffle=True) 

    criterion = nn.MSELoss(reduction = 'mean')
    optimizer = optim.Adam(model.parameters(), lr=0.001)

    train = sys.argv[1]
    if train == "train":
        n_epoch = 10000
        training(n_epoch, train_dataloader)

        torch.save(model.state_dict(), "/home/lozer/franka_emika_ws/src/neural_network/data/robot_pose_NN_model.pth")

        evaluation(eval_dataloader, print_out=True)

    elif train == "eval":
        model.load_state_dict(torch.load("/home/lozer/franka_emika_ws/src/neural_network/data/robot_pose_NN_model.pth", weights_only=False))

        evaluation(eval_dataloader)
    
    elif train == "test":
        model.load_state_dict(torch.load("/home/lozer/franka_emika_ws/src/neural_network/data/robot_pose_NN_model.pth", weights_only=False))

        evaluation(test_dataloader, print_out=True)
