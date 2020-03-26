import os
from itertools import zip_longest

import pandas as pd
import numpy as np

import pickle
import tables

import torch
import torch.utils.data as Data

import matplotlib.pyplot as plt
import matplotlib._color_data as mcd

from sklearn.metrics import *
from sklearn.metrics import roc_curve, auc
from sklearn.model_selection import train_test_split


def newdir(model_idx):
    cwd = os.getcwd()
    modelpath = 'model_' + str(model_idx)
    dirpath = os.path.join(cwd, modelpath)
    if not os.path.exists(dirpath):
        os.makedirs(dirpath)
    else:
        print('path already exists')


def plot_roc_pair(dic, file='model.jpg', y='y', yp='yp', size=[3, 3], lw=1, colors=mcd.XKCD_COLORS):
    plt.figure(figsize=size, dpi=300)
    roc_auc = {}
    for key, c in zip(dic.keys(), colors):
        fpr, tpr, threshold = roc_curve(
            dic[key][y],
            dic[key][yp]
        )
        roc_auc[key] = auc(fpr, tpr)
        plt.plot(
            fpr,
            tpr,
            lw=lw,
            color=c,
            alpha=0.3
        )
#     auc_min = min(zip(roc_auc.values(), roc_auc.keys()))
#     auc_mac = max(zip(roc_auc.values(), roc_auc.keys()))
#     plt.text(0.6, 0.2, f'{auc_mac[1]} (area = {auc_mac[0]:.3f})', fontsize=4)
#     plt.text(0.6, 0.15, f'{auc_min[1]} (area = {auc_min[0]:.3f})', fontsize=4)

    plt.plot(
        [0, 1],
        [0, 1],
        color='navy',
        lw=lw,
        linestyle='--'
    )

    plt.xlim([0.0, 1.0])
    plt.ylim([0.0, 1.0])
    plt.xlabel(
        'False Positive Rate',
        fontsize=11
    )
    plt.ylabel(
        'True Positive Rate',
        fontsize=11
    )
    #     plt.legend(loc="lower right")
    plt.tight_layout()
    plt.savefig(f'{file}')
    plt.show()
    
#     pickle.dump(fpr, open(file[:-4] + '_fpr.pkl', 'wb'))
#     pickle.dump(tpr, open(file[:-4] + '_tpr.pkl', 'wb'))

    pd.Series(roc_auc).to_csv(file[:-3] + 'csv', header=['AUROC'])


def cal_auc(model_index):
    df1 = pd.read_csv(f'./model_{model_index}/roc_train.csv')
    df2 = pd.read_csv(f'./model_{model_index}/roc_test.csv')
    print(f'model: {model_index}')
    print('mean of train: {}'.format(str(df1.mean()).split("\n")[0].split(' ')[-1]))
    print('mean of test: {}'.format(str(df2.mean()).split("\n")[0].split(' ')[-1]))
    print('median of train: {}'.format(str(df1.median()).split("\n")[0].split(' ')[-1]))
    print('median of test: {}'.format(str(df2.median()).split("\n")[0].split(' ')[-1]))
    print('minimun of train: {}'.format(str(df1.min()).split("\n")[1].split(' ')[-1]))
    print('minimum of test: {}'.format(str(df2.min()).split("\n")[1].split(' ')[-1]))

def prep_dataset(size):
    with tables.open_file(f'./datasets/fp_{size}indication.h5', 'r') as hdf5:
        x = hdf5.root.mol_fp[:]
        y = hdf5.root.mol_indication[:]
    x_train, x_test, y_train, y_test = train_test_split(x,y,test_size=0.1,random_state=0)

    x_train = torch.Tensor(x_train)
    x_test = torch.Tensor(x_test)
    y_train = torch.Tensor(y_train)
    y_test = torch.Tensor(y_test)

    train_dataset = Data.TensorDataset(x_train, y_train)
    test_dataset = Data.TensorDataset(x_test, y_test)

    return x_train, x_test, y_train, y_test, train_dataset, test_dataset

def prep_roc(x_train, x_test, y_train, y_test, model, size=100, batch_size=100, device = torch.device("cuda:0")):
    dic_train = {}
    dic_test = {}
    
    with open(f'./datasets/top{size}_indication.pickle', 'rb') as f:
        indications = pickle.load(f)
        
    for indication in indications.keys(): 
        dic_train[indication] = {}
        dic_test[indication] = {}
        dic_train[indication]['y'] = []
        dic_train[indication]['yp'] = []
        dic_test[indication]['y'] = []
        dic_test[indication]['yp'] = []

    x_train, y_train, x_test, y_test = x_train.to(device), y_train.to(device), x_test.to(device), y_test.to(device)

    batch_x_train = zip_longest(*[iter(x_train), ] * batch_size)
    y_train_pred = []
    with torch.no_grad():
        for batch in batch_x_train:
            batch = [tensor for tensor in batch if tensor is not None]
            batch = torch.stack(batch)
            y_train_pred.append(model(batch))
    y_train_pred = torch.cat(y_train_pred)

    batch_x_test = zip_longest(*[iter(x_test), ] * batch_size)
    y_test_pred = []
    with torch.no_grad():
        for batch in batch_x_test:
            batch = [tensor for tensor in batch if tensor is not None]
            batch = torch.stack(batch)
            y_test_pred.append(model(batch))
    y_test_pred = torch.cat(y_test_pred)

    for i, indication in enumerate(indications.keys()): 
        dic_train[indication]['y'] = y_train[:,i].cpu()
        dic_train[indication]['yp'] = y_train_pred[:,i].cpu()

    for i, indication in enumerate(indications.keys()): 
        dic_test[indication]['y'] = y_test[:,i].cpu()
        dic_test[indication]['yp'] = y_test_pred[:,i].cpu()
        
    return dic_train, dic_test