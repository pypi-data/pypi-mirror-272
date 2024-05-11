
import torch
from torch import nn



class PFLModel(nn.Module):
    def __init__(self, n_obj=2):
        super().__init__()
        # self.args = args
        hidden_size = 128
        self.model = nn.Sequential(
            nn.Linear(n_obj, hidden_size),
            nn.ReLU(),
            nn.Linear(hidden_size, hidden_size),
            nn.ReLU(),
            nn.Linear(hidden_size, hidden_size),
            nn.ReLU(),
            nn.Linear(hidden_size, n_obj)
        )

    def forward(self, x):
        '''
        :param x: input
        :return: the predicted Pareto front
        '''
        # raise NotImplementedError
        return self.model(x)