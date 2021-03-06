# -*- coding: utf-8 -*-
"""
Comparación con y sin la jaula.

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
LegendSize=10
NumberSize=10

plt.close('all')

plt.rc('text', usetex=False)
plt.rc('font', family='serif')

#%%

GuardarComoCSV = False # si queremos guardar los datos como CSV.

files = glob.glob(path + '/' + 'LOG_*.TXT') # Identifica la cantidad de archivos que se quieren leer.

data = {}   # Diccionario con los DataFrames de cada archivo. 

for file in files:
    
    filename = file.split('\\')[-1]
    filename = filename.split('.')[0]

    data[filename] = pd.read_csv(file, delimiter=",", skiprows=18)
    #data[filename] = data[filename].dropna()    # Eliminamos la línea de puntos del principio.

    if GuardarComoCSV:
        data[filename].to_csv(path + '/' + filename + '.CSV')


#%%

# Gráfico del aparato en aire, luego sumergido hasta el fondo, y finalmente sumergido en superficie:

#time = data['LOG_0028']['hh:mm:ss.sss']
signalCJ = []
signalSJ = []
plt.figure()

freq = [415.1, 560.7, 634.9, 659.6, 731.9, 850.0]
color = ['purple', 'green', 'orangered', 'red', 'lightcoral','silver']

for i in range(6):
    SIG = 'Sig[' + str(i) + ']'
    signalCJ.append(data['LOG_0028'][SIG])  # con la jaula
    signalSJ.append(data['LOG_0029'][SIG])  # sin la jaula
    plt.plot(signalCJ[i], label = str(freq[i]) + ' nm (CJ)', color = color[i])
    plt.plot(signalSJ[i],'--', label = str(freq[i]) + ' nm (SJ)', color = color[i])    

plt.legend(loc='best', fontsize=LegendSize)
plt.title(r'Efecto de la jaula (agua clara)', fontsize=TitleSize)
plt.xlabel(r'Número de scan', fontsize=AxisLabelSize)
plt.ylabel(r'Signal', fontsize=AxisLabelSize)
#plt.grid(axis='both', color='k', linestyle='dashed', linewidth=2, alpha=0.2)
plt.savefig(path + '/EfectoDelBorde.png')
plt.show()

