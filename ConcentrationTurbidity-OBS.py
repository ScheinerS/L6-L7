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


#%%

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

archivos=['ConcentrationTurbidity-OBS'] # Por si queremos agregar más archivos después.

for s in archivos:
    FILE=path+'/'+s+'.csv'
    data = pd.read_csv(FILE)
    # Extraemos las cuatro columnas que nos interesan:
    y_df = pd.DataFrame(data, columns= ['Concentración'])
    
    y_df = np.array(y_df)
    y_df = y_df[:12]
    
    x = pd.DataFrame(data, columns= ['Sample 1 (FNU)','Sample 2 (FNU)','Sample 3 (FNU)'])
    x = x.dropna(axis=0)
    x = np.array(x)
    #x = x[:12,:]   # no tiene sentido seguir haciéndolo, porque  dropna() ya le sacó las nulas.
    
    x_Hach=np.zeros(len(x))
    x_Hach_err=np.zeros((2,len(x)))
    x_Hach_err_tot=np.zeros(len(x))
    
    x_OBS_df = pd.DataFrame(data, columns= ['SS'])
    x_OBS_df = np.array(x_OBS_df)
    x_OBS_df = x_OBS_df[:12]
    
    y_OBS=np.zeros(len(y_df))
    x_OBS=np.zeros(len(y_df))
    x_OBS_err=10*np.ones(len(x_OBS))
    
    y_Hach=[486.0606061, 324.040404, 241.0703812, 158.9673315, 118.9453447, 79.11100286, 0] # A mano. Ya fue.
    y_Hach_err=np.zeros(len(y_Hach))    # FALTA AGREGAR LOS ERRORES.
    
    for i in range(len(x)):
       x_Hach[i]=np.median(x[i])
       x_Hach_err[0,i]=x_Hach[i] - np.min(x[i])
       x_Hach_err[1,i]=np.max(x[i]) - x_Hach[i]
       x_Hach_err_tot[i]=x_Hach_err[1,i] - x_Hach_err[0,i]
       
       y_OBS[i]=y_df[i]
       x_OBS[i]= x_OBS_df[i]
       
    # Ajuste:
    
    def lineal_con_offset(x, a, b):
        return a*x+ b
    
    def lineal(x, a):
        return a*x
    
    Ajustar(lineal_con_offset(x_Hach),x_Hach,y_Hach,x_Hach_err,y_Hach_err)
    '''
    popt_Hach, pcov_Hach = curve_fit(modelo, x_med, y_Hach, p0=None)    
    popt_OBS, pcov_OBS = curve_fit(modelo, x_OBS, y_OBS, p0=None)
    
    popt_Hach_real, pcov_Hach_real = curve_fit(modelo_real, x_med, y_Hach, p0=None)    
    popt_OBS_real, pcov_OBS_real = curve_fit(modelo_real, x_OBS, y_OBS, p0=None)
    
    pstd_Hach = np.sqrt(np.diag(pcov_Hach))
    pstd_OBS = np.sqrt(np.diag(pcov_OBS))
    
    pstd_Hach_real = np.sqrt(np.diag(pcov_Hach_real))
    pstd_OBS_real = np.sqrt(np.diag(pcov_OBS_real))
    
    
    nombres_de_param = ['a', 'b']

    print('\nResultado del ajuste (Hach):\n')
    for c, v in enumerate(popt_Hach):
        print('%s = %5.4f ± %5.4f' % (nombres_de_param[c], v, pstd_Hach[c]/2))
    
    print('\nResultado del ajuste (OBS):\n')
    for c, v in enumerate(popt_OBS):
        print('%s = %5.4f ± %5.4f' % (nombres_de_param[c], v, pstd_OBS[c]/2))
    
    nombres_de_param_reales = ['a']

    print('\nResultado del ajuste (Hach):\n')
    for c, v in enumerate(popt_Hach_real):
        print('%s = %5.4f ± %5.4f' % (nombres_de_param_reales[c], v, pstd_Hach_real[c]/2))
    
    print('\nResultado del ajuste (OBS):\n')
    for c, v in enumerate(popt_OBS_real):
        print('%s = %5.4f ± %5.4f' % (nombres_de_param_reales[c], v, pstd_OBS_real[c]/2))
    '''
    #####################################
    # Gráfico del ajuste ax+b:
    
    plt.figure()
    
    plt.errorbar(x_med, y_Hach, xerr=x_err, yerr=None, fmt='o',color='darkred', label=r'Hach', ms=5.5, zorder=0)
    plt.plot(x_med, modelo(x_med, *popt_Hach), color='red', label=r'Ajuste: $y = %.4f \; x + %.4f $'%(popt_Hach[0],popt_Hach[1]), lw=1, zorder=4)

    plt.errorbar(x_OBS, y_OBS, xerr=xerr_OBS, yerr=None, fmt='o', color='darkblue', label=r'OBS', ms=5.5, zorder=0)
    plt.plot(x_OBS, modelo(x_OBS, *popt_OBS),  color='blue', label=r'Ajuste: $y = %.4f \; x %.4f $'%(popt_OBS[0],popt_OBS[1]), lw=1, zorder=4)


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

#%% Gráfico
'''
plt.figure(dpi=100)

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