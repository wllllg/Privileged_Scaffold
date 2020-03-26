import torch
from torch import nn
from torch.nn import functional as F

class MLP(nn.Module):
    def __init__(self, in_features, h1, h2, out_features):
        super().__init__()
        self.fc1 = nn.Linear(in_features, h1)
        self.bn1 = nn.BatchNorm1d(h1)
        self.fc2 = nn.Linear(h1, h2)
        self.bn2 = nn.BatchNorm1d(h2)
        self.fc3 = nn.Linear(h2, out_features)

    def forward(self, x):
        x = self.bn1(F.leaky_relu(self.fc1(x)))
        x = self.bn2(F.leaky_relu(self.fc2(x)))
        x = torch.sigmoid(self.fc3(x))
        return x