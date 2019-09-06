'''
Programa para leer los archivos en formato CSV y graficarlos.
'''

import sys
import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
from scipy.odr import Model,RealData,ODR
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


#%% Función que va a funcionar después:

def Ajustar(function,x,y,x_err,y_err):
        # Create a model for fitting.
    model = Model(function)
    # Create a RealData object using our initiated data from above.
    D = RealData(x, y, sx=x_err, sy=y_err)
    # Set up ODR with the model and data.
    odr = ODR(D, model, beta0=[0., 1.])
    # Run the regression.
    out = odr.run()
    # Use the in-built pprint method to give us results.
    out.pprint()
    
    return out

#%%

archivos=['ConcentrationTurbidity-OBS'] # Por si queremos agregar más archivos después.

for s in archivos:
    FILE=path+'/'+s+'.csv'
    data = pd.read_csv(FILE)

    y = pd.DataFrame(data, columns= ['Concentración'])
    y = y.dropna(axis=0)
    y = np.array(y)

    x = pd.DataFrame(data, columns= ['Sample 1 (FNU)','Sample 2 (FNU)','Sample 3 (FNU)'])
    x = x.dropna(axis=0)
    x = np.array(x)
    
    x_Hach=np.zeros(len(x))
    x_Hach_err=np.zeros((2,len(x)))
    x_Hach_err_tot=np.zeros(len(x))
    
    x_OBS = pd.DataFrame(data, columns= ['SS'])
    x_OBS = data['SS']
    x_OBS = x_OBS.dropna()
    x_OBS = np.array(x_OBS)
    
    y_OBS = np.zeros(len(y))


    x_OBS_err = 10*np.ones(len(x_OBS))
    
    y = np.array([486.0606061, 324.040404, 241.0703812, 158.9673315, 118.9453447, 79.11100286, 0]) # A mano. Ya fue.
    y_err = np.zeros(len(y))    # FALTA AGREGAR LOS ERRORES.
    
    for i in range(len(x)):
       x_Hach[i]=np.median(x[i])
       x_Hach_err[0,i]=x_Hach[i] - np.min(x[i])
       x_Hach_err[1,i]=np.max(x[i]) - x_Hach[i]
       x_Hach_err_tot[i]=x_Hach_err[1,i] - x_Hach_err[0,i]
       
    # Ajuste:
 
    def lineal_con_offset(p0, x):
        a, b = p0 # parámetros iniciales
        return a*x+ b
    
    def lineal(x, a):
        return a*x
    
    fit = Ajustar(lineal_con_offset,x_Hach,y,x_Hach_err_tot,y_err)
    
    #####################################
    # Gráfico del ajuste ax+b:
    
    x_fit_Hach = np.linspace(x_Hach[0], x_Hach[-1], 1000)
    y_fit_Hach = lineal_con_offset(fit.beta, x_fit_Hach)
    

    plt.figure()
    
    plt.errorbar(x_Hach, y, xerr=x_Hach_err, yerr=None, fmt='o',color='darkred', label=r'Hach', ms=5.5, zorder=0)
    plt.plot(x_fit_Hach, y_fit_Hach, color='red', label=r'Ajuste: $y = %.4f \; x + %.4f $'%(fit.beta[0],fit.beta[1]), lw=1, zorder=4)

    plt.errorbar(x_OBS, y, xerr=x_OBS_err, yerr=None, fmt='o', color='darkblue', label=r'OBS', ms=5.5, zorder=0)
    #plt.plot(x_OBS, modelo(x_OBS, *popt_OBS),  color='blue', label=r'Ajuste: $y = %.4f \; x %.4f $'%(popt_OBS[0],popt_OBS[1]), lw=1, zorder=4)


    plt.tick_params(axis='both', which='major', labelsize=NumberSize)
    plt.xlabel(r'Turbidez (FNU)', fontsize=AxisLabelSize)
    plt.ylabel(r'Concentraci\'on (mg/l)', fontsize=AxisLabelSize)
    plt.title(r'Ajuste $y=ax+b$', fontsize=TitleSize)
    plt.legend(loc='best', fontsize=LegendSize)
    plt.grid(axis='both', color='k', linestyle='dashed', linewidth=2, alpha=0.1)
    plt.show()
    plt.savefig(path+'/'+s+'.png')
    
    #####################################
    # Gráfico del ajuste ax:
    '''
    plt.figure()
    
    plt.errorbar(x_med, y_Hach, xerr=x_err, yerr=None, fmt='o',color='darkred', label=r'Hach', ms=5.5, zorder=0)
    plt.plot(x_med, modelo_real(x_med, *popt_Hach_real), color='red', label=r'Ajuste: $y = %.4f \; x$'%(popt_Hach_real[0]), lw=1, zorder=4)

    plt.errorbar(x_OBS, y_OBS, xerr=xerr_OBS, yerr=None, fmt='o', color='darkblue', label=r'OBS', ms=5.5, zorder=0)
    plt.plot(x_OBS, modelo_real(x_OBS, *popt_OBS_real),  color='blue', label=r'Ajuste: $y = %.4f \; x$'%(popt_OBS_real[0]), lw=1, zorder=4)


    plt.tick_params(axis='both', which='major', labelsize=NumberSize)
    plt.xlabel(r'Turbidez (FNU)', fontsize=AxisLabelSize)
    plt.ylabel(r'Concentraci\'on (mg/l)', fontsize=AxisLabelSize)
    plt.title(r'Ajuste $y=ax$', fontsize=TitleSize)
    plt.legend(loc='best', fontsize=LegendSize)
    plt.grid(axis='both', color='k', linestyle='dashed', linewidth=2, alpha=0.1)
    plt.show()
    plt.savefig(path+'/'+s+'real.png')
    '''