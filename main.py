import os
import shutil

from multiprocessing import cpu_count
from itertools import zip_longest

from random import shuffle
from copy import deepcopy

import rdkit
from rdkit import Chem
from rdkit.Chem import AllChem

from ipypb import track

import pickle
import tables

import torch
from torch import nn
from torch.nn import functional as F
from torch.utils.tensorboard import SummaryWriter
import torch.utils.data as Data

import adabound

import pandas as pd

import numpy as np

import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import matplotlib._color_data as mcd

from sklearn.metrics import *
from sklearn.metrics import roc_curve, auc
from sklearn.model_selection import train_test_split

from utils import *
from model import *

size = 100 # from 100 to 500
model_idx = f'size_{size}'

device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
x_train, x_test, y_train, y_test, train_dataset, test_dataset = prep_dataset(size)

if os.path.exists(f'./model_{model_idx}'):
    shutil.rmtree(f'./model_{model_idx}')
newdir(model_idx)
with SummaryWriter(f'./model_{model_idx}/') as writer:
        mlp = MLP(2048, 2400, 1500, size)
        mlp = mlp.to(device)
        optim = adabound.AdaBound(mlp.parameters(), lr=1e-3, final_lr=0.1)
        loss_fn = torch.nn.BCELoss()
        mlp.train()
        num_epoch = 1000
        BATCH_SIZE = 1024
        total_step = 0
        
        for epoch in range(num_epoch): 
            train_loader = Data.DataLoader(
                dataset=train_dataset,
                batch_size=BATCH_SIZE,
                shuffle=True,
                num_workers=1)
            for step, train_data in enumerate(train_loader):
                total_step += 1
                x_batch, y_batch = train_data
                x_batch, y_batch = x_batch.to(device), y_batch.to(device)
                y_pred = mlp(x_batch)                
                optim.zero_grad()
                loss = loss_fn(y_pred, y_batch)
                loss.backward()
                optim.step()
                writer.add_scalar('train_loss', loss.item(), total_step)
            
            if (epoch%10 - 9)==0:
                torch.save(mlp, f'./model_{model_idx}/mlp_ckpt_{str(epoch)}')
                
            test_loader = Data.DataLoader(
                dataset=test_dataset,
                batch_size=BATCH_SIZE,
                shuffle=False,
                num_workers=1)
            test_loss = 0
            test_step = 0
            for step, test_data in enumerate(test_loader):
                x_batch, y_batch = test_data
                x_batch, y_batch = x_batch.to(device), y_batch.to(device)
                y_pred = mlp(x_batch)
                test_loss += loss_fn(y_pred, y_batch)
                test_step += 1
            test_loss /= test_step
            writer.add_scalar('test_loss', test_loss.item(), total_step)
            
mlp.eval()

dic_train, dic_test = prep_roc(x_train, x_test, y_train, y_test, model=mlp, size=size)

plot_roc_pair(
    dic_train,
    file=f'./model_{model_idx}/roc_train.jpg'
)
plot_roc_pair(
    dic_test,
    file=f'./model_{model_idx}/roc_test.jpg'
)
cal_auc(model_idx)
