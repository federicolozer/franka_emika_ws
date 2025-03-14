#!/usr/bin/env python3
# coding=utf-8

import torch
import torch.nn as nn
import torch.optim as optim
import NN_engine as engine
import json
import time
import rospkg

model = None
model_path = rospkg.RosPack().get_path("neural_network") + "/data/model/NN_model.pth"
dataset_path = rospkg.RosPack().get_path("neural_network") + "data/dataset/humanPoses.csv"
json_path = rospkg.RosPack().get_path("user_interface") + "/data/model/config.json"



def elaps_time(func):
    def inner(dataloader, n_epoch, prnt):
        t_start = time.time()
        func(dataloader, n_epoch, prnt)
        print("Elapsed time for training = ", time.time()-t_start, "s")
    
    return inner

    

@elaps_time
def training(dataloader, n_epoch, prnt=False):
    global model

    prev_loss = 1
    for epoch in range(n_epoch):
        model.train()
        for IN_data, OUT_data in dataloader: 
            outputs = model(IN_data)
            loss = model.criterion(outputs, OUT_data)
            
            model.optimizer.zero_grad()
            loss.backward()
            model.optimizer.step()

        if loss.item() <= 0.000001:
            break

        if abs(loss.item() - prev_loss) <= 0.000001:
            break
        prev_loss = loss.item()

        if prnt:
            if (epoch + 1) % 10 == 0:
                print(f'Epoch [{epoch + 1}/{n_epoch}], Loss: {loss.item():.4f}')



def evaluation(dataloader):
    global model

    model.eval()
    with torch.no_grad():
        for IN_data, OUT_data in dataloader: 
            outputs = model(IN_data)
            loss = model.criterion(outputs, OUT_data)

    return loss



def test(dataloader):
    global model

    total_correct = 0
    total_instances = 0

    model.eval()
    with torch.no_grad():
        for IN_data, OUT_data in dataloader: 
            classifications = torch.argmax(model(IN_data), dim=1)
            total_correct += sum(classifications==OUT_data).item()
            total_instances += len(IN_data)

    return round(total_correct/total_instances, 3)



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




if __name__ == "__main__":
    n_epoch = 1000
    batch = 10 

    print("------------------")

    model = NN(8)
    dataset = engine.DS(batch) 

    training(dataset.train_dataloader, n_epoch, True)
    loss = evaluation(dataset.eval_dataloader)
    print("Loss = ", loss)

    accuracy = evaluation(dataset.test_dataloader)
    print("Accuracy = ", accuracy)

    torch.save(model.state_dict(), model_path)



