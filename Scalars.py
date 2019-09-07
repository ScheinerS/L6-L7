'''
Programa para leer SCALARS.xlsx.
'''

import sys
import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
from matplotlib.ticker import AutoMinorLocator

path = os.path.dirname(os.path.realpath('__file__'))
sys.path.append(path)

TitleSize=30
AxisLabelSize=15
LegendSize=12
NumberSize=10

plt.close('all')

plt.rc('text', usetex=True)
plt.rc('font', family='serif')


#%%

archivo='SCALARS'

FILE=path + '/' + archivo + '.xlsx'

data = pd.read_excel(FILE,header=0)
#data = data.rename(columns=data.iloc[0])
#data = data.drop(0)

hach = data['HACH_Mean']
hach_err = data['HACH_Mean']*data['HACH_CV']/100
# hach_err = data['HACH_Mean']

ss = data['SS_OBS501_Mean']
ss_err = data['SS_OBS501_Mean']*data['SS_OBS501_CV']/100

spm = data['SPM_Mean']
spm_err = data['SPM_CV']*data['SPM_Mean']/100

#%%

# Gráfico de Hach vs OBS.

plt.figure()

plt.errorbar(hach, ss, xerr=hach_err , yerr=ss_err , fmt='o', color='darkblue', label=r'', ms=5.5, zorder=0)

#plt.ylim(0,170)
plt.xlabel(r'Hach (FNU)', fontsize=AxisLabelSize)
plt.ylabel(r'OBS - SS (FNU)', fontsize=AxisLabelSize)
# plt.title(r'', fontsize=TitleSize)
#plt.legend(loc='best', fontsize=LegendSize)
plt.grid(axis='both', color='k', linestyle='dashed', linewidth=2, alpha=0.1)
plt.show()

#%%

# Gráfico de Turbidez vs Concentración.

plt.figure()

plt.errorbar(hach, spm, xerr=hach_err , yerr=spm_err , fmt='o', color='darkred', label=r'Hach', ms=5.5, zorder=0)
plt.errorbar(ss, spm, xerr=ss_err , yerr=spm_err , fmt='o', color='darkblue', label=r'OBS (SS)', ms=5.5, zorder=0)

#plt.ylim(0,170)
plt.xlabel(r'Turbidez (FNU)', fontsize=AxisLabelSize)
plt.ylabel(r'MPS (mg/l)', fontsize=AxisLabelSize)
plt.title(r'', fontsize=TitleSize)
plt.legend(loc='best', fontsize=LegendSize)
plt.grid(axis='both', color='k', linestyle='dashed', linewidth=2, alpha=0.1)
plt.show()
















