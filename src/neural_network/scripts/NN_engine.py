#!/usr/bin/env python3
# coding=utf-8

import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import Dataset, DataLoader, random_split
import json
import numpy as np
import rospkg

model_path = rospkg.RosPack().get_path("neural_network") + "/data/models/NN_model.pth"
dataset_path = rospkg.RosPack().get_path("neural_network") + "/data/dataset/main.csv"
json_path = rospkg.RosPack().get_path("neural_network") + "/data/models/hyperparams.json"



class NN(nn.Module):
    def __init__(self, layers, activation_fn, loss_fn, optimizer_fn, lr):
        super(NN, self).__init__()
        #self.flatten = nn.Flatten()
        if layers[1] == 0:
            self.layer_logic = nn.Sequential(
                nn.Linear(7, layers[0]),
                activation_fn(),
                nn.Linear(layers[0], 1)
            )
        elif layers[2] == 0:
            self.layer_logic = nn.Sequential(
                nn.Linear(7, layers[0]),
                activation_fn(),
                nn.Linear(layers[0], layers[1]),
                activation_fn(),
                nn.Linear(layers[1], 1)
            )
        elif layers[3] == 0:
            self.layer_logic = nn.Sequential(
                nn.Linear(7, layers[0]),
                activation_fn(),
                nn.Linear(layers[0], layers[1]),
                activation_fn(),
                nn.Linear(layers[1], layers[2]),
                activation_fn(),
                nn.Linear(layers[2], 1)
            )
        elif layers[4] == 0:
            self.layer_logic = nn.Sequential(
                nn.Linear(7, layers[0]),
                activation_fn(),
                nn.Linear(layers[0], layers[1]),
                activation_fn(),
                nn.Linear(layers[1], layers[2]),
                activation_fn(),
                nn.Linear(layers[2], layers[3]),
                activation_fn(),
                nn.Linear(layers[3], 1)
            )
        elif layers[5] == 0:
            self.layer_logic = nn.Sequential(
                nn.Linear(7, layers[0]),
                activation_fn(),
                nn.Linear(layers[0], layers[1]),
                activation_fn(),
                nn.Linear(layers[1], layers[2]),
                activation_fn(),
                nn.Linear(layers[2], layers[3]),
                activation_fn(),
                nn.Linear(layers[3], layers[4]),
                activation_fn(),
                nn.Linear(layers[4], 1)
            )
        elif layers[6] == 0:
            self.layer_logic = nn.Sequential(
                nn.Linear(7, layers[0]),
                activation_fn(),
                nn.Linear(layers[0], layers[1]),
                activation_fn(),
                nn.Linear(layers[1], layers[2]),
                activation_fn(),
                nn.Linear(layers[2], layers[3]),
                activation_fn(),
                nn.Linear(layers[3], layers[4]),
                activation_fn(),
                nn.Linear(layers[4], layers[5]),
                activation_fn(),
                nn.Linear(layers[5], 1)
            )
        elif layers[7] == 0:
            self.layer_logic = nn.Sequential(
                nn.Linear(7, layers[0]),
                activation_fn(),
                nn.Linear(layers[0], layers[1]),
                activation_fn(),
                nn.Linear(layers[1], layers[2]),
                activation_fn(),
                nn.Linear(layers[2], layers[3]),
                activation_fn(),
                nn.Linear(layers[3], layers[4]),
                activation_fn(),
                nn.Linear(layers[4], layers[5]),
                activation_fn(),
                nn.Linear(layers[5], layers[6]),
                activation_fn(),
                nn.Linear(layers[6], 1)
            )
        elif layers[8] == 0:
            self.layer_logic = nn.Sequential(
                nn.Linear(7, layers[0]),
                activation_fn(),
                nn.Linear(layers[0], layers[1]),
                activation_fn(),
                nn.Linear(layers[1], layers[2]),
                activation_fn(),
                nn.Linear(layers[2], layers[3]),
                activation_fn(),
                nn.Linear(layers[3], layers[4]),
                activation_fn(),
                nn.Linear(layers[4], layers[5]),
                activation_fn(),
                nn.Linear(layers[5], layers[6]),
                activation_fn(),
                nn.Linear(layers[6], layers[7]),
                activation_fn(),
                nn.Linear(layers[7], 1)
            )
        elif layers[9] == 0:
            self.layer_logic = nn.Sequential(
                nn.Linear(7, layers[0]),
                activation_fn(),
                nn.Linear(layers[0], layers[1]),
                activation_fn(),
                nn.Linear(layers[1], layers[2]),
                activation_fn(),
                nn.Linear(layers[2], layers[3]),
                activation_fn(),
                nn.Linear(layers[3], layers[4]),
                activation_fn(),
                nn.Linear(layers[4], layers[5]),
                activation_fn(),
                nn.Linear(layers[5], layers[6]),
                activation_fn(),
                nn.Linear(layers[6], layers[7]),
                activation_fn(),
                nn.Linear(layers[7], layers[8]),
                activation_fn(),
                nn.Linear(layers[8], 1)
            )
        else:
            self.layer_logic = nn.Sequential(
                nn.Linear(7, layers[0]),
                activation_fn(),
                nn.Linear(layers[0], layers[1]),
                activation_fn(),
                nn.Linear(layers[1], layers[2]),
                activation_fn(),
                nn.Linear(layers[2], layers[3]),
                activation_fn(),
                nn.Linear(layers[3], layers[4]),
                activation_fn(),
                nn.Linear(layers[4], layers[5]),
                activation_fn(),
                nn.Linear(layers[5], layers[6]),
                activation_fn(),
                nn.Linear(layers[6], layers[7]),
                activation_fn(),
                nn.Linear(layers[7], layers[8]),
                activation_fn(),
                nn.Linear(layers[8], layers[9]),
                activation_fn(),
                nn.Linear(layers[9], 1)
            )

        self.loss = loss_fn()
        self.optimizer = optimizer_fn(self.parameters(), lr=lr)

    def forward(self, input):
        #mid = self.flatten(input)
        output = self.layer_logic(input)
        
        return output



