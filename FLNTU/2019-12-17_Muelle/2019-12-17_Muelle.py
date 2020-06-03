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
#import datetime as dt
import matplotlib.dates as md

path = os.path.dirname(os.path.realpath('__file__'))
sys.path.append(path)

TitleSize = 15
AxisLabelSize = 12
LegendSize = 12
NumberSize = 12

plt.close('all')

if os.name == 'posix':
    Linux = True

plt.rc('text', usetex=Linux)
plt.rc('font', family='serif')


campaign = 'RdP_20191217_Muelle'

#%% Continuous:
# ECO:
pathECO_Continuous = '/home/santiago/Documents/L6-L7/FLNTU/Base de datos/Datos/regions/RdP/RdP_20191217_Muelle/ECO_FLNTU/RdP_20191217_cleaned.xlsx'
pathECO_Smooth1min = '/home/santiago/Documents/L6-L7/FLNTU/Base de datos/Datos/regions/RdP/RdP_20191217_Muelle/ECO_FLNTUProcessed/RdP_20191217_ECO-FLNTU.xlsx'

# OBS:
pathOBS_Continuous = '/home/santiago/Documents/L6-L7/FLNTU/Base de datos/Datos/regions/RdP/RdP_20191217_Muelle/campbellContinuous/CR800_I2016.dat'
pathOBS_Smooth1min = '/home/santiago/Documents/L6-L7/FLNTU/Base de datos/Datos/regions/RdP/RdP_20191217_Muelle/campbellProcessed/RdP_20191217_Campbell.xlsx'

# HACH:
# No hay datos en contiuno para el Hach.

dataECO_Continuous = pd.read_excel(pathECO_Continuous)#,delimiter="\t", skiprows=0, header=None,usecols=range(0,7))
dataOBS_Continuous = pd.read_csv(pathOBS_Continuous, delimiter=",", skiprows=1)

dataECO_Smooth1min = pd.read_excel(pathECO_Smooth1min, sheet_name='ECOContSmooth1min')
dataOBS_Smooth1min = pd.read_excel(pathOBS_Smooth1min, sheet_name='CR800_I2016ContSmooth1min')

dataOBS_Continuous.drop(index=[0,1], inplace=True)

# ECO:
time_ECO_Continuous = dataECO_Continuous['timestamp']
ntu_ECO_Continuous = dataECO_Continuous['turbidity (NTU)']
chl_ECO_Continuous = dataECO_Continuous['chl (ug/l)']
time_ECO_Smooth1min = dataECO_Smooth1min['Unnamed: 0']
ntu_ECO_Smooth1min = dataECO_Smooth1min['turbidity (NTU)Mean']
chl_ECO_Smooth1min = dataECO_Smooth1min['chl (ug/l)Mean']


# OBS:
time_OBS_Continuous = dataOBS_Continuous['TIMESTAMP']
ntu_OBS_Continuous = dataOBS_Continuous['SS_OBS501_I2016']
time_OBS_Smooth1min = dataOBS_Smooth1min['Unnamed: 0']
ntu_OBS_Smooth1min = dataOBS_Smooth1min['SS_OBS501_I2016[FNU]Mean']


# Convertimos los tiempos a formato de fecha:
    
time_ECO_Continuous = pd.to_datetime(time_ECO_Continuous)
time_OBS_Continuous = pd.to_datetime(time_OBS_Continuous)

# Pasamos los números a float, porque están como string:
ntu_OBS_Continuous = pd.to_numeric(ntu_OBS_Continuous)


#%%
# Gráfico (ECO y OBS - mediciones en continuo):

plt.figure()


plt.plot(time_OBS_Continuous, ntu_OBS_Continuous, '-', color='blue', label=r'OBS501 (2016) [SS]')
plt.plot(time_ECO_Continuous, ntu_ECO_Continuous, '-', color='orange', label=r'ECO FLNTU')
#plt.plot(stations,ntu_HACH, '-o', color='red', label=r'HACH')

plt.legend(loc='best', fontsize=LegendSize)
plt.title(r'Continuo (2019-12-17 - Muelle)', fontsize=TitleSize)
plt.xlabel(r'UTC Time', fontsize=AxisLabelSize)
plt.ylabel(r'ECO (NTU), OBS (FNU)', fontsize=AxisLabelSize)
#plt.ylim(0,300)
plt.xticks(rotation=25)
ax=plt.gca()
xfmt = md.DateFormatter('%H:%M')
#xfmt = md.DateFormatter('%Y-%m-%d %H:%M:%S')
ax.xaxis.set_major_formatter(xfmt)

# Anotaciones en el gráfico:
#plt.arrow(20, 0, 10, 10)
#plt.annotate(s, (x,y))     # s: anotación, (x,y): coordenadas

plt.locator_params(axis='y', nbins=8)
plt.grid(axis='both', color='k', linestyle='dashed', linewidth=2, alpha=0.2)
plt.show()

if Linux:
    plt.savefig(path + '/' + campaign + '_Continuous.png')

