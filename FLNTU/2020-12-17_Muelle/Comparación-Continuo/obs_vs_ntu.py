
import sys
import os
#import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit

path = os.path.dirname(os.path.realpath('__file__'))
sys.path.append(path)

TitleSize = 15
AxisLabelSize = 12
LegendSize = 12
NumberSize = 12

plt.close('all')

plt.rc('text', usetex=False)
plt.rc('font', family='serif')


#%%
obs_vs_ntu = np.loadtxt('obs_ss__(fnu)vs_eco_(ntu).csv', skiprows=1, delimiter=',', unpack=True)

obs = obs_vs_ntu[0]
eco = obs_vs_ntu[1]

stations = np.loadtxt('OBS_and_ECO_stations.csv', skiprows=1, delimiter=',', unpack=True)
obs_stations = stations[0]
eco_stations = stations[1]


#%%

def modelo(x, m, b):
    return m*x

parametros_iniciales = [0.3,0]

popt, pcov = curve_fit(modelo, obs, eco, p0 = parametros_iniciales)

# Constantes del ajuste lineal:
m=popt[0]
b=popt[1]


print('\nAjuste lineal (y=mx+b):\nm=%2.4f\tb=%2.4f'%(m,b))

plt.figure()
plt.plot(obs, eco, '.')
plt.plot(obs_stations, eco_stations, '.k')

x_modelo = np.linspace(0, 70, 1000)
plt.plot(x_modelo,modelo(x_modelo, *popt), color='blue', label=r'$y=%.4g+%.4g$'%(m,b))


plt.legend(loc='best', fontsize=LegendSize)
plt.title(r'Smooth-1 min (2019-12-17 - Muelle)', fontsize=TitleSize)
plt.xlabel(r'OBS (FNU)', fontsize=AxisLabelSize)
plt.ylabel(r'ECO (NTU)', fontsize=AxisLabelSize)

plt.grid(axis='both', color='k', linestyle='dashed', linewidth=2, alpha=0.2)
plt.show()

plt.savefig(path + '/OBS_vs_ECO(Smooth-1min).png')