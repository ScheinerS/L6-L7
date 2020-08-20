
import sys
import os
import matplotlib.pyplot as plt
#from matplotlib import rcParams, cycler
#import csv
import numpy as np
import pandas as pd
from scipy.optimize import curve_fit

#import Matchups as M

path = os.path.dirname(os.path.realpath('__file__'))
sys.path.append(path)

TitleSize = 15
AxisLabelSize = 15
LegendSize = 12
NumberSize = 15

plt.close('all')

plt.rc('text', usetex=True)
#plt.rc('font', family='serif')

CV_threshold = 20


data_IMG= pd.read_excel('Datos/IMG.xlsx', skiprows=None)
data_Trios= pd.read_excel('Datos/TriOS.xlsx', skiprows=None)

longitudes = [645, 860]
A = {645: 228.1, 860: 3078.9}
C = {645: 0.1641, 860: 0.2112}

rho_Trios = {}


Campaign = ['20191210 ST06', '20191217 ST11']
T_Trios_645 = [23.005171, 28.917258]
T_Trios_860 = [49.025266, 51.199416]


def D2015(l, rho):
    return (A[l]*rho)/(1-rho/C[l])

data_IMG['T_645'] = D2015(645, data_IMG[667])
data_IMG['T_860'] = D2015(860, data_IMG[868])

#data_Trios['T_645'] = D2015(645, data_Trios['645.0'])
#data_Trios['T_860'] = D2015(860, data_Trios['860.0'])

# Algo anda mal, debería dar:
data_Trios['T_645'] = [23.005171, 28.917258]
data_Trios['T_860'] = [49.025266, 51.199416]

#%%

# 645 nm:

plt.figure()

for i in range(len(data_IMG)):
    plt.scatter(data_IMG['StationID'][i], data_IMG['T_645'][i], label=data_IMG['Algoritmo'][i])

#plt.scatter(data_IMG['StationID'], data_IMG['T_645'], label='IMG')
plt.scatter(data_Trios['StationID'], data_Trios['T_645'], color='black', label='TriOS')

plt.legend(loc='best', fontsize=LegendSize)
plt.title(r'645 nm', fontsize=TitleSize)
plt.xlabel(r'Estación', fontsize=AxisLabelSize)
plt.ylabel(r'D2015 (FNU)', fontsize=AxisLabelSize)
plt.grid(axis='both', color='k', linestyle='dashed', linewidth=2, alpha=0.2)
plt.show()

plt.savefig('_645nm.png')

#%%

# 860 nm:

plt.figure()

for i in range(len(data_IMG)):
    plt.scatter(data_IMG['StationID'][i], data_IMG['T_860'][i], label=data_IMG['Algoritmo'][i])

#plt.scatter(data_IMG['StationID'], data_IMG['T_860'], label='IMG')
plt.scatter(data_Trios['StationID'], data_Trios['T_860'], color='black', label='TriOS')

plt.legend(loc='best', fontsize=LegendSize)
plt.title(r'860 nm', fontsize=TitleSize)
plt.xlabel(r'Estación', fontsize=AxisLabelSize)
plt.ylabel(r'D2015 (FNU)', fontsize=AxisLabelSize)
plt.grid(axis='both', color='k', linestyle='dashed', linewidth=2, alpha=0.2)
plt.show()

plt.savefig('_860nm.png')