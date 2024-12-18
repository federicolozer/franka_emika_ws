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
        self.fc1 = nn.Linear(6, 15)
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
                           dtype=np.float32, skiprows=2) 
        
        self.inputs = torch.from_numpy(data[:, 0:6]) 
        self.outputs = torch.from_numpy(data[:, [6]]) 
        self.n_samples = data.shape[0]  
      

    def __getitem__(self, index): 
        return self.inputs[index], self.outputs[index] 

    def __len__(self): 
        return self.n_samples 



def training(n_epoch, dataloader):
    for epoch in range(n_epoch):
        model.train()
        for X_train, y_train in dataloader: 
            outputs = model(X_train)
            loss = criterion(outputs, y_train)
            
            optimizer.zero_grad()
            grad = loss.backward()
            optimizer.step()

        if loss.item() <= 0.01:
            break

        if (epoch + 1) % 100 == 0:
            print(f'Epoch [{epoch + 1}/{n_epoch}], Loss: {loss.item():.4f}')



def evaluation():
    model.eval()
    with torch.no_grad():
        test_data = torch.tensor([[4.0, 2.0], [3.0, 3.0], [5.0, 3.0], [7.0, 7.0]])
        predictions = model(test_data)

        print()
        print("------------------")
        print(f'Predictions:\n{predictions}')
        print("------------------")
        print(f'Correct output:\n{torch.tensor([[8.0], [9.0], [15.0], [49.0]])}')



if __name__ == "__main__":
    #rospy.init_node('NN', anonymous=True)

    model = NN()

    dataset = cDataSet() 
    train_data, eval_data = random_split(dataset, [100, 10])
    dataloader = DataLoader(dataset=train_data, batch_size=100, shuffle=True) 

    criterion = nn.MSELoss(reduction = 'mean')
    optimizer = optim.Adam(model.parameters(), lr=0.001)

    train = int(sys.argv[1])
    if train == 1:
        n_epoch = 10000
        training(n_epoch, dataloader)

        torch.save(model.state_dict(), "/home/lozer/franka_emika_ws/src/neural_network/data/robot_pose_NN_model.pth")

        evaluation()
    else:
        model.load_state_dict(torch.load("/home/lozer/franka_emika_ws/src/neural_network/data/robot_pose_NN_model.pth", weights_only=True))

        evaluation_new()
