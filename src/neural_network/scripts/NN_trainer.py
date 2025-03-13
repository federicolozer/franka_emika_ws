#!/usr/bin/env python3
# coding=utf-8

import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import Dataset, DataLoader, random_split
import sys
import numpy as np
import NN_engine as engine

model_path = "/home/lozer/franka_emika_ws/src/neural_network/data/model/NN_model.pth"
dataset_path = "/home/lozer/franka_emika_ws/src/neural_network/data/dataset/humanPoses.csv"



def training(n_epoch, dataloader):
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

        if (epoch + 1) % 100 == 0:
            print(f'Epoch [{epoch + 1}/{n_epoch}], Loss: {loss.item():.4f}')

    return loss.item()



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



def test(dataloader, print_out=False):
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





if __name__ == "__main__":
    
    dataset = DS(10) 
    print(len(dataset))
    print(":::::::::::::::::::")
    quit()

    batch #batch size
    batch #batch size
    batch #batch size
    batch #batch size

    for i in range(5):
        mode = sys.argv[1]
        if mode == "--train":
            n_epoch = 10000

            model = NN()
            dataset = DS(batch) 

            training(n_epoch, dataset.train_dataloader)




            torch.save(model.state_dict(), model_path)





        elif mode == "--eval":
            if not model_path:
                raise ValueError('wrong neural network model path')
            else:
                model.load_state_dict(torch.load(model_path, weights_only=False))


