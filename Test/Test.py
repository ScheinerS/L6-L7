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

archivo = 'ConcentrationTurbidity-OBS'

FILE=path+'/'+archivo+'.csv'
data = pd.read_csv(FILE)

x = data[['Sample 1 (FNU)','Sample 2 (FNU)','Sample 3 (FNU)']]
x = x.dropna(axis=0)
x = np.array(x)

x_Hach = np.zeros(len(x))
x_Hach_err = np.zeros((2,len(x)))
x_Hach_err_tot = np.zeros(len(x))

y_Hach = np.array([486.0606061, 324.040404, 241.0703812, 158.9673315, 118.9453447, 79.11100286, 0]) # A mano. Ya fue.
y_Hach_err = 0.04*y_Hach # 4% de error.


# OBS:

x_OBS = data['SS']
x_OBS = x_OBS.dropna()
x_OBS = np.array(x_OBS)

y_OBS = data['Concentración']
y_OBS = y_OBS.dropna(axis=0)
y_OBS = np.array(y_OBS)

x_OBS_err = 10*np.ones(len(x_OBS))
y_OBS_err = 0.04*y_OBS

# Para que no haya ceros en el vector de errores.
y_Hach_err[-1] = 0.01
y_OBS_err[-1] = 0.01
#%%
for i in range(len(x)):
   x_Hach[i]=np.median(x[i])
   x_Hach_err[0,i]=x_Hach[i] - np.min(x[i])
   x_Hach_err[1,i]=np.max(x[i]) - x_Hach[i]
   x_Hach_err_tot[i]=x_Hach_err[0,i] + x_Hach_err[1,i]


# Generamos los datos aleatorios:


x_Hach_nuevo = np.zeros(len(x_Hach))
y_Hach_nuevo = np.zeros(len(y_Hach))

x_OBS_nuevo = np.zeros(len(x_OBS))
y_OBS_nuevo = np.zeros(len(y_OBS))


N = 100000 # Cantidad de datos generados.

m_Hach = np.zeros(N)
m_OBS = np.zeros(N)

for j in range(N):
    for i in range(len(x_Hach_nuevo)):
        x_Hach_nuevo[i] = x_Hach[i] - x_Hach_err[0,i] + x_Hach_err_tot[i]*np.random.rand()
        y_Hach_nuevo[i] = y_Hach[i] - y_Hach_err[i]*(np.random.rand()-0.5)
    for i in range(len(x_OBS_nuevo)):
        x_OBS_nuevo[i] = x_OBS[i] - x_OBS_err[i]*(np.random.rand()-0.5)
        y_OBS_nuevo[i] = y_OBS[i] - y_OBS_err[i]*(np.random.rand()-0.5)
    
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
