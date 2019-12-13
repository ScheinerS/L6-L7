# -*- coding: utf-8 -*-
"""
Test estadístico: In Situ - Laboratorio.
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

if os.name == 'posix':   # Si es Linux.
    Linux = True

plt.rc('text', usetex=Linux)    # Solo usa Latex si es Linux.
plt.rc('font', family='serif')

#%%

lugares = ['In Situ','Laboratorio']

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

N = 10000 # Cantidad de datos generados.

datos_nuevos = {}   # Diccionario auxiliar, análogo al otro, pero en el que generamos los datos de forma aleatoria.

Pendientes = {}
 
for lugar in lugares:
    
    datos_nuevos[lugar] = {}
    
        
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
    
    Pendientes[lugar] = {}
    Pendientes[lugar]['hach'] = {}
    Pendientes[lugar]['ss'] = {}
    
#    Pendientes[lugar]['hach' + '_' + 'ss'] = []
    
    Pendientes[lugar]['hach']['ss'] = []    # lista de las N pendientes de x='hach' e y='ss'
    Pendientes[lugar]['hach']['spm'] = []
    Pendientes[lugar]['ss']['spm'] = []
    
    def Ajuste(x,y):
        cond = (~ datos_nuevos[lugar][x].isna()) & (~ datos_nuevos[lugar][y].isna())
        # 'x' e 'y' son los strings: 'hach','ss','spm'.
        nominador   = (datos_nuevos[lugar][x].loc[cond]*datos_nuevos[lugar][y].loc[cond]).sum(skipna=True)
        denominador = (datos_nuevos[lugar][x].loc[cond]*datos_nuevos[lugar][x].loc[cond]).sum(skipna=True)
        return nominador/denominador
    
    # Para cada combinación, 
    for j in range(N):
        # Simulamos los puntos:
        datos_nuevos[lugar]['hach'] = datos[lugar]['hach'] + 2*datos[lugar]['hach_err']*(np.random.rand(len(datos[lugar]['hach']))-0.5)
        datos_nuevos[lugar]['ss'] = datos[lugar]['ss'] + 2*datos[lugar]['ss_err']*(np.random.rand(len(datos[lugar]['ss']))-0.5)
        datos_nuevos[lugar]['spm'] = datos[lugar]['spm'] + 2*datos[lugar]['spm_err']*(np.random.rand(len(datos[lugar]['spm']))-0.5)

        # Los guardamos en 'Pendientes':
        Pendientes[lugar]['hach']['ss'].append(Ajuste('hach','ss'))     # se agrega el ajuste j-ésimo.
        Pendientes[lugar]['hach']['spm'].append(Ajuste('hach','spm'))
        Pendientes[lugar]['ss']['spm'].append(Ajuste('ss','spm'))
               
        # Graficamos uno, para ver si vamos bien:    
        if lugar=='In Situ':
            plt.plot(j,Pendientes[lugar]['ss']['spm'][j],'.',color='blue',label=lugar)
        else:
            plt.plot(j,Pendientes[lugar]['ss']['spm'][j],'.',color='red',label=lugar)
       

#plt.axhline(y=0.7536,color='red',label='Datos reales (Laboratorio)')
#plt.axhline(y=0)

plt.legend(loc='best', fontsize=LegendSize)
plt.title(r'Cantidad de simulaciones: N = %d'%(N), fontsize=TitleSize)
plt.xlabel(r'N\'umero de la simulaci\'on', fontsize=AxisLabelSize)
plt.ylabel(r'Pendiente', fontsize=AxisLabelSize)
plt.grid(axis='both', color='k', linestyle='dashed', linewidth=2, alpha=0.2)

if Linux:
    plt.savefig(path + '/Simulaciones.png')


# Corroborar.

# La cuenta que hay que hacer es:      
# m = np.dot(x,y)/np.dot(x,x)

# FALTA VER QUE LAS DISTRIBUCIONES SON GAUSSIANAS.

#print(Pendientes['Laboratorio']['hach']['ss'])

#%%


# TEST:
experimentos = {0:'hach', 1:'ss', 2:'spm'}

for i in range(3):
    for j in range(i+1,3):
        print(experimentos[i],experimentos[j])
        
        LAB = Pendientes['Laboratorio'][experimentos[i]][experimentos[j]]
        IS = Pendientes['In Situ'][experimentos[i]][experimentos[j]]

        # Gráfico:
        
        plt.figure()
        
        plt.hist(LAB, bins = int(np.sqrt(N)), label='Laboratorio', color = 'red')
        plt.hist(IS, bins = int(np.sqrt(N)), label='In Situ', color = 'blue')
        
        plt.xlim(0,1.2)
        
        plt.xlabel(r'm', fontsize=AxisLabelSize)
        plt.ylabel(r'', fontsize=AxisLabelSize)
        plt.title(r'Pendiente: %s - %s [N = %d]'%(experimentos[i],experimentos[j],N), fontsize=TitleSize)
        plt.legend(loc='best', fontsize=LegendSize)
        plt.grid(axis='both', color='k', linestyle='dashed', linewidth=2, alpha=0.2)
        plt.show()
        
        if Linux:
            plt.savefig(path + '/Simulación: %s - %s [N = %d].png'%(experimentos[i],experimentos[j],N))


'''

Cosas que faltaría hacer para terminar esta parte del trabajo:
    
    - Eliminar los outliers y ajustar para corroborar que los seis valores de m simulados éstén dentro de lo esperado.
    
    - SI TIENE SENTIDO, corroborar que las distribuciones sean normales.
    
    - 
    

'''