class DS(Dataset): 
    def __init__(self, batch_size): 
        global dataset_path

        data = np.loadtxt(dataset_path, delimiter=',', dtype=np.float32, skiprows=1) 

        self.inputs = torch.from_numpy(data[:, 0:7]) 
        self.outputs = torch.from_numpy(data[:, [7]]) 
        # self.outputs +=
        # print(max(self.outputs))
        # print(min(self.outputs))
        # quit()
        self.n_samples = data.shape[0] 
        self.create_dataset(batch_size)
      
    def __getitem__(self, index): 
        return self.inputs[index], self.outputs[index] 

    def __len__(self): 
        return self.n_samples 
    
    def create_dataset(self, batch_size):
        sz = int(0.2*len(self))
        eval_data, train_data = random_split(self, [sz, len(self)-sz]) 
        self.eval_dataloader = DataLoader(dataset=eval_data, batch_size=batch_size, shuffle=True)
        self.train_dataloader = DataLoader(dataset=train_data, batch_size=batch_size, shuffle=True)

    def create_dataset_OLD(self, batch_size):
        sz = int(0.2*len(self))
        test_data, eval_data, train_data = random_split(self, [sz, sz, len(self)-2*sz])
        self.test_dataloader = DataLoader(dataset=test_data, batch_size=batch_size, shuffle=True) 
        self.eval_dataloader = DataLoader(dataset=eval_data, batch_size=batch_size, shuffle=True)
        self.train_dataloader = DataLoader(dataset=train_data, batch_size=batch_size, shuffle=True)



def createModel():
    with open(json_path, "r") as file:
        config = json.load(file)

    layers =[]

    layers.append(config["n1"])
    layers.append(config["n2"])
    layers.append(config["n3"])
    layers.append(config["n4"])
    layers.append(config["n5"])
    layers.append(config["n6"])
    layers.append(config["n7"])
    layers.append(config["n8"])
    layers.append(config["n9"])
    layers.append(config["n10"])
    activation_fn = eval(config["activation_fn"])
    loss_fn = eval(config["loss_fn"])
    optimizer_fn = eval(config["optimizer_fn"])
    lr = config["lr"]

    model = NN(layers, activation_fn, loss_fn, optimizer_fn, lr)

    return model



def neuralNetwork(model, inputData):
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
