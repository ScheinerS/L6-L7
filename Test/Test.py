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

TitleSize=15
AxisLabelSize=15
LegendSize=12
NumberSize=10

plt.close('all')

plt.rc('text', usetex=True)
plt.rc('font', family='serif')

#%%

lugares = ['In Situ','Laboratorio']
experimentos = ['hach','ss','spm']

data = {}   # Diccionario de DataFrames con los datos de cada lugar: IS y LAB.
datos = {}  # Diccionario de Series con los valores para generar los datos
                # nuevos de cada lugar: IS y LAB.

for lugar in lugares:
    
    datos[lugar] = {}   # Cada uno es un diccionario, porque va a tener cada una de las series adentro.
    
    data[lugar] = pd.read_excel(path + '/' + lugar + '.xlsx',header=0)
    #data = data.rename(columns=data.iloc[0])
    #data = data.drop(0)
    
    datos[lugar]['hach'] = data[lugar]['HACH_Mean']
    datos[lugar]['hach_err'] = data[lugar]['HACH_Mean']*data[lugar]['HACH_CV']/100
    
    datos[lugar]['ss'] = data[lugar]['SS_OBS501_Mean']
    datos[lugar]['ss_err'] = data[lugar]['SS_OBS501_Mean']*data[lugar]['SS_OBS501_CV']/100
    
    datos[lugar]['spm'] = data[lugar]['SPM_Mean']
    datos[lugar]['spm_err'] = data[lugar]['SPM_CV']*data[lugar]['SPM_Mean']/100


#%%

# Generamos los datos aleatorios:

N = 100 # Cantidad de datos generados.

datos_nuevos = {}   # Diccionario auxiliar, análogo al otro, pero en el que generamos los datos de forma aleatoria.

Pendientes = []

for j in range(N):
    Pendientes.append({})  # Diccionario al que se accede igual que en los otros, pero que solo guarda las pendientes.

    for lugar in lugares:
        datos_nuevos[lugar] = {}
        
        datos_nuevos[lugar]['hach'] = datos[lugar]['hach'] + 2*datos[lugar]['hach_err']*(np.random.rand(len(datos[lugar]['hach']))-0.5)
        datos_nuevos[lugar]['ss'] = datos[lugar]['ss'] + 2*datos[lugar]['ss_err']*(np.random.rand(len(datos[lugar]['ss']))-0.5)
        datos_nuevos[lugar]['spm'] = datos[lugar]['spm'] + 2*datos[lugar]['spm_err']*(np.random.rand(len(datos[lugar]['spm']))-0.5)
        
        # Si queremos graficar los valores aleatorios:
        GraficarErrores = False
    
        if GraficarErrores:
            # Hacemos un gráfico de los errores para corroborar si se generan como buscamos:
            plt.errorbar(datos[lugar]['hach'], datos[lugar]['ss'], xerr=datos[lugar]['hach_err'], yerr=datos[lugar]['ss_err'], fmt='.',color='darkred', label=r'Hach', ms=5.5, zorder=0)
            plt.plot(datos_nuevos[lugar]['hach'],datos_nuevos[lugar]['ss'],'.')
            plt.xlabel(r'hach', fontsize=AxisLabelSize)
            plt.ylabel(r'ss', fontsize=AxisLabelSize)
            plt.title(r'%d puntos generados'%(N), fontsize=TitleSize)
            #plt.legend(loc='best', fontsize=LegendSize)
            plt.grid(axis='both', color='k', linestyle='dashed', linewidth=2, alpha=0.1)
            plt.show()
        
        # Ajuste de los datos generados:
        
        Pendientes[j][lugar] = {}
        Pendientes[j][lugar]['hach'] = {}
        Pendientes[j][lugar]['ss'] = {}
        
        Pendientes[j][lugar]['hach']['ss'] = (datos_nuevos[lugar]['hach']*datos_nuevos[lugar]['ss']).sum(skipna=True)/(datos_nuevos[lugar]['hach']*datos_nuevos[lugar]['hach']).sum(skipna=True)
        Pendientes[j][lugar]['hach']['spm'] = (datos_nuevos[lugar]['hach']*datos_nuevos[lugar]['spm']).sum(skipna=True)/(datos_nuevos[lugar]['hach']*datos_nuevos[lugar]['hach']).sum(skipna=True)
        aa=Pendientes[j][lugar]['ss']['spm'] = (datos_nuevos[lugar]['ss']*datos_nuevos[lugar]['spm']).sum(skipna=True)/(datos_nuevos[lugar]['ss']*datos_nuevos[lugar]['ss']).sum(skipna=True)
        
        # CORROBORAR QUE ESTÉ BIEN HECHA ESA CUENTA.
        if lugar=='In Situ':
            plt.plot(j,Pendientes[j][lugar]['ss']['spm'],'.',color='blue',label=lugar)
        else:
            plt.plot(j,Pendientes[j][lugar]['ss']['spm'],'.',color='red',label=lugar)
        

plt.legend(loc='best', fontsize=LegendSize)
plt.title(r'Cantidad de simulaciones: N = %d'%(N), fontsize=TitleSize)
#plt.xlabel(r'número de la simulación', fontsize=AxisLabelSize)
#plt.ylabel(r'Pendiente', fontsize=AxisLabelSize)




# La cuenta que hay que hacer es:      
# m= np.dot(x,y)/np.dot(x,x)


##################
# FALTA VER QUE LAS DISTRIBUCIONES SON GAUSSIANAS.







#%%

'''

for lugar in lugares:
    plt.figure()
    
    plt.hist(m_Hach,bins = int(np.sqrt(N)),label='Hach',color = 'red')
    plt.hist(m_OBS,bins = int(np.sqrt(N)),label='OBS',color = 'blue')


plt.xlabel(r'm', fontsize=AxisLabelSize)
plt.ylabel(r'', fontsize=AxisLabelSize)
plt.title(r'N = %d'%(N), fontsize=TitleSize)
plt.legend(loc='best', fontsize=LegendSize)
plt.grid(axis='both', color='k', linestyle='dashed', linewidth=2, alpha=0.1)
plt.show()



'''









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
