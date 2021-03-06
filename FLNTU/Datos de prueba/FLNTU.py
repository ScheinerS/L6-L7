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
from scipy.optimize import curve_fit
#from scipy.odr import Model,RealData,ODR

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

files = glob.glob(path + '/Pruebas 23-10-19/' + 'estación' + '*.csv') # Identifica la cantidad de archivos que se quieren leer.

tabla = pd.DataFrame()  # DataFrame donde vamos a guardar los datos de hach, ntu y fl.



#%%

filename_hach = path + '/Turbidez(Hach-FLNTU) - Hoja 1.csv'

hach = pd.read_csv(filename_hach, delimiter = ",", skiprows=1, header=None)
hach.set_index(0)


tabla['hach'] = hach[5]
tabla['hach_err'] = hach[[2,3,4]].max(axis=1) - hach[[2,3,4]].min(axis=1)

tabla.set_index(hach[0],inplace=True)
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
        
    station = filename.split('.')[0]

    data[station] = pd.read_csv(file, delimiter="\t", skiprows=1, header=None)
    #data[filename] = data[filename].dropna()
    
    # Leemos los datos del archivo correspondiente a cada estación:
    NTU = data[station][3] # datos de turbidez
    FL = data[station][5]  # datos de fluorecencia
    
    # Calculamos la media y el error (std/sqrt(n)):
    ntu_mean = np.mean(NTU)
    ntu_std = np.std(NTU)/np.sqrt(len(NTU))
    
    fl_mean = np.mean(FL)
    fl_std = np.std(FL)/np.sqrt(len(FL))
    
    # Lo guardamos en la tabla definitiva:
    tabla.at[station, 'ntu'] = ntu_mean
    tabla.at[station, 'ntu_err'] = ntu_std

    tabla.at[station, 'fl'] = fl_mean
    tabla.at[station, 'fl_err'] = fl_std
    
    
    #tabla['fl'] = np.mean(FL)
    #tabla['fl_err'] = np.std(FL)/np.sqrt(len(FL))
    

    # Falta guardar el valor de cada archivo en un único vector.
    
    #data[filename].to_csv(path + '/' + filename + '.CSV')
#%%

# Ajuste:

# De la hoja de caracterización del FLNTU:

DC = 50 # counts
SF = 0.2438 # NTU/counts


x = tabla['hach']
y = SF * (tabla['ntu'] - DC)

#x = list(x)
#y = list(y)

x_err = tabla['hach_err']
y_err = SF*tabla['ntu_err']


def lineal(x, a):
    return a*x 

parametros_iniciales  = [0.5,0]

popt, pcov = curve_fit(lineal, x, y, p0=None)

pstd = np.sqrt(np.diag(pcov))
nombres_de_param = ['a', 'b']

print('Resultado del ajuste:\n')
for c, v in enumerate(popt):
    print('%s = %5.4f ± %5.4f' % (nombres_de_param[c], v, pstd[c]/2))


#%%
# Gráfico:

plt.figure()

plt.errorbar(x,y, xerr=x_err, yerr=y_err, fmt='.',color='darkred', label=r'', ms=5.5, zorder=0)

plt.plot(x, lineal(x, *popt), 'r-', label=r'Ajuste: $y = %.4f \; x $'%(popt[0]))


plt.legend(loc='best', fontsize=LegendSize)
plt.title(r'Correlaci\'on Hach-FLNTU', fontsize=TitleSize)
plt.xlabel(r'HACH (FNU)', fontsize=AxisLabelSize)
plt.ylabel(r'ECO FLNTU (NTU)', fontsize=AxisLabelSize)
plt.grid(axis='both', color='k', linestyle='dashed', linewidth=2, alpha=0.2)
plt.show()

if Linux:
    plt.savefig(path + '/Hach-FLNTU.png')