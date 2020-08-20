#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Comparación de los espectros del Trios y los de las CA.

Los datos de Trios estan en RdP_20191210_Trios_QC_RhowStd750_SatSensors.xlsx

Y los de los diferentes CA en matchUps_RdP_VNOAA20_GW94-SWIR12_rhow_visnir_3x3_s3vt.xlsx

"""


import sys
import os
import matplotlib.pyplot as plt
import glob
#from matplotlib import rcParams, cycler
#import csv
#import numpy as np
import pandas as pd


path = os.path.dirname(os.path.realpath('__file__'))
sys.path.append(path)

TitleSize = 15
AxisLabelSize = 15
LegendSize = 10
NumberSize = 15

plt.close('all')

plt.rc('text', usetex=True)
plt.rc('font', family='serif')

CV_threshold = 20


#path_Trios10 = 'RdP_20191210_Trios_QC_RhowStd750_SatSensors.xlsx'

#path_Trios17 = 'RdP_20191217_Trios_QC_RhowStd750_SatSensors.xlsx'

l = [410, 443, 486, 551, 671, 745, 862]
l_IMG = [411, 445, 489, 556, 667, 746, 868]

data_Trios_10_st06 = [0.021421366665521, 0.026871622850528, 0.03544487982624, 0.053593607118962, 0.056071425609191, 0.026539213633342, 0.014580383505945]
data_Trios_17_st11 = [0.023863436633459, 0.030196618964652, 0.04046881531125, 0.063253887427756, 0.061992684957239, 0.027771661342758, 0.01529295257163]


files = glob.glob('CA/*.xlsx')

data_IMG = {}

for f in files:
    algoritmo = f.split('_')[3]
    data_IMG[algoritmo] = pd.read_excel(f, sheet_name='rhow_Mean', skiprows=None)
    data_IMG[algoritmo] = data_IMG[algoritmo].set_index('Unnamed: 0')


colores_algoritmos = {'GW94-SWIR12': 'blue',
                      'GW94-SWIR13': 'red',
                      'GW94-SWIR23': 'orange',
                      'PCA-SWIR12': 'darkgreen',
                      'PCA-SWIR13': 'purple',
                      'PCA-SWIR23': 'brown',
                      'PCA-SWIR123': 'gray'}

#%%

plt.figure()

plt.plot(l, data_Trios_10_st06, '--o', color='black', label='2019-12-10 ST06')

for algoritmo in list(data_IMG.keys()):
    try:
        plt.plot(l_IMG, data_IMG[algoritmo].loc['RdP_20191210_ST06'], '-o', label=algoritmo, color=colores_algoritmos[algoritmo])
    except:
        print('Error:\t', algoritmo)
        #print(data_IMG[algoritmo].loc['RdP_20191210_ST06'])

plt.ylim((0,0.1))
plt.legend(loc='best', fontsize=LegendSize)
plt.title(r'RdP 20191210 ST06', fontsize=TitleSize)
plt.xlabel(r'$\lambda$ (nm)', fontsize=AxisLabelSize)
plt.ylabel(r'$\rho$', fontsize=AxisLabelSize)
plt.grid(axis='both', color='k', linestyle='dashed', linewidth=2, alpha=0.2)
plt.show()

plt.savefig('Espectros_10.png')

#%%


plt.figure()

plt.plot(l, data_Trios_17_st11, '--s', color='black', label='2019-12-17 ST11')


for algoritmo in list(data_IMG.keys()):
    try:
        plt.plot(l_IMG, data_IMG[algoritmo].loc['RdP_20191217_ST11'], '-o', label=algoritmo, color=colores_algoritmos[algoritmo])
    except:
        print('Error:\t', algoritmo)

plt.ylim((0,0.1))
plt.legend(loc='best', fontsize=LegendSize)
plt.title(r'RdP 20191217 ST11', fontsize=TitleSize)
plt.xlabel(r'$\lambda$ (nm)', fontsize=AxisLabelSize)
plt.ylabel(r'$\rho$', fontsize=AxisLabelSize)
plt.grid(axis='both', color='k', linestyle='dashed', linewidth=2, alpha=0.2)
plt.show()

plt.savefig('Espectros_17.png')

