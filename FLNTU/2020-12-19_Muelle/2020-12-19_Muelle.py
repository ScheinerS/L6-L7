#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Comparamos las curvas de turbidez con los de otros instrumentos para la campaña de 2019-12-17.
"""

import sys
import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.odr import Model,RealData,ODR

path = os.path.dirname(os.path.realpath('__file__'))
sys.path.append(path)

TitleSize = 20
AxisLabelSize = 15
LegendSize = 15
NumberSize = 15

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
 
#def lineal_con_offset(p0,x):
#    a, b = p0 # parámetros iniciales
#    return a*x + b

def linear(p0,x):
    a, b = p0
    return a*x

def ODR_Fit(function,x,y,x_err,y_err):
    print('Fit:\t',function.__name__,'\n')
    # Create a model for fitting.
    model = Model(function)
    # Create a RealData object using our initiated data from above.
    D = RealData(x, y, sx=x_err, sy=y_err)
    # Set up ODR with the model and data.
    odr = ODR(D, model, beta0=[0.7, 0.])
    # Run the regression.
    out = odr.run()
    # Use the in-built pprint method to give us results.
    out.pprint()
    print('\n')
    return out

print(40*'*'+'\n\t\tOBS\n'+40*'*')
fit_OBS = ODR_Fit(linear, ntu_OBS, ntu_ECO, ntu_OBS_err, ntu_ECO_err)

print(40*'*'+'\n\t\tHACH\n'+40*'*')
fit_HACH = ODR_Fit(linear, ntu_HACH, ntu_ECO, ntu_HACH_err, ntu_ECO_err)

#%%
# Gráfico OBS-ECO:

plt.figure()

plt.errorbar(ntu_OBS, ntu_ECO, xerr=ntu_OBS_err, yerr=ntu_ECO_err, fmt='o',color='blue', label=r'', ms=5.5, zorder=0)

[m, b] = fit_OBS.beta
x = np.linspace(0, max(ntu_OBS), 50)
y = m*x + b

plt.plot(x,y, color='skyblue', label=r'%.4g $x$ + %.4g'%(m,b))

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

plt.errorbar(ntu_HACH, ntu_ECO, xerr=ntu_HACH_err, yerr=ntu_ECO_err, fmt='o',color='red', label=r'', ms=5.5, zorder=0)

[m, b] = fit_HACH.beta
x = np.linspace(0, max(ntu_HACH), 50)
y = m*x + b

plt.plot(x,y, color='coral', label=r'%.4g $x$ + %.4g'%(m,b))

plt.legend(loc='best', fontsize=LegendSize)
plt.title(r'2020-12-17 -- Muelle (Stations Mean)', fontsize=TitleSize)
plt.xlabel(r'HACH (NTU)', fontsize=AxisLabelSize)
plt.ylabel(r'ECO (NTU)', fontsize=AxisLabelSize)
plt.grid(axis='both', color='k', linestyle='dashed', linewidth=2, alpha=0.2)
plt.show()

if Linux:
    plt.savefig(path + '/' + campaign + '_HACH-ECO' +  '.png')