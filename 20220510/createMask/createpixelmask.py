#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon May  9 16:18:26 2022

@author: julianschmehr
"""


import numpy as np
import matplotlib.pyplot as plt
import h5py
import os

chippositions = np.array([[260,0],[260,260],[0,0],[0,260]])
rotation = np.array([1,3,1,3])
chipno = 4
def load_data(file):
    fh5 = h5py.File(file,'r')
    key = 'entry/instrument/detector/data'
    output=np.asarray(fh5[key])
   
    del fh5
    return output

def createmask(data):
    chipdata = np.zeros([chipno,100,256,256])
    for i in range(chipno):
        chipdata[i] = np.rot90(data[:,chippositions[i,0]:chippositions[i,0]+256,chippositions[i,1]:chippositions[i,1]+256],k=-rotation[i],axes=(1,2))
    chipdatasummed = np.sum(chipdata,axis=1)
    chipmask = np.where(chipdatasummed>3,1,0)
    for i in range(chipno):
        filen = 'Chip'+str(i+1)+'_mask.bin'
        chipmask[i].astype('>i2').flatten().tofile(filen)
    return chipmask



file = "/home/xspadmin/tmp/darks-4keV_00000.nxs"


data = load_data(file)
mask = createmask(data)

plt.imshow(mask[0],vmin=0,vmax=1)
plt.show()
