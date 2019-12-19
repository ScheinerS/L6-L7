# -*- coding: utf-8 -*-
"""
Este programa lee los archivos del FLNTU.

Última actualización: 24/10/2019.
"""

import sys
import os
import pandas as pd
#import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as md
import dateutil
#import glob


path = os.path.dirname(os.path.realpath('__file__'))
sys.path.append(path)

TitleSize=15
AxisLabelSize=15
LegendSize=12
NumberSize=10

plt.close('all')

if os.name == 'posix':   # Si es Linux.
    Linux = True

plt.rc('text', usetex=Linux)    # Solo usa Latex si es Linux.
plt.rc('font', family='serif')

#%%

#files = glob.glob(path + '/*.csv') # Identifica la cantidad de archivos que se quieren leer.

#tabla = pd.DataFrame()  # DataFrame donde vamos a guardar los datos de hach, ntu y fl.



#%%

file = path + '/' + 'RDP_20191217.xlsx'

data = pd.read_excel(file,
                     delimiter="\t",
                     skiprows=1,
                     header=None,usecols=range(0,7),
                     #names = ['date', 'time', '', 'ntu', '','fl',''],
                     #dtype={'date': str, 'time': str, 'ntu': int , 'fl': int},
                     #errors='coerce'
                     )

data = data.dropna()

i=0

while i<len(data):
    L = data.iloc[i]
    if not ((type(L[0]) == type(L[1]) == str) and (type(L[2]) == type(L[3]) == type(L[4]) == type(L[5]) == type(L[6]) == int)):
        print('Error de formato:\t',i)
        #data.drop([i], axis = 0, inplace = True)
        data.drop(data.index[i],inplace=True)
    else:
            # Y a veces, se pegan dos enteros y aparecen números enormes:
        if (not 0<L[3]<4131) or (not 0<L[5]<4131):
            print('Error de límite:\t',i)
            data.drop(data.index[i],inplace=True)
            # ESTA PARTE NO PARECE ESTAR FUNCIONANDO...
        else:
            i=i+1


time = data[1][:]
ntu = data[3][:]
fl = data[5][:]

#%%
# Gráfico:

plt.figure()

plt.plot(ntu, color='orange', label=r'NTU')
plt.plot(fl, color='green', label=r'FL')

plt.legend(loc='best', fontsize=LegendSize)
plt.title(r'ECO FLNTU (17 DIC 2019)', fontsize=TitleSize)
plt.xlabel(r'N\'umero de medici\'on', fontsize=AxisLabelSize)
plt.ylabel(r'ECO-FLNTU (Counts)', fontsize=AxisLabelSize)
plt.grid(axis='both', color='k', linestyle='dashed', linewidth=2, alpha=0.2)
plt.show()

if Linux:
    plt.savefig(path + '/ECO FLNTU.png')