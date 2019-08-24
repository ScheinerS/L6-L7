'''
Programa para leer los archivos en formato CSV y graficarlos.
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

plt.close('all')

TitleSize=30
AxisLabelSize=15
LegendSize=15
NumberSize=10

#%%

archivos=['ConcentrationTurbidity'] # Por si queremos agregar más archivos después.

for s in archivos:
    FILE=path+'/'+s+'.csv'
    data = pd.read_csv(FILE)
    # Extraemos las cuatro columnas que nos interesan:
    y_df = pd.DataFrame(data, columns= ['Concentración'])
    
    
    y_df=np.array(y_df)
    y_df = y_df[:26]
    
    x = pd.DataFrame(data, columns= ['Sample 1 (FNU)','Sample 2 (FNU)','Sample 3 (FNU)'])
    x=np.array(x)
    x = x[:26,:]
    
    x_med=np.zeros(len(x))
    x_err=np.zeros((2,len(x)))
    x_err_tot=np.zeros(len(x))
    y=np.zeros(len(x))
    
    for i in range(len(x)):
       x_med[i]=np.median(x[i])
       x_err[0,i]=x_med[i] - np.min(x[i])
       x_err[1,i]=np.max(x[i]) - x_med[i]
       x_err_tot[i]=x_err[1,i] - x_err[0,i]
       y[i]=y_df[i] # Esto parece que no tiene sentido pero es para arreglar la dimensión de y. Size(y_df)=(26,1) y Size(y)=(26,).
       
    # Ajuste:
    
    def modelo(x, a, b):
        return a*x+ b
    
    parametros_iniciales  = [0.5,0]
    
    popt, pcov = curve_fit(modelo, x_med, y, p0=None)    
    
    pstd = np.sqrt(np.diag(pcov))
    nombres_de_param = ['a', 'b']

    print('Resultado del ajuste:\n')
    for c, v in enumerate(popt):
        print('%s = %5.4f ± %5.4f' % (nombres_de_param[c], v, pstd[c]/2))
    
    plt.errorbar(x_med, y, xerr=x_err, yerr=None, fmt='o', label=r'')#, ms=5.5, capsize=4, zorder=2)
    plt.plot(x_med, modelo(x_med, *popt), 'r-', label=r'Ajuste: $y = %.4f \; x + %.4f $'%(popt[0],popt[1]))#, lw=2.5, zorder=4)

    plt.tick_params(axis='both', which='major', labelsize=NumberSize)
    plt.xlabel(r'Turbidez (FNU)', fontsize=AxisLabelSize)
    plt.ylabel(r'Concentraci\'on (mg/l)', fontsize=AxisLabelSize)
    plt.title(r'', fontsize=TitleSize)
    plt.legend(loc='upper left', fontsize=LegendSize)
    plt.grid(axis='both', color='k', linestyle='dashed', linewidth=2, alpha=0.1)
    plt.show()
    plt.savefig(path+'/'+s+'.png')


#%% Gráfico
'''
plt.figure(dpi=100)
plt.rc('text', usetex=True)
plt.rc('font', family='serif')

ax = plt.gca()
ax.xaxis.set_minor_locator(AutoMinorLocator(4))
ax.yaxis.set_minor_locator(AutoMinorLocator(5))
ax.grid(zorder=1)

plt.errorbar(x_datos, y_datos, xerr=None, yerr=2, fmt='o', label=r'datos medidos (baja presi\'{o}n)', ms=5.5, capsize=4, zorder=2)
plt.plot(x_modelo, modelo(x_modelo, *popt), 'r-', label=r'ajuste $y = a + (b - a)\exp{(-cx)}$', lw=2.5, zorder=4)
plt.errorbar(x_datos2, y_datos2, xerr=None, yerr=2, fmt='s', label=r'datos medidos (alta presi\'{o}n)', ms=5.5, capsize=4, zorder=3)
plt.plot(x_modelo2, modelo(x_modelo2, *popt2), 'g--', label=r'ajuste $y = a + (b - a)\exp{(-cx)}$', lw=2.5, zorder=5)

plt.xlabel(r'tiempo (s)', fontsize=17)
plt.ylabel(r'temperatura ($^\circ$C)', fontsize=17)
plt.xticks(fontsize=14)
plt.yticks(fontsize=14)
plt.legend(loc='best', fontsize=15)

plt.tight_layout()
plt.show()
'''