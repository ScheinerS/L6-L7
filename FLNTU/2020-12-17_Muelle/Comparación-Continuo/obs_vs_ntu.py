
import sys
import os
#import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
from scipy.odr import Model,RealData,ODR

path = os.path.dirname(os.path.realpath('__file__'))
sys.path.append(path)

TitleSize = 15
AxisLabelSize = 12
LegendSize = 12
NumberSize = 12

plt.close('all')

#plt.rc('text', usetex=False)
#plt.rc('font', family='serif')


#%%
obs_vs_ntu = np.loadtxt('OBS_and_ECO_smooth1min.csv', skiprows=1, delimiter=',', unpack=True)

obs = obs_vs_ntu[0]
eco = obs_vs_ntu[1]

# 
obs_err = np.ones(len(obs))
eco_err = np.ones(len(eco))

stations = np.loadtxt('OBS_and_ECO_stations.csv', skiprows=1, delimiter=',', unpack=True)
obs_stations = stations[0]
eco_stations = stations[1]


#%%

def linear(p0,x):
    a, b = p0
    return a*x

def ODR_Fit(function,x,y,x_err,y_err):
    print('Fit:\t',function.__name__,'\n')
    # Create a model for fitting.
    model = Model(function)
    # Create a RealData object using our initiated data from above.
    D = RealData(x, y, sx=x_err, sy=y_err)
    # Set up ODR with the model and data.
    odr = ODR(D, model, beta0=[0.7, 0.])
    # Run the regression.
    out = odr.run()
    # Use the in-built pprint method to give us results.
    out.pprint()
    print('\n')
    return out

print(45*'*'+'\n\t\tOBS vs ECO\n'+45*'*')
ajuste = ODR_Fit(linear, obs, eco, obs_err, eco_err)

'''
def modelo(x, m, b):
    return m*x

parametros_iniciales = [0.3,0]

popt, pcov = curve_fit(modelo, obs, eco, p0 = parametros_iniciales)

# Constantes del ajuste lineal:
m=popt[0]
b=popt[1]


print('\nAjuste lineal (y=mx+b):\nm=%2.4f\tb=%2.4f'%(m,b))

'''

'''
# Gráfico del ajuste:

[m, b] = fit_OBS.beta
x = np.linspace(0, max(ntu_OBS), 50)
y = m*x + b
'''


plt.figure()
plt.plot(obs, eco, '.', color='skyblue', label=r'smooth-1min')
plt.plot(obs_stations, eco_stations, '.k', label=r'estaciones')

[m, b] = ajuste.beta
x = np.linspace(0, max(obs), 50)
y = m*x + b

plt.plot(x,y, color='blue', label=r'$y=%.4g+%.4g$'%(m,b))


plt.legend(loc='best', fontsize=LegendSize)
plt.title(r'Smooth-1 min (2019-12-17 - Muelle)', fontsize=TitleSize)
plt.xlabel(r'OBS (FNU)', fontsize=AxisLabelSize)
plt.ylabel(r'ECO (NTU)', fontsize=AxisLabelSize)

plt.grid(axis='both', color='k', linestyle='dashed', linewidth=2, alpha=0.2)
plt.show()

plt.savefig(path + '/OBS_vs_ECO(Smooth-1min).png')