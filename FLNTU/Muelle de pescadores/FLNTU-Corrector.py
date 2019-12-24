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

def check_date(date):
    try:
        date = date.split('/')
        if not len(date)==3:
            return False
        
        # La fecha está en el formato mm-dd-aaaa
        day = int(date[1])
        month = int(date[0])
        year = int(date[2])
        
    except:
        return False
            
    if day>0 and day<32:
        if month>0 and month<13:
            if year>18 and year<22: # Va a haber que cambiarlo en 2022.
                return True
            else:
                return False
        else:
            return False
    else:
        print('\nError de lectura\n')
        return False
    
#######################

def check_time(time):
    try:
        time = time.split(':')
        if not len(time)==3:
            return False
        
        hour = int(time[0])
        min = int(time[1])
        sec = int(time[2])
    except:
        return False
            
    if hour>=0 and hour<24:
        if min>=0 and min<60:
            if sec>=0 and sec<60:
                return True
            else:
                return False
        else:
            return False
    else:
        print('\nError de lectura\n')
        return False
   
#######################

def check_counts(counts):
    try:
        counts = int(counts)
    except:
        return False
    
    if counts>0 and counts<4131:
        return True
    else:
        print('\nError de lectura\n')
        return False
    
def check_all(L):
    # esta función verifica todas las columnas para la línea L
    date = L[0]
    time = L[1]
    
    ntu_counts = L[3]
    fl_counts = L[5]
    
    a = check_date(date)
    b = check_time(time)
    c = check_counts(ntu_counts)
    d = check_counts(fl_counts)
    
    if a and b and c and d:
        return True
    else:
        return False

#%%

# Armamos un archivo definitivo a partir del archivo A, y si hay un error, buscamos en el archivo B:

file = pd.DataFrame()

for i in range(10): #range(len(data[fileA])):
    
    L = data[fileA].iloc[i]
    if check_all(L):
        file.append(data[fileA].iloc[i])
        print('A')
        
    else:
        L = data[fileB].iloc[i]
        if check_all(L):
            file.append(data[fileB].iloc[i])
        else:
            print('El dato está dañado en ambos archivos.')

print(file)


# ARREGLAR. EL ARCHIVO 'file' NO SE ARMA.

#%%
# De la hoja de caracterización del FLNTU:

DC = 50 # counts
SF = 0.2438 # NTU/counts

'''
x = tabla['hach']
y = SF * (tabla['ntu'] - DC)
'''
#%%
