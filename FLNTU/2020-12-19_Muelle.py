#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Comparamos las curvas de turbidez con los de otros instrumentos para la campaña de 2019-12-17.
"""

import sys
import os
import pandas as pd
#import numpy as np
import matplotlib.pyplot as plt
from scipy.odr import Model,RealData,ODR

path = os.path.dirname(os.path.realpath('__file__'))
sys.path.append(path)

TitleSize=15
AxisLabelSize=15
LegendSize=12
NumberSize=10

plt.close('all')

if os.name == 'posix':   # Linux
    Linux = True

plt.rc('text', usetex=Linux)
plt.rc('font', family='serif')

pathECO = '/home/santiago/Documents/L6-L7/FLNTU/Base de datos/Datos/regions/RdP/RdP_20191217_Muelle/ECO_FLNTUProcessed/RdP_20191217_ECO-FLNTU.xlsx'

pathOBS = '/home/santiago/Documents/L6-L7/FLNTU/Base de datos/Datos/regions/RdP/RdP_20191217_Muelle/campbellProcessed/RdP_20191217_Campbell.xlsx'

pathHACH = '/home/santiago/Documents/L6-L7/FLNTU/Base de datos/Datos/regions/RdP/RdP_20191217_Muelle/RdP_20191217.xlsx'

campaign = 'RdP_20191217_Muelle'
#%%

dataECO_Mean = pd.read_excel(pathECO ,sheet_name='Stations_Mean',skiprows=1)
dataOBS_Mean = pd.read_excel(pathOBS ,sheet_name='Stations_Mean',skiprows=1)
dataHACH_Mean = pd.read_excel(pathHACH ,sheet_name='turbidityHACH',skiprows=1)

dataECO_CV = pd.read_excel(pathECO ,sheet_name='Stations_CV',skiprows=1)
dataOBS_CV = pd.read_excel(pathOBS ,sheet_name='Stations_CV',skiprows=1)
dataHACH_CV = pd.read_excel(pathHACH ,sheet_name='turbidityHACH',skiprows=1)

ntu_ECO = dataECO_Mean['ntu (NTU)']
ntu_OBS = dataOBS_Mean['SS_OBS501_I2016[FNU]']
ntu_HACH = dataHACH_Mean['Mean']

# CV: coefficient of variation
ntu_ECO_err = dataECO_Mean['ntu (NTU)'] * dataECO_CV['ntu (NTU)']/100
ntu_OBS_err = dataOBS_Mean['SS_OBS501_I2016[FNU]'] * dataOBS_CV['SS_OBS501_I2016[FNU]']/100
ntu_HACH_err = dataHACH_Mean['Mean'] * dataHACH_CV['CV[%]']/100

#%%
# Gráfico:

plt.figure()

stations = range(1,13)

plt.plot(stations,ntu_ECO, '-o', color='orange', label=r'ECO')
plt.plot(stations,ntu_OBS, '-o', color='blue', label=r'OBS')
plt.plot(stations,ntu_HACH, '-o', color='red', label=r'HACH')

plt.legend(loc='best', fontsize=LegendSize)
plt.title(r'NTU (17 DIC 2019)', fontsize=TitleSize)
plt.xlabel(r'Station (STxx)', fontsize=AxisLabelSize)
plt.ylabel(r'NTU', fontsize=AxisLabelSize)
plt.grid(axis='both', color='k', linestyle='dashed', linewidth=2, alpha=0.2)
plt.show()

if Linux:
    plt.savefig(path + '/' + campaign + '.png')

#%% Ajuste:


#%%
# Gráfico OBS-ECO:

plt.figure()

stations = range(1,13)

plt.errorbar(ntu_OBS, ntu_ECO, xerr=ntu_OBS_err, yerr=ntu_ECO_err, fmt='o',color='blue', label=r'', ms=5.5, zorder=0)
#plt.plot(ntu_HACH,ntu_ECO, 'o', color='red', label=r'HACH')

plt.legend(loc='best', fontsize=LegendSize)
plt.title(r'2020-12-17 -- Muelle (Stations Mean)', fontsize=TitleSize)
plt.xlabel(r'OBS (FNU)', fontsize=AxisLabelSize)
plt.ylabel(r'ECO (NTU)', fontsize=AxisLabelSize)
plt.grid(axis='both', color='k', linestyle='dashed', linewidth=2, alpha=0.2)
plt.show()

if Linux:
    plt.savefig(path + '/' + campaign + '_OBS-ECO' +  '.png')

#%%
# Gráfico HACH-ECO:

plt.figure()

stations = range(1,13)

plt.errorbar(ntu_HACH, ntu_ECO, xerr=ntu_HACH_err, yerr=ntu_ECO_err, fmt='o',color='red', label=r'', ms=5.5, zorder=0)

plt.legend(loc='best', fontsize=LegendSize)
plt.title(r'2020-12-17 -- Muelle (Stations Mean)', fontsize=TitleSize)
plt.xlabel(r'HACH (NTU)', fontsize=AxisLabelSize)
plt.ylabel(r'ECO (NTU)', fontsize=AxisLabelSize)
plt.grid(axis='both', color='k', linestyle='dashed', linewidth=2, alpha=0.2)
plt.show()

if Linux:
    plt.savefig(path + '/' + campaign + '_HACH-ECO' +  '.png')