#%%
# Gráfico (ECO y OBS - mediciones en continuo: Detalle de las 14:53):

plt.figure()


plt.plot(time_OBS_Continuous, ntu_OBS_Continuous, '-', color='blue', label=r'OBS501 (2016) [SS]')
plt.plot(time_ECO_Continuous, ntu_ECO_Continuous, '-', color='orange', label=r'ECO FLNTU')
#plt.plot(stations,ntu_HACH, '-o', color='red', label=r'HACH')

plt.legend(loc='best', fontsize=LegendSize)
plt.title(r'Continuo (2019-12-17 - Muelle)', fontsize=TitleSize)
plt.xlabel(r'UTC Time', fontsize=AxisLabelSize)
plt.ylabel(r'ECO (NTU), OBS (FNU)', fontsize=AxisLabelSize)

t_0 = pd.to_datetime(r'2019-12-17 14:42:00')
t_f = pd.to_datetime(r'2019-12-17 15:03:00')
plt.xlim(t_0,t_f)

plt.xticks(rotation=25)
ax=plt.gca()
xfmt = md.DateFormatter(r'%H:%M')
#xfmt = md.DateFormatter('%Y-%m-%d %H:%M:%S')
ax.xaxis.set_major_formatter(xfmt)

# Anotaciones en el gráfico:
#plt.arrow(20, 0, 10, 10)
#plt.annotate(s, (x,y))     # s: anotación, (x,y): coordenadas

plt.locator_params(axis='y', nbins=8)
plt.grid(axis='both', color='k', linestyle='dashed', linewidth=2, alpha=0.2)
plt.show()

if Linux:
    plt.savefig(path + '/' + campaign + '_Continuous-Detalle_14:53.png')

#%%
# Gráfico (ECO y OBS - continuo y suavizado):

plt.figure()

plt.plot(time_ECO_Continuous, ntu_ECO_Continuous, '-', color='orange', label=r'ECO FLNTU')
plt.plot(time_ECO_Smooth1min, ntu_ECO_Smooth1min, '-', color='orangered', label=r'ECO FLNTU (Smooth1min)')
plt.plot(time_OBS_Continuous, ntu_OBS_Continuous, '-', color='blue', label=r'OBS501 (2016) [SS]')
plt.plot(time_OBS_Smooth1min, ntu_OBS_Smooth1min, '-', color='darkturquoise', label=r'OBS501 (2016) [SS] (Smooth1min)')

#plt.plot(stations,ntu_HACH, '-o', color='red', label=r'HACH')

plt.legend(loc='best', fontsize=LegendSize)
plt.title(r'Suavizado: 1 minuto (2019-12-17 - Muelle)', fontsize=TitleSize)
plt.xlabel(r'UTC Time', fontsize=AxisLabelSize)
plt.ylabel(r'ECO (NTU)', fontsize=AxisLabelSize)
#plt.ylim(0,300)
plt.xticks(rotation=25)
ax=plt.gca()
xfmt = md.DateFormatter('%H:%M')
#xfmt = md.DateFormatter('%Y-%m-%d %H:%M:%S')
ax.xaxis.set_major_formatter(xfmt)

# Anotaciones en el gráfico:
#plt.arrow(20, 0, 10, 10)
#plt.annotate(s, (x,y))     # s: anotación, (x,y): coordenadas

plt.locator_params(axis='y', nbins=8)
plt.grid(axis='both', color='k', linestyle='dashed', linewidth=2, alpha=0.2)
plt.show()

if Linux:
    plt.savefig(path + '/' + campaign + '_Continuo_y_suavizado.png')

#%%
# Gráfico (ECO y OBS - suavizado):

plt.figure()

#plt.plot(time_ECO_Continuous, ntu_ECO_Continuous, '-', color='orange', label=r'ECO FLNTU')
plt.plot(time_ECO_Smooth1min, ntu_ECO_Smooth1min, '-', color='orangered', label=r'ECO FLNTU (Smooth1min)')
#plt.plot(time_OBS_Continuous, ntu_OBS_Continuous, '-', color='blue', label=r'OBS501 (2016) [SS]')
plt.plot(time_OBS_Smooth1min, ntu_OBS_Smooth1min, '-', color='darkturquoise', label=r'OBS501 (2016) [SS] (Smooth1min)')

#plt.plot(stations,ntu_HACH, '-o', color='red', label=r'HACH')

plt.legend(loc='best', fontsize=LegendSize)
plt.title(r'Suavizado: 1 minuto (2019-12-17 - Muelle)', fontsize=TitleSize)
plt.xlabel(r'UTC Time', fontsize=AxisLabelSize)
plt.ylabel(r'ECO (NTU)', fontsize=AxisLabelSize)
#plt.ylim(0,300)
plt.xticks(rotation=25)
ax=plt.gca()
xfmt = md.DateFormatter('%H:%M')
#xfmt = md.DateFormatter('%Y-%m-%d %H:%M:%S')
ax.xaxis.set_major_formatter(xfmt)

