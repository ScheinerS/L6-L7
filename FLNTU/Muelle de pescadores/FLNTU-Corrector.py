# -*- coding: utf-8 -*-
"""
Corrector de errores de transferencia del ECO FLNTU.

    Este programa lee dos archivos del FLNTU correspondientes a la misma campaña (i.e. idénticos, pero transferidos por separado) y los compara, en búsqueda de errores. Cuando una fila no tiene el formato que se espera (siete columnas), la elimina y toma el dato del otro archivo.

Para hacer más adelante:
    
    Asumimos que no se repiten los datos con error en dos transferencias separadas, pero podría ocurrir. El próximo paso sería hacerlo con tres transferencias diferentes.

Última actualización: 18/12/2019.
"""

import sys
import os
import pandas as pd
#import numpy as np
import matplotlib.pyplot as plt
#import glob
#from scipy.optimize import curve_fit
#from scipy.odr import Model,RealData,ODR

path = os.path.dirname(os.path.realpath('__file__'))
sys.path.append(path)



#%%

data = {}   # Diccionario con los DataFrames de cada archivo. 

# Lectura de los archivos del FLNTU:
fileA = path + '/' + 'RDP_20191217.xlsx'
fileB = path + '/' + 'RDP_20191217(transferenciaB).xlsx'

try:
    data[fileA] = pd.read_excel(fileA, delimiter="\t", skiprows=1, header=None,usecols=range(0,7))
    data[fileB] = pd.read_excel(fileB, delimiter="\t", skiprows=1, header=None,usecols=range(0,7))
except:
    print('\nError de lectura\n')
    
data[fileA] = data[fileA].dropna()
data[fileB] = data[fileB].dropna()

#%%

# Armamos un archivo definitivo a partir del archivo A, y si hay un error, buscamos en el archivo B:

file = pd.DataFrame()

for i in range(10): #range(len(data[fileA])):
    L = data[fileA].iloc[i]
    if type(L[0]) == type(L[1]) == str and type(L[2]) == type(L[3]) == type(L[4]) == type(L[5]) == type(L[6]) == int:
        file.append(data[fileA].iloc[i])
    else:
        L = data[fileB].iloc[i]
        if type(L[0]) == type(L[1]) == str and type(L[2]) == type(L[3]) == type(L[4]) == type(L[5]) == type(L[6]) == int:
            file.append(data[fileB].iloc[i])
        else:
            print('El dato está dañado en ambos archivos.')

print(file)

    
#%%
# De la hoja de caracterización del FLNTU:

DC = 50 # counts
SF = 0.2438 # NTU/counts


x = tabla['hach']
y = SF * (tabla['ntu'] - DC)

#%%
