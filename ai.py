""" This module is responsible for the ai part """
import collections
import numpy as np
import torch
import torch.nn as nn

class Network(nn.Module):

    def __init__(self,n_in=5,n_out=3):
        super(Network,self).__init__()
        self.net = nn.Sequential(
                nn.Linear(n_in,30),
                nn.ReLU(),
                nn.Linear(30,n_out))

    def forward(x):
        return self.net(x)
        

class Dqn(nn.Module):
    
    def __init__(self):
        super(Brain,self).__init__()

        # First initialize the Experince Buffer