# Anotaciones en el gráfico:
#plt.arrow(20, 0, 10, 10)
#plt.annotate(s, (x,y))     # s: anotación, (x,y): coordenadas

plt.locator_params(axis='y', nbins=8)
plt.grid(axis='both', color='k', linestyle='dashed', linewidth=2, alpha=0.2)
plt.show()

if Linux:
    plt.savefig(path + '/' + campaign + '_suavizados.png')

#%% Processed

pathECO = '/home/santiago/Documents/L6-L7/FLNTU/Base de datos/Datos/regions/RdP/RdP_20191217_Muelle/ECO_FLNTUProcessed/RdP_20191217_ECO-FLNTU.xlsx'

pathOBS = '/home/santiago/Documents/L6-L7/FLNTU/Base de datos/Datos/regions/RdP/RdP_20191217_Muelle/campbellProcessed/RdP_20191217_Campbell.xlsx'

pathHACH = '/home/santiago/Documents/L6-L7/FLNTU/Base de datos/Datos/regions/RdP/RdP_20191217_Muelle/RdP_20191217.xlsx'

#%%

dataECO_Mean = pd.read_excel(pathECO ,sheet_name='Stations_Mean',skiprows=1)
dataOBS_Mean = pd.read_excel(pathOBS ,sheet_name='Stations_Mean',skiprows=1)
dataHACH_Mean = pd.read_excel(pathHACH ,sheet_name='turbidityHACH',skiprows=1)

dataECO_CV = pd.read_excel(pathECO ,sheet_name='Stations_CV',skiprows=1)
dataOBS_CV = pd.read_excel(pathOBS ,sheet_name='Stations_CV',skiprows=1)
dataHACH_CV = pd.read_excel(pathHACH ,sheet_name='turbidityHACH',skiprows=1)

ntu_ECO = dataECO_Mean['turbidity (NTU)']
ntu_OBS = dataOBS_Mean['SS_OBS501_I2016[FNU]']
ntu_HACH = dataHACH_Mean['Mean']

# CV: coefficient of variation
ntu_ECO_err = dataECO_Mean['turbidity (NTU)'] * dataECO_CV['turbidity (NTU)']/100
ntu_OBS_err = dataOBS_Mean['SS_OBS501_I2016[FNU]'] * dataOBS_CV['SS_OBS501_I2016[FNU]']/100
ntu_HACH_err = dataHACH_Mean['Mean'] * dataHACH_CV['CV[%]']/100

#%%
# Gráfico:

plt.figure()

stations = range(1,13)

plt.plot(stations,ntu_ECO, '-o', color='orange', label=r'ECO FLNTU')
plt.plot(stations,ntu_OBS, '-o', color='blue', label=r'OBS501 (2016) [SS]')
plt.plot(stations,ntu_HACH, '-o', color='red', label=r'HACH')

plt.legend(loc='best', fontsize=LegendSize)
plt.title(r'Turbidity (2019-12-17 - Muelle)', fontsize=TitleSize)
plt.xlabel(r'Station (STxx)', fontsize=AxisLabelSize)
plt.ylabel(r'Turbidity (NTU)', fontsize=AxisLabelSize)
plt.grid(axis='both', color='k', linestyle='dashed', linewidth=2, alpha=0.2)
plt.show()

if Linux:
    plt.savefig(path + '/' + campaign + '.png')

#plt.pause(1)
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
plt.xlabel(r'OBS501 (2016) [SS] (FNU)', fontsize=AxisLabelSize)
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
#%%
# Gráfico (ECO - Clorofila - continuo y suavizado):

plt.figure()

plt.plot(time_ECO_Continuous, chl_ECO_Continuous, '-', color='darkgreen', label=r'ECO FLNTU (chl)')
plt.plot(time_ECO_Smooth1min, chl_ECO_Smooth1min, '-', color='lime', label=r'ECO FLNTU (Smooth1min)')

#plt.plot(stations,ntu_HACH, '-o', color='red', label=r'HACH')

plt.legend(loc='best', fontsize=LegendSize)
plt.title(r'Suavizado: 1 minuto (2019-12-17 - Muelle)', fontsize=TitleSize)
plt.xlabel(r'UTC Time', fontsize=AxisLabelSize)
plt.ylabel(r'ECO (NTU)', fontsize=AxisLabelSize)
#plt.ylim(0,300)
plt.xticks(rotation=25)
ax=plt.gca()
xfmt = md.DateFormatter('%H:%M')
#xfmt = md.DateFormatter('%Y-%m-%d %H:%M:%S')
ax.xaxis.set_major_formatter(xfmt)

# Anotaciones en el gráfico:
#plt.arrow(20, 0, 10, 10)
#plt.annotate(s, (x,y))     # s: anotación, (x,y): coordenadas

plt.locator_params(axis='y', nbins=8)
plt.grid(axis='both', color='k', linestyle='dashed', linewidth=2, alpha=0.2)
plt.show()

if Linux:
    plt.savefig(path + '/' + campaign + '_CHL_Continuo_y_suavizado.png')

#%%
