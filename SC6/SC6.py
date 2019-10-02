# -*- coding: utf-8 -*-
"""
Este programa lee los archivos del SC6 de tipo: 'LOG_XXXX.TXT' y los exporta con los mismos nombres e formato .CSV, en la misma carpeta.

Última actualización: 25/09/2019.
"""

import sys
import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import glob

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

files = glob.glob(path + '/' + 'LOG_*.TXT') # Identifica la cantidad de archivos que se quieren leer.

data = {}   # Diccionario con los DataFrames de cada archivo. 

for file in files:
    
    filename = file.split('\\')[-1]
    filename = filename.split('.')[0]

    data[filename] = pd.read_csv(file, delimiter=",", skiprows=18)
    data[filename] = data[filename].dropna()    # Eliminamos la línea de puntos del principio.

    data[filename].to_csv(path + '/' + filename + '.CSV')
#%%