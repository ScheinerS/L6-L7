# -*- coding: utf-8 -*-
"""
Este programa lee los archivos del FLNTU.

Última actualización: 24/10/2019.
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

files = glob.glob(path + '/Datos/Pruebas 23-10-19/' + 'estación' + '*.csv') # Identifica la cantidad de archivos que se quieren leer.

data = {}   # Diccionario con los DataFrames de cada archivo. 
'''
# HACH
hach = {}

# FLNTU
ntu = {}
fl = {}
'''
for file in files:
    
    if os.name == 'posix':   # Si es Linux.
        filename = file.split('/')[-1]
    elif os.name == 'nt':   # Si es Windows.
        filename = file.split('\\')[-1]
        
    filename = filename.split('.')[0]

    data[filename] = pd.read_csv(file, delimiter="\t", skiprows=1, header=None)
    #data[filename] = data[filename].dropna()
    
    ntu = data[filename][3]
    fl = data[filename][5]
    
    ntu_mean = np.mean(ntu)
    ntu_err = np.std(ntu)/np.sqrt(len(ntu))
    
    fl_mean = np.mean(fl)
    fl_err = np.std(fl)/np.sqrt(len(fl))

    # Falta guardar el valor de cada archivo en un único vector.
    
    #data[filename].to_csv(path + '/' + filename + '.CSV')
#%%