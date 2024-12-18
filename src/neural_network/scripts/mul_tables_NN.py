#!/usr/bin/env python3
# coding=utf-8

import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import Dataset, DataLoader 
import sys
import numpy as np


# Define the Neural Network Class
class NN(nn.Module):
    def __init__(self):
        super(NN, self).__init__()
        self.fc1 = nn.Linear(2, 10)  # Input layer to hidden layer
        self.fc2 = nn.Linear(10, 20)   # Hidden layer to hidden layer 
        self.fc3 = nn.Linear(20, 1)   # Hidden layer to output layer 

    def forward(self, x):
        x = torch.relu(self.fc1(x))  # Apply ReLU activation
        x = torch.relu(self.fc2(x))  # Apply ReLU activation
        x = self.fc3(x)               # Output layer
        return x



# Define the Dataset Class
class cDataSet(Dataset): 
    def __init__(self): 
        
        # loading the csv file from the folder path 
        data1 = np.loadtxt('../data/mul_tables.csv', delimiter=',', 
                           dtype=np.float32, skiprows=1) 
        
        self.x = torch.from_numpy(data1[:, 0:2]) 
        self.y = torch.from_numpy(data1[:, [2]]) 
        self.n_samples = data1.shape[0]  
      
    # support indexing such that dataset[i] can  
    # be used to get i-th sample 
    def __getitem__(self, index): 
        return self.x[index], self.y[index] 
        
    # we can call len(dataset) to return the size 
    def __len__(self): 
        return self.n_samples 



def training(n_epoch, dataloader):
    # Training the Model
    for epoch in range(n_epoch):  # Run for 100 epochs
        model.train()  # Set the model to training mode
        for X_train, y_train in dataloader: 
            # Forward pass
            outputs = model(X_train)
            loss = criterion(outputs, y_train)  # Calculate the loss
            
            # Backward pass and optimize
            optimizer.zero_grad()  # Clear previous gradients
            grad = loss.backward()  # Compute gradients
            optimizer.step()  # Update weights

        if loss.item() <= 0.01:
            break

        if (epoch + 1) % 100 == 0:  # Print loss every 10 epochs
            print(f'Epoch [{epoch + 1}/{n_epoch}], Loss: {loss.item():.4f}')



def evaluation():
    # Testing the Model
    model.eval()  # Set the model to evaluation mode
    with torch.no_grad():  # Disable gradient calculation
        test_data = torch.tensor([[4.0, 8.0], [6.0, 7.0], [5.0, 3.0], [7.0, 9.0]])
        predictions = model(test_data)  # Get predictions

        print()
        print("------------------")
        print(f'Predictions:\n{torch.round(predictions)}')
        print("------------------")
        print(f'Correct output:\n{test_data[:, 0]*test_data[:, 1]}')




if __name__ == "__main__":
    dataset = cDataSet() 
    dataloader = DataLoader(dataset=dataset, batch_size=100, shuffle=True) 

    # Instantiate the Model, Define Loss Function and Optimizer
    model = NN()  # Instantiate the model

    criterion = nn.MSELoss(reduction = 'mean')  # Mean Squared Error for regression
    optimizer = optim.Adam(model.parameters(), lr=0.001)  # Stochastic Gradient Descent 

    train = int(sys.argv[1])
    if train == 1:
        n_epoch = 10000
        training(n_epoch, dataloader)

        torch.save(model.state_dict(), "../data/mul_tables_NN_model.pth")

        evaluation()
    else:
        model.load_state_dict(torch.load("../data/mul_tables_NN_model.pth", weights_only=True))

        evaluation()
