# -*- coding: utf-8 -*-
"""

"""

import sys
import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.odr import Model,RealData,ODR
from matplotlib.ticker import AutoMinorLocator

path = os.path.dirname(os.path.realpath('__file__'))
sys.path.append(path)

TitleSize=20
AxisLabelSize=15
LegendSize=12
NumberSize=10

plt.close('all')

plt.rc('text', usetex=False)
plt.rc('font', family='serif')

#%%

lugares = ['In Situ','Laboratorio']
experimentos = ['hach','ss','spm']

data = {}

for lugar in lugares:

    data[lugar] = pd.read_excel(path + '/' + lugar + '.xlsx',header=0)
    #data = data.rename(columns=data.iloc[0])
    #data = data.drop(0)
    
    hach = data[lugar]['HACH_Mean']
    hach_err = data[lugar]['HACH_Mean']*data[lugar]['HACH_CV']/100
    # hach_err = data['HACH_Mean']
    
    ss = data[lugar]['SS_OBS501_Mean']
    ss_err = data[lugar]['SS_OBS501_Mean']*data[lugar]['SS_OBS501_CV']/100
    
    spm = data[lugar]['SPM_Mean']
    spm_err = data[lugar]['SPM_CV']*data[lugar]['SPM_Mean']/100


#%%
   
# Generamos los datos aleatorios:

N = 10000 # Cantidad de datos generados.

#for j in range(N):
    

    
    
    
    
    hach_nuevo = np.zeros(len(hach))
    ss_nuevo = np.zeros(len(ss))
    
    




    
# Ajuste de los datos generados:

m_Hach[j] = np.dot(x_Hach_nuevo,y_Hach_nuevo)/np.dot(x_Hach_nuevo,x_Hach_nuevo)
m_OBS[j] = np.dot(x_OBS_nuevo,y_OBS_nuevo)/np.dot(x_OBS_nuevo,x_OBS_nuevo)
    
    
plt.figure()

plt.hist(m_Hach,bins = int(np.sqrt(N)),label='Hach',color = 'red')
plt.hist(m_OBS,bins = int(np.sqrt(N)),label='OBS',color = 'blue')


plt.xlabel(r'm', fontsize=AxisLabelSize)
plt.ylabel(r'', fontsize=AxisLabelSize)
plt.title(r'N = %d'%(N), fontsize=TitleSize)
plt.legend(loc='best', fontsize=LegendSize)
plt.grid(axis='both', color='k', linestyle='dashed', linewidth=2, alpha=0.1)
plt.show()













#%%
'''
plt.figure()
plt.errorbar(x_Hach, y_Hach, xerr=x_Hach_err, yerr=y_Hach_err, fmt='.',color='darkred', label=r'Hach', ms=5.5, zorder=0)
plt.plot(x_Hach_nuevo,y_Hach_nuevo,'.')

plt.figure()
plt.errorbar(x_OBS, y_OBS, xerr=x_OBS_err, yerr=y_OBS_err, fmt='.',color='darkred', label=r'Hach', ms=5.5, zorder=0)
plt.plot(x_OBS_nuevo,y_OBS_nuevo,'.')


# Gráfico del ajuste ax:

plt.figure()

plt.errorbar(x_Hach, y_Hach, xerr=x_Hach_err, yerr=y_Hach_err, fmt='.',color='darkred', label=r'Hach', ms=5.5, zorder=0)
plt.plot(x_fit_Hach, y_fit_Hach, color='red', label=r'Ajuste: $y = %.4f \; x$'%(fit_Hach.beta[0]), lw=1, zorder=4)

plt.errorbar(x_OBS, y_OBS, xerr=x_OBS_err, yerr=y_OBS_err, fmt='.', color='darkblue', label=r'OBS', ms=5.5, zorder=0)
plt.plot(x_fit_OBS, y_fit_OBS, color='blue', label=r'Ajuste: $y = %.4f \; x$'%(fit_OBS.beta[0]), lw=1, zorder=4)


plt.tick_params(axis='both', which='major', labelsize=NumberSize)
plt.xlabel(r'Turbidez (FNU)', fontsize=AxisLabelSize)
plt.ylabel(r'Concentraci\'on (mg/l)', fontsize=AxisLabelSize)
plt.title(r'Ajuste $y=ax$', fontsize=TitleSize)
plt.legend(loc='best', fontsize=LegendSize)
plt.grid(axis='both', color='k', linestyle='dashed', linewidth=2, alpha=0.1)
plt.show()
plt.savefig(path + '/' + archivo + 'real.png')
'''
