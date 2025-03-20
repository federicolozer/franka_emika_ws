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
import sys
from copy import deepcopy

model = None
stamp = False
config = {}
model_path = rospkg.RosPack().get_path("neural_network") + "/data/models/NN_model.pth"
json_path = rospkg.RosPack().get_path("neural_network") + "/data/models/hyperparams.json"



def progress(it, prefix="", size=60, out=sys.stdout): # Python3.6+
    count = len(it)
    start = time.time() # time estimate start
    def show(j):
        x = int(size*j/count)
        # time estimate calculation and string
        remaining = ((time.time() - start) / j) * (count - j)        
        mins, sec = divmod(remaining, 60) # limited to minutes
        time_str = f"{int(mins):02}:{sec:03.1f}"
        print(f"{prefix}[{u'█'*x}{('.'*(size-x))}] {j}/{count} Est wait {time_str}", end='\r', file=out, flush=True)
    show(0.1) # avoid div/0 
    for i, item in enumerate(it):
        yield item
        show(i+1)
    print("\n", flush=True, file=out)



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
            loss.backward()
            model.optimizer.step()
            model.optimizer.zero_grad()

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

            toll = 0.03  #1% error in 180 degrees
            comp = (outputs < (OUT_data+toll)) == (outputs > (OUT_data-toll))
            correct += (comp).type(torch.float).sum().item()

    tot_loss /= len(dataloader)
    correct /= len(dataloader.dataset)
    print(f"Accuracy: {(100*correct):>0.1f}% - Loss: {tot_loss:>0.4f} \n")

    return tot_loss




def set_config(loss, epochs, batch_size, n1, n2, activation_fn, loss_fn, optimizer_fn, lr):
    global config 

    config["loss"] = loss
    config["epochs"] = epochs
    config["batch_size"] = batch_size
    config["n1"] = n1
    config["n2"] = n2
    config["activation_fn"] = activation_fn
    config["loss_fn"] = loss_fn
    config["optimizer_fn"] = optimizer_fn
    config["lr"] = lr



def get_config():
    global config 

    epochs = config["epochs"]
    batch_size = config["batch_size"]
    n1 = config["n1"] 
    n2 = config["n2"]
    activation_fn = config["activation_fn"]
    loss_fn = config["loss_fn"]
    optimizer_fn = config["optimizer_fn"]
    lr = config["lr"]

    return epochs, batch_size, n1, n2, activation_fn, loss_fn, optimizer_fn, lr



def save_config():
    global config 
    
    epochs, batch_size, n1, n2, activation_fn, loss_fn, optimizer_fn, lr = get_config()
    set_config(loss, epochs, batch_size, n1, n2, str(activation_fn), str(loss_fn), str(optimizer_fn), lr)
    
    print(config)
    with open(json_path, "w") as file:
        json.dump(config, file, indent=4)




if __name__ == "__main__":
    epochs = 100
    batch_list = [1000]
    n1_list = [5, 10, 15, 20]
    n2_list = [0, 5, 10, 15, 20]
    activation_list = [nn.ReLU, nn.Sigmoid, nn.Tanh]
    loss_list = [nn.MSELoss]
    optimizer_list = [optim.Adagrad, optim.Adam, optim.RMSprop, optim.SGD]
    lr_list = [0.1, 0.01, 0.001]
    
    cnt = 0
    n_iter = len(batch_list)*len(n1_list)*len(n2_list)*len(activation_list)*len(loss_list)*len(optimizer_list)*len(lr_list)

    doOnce = True
    for batch_size in batch_list:
        dataset = engine.DS(batch_size) 
        for n1 in n1_list:
            for n2 in n2_list:
                for activation_fn in activation_list:
                    for loss_fn in loss_list:
                        for optimizer_fn in optimizer_list: 
                            for lr in lr_list:
                                cnt += 1
                                print("\n=============================================================")
                                print(f"\tProgress: {cnt}/{n_iter}")
                                print("===============================================================")
                                if stamp:
                                    print(f"\tBatch size: \t{batch_size}")
                                    print(f"\tNeurons in the first layer: \t{n1}")
                                    print(f"\tNeurons in the second layer: \t{n2}")
                                    print(f"\tActivation function: \t{activation_fn}")
                                    print(f"\tLoss function: \t{loss_fn}")
                                    print(f"\tOptimization function: \t{optimizer_fn}")
                                    print(f"\tLearning rate: \t{lr}")
                                    print("---------------------------------------------------------------")
                                
                                model = engine.NN(n1, n2, activation_fn, loss_fn, optimizer_fn, lr)

                                print("\n--------- Training NN ----------\n")
                                training(dataset.train_dataloader, epochs)

                                print("\n-------- Evaluating NN ---------\n")
                                loss = evaluation(dataset.eval_dataloader)

                                if doOnce:
                                    set_config(loss, epochs, batch_size, n1, n2, activation_fn, loss_fn, optimizer_fn, lr)
                                    torch.save(model.state_dict(), model_path)
                                    doOnce = False
                                else:
                                    if config["loss"] > loss:
                                        set_config(loss, epochs, batch_size, n1, n2, activation_fn, loss_fn, optimizer_fn, lr)
                                        torch.save(model.state_dict(), model_path)

        epochs, batch_size, n1, n2, activation_fn, loss_fn, optimizer_fn, lr = get_config()
        model = engine.NN(n1, n2, activation_fn, loss_fn, optimizer_fn, lr)
        model.load_state_dict(torch.load(model_path, weights_only=False))
        summary(model, input_size=(1, 7))

        print("\n--------- Testing NN -----------\n")
        evaluation(dataset.test_dataloader)

        

        save_config()

        quit()
