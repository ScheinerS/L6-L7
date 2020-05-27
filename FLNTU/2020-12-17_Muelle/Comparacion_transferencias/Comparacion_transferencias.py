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

plt.rc('text', usetex=False)
plt.rc('font', family='serif')

fileA = 'RdP_20191217_cleaned-A.xlsx'
fileB = 'RdP_20191217_cleaned-B.xlsx'

dataA = pd.read_excel(fileA)
dataB = pd.read_excel(fileB)

time_A = dataA['timestamp']
ECO_A = dataA['turbidity (NTU)']

time_B = dataB['timestamp']
ECO_B = dataB['turbidity (NTU)']

# Convertimos los timestamps a formato 'datetime' para que Matplotlib lo entienda:

time_A = pd.to_datetime(time_A)
time_B = pd.to_datetime(time_B)

#%%
# Gráfico (ECO y OBS - mediciones en continuo):

plt.figure()

plt.plot(time_A, ECO_A, '-', color='green', label=r'Transferencia A')
plt.plot(time_B, ECO_B, '-', color='fuchsia', label=r'Transferencia B')
#plt.plot(time_OBS_Continuous, ntu_OBS_Continuous, '-', color='blue', label=r'OBS501 (2016) [SS]')
#plt.plot(stations,ntu_HACH, '-o', color='red', label=r'HACH')

plt.legend(loc='best', fontsize=LegendSize)
#plt.title(r'Comparaci\'on de las transferencias (2019-12-17 - Muelle)', fontsize=TitleSize)
plt.xlabel(r'UTC Time', fontsize=AxisLabelSize)
plt.ylabel(r'ECO (NTU), OBS (FNU)', fontsize=AxisLabelSize)
plt.ylim(0,300)
plt.xticks(rotation=0)#25)
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

plt.savefig(path + '/' + 'Comparacion_transferencias.png')
