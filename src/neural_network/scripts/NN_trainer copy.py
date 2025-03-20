#!/usr/bin/env python3
# coding=utf-8

import torch
import torch.nn as nn
import torch.optim as optim
import NN_engine as engine
import json
import time
import rospkg
import random
from copy import deepcopy

model = None
stamp = True
config = {}
model_path = rospkg.RosPack().get_path("neural_network") + "/data/models/NN_model.pth"
json_path = rospkg.RosPack().get_path("neural_network") + "/data/models/parameters.json"



def elaps_time(func):
    def inner(dataloader, n_epoch):
        t_start = time.time()
        func(dataloader, n_epoch)
        print("Elapsed time for training = ", time.time()-t_start, "s")
    
    return inner

    

@elaps_time
def training(dataloader, n_epoch):
    global model

    model.train()
    for epoch in range(n_epoch):
        for IN_data, OUT_data in dataloader: 
            outputs = model(IN_data)
            loss = model.loss(outputs, OUT_data)
            
            # Backpropagation
            loss.backward()
            model.optimizer.step()
            model.optimizer.zero_grad()

        if stamp:
            if (epoch + 1) % 10 == 0:
                print(f'Epoch [{epoch + 1}/{n_epoch}], Loss: {loss.item():.4f}')



def evaluation(dataloader):
    global model

    model.eval()
    with torch.no_grad():
        for IN_data, OUT_data in dataloader: 
            outputs = model(IN_data)
            loss = model.loss(outputs, OUT_data)

    return loss



def test(dataloader):
    global model

    total_correct = 0
    total_instances = 0

    model.eval()
    with torch.no_grad():
        for IN_data, OUT_data in dataloader: 
            print(model(IN_data))
            print(OUT_data)
            classifications = torch.argmax(model(IN_data), dim=1)
            print(classifications)
            total_correct += sum(classifications==OUT_data).item()
            total_instances += len(IN_data)

    return round(total_correct/total_instances, 3)



def set_config(loss, n1, n2, activation, loss, optimizer):
    global config 

    config["loss"] = loss
    config["n1"] = n1
    config["n2"] = n2
    config["activation"] = activation
    config["loss"] = loss
    config["optimizer"] = optimizer



def get_config():
    global config 

    n1 = config["n1"] 
    n2 = config["n2"]
    activation = config["activation"]
    loss = config["loss"]
    optimizer = config["optimizer"]

    return n1, n2, activation, loss, optimizer



def pick_random(list):
    ind = round(random.random()*(len(list)-1))

    return list[ind]




if __name__ == "__main__":
    n_epoch = 100
    batch = 500
    n1_list = [5, 10, 15, 20]
    n2_list = [None, 5, 10, 15, 20]
    activation_list = [nn.ReLU, nn.SELU, nn.CELU, nn.GELU, nn.Sigmoid, nn.SiLU, nn.Tanh]
    loss = [nn.L1Loss]
    optimizer_list = [optim.Adagrad, optim.Adam, optim.RMSprop, optim.SGD]
    
    dataset = engine.DS(batch)  

    doOnce = True
    for n1 in n1_list:
        for n2 in n2_list:
            for activation in activation_list:
                for optimizer in optimizer_list: 
                    print("------------------")

                    model = engine.NN(n1, n2, activation, loss, optimizer)
                    print(model)
                    print(model.optimizer)

                    training(dataset.train_dataloader, n_epoch)
                    loss = evaluation(dataset.eval_dataloader)[0]
                    print("loss = ", loss)

                    if doOnce:
                        set_config(loss, n1, n2, activation, loss, optimizer)
                        torch.save(model.state_dict(), model_path)
                        doOnce = False
                    else:
                        if config["loss"] > loss:
                            set_config(loss, n1, n2, activation, loss, optimizer)
                            torch.save(model.state_dict(), model_path)


    print("################################")
    print("######## Resulting NN ##########")
    print("################################")

    n1, n2, activation, loss, optimizer = get_config()
    model = engine.NN(n1, n2, activation, loss, optimizer)
    print(model)
    print(model.optimizer)

    #result = test(dataset.test_dataloader)

    print("final config = ", config)

    with open(json_path, "w") as file:
        json.dump(config, file, indent=4)


    #torch.save(model.state_dict(), model_path)
    #model.load_state_dict(torch.load(model_path, weights_only=False))
