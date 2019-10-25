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

tabla = pd.DataFrame()  # DataFrame donde vamos a guardar los datos de hach, ntu y fl.



#%%

filename_hach = path + '/Datos/' + 'Turbidez(Hach-FLNTU) - Hoja 1.csv'

hach = pd.read_csv(filename_hach, delimiter = ",", skiprows=1, header=None)
hach.set_index(0)


tabla['hach'] = hach[5]
tabla['hach_err'] = hach[[2,3,4]].max(axis=1) - hach[[2,3,4]].min(axis=1)

tabla.set_index(hach[0])
#%%
data = {}   # Diccionario con los DataFrames de cada archivo. 

tabla['ntu'] = None
tabla['ntu_err'] = None
tabla['fl'] = None
tabla['fl_err'] = None

# Lectura de los archivos del FLNTU:
for file in files:
    
    if os.name == 'posix':   # Si es Linux.
        filename = file.split('/')[-1]
    elif os.name == 'nt':   # Si es Windows.
        filename = file.split('\\')[-1]
        
    filename = filename.split('.')[0]

    data[filename] = pd.read_csv(file, delimiter="\t", skiprows=1, header=None)
    #data[filename] = data[filename].dropna()
    
    NTU = data[filename][3] # datos de turbidez
    FL = data[filename][5]  # datos de fluorecencia
    
    tabla['ntu'].append(pd.Series(np.mean(NTU)))
    tabla['ntu_err'].append(np.std(NTU)/np.sqrt(len(NTU)))
    
    tabla.set_value('ntu', filename, 1000)
    #tabla['fl'] = np.mean(FL)
    #tabla['fl_err'] = np.std(FL)/np.sqrt(len(FL))
    

    # Falta guardar el valor de cada archivo en un único vector.
    
    #data[filename].to_csv(path + '/' + filename + '.CSV')
#%%