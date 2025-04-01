#!/usr/bin/env python3
# coding=utf-8

import torch
import torch.nn as nn
import torch.optim as optim
from torchsummary import summary
import NN_engine as engine
import json
import time
import rospkg
from copy import deepcopy

model = None
stamp = True
config = {}
model_path = rospkg.RosPack().get_path("neural_network") + "/data/models/NN_model.pth"
json_path = rospkg.RosPack().get_path("neural_network") + "/data/models/hyperparams.json"



def elaps_time(func):
    def inner(dataloader, epochs):
        t_start = time.time()
        func(dataloader, epochs)
        print("Elapsed time for training = ", time.time()-t_start, "s")
    
    return inner

    

@elaps_time
def training(dataloader, epochs):
    global model

    tot_loss = 0

    print(f"\r\rEpoch: {'⬛'*20} - Loss = ...", end='')

    model.train()
    for epoch in range(epochs):
        for IN_data, OUT_data in dataloader: 
            outputs = model(IN_data)
            loss = model.loss(outputs, OUT_data)
            
            # Backpropagation
            model.optimizer.zero_grad()
            loss.backward()
            model.optimizer.step()
            
            tot_loss += loss

        size = len(dataloader)
        tot_loss /= size
        prog = round((epoch+1)/epochs*20)
        print(f"\rEpoch: {'⬜'*prog}{'⬛'*(20-prog)} - Loss: {tot_loss:>0.4f}", end='')
    
    print()



def evaluation(dataloader):
    global model

    tot_loss = 0
    correct = 0
    
    model.eval()
    with torch.no_grad():
        for IN_data, OUT_data in dataloader: 
            outputs = model(IN_data)
            tot_loss += model.loss(outputs, OUT_data).item()

            toll = 2*2.8973*0.01  #1% error of q7 range
            comp = (outputs < (OUT_data+toll)) == (outputs > (OUT_data-toll))
            correct += (comp).type(torch.float).sum().item()

    tot_loss /= len(dataloader)
    correct /= len(dataloader.dataset)
    print(f"Accuracy: {(100*correct):>0.1f}% - Loss: {tot_loss:>0.4f} \n")

    return tot_loss




def set_config(loss, epochs, batch_size, layers, activation_fn, loss_fn, optimizer_fn, lr):
    global config 

    config["loss"] = loss
    config["epochs"] = epochs
    config["batch_size"] = batch_size
    config["n1"] = layers[0]
    config["n2"] = layers[1]
    config["n3"] = layers[2]
    config["n4"] = layers[3]
    config["n5"] = layers[4]
    config["n6"] = layers[5]
    config["n7"] = layers[6]
    config["n8"] = layers[7]
    config["n9"] = layers[8]
    config["n10"] = layers[9]
    config["activation_fn"] = activation_fn
    config["loss_fn"] = loss_fn
    config["optimizer_fn"] = optimizer_fn
    config["lr"] = lr



def get_config():
    global config 

    layers =[]

    epochs = config["epochs"]
    batch_size = config["batch_size"]
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
    activation_fn = config["activation_fn"]
    loss_fn = config["loss_fn"]
    optimizer_fn = config["optimizer_fn"]
    lr = config["lr"]

    return epochs, batch_size, layers, activation_fn, loss_fn, optimizer_fn, lr



def save_config():
    global config 
    
    print(config)
    with open(json_path, "w") as file:
        json.dump(config, file, indent=4)




if __name__ == "__main__":
    epochs = 20
    batch_list = [1000]
    n1_list = [30]
    n2_list = [70]
    n3_list = [60, 65, 70]
    n4_list = [60, 65, 70]
    n5_list = [60, 65, 70]
    n6_list = [50, 55, 60]
    n7_list = [30, 35, 40]
    n8_list = [10, 15, 20]
    n9_list = [0, 5, 10]
    n10_list = [0, 5, 10]
    activation_list = ["nn.Tanh"]
    loss_list = ["nn.MSELoss"]
    optimizer_list = ["optim.Adam"]
    lr_list = [0.01]


    epochs = 100
    batch_list = [1000]
    n1_list = [30]
    n2_list = [70]
    n3_list = [60]
    n4_list = [70]
    n5_list = [60]
    n6_list = [55]
    n7_list = [35]
    n8_list = [15]
    n9_list = [5]
    n10_list = [0]
    activation_list = ["nn.Tanh"]
    loss_list = ["nn.MSELoss"]
    optimizer_list = ["optim.Adam"]
    lr_list = [0.01]


    layers_list = []
    for n1 in n1_list:
        layer = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        layer[0] = n1
        for n2 in n2_list:
            if n2 == 0:
                layers_list.append(deepcopy(layer))
                continue
            else:
                layer[1] = n2
            for n3 in n3_list:
                if n3 == 0:
                    layers_list.append(deepcopy(layer))
                    continue
                else:
                    layer[2] = n3
                for n4 in n4_list:
                    if n4 == 0:
                        layers_list.append(deepcopy(layer))
                        continue
                    else:
                        layer[3] = n4
                    for n5 in n5_list:
                        if n5 == 0:
                            layers_list.append(deepcopy(layer))
                            continue
                        else:
                            layer[4] = n5
                        for n6 in n6_list:
                            if n6 == 0:
                                layers_list.append(deepcopy(layer))
                                continue
                            else:
                                layer[5] = n6
                            for n7 in n7_list:
                                if n7 == 0:
                                    layers_list.append(deepcopy(layer))
                                    continue
                                else:
                                    layer[6] = n7
                                for n8 in n8_list:
                                    if n8 == 0:
                                        layers_list.append(deepcopy(layer))
                                        continue
                                    else:
                                        layer[7] = n8
                                    for n9 in n9_list:
                                        if n9 == 0:
                                            layers_list.append(deepcopy(layer))
                                            continue
                                        else:
                                            layer[8] = n9
                                        for n10 in n10_list:
                                            layer[9] = n10
                                            layers_list.append(deepcopy(layer))      
    
    cnt = 0
    n_iter = len(batch_list)*len(layers_list)*len(activation_list)*len(loss_list)*len(optimizer_list)*len(lr_list)

    doOnce = True
    for batch_size in batch_list:
        dataset = engine.DS(batch_size) 
        for layers in layers_list:
            for activation_fn in activation_list:
                for loss_fn in loss_list:
                    for optimizer_fn in optimizer_list: 
                        for lr in lr_list:
                            cnt += 1
                            print("\n===============================================================")
                            print(f"\tProgress: {cnt}/{n_iter}")
                            print("===============================================================")
                            if stamp:
                                print(f"\tBatch size: \t\t{batch_size}")
                                print(f"\tNeurons in layers: \t{layers}")
                                print(f"\tActivation function: \t{activation_fn}")
                                print(f"\tLoss function: \t\t{loss_fn}")
                                print(f"\tOptimization function: \t{optimizer_fn}")
                                print(f"\tLearning rate: \t\t{lr}")
                                print("---------------------------------------------------------------")
                            
                            model = engine.NN(layers, eval(activation_fn), eval(loss_fn), eval(optimizer_fn), lr)

                            print("\n--------- Training NN -----------------------------------------\n")
                            training(dataset.train_dataloader, epochs)

                            print("\n-------- Evaluating NN ----------------------------------------\n")
                            loss = evaluation(dataset.eval_dataloader)

                            if doOnce:
                                set_config(loss, epochs, batch_size, layers, activation_fn, loss_fn, optimizer_fn, lr)
                                torch.save(model.state_dict(), model_path)
                                doOnce = False
                            else:
                                if config["loss"] > loss:
                                    set_config(loss, epochs, batch_size, layers, activation_fn, loss_fn, optimizer_fn, lr)
                                    torch.save(model.state_dict(), model_path)

        epochs, batch_size, layers, activation_fn, loss_fn, optimizer_fn, lr = get_config()
        model = engine.NN(layers, eval(activation_fn), eval(loss_fn), eval(optimizer_fn), lr)
        model.load_state_dict(torch.load(model_path, weights_only=False))
        summary(model, input_size=(1, 7))

        print("\n--------- Testing NN -----------\n")
        evaluation(dataset.eval_dataloader)

        save_config()
