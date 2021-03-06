'''
Programa para leer los archivos en formato CSV y graficarlos.
'''

import sys
import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
#from scipy.optimize import curve_fit
from scipy.odr import Model,RealData,ODR
#from matplotlib.ticker import AutoMinorLocator

path = os.path.dirname(os.path.realpath('__file__'))
sys.path.append(path)

TitleSize=20
AxisLabelSize=15
LegendSize=12
NumberSize=10

plt.close('all')

if os.name == 'posix':   # Si es Linux.
    Linux = True

plt.rc('text', usetex=Linux)    # Solo usa Latex si es Linux.
plt.rc('font', family='serif')

#%%

archivo = 'Dilucion-OBS'

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
#%%

# Ajustes:
 
def lineal_con_offset(p0,x):
    a, b = p0 # parámetros iniciales
    return a*x + b

def lineal(p0,x):
    a, b = p0
    return a*x

def Ajustar(function,x,y,x_err,y_err):
    print('Ajuste:\t',function.__name__,'\n')
    # Create a model for fitting.
    model = Model(function)
    # Create a RealData object using our initiated data from above.
    D = RealData(x, y, sx=x_err, sy=y_err)
    # Set up ODR with the model and data.
    odr = ODR(D, model, beta0=[0.5, 0.])
    # Run the regression.
    out = odr.run()
    # Use the in-built pprint method to give us results.
    out.pprint()
    print(40*'-')
    return out

print(40*'*'+'\n\t\tHACH\n'+40*'*')
fit_Hach_offset = Ajustar(lineal_con_offset,x_Hach,y_Hach,x_Hach_err_tot,y_Hach_err)
fit_OBS_offset = Ajustar(lineal_con_offset,x_OBS,y_OBS,x_OBS_err,y_OBS_err)

print(40*'*'+'\n\t\tOBS\n'+40*'*')
fit_Hach = Ajustar(lineal,x_Hach,y_Hach,x_Hach_err_tot,y_Hach_err)
fit_OBS = Ajustar(lineal,x_OBS,y_OBS,x_OBS_err,y_OBS_err)

#%%

# Vectores para graficar los ajustes:

x_fit_Hach = np.linspace(x_Hach[0], x_Hach[-1], 1000)
y_fit_Hach_offset = lineal_con_offset(fit_Hach_offset.beta, x_fit_Hach)
y_fit_Hach = lineal(fit_Hach.beta, x_fit_Hach)


x_fit_OBS = np.linspace(x_OBS[0], x_OBS[-1], 1000)
y_fit_OBS_offset = lineal_con_offset(fit_OBS_offset.beta, x_fit_OBS)
y_fit_OBS = lineal(fit_OBS.beta, x_fit_OBS)

#%%
# Gráfico del ajuste ax+b:
plt.figure()

plt.errorbar(x_Hach, y_Hach, xerr=x_Hach_err, yerr=y_Hach_err, fmt='.',color='darkred', label=r'Hach', ms=5.5, zorder=0)
plt.plot(x_fit_Hach, y_fit_Hach_offset, color='red', label=r'Ajuste: $y = %.4f \; x %.4f $'%(fit_Hach_offset.beta[0],fit_Hach_offset.beta[1]), lw=1, zorder=4)

plt.errorbar(x_OBS, y_OBS, xerr=x_OBS_err, yerr=y_OBS_err, fmt='.', color='darkblue', label=r'OBS', ms=5.5, zorder=0)
plt.plot(x_fit_OBS, y_fit_OBS_offset, color='blue', label=r'Ajuste: $y = %.4f \; x %.4f $'%(fit_OBS_offset.beta[0],fit_OBS_offset.beta[1]), lw=1, zorder=4)


plt.tick_params(axis='both', which='major', labelsize=NumberSize)
plt.xlabel(r'Turbidez (FNU)', fontsize=AxisLabelSize)
plt.ylabel(r'Concentraci\'on (mg/l)', fontsize=AxisLabelSize)
plt.title(r'Ajuste $y=ax+b$', fontsize=TitleSize)
plt.legend(loc='best', fontsize=LegendSize)
plt.grid(axis='both', color='k', linestyle='dashed', linewidth=2, alpha=0.1)
plt.show()
if Linux:
    plt.savefig(path + '/' + archivo + '.png')

#####################################
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

if Linux: # Solo guarda la imagen en Linux.
    plt.savefig(path + '/' + archivo + 'real.png')
