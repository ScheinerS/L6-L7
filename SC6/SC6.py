# -*- coding: utf-8 -*-
"""
Test estadístico: In Situ - Laboratorio.
"""

import sys
import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

path = os.path.dirname(os.path.realpath('__file__'))
sys.path.append(path)

TitleSize=15
AxisLabelSize=15
LegendSize=12
NumberSize=10

plt.close('all')

plt.rc('text', usetex=True)
plt.rc('font', family='serif')

#%%

N_LOG = 2   # Cantidad de archivos que se quieren leer.

data = {}   # Diccionario con los DataFrames de cada archivo. 

for i in range(1,N_LOG+1):
    
    FILE = path + '/' + 'LOG_%04d.TXT'%(i)
    filename = 'LOG_%04d'%i
        
    data[filename] = pd.read_csv(FILE, delimiter=",", skiprows=18)
    data[filename] = data[filename].dropna()    # Eliminamos la línea de puntos del principio.

#%%