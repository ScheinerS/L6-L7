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
LegendSize=15
NumberSize=10

plt.close('all')

plt.rc('text', usetex=True)
plt.rc('font', family='serif')

#%%

GuardarComoCSV = False # si queremos guardar los datos como CSV.

files = glob.glob(path + '/' + 'LOG_*.TXT') # Identifica la cantidad de archivos que se quieren leer.

data = {}   # Diccionario con los DataFrames de cada archivo. 

for file in files:
    
    filename = file.split('/')[-1]  # En Windows: '\\'
    filename = filename.split('.')[0]

    data[filename] = pd.read_csv(file, delimiter=",", skiprows=18)
    data[filename] = data[filename].dropna()    # Eliminamos la línea de puntos del principio.

    if GuardarComoCSV:
        data[filename].to_csv(path + '/' + filename + '.CSV')


#%%

signalCJ = []
signalSJ = []

long = [415.1, 560.7, 634.9, 659.6, 731.9, 850.0]
color = ['purple', 'green', 'orange', 'red', 'lightcoral','silver']

for i in range(6):
    SIG = 'Sig[' + str(i) + ']'
    signalCJ.append(data['LOG_0050'][SIG])  # con la jaula
    signalSJ.append(data['LOG_0051'][SIG])  # sin la jaula
    
    meanCJ = np.mean(signalCJ[i])    
    meanSJ = np.mean(signalSJ[i])
    
    stdCJ = np.std(signalCJ[i])    
    stdSJ = np.std(signalSJ[i])
    
    plt.figure()
    plt.hist(signalSJ[i], label = 'Sin estructura\n$\mu = %.2f$\n$\sigma = %.2f$'%(meanSJ, stdSJ), alpha = 0.8, bins=int(np.sqrt(len(signalSJ[i]))))
    plt.hist(signalCJ[i], label = 'Con estructura\n$\mu = %.2f$\n$\sigma = %.2f$'%(meanCJ, stdCJ),alpha = 0.8, bins=int(np.sqrt(len(signalCJ[i]))))
    
    plt.legend(loc='best', fontsize=LegendSize)
    plt.title(r'$\lambda$ = %s nm'%(long[i]), fontsize=TitleSize)
    plt.xlabel(r'Signal', fontsize=AxisLabelSize)
    plt.ylabel(r'', fontsize=AxisLabelSize)
    plt.grid(axis='both', color='k', linestyle='dashed', linewidth=2, alpha=0.2)
    plt.savefig(path + '/EfectoDelBorde[%s nm].png'%(long[i]))
    #plt.pause(0.5)
    plt.show()


