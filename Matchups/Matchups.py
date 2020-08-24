
import sys
import os
import matplotlib.pyplot as plt
from matplotlib import rcParams, cycler
#import csv
import numpy as np
import pandas as pd
from scipy.optimize import curve_fit

path = os.path.dirname(os.path.realpath('__file__'))
sys.path.append(path)

TitleSize = 15
AxisLabelSize = 15
LegendSize = 10
NumberSize = 12

plt.close('all')

if os.name == 'posix':
    Linux = True

plt.rc('text', usetex=Linux)
plt.rc('font', family='serif')

CV_threshold = 20

#%%
filenames_10 = {'IMG': 'IMG_20191210.xlsx',
                'Trios': 'RdP_20191210_Trios_QC_RhowStd750_SatSensors.xlsx',
                'ECO': 'RdP_20191210_ECO-FLNTU.xlsx',
                'OBS': 'RdP_20191210_Campbell.xlsx',
                'HACH': 'RdP_20191210.xlsx'}

filenames_17 = {'IMG': 'IMG_20191217.xlsx',
                'Trios': 'RdP_20191217_Trios_QC_RhowStd750_SatSensors.xlsx',
                'ECO': 'RdP_20191217_ECO-FLNTU.xlsx',
                'OBS': 'RdP_20191217_Campbell.xlsx',
                'HACH': 'RdP_20191217.xlsx'}

filenames = {'2019-12-10': filenames_10,
             '2019-12-17': filenames_17
             }

#Estaciones de las que tenemos imágenes para cada campaña:
stations_IMG = {'2019-12-10': 6,    # solo ST06
                '2019-12-17': 11    # solo ST11
                }

for Campaign in filenames.keys():
    
    print('Campaña:\t',Campaign)
    
    # Paths:

    path_datos = path + '/Datos/' + Campaign + '/'
    
    path_IMG = path_datos + filenames[Campaign]['IMG']
    path_Trios = path_datos + filenames[Campaign]['Trios']
    pathECO = path_datos + filenames[Campaign]['ECO']
    pathOBS = path_datos + filenames[Campaign]['OBS']
    pathHACH = path_datos + filenames[Campaign]['HACH']

    # Data:
    data_IMG_Mean = pd.read_excel(path_IMG, skiprows=None)
    data_Trios_Mean = pd.read_excel(path_Trios, sheet_name='Rhow', skiprows=1)
    data_Trios_MA = pd.read_excel(path_Trios, sheet_name='MA', skiprows=1)
    data_Trios_VIIRS = pd.read_excel(path_Trios, sheet_name='VIIRS', skiprows=1)
    dataECO_Mean = pd.read_excel(pathECO ,sheet_name='Stations_Mean',skiprows=1)
    dataOBS_Mean = pd.read_excel(pathOBS ,sheet_name='Stations_Mean',skiprows=1)
    dataHACH_Mean = pd.read_excel(pathHACH ,sheet_name='turbidityHACH',skiprows=1)
    
    data_Trios_CV = pd.read_excel(path_Trios, sheet_name='TriosStats', skiprows=1)
    data_Trios_Std = pd.read_excel(path_Trios, sheet_name='RhowStd', skiprows=1)
    data_Trios_MAStd = pd.read_excel(path_Trios, sheet_name='MAStd', skiprows=1)
    data_Trios_VIIRSStd = pd.read_excel(path_Trios, sheet_name='VIIRSStd', skiprows=1)
    dataECO_CV = pd.read_excel(pathECO ,sheet_name='Stations_CV',skiprows=1)
    dataOBS_CV = pd.read_excel(pathOBS ,sheet_name='Stations_CV',skiprows=1)
    dataHACH_CV = pd.read_excel(pathHACH ,sheet_name='turbidityHACH',skiprows=1)
    
    ntu_ECO = dataECO_Mean['turbidity (NTU)']
    #chl_ECO = dataECO_Mean['chl (ug/l)']
    ntu_OBS = dataOBS_Mean['SS_OBS501_I2016[FNU]']
    #temp_OBS = dataOBS_Mean['PTemp_CR800_I2016[DegC]']
    ntu_HACH = dataHACH_Mean['Mean']
    
    # CV: coefficient of variation
    ntu_ECO_err = dataECO_Mean['turbidity (NTU)'] * dataECO_CV['turbidity (NTU)']/100
    #chl_ECO_err = dataECO_Mean['chl (ug/l)'] * dataECO_CV['chl (ug/l)']/100
    ntu_OBS_err = dataOBS_Mean['SS_OBS501_I2016[FNU]'] * dataOBS_CV['SS_OBS501_I2016[FNU]']/100
    ntu_HACH_err = dataHACH_Mean['Mean'] * dataHACH_CV['CV[%]']/100
    
    
    rho_Trios = {}
    rho_Trios_err = {}
    rho_Trios_MA = {}
    rho_Trios_MA_err = {}
    rho_Trios_VIIRS = {}
    rho_Trios_VIIRS_err = {}
    rho_IMG = {}    
    #longitudes = [645, 859]
    
    # Rhow:
    rho_Trios[645] = data_Trios_Mean['645.0']
    rho_Trios[860] = data_Trios_Mean['860.0']
    
    rho_Trios_err[645] = data_Trios_Std['645.0']
    rho_Trios_err[860] = data_Trios_Std['860.0']
    
    # MA:
    rho_Trios_MA[645] = data_Trios_MA[645]
    rho_Trios_MA[860] = data_Trios_MA[859]
    
    rho_Trios_MA_err[645] = data_Trios_MAStd[645]
    rho_Trios_MA_err[860] = data_Trios_MAStd[859]
    
    # VIIRS:
    rho_Trios_VIIRS[645] = data_Trios_VIIRS[671]
    rho_Trios_VIIRS[860] = data_Trios_VIIRS[862]
    
    rho_Trios_VIIRS_err[645] = data_Trios_VIIRSStd[671]
    rho_Trios_VIIRS_err[860] = data_Trios_VIIRSStd[862]
    
    rho_IMG[645] = data_IMG_Mean[667]
    rho_IMG[860] = data_IMG_Mean[868]
    
    
    longitudes = [645, 860]
    A = {645: 228.1, 860: 3078.9}
    C = {645: 0.1641, 860: 0.2112}

    stations = range(len(ntu_ECO)) # Cantidad de estaciones.
    IMGstation = stations_IMG[Campaign]*np.ones(len(rho_IMG[645]))

    ############################################################

    def Algoritmo(stations, rho):
        T = np.empty(len(stations))
        T_err = np.empty(len(stations))
        T.fill(np.nan)
        T_err.fill(np.nan)
        
        markers = []
        
        # Recorremos cada valor de rho[645]:
        for st in range(len(stations)):
            
            r_645 = rho[645][st]
            
            if r_645<0.05:
                r = rho[645][st]
                T[st] = (A[645]*r)/(1-r/C[645])
                T_err[st] = ((A[645]*C[645]**2)/(C[645]-r)**2)*rho_Trios_err[645][st]
                markers.append('+')
                
            elif r_645>0.07:
                r = rho[860][st]
                T[st] = (A[860]*r)/(1-r/C[860])
                T_err[st] = ((A[860]*C[860]**2)/(C[860]-r)**2)*rho_Trios_err[860][st]
                markers.append('x')
                
            elif 0.05<r_645<0.07:
                # (Caso intermedio)
                
                T_645 = (A[645]*rho[645][st])/(1-rho[645][st]/C[645])
                T_860 = (A[860]*rho[860][st])/(1-rho[860][st]/C[860])
                
                T_645_err = ((A[645]*C[645]**2)/(C[645]-rho[645][st])**2)*rho_Trios_err[645][st]
                T_860_err = ((A[860]*C[860]**2)/(C[860]-rho[860][st])**2)*rho_Trios_err[860][st]
                
                # Peso:
                w = 50*r_645 - 2.5
                T[st] = (1-w)*T_645 + w*T_860
                T_err[st] = (1-w)*T_645_err + w*T_860_err
                markers.append('o')
    
            else:
                T[st] = None
                T_err[st] = None
                markers.append(None)
        return [T, T_err, markers]
    
    
    # Turbidez usando el algoritmo:
    [T_Trios, T_Trios_err, Trios_markers] = Algoritmo(stations,rho_Trios)
    [T_Trios_MA, T_Trios_MA_err, Trios_MA_markers] = Algoritmo(stations,rho_Trios_MA)
    [T_Trios_VIIRS, T_Trios_VIIRS_err, Trios_VIIRS_markers] = Algoritmo(stations,rho_Trios_VIIRS)
    
    [T_IMG, T_IMG_err, IMG_markers] = Algoritmo(IMGstation,rho_IMG)
    


    # Antigua forma de calcular la turbidez:
    T_Trios_viejo = {}
    T_Trios_MA_viejo = {}
    T_Trios_VIIRS_viejo = {}
    T_IMG_viejo = {}
    
    for l in longitudes:
        T_Trios_viejo[l] = (A[l]*rho_Trios[l])/(1-rho_Trios[l]/C[l])
        T_Trios_MA_viejo[l] = (A[l]*rho_Trios_MA[l])/(1-rho_Trios_MA[l]/C[l])
        T_Trios_VIIRS_viejo[l] = (A[l]*rho_Trios_VIIRS[l])/(1-rho_Trios_VIIRS[l]/C[l])
        
        T_IMG_viejo[l] = (A[l]*rho_IMG[l])/(1-rho_IMG[l]/C[l])
    print(T_Trios_viejo)
    ############################################################
    
    # Filtramos los que tengan CV>CV_threshold:
    
    def Filtrar(stations, T, CV_threshold):
        for st in stations:
            if data_Trios_CV['MaxCV400:900 [%]'][st]>CV_threshold:
                T[st] = None
        return T

    Filtrar(stations, T_Trios, CV_threshold)
    Filtrar(stations, T_Trios_MA, CV_threshold)
    Filtrar(stations, T_Trios_VIIRS, CV_threshold)
    Filtrar(IMGstation, T_IMG, CV_threshold)
    
    for l in longitudes:    
        Filtrar(stations, T_Trios_viejo[l], CV_threshold)
        Filtrar(stations, T_Trios_MA_viejo[l], CV_threshold)
        Filtrar(stations, T_Trios_VIIRS_viejo[l], CV_threshold)
        #Filtrar(IMGstation, T_IMG_viejo[l], CV_threshold)
    ############################################################
    
    # Gráfico (turbidez - estaciones) [Rhow]:
    
    plt.figure()
    
    #IMG_colours = {645: 'black', 860: 'darkgray'}
    '''
    IMG_shapes = {'GW94-SWIR12': 'o',
                  'GW94-SWIR13': 's',
                  'GW94-SWIR23': '^',
                  'PCA-SWIR12': '*',
                  'PCA-SWIR13': '+',
                  'PCA-SWIR23': 'x',
                  'PCA-SWIR123': '2'}
    '''
    IMG_shapes = ['o', 's', '^', '*', '+', 'x', '2']
    Algoritmos = ['GW94-SWIR12', 'GW94-SWIR13', 'GW94-SWIR23', 'PCA-SWIR12', 'PCA-SWIR13', 'PCA-SWIR23', 'PCA-SWIR123']
    
    estaciones = range(1,len(stations)+1) # Para los gráficos.
    
    plt.plot(estaciones,ntu_ECO, '-o', color='orange', label=r'ECO FLNTU')
    plt.plot(estaciones,ntu_OBS, '-o', color='blue', label=r'OBS501 (2016) [SS]')
    plt.plot(estaciones,ntu_HACH, '-o', color='red', label=r'HACH')
    
    plt.errorbar(estaciones, T_Trios_viejo[645], yerr=T_Trios_err, color='springgreen', label=r'TriOS+D2015 ($\lambda = 645$)')
    plt.errorbar(estaciones, T_Trios_viejo[860], yerr=T_Trios_err, color='forestgreen', label=r'TriOS+D2015 ($\lambda = 860$)')
    
    plt.errorbar(estaciones, T_Trios, yerr=T_Trios_err, color='gray', label=r'TriOS+D2015')

    for st in stations:
        plt.plot(estaciones[st], T_Trios[st], marker=Trios_markers[st], color='gray')
    
    for i in range(len(Algoritmos)):
        print('Algoritmo:', Algoritmos[i], '\tTurbidez:', T_IMG[i])
    
    # Sacamos los puntos de IMG del gráfico:
    #for i in range(len(Algoritmos)):
    #    plt.scatter(IMGstation[i],T_IMG[i], color='darkslategray', label=r'%s'%Algoritmos[i], marker=IMG_shapes[i])
    
    
    plt.legend(loc='best', fontsize=LegendSize)
    plt.title(r'%s'%Campaign, fontsize=TitleSize)
    plt.xlabel(r'Estación (STxx)', fontsize=AxisLabelSize)
    plt.ylabel(r'Turbidez (FNU)', fontsize=AxisLabelSize)
    plt.grid(axis='both', color='k', linestyle='dashed', linewidth=2, alpha=0.2)
    plt.show()
    
    if Linux:
        plt.savefig(path + '/Algoritmo-Trios/' + '[%s] Trios_Rhow.png'%Campaign)

    ############################################################
        
    # Gráfico (turbidez - estaciones) [MA]:
    
    plt.figure()
    
    #IMG_colours = {645: 'black', 860: 'darkgray'}
    '''
    IMG_shapes = {'GW94-SWIR12': 'o',
                  'GW94-SWIR13': 's',
                  'GW94-SWIR23': '^',
                  'PCA-SWIR12': '*',
                  'PCA-SWIR13': '+',
                  'PCA-SWIR23': 'x',
                  'PCA-SWIR123': '2'}
    '''
    IMG_shapes = ['o', 's', '^', '*', '+', 'x', '2']
    Algoritmos = ['GW94-SWIR12', 'GW94-SWIR13', 'GW94-SWIR23', 'PCA-SWIR12', 'PCA-SWIR13', 'PCA-SWIR23', 'PCA-SWIR123']
    
    estaciones = range(1,len(stations)+1) # Para los gráficos.
    
    plt.plot(estaciones,ntu_ECO, '-o', color='orange', label=r'ECO FLNTU')
    plt.plot(estaciones,ntu_OBS, '-o', color='blue', label=r'OBS501 (2016) [SS]')
    plt.plot(estaciones,ntu_HACH, '-o', color='red', label=r'HACH')
    
    plt.errorbar(estaciones, T_Trios_MA_viejo[645], yerr=T_Trios_MA_err, color='springgreen', label=r'TriOS+D2015 ($\lambda = 645$)')
    plt.errorbar(estaciones, T_Trios_MA_viejo[860], yerr=T_Trios_MA_err, color='forestgreen', label=r'TriOS+D2015 ($\lambda = 860$)')
    
    plt.errorbar(estaciones, T_Trios_MA, yerr=T_Trios_MA_err, color='gray', label=r'TriOS+D2015')

    for st in stations:
        
        plt.plot(estaciones[st], T_Trios_MA[st], marker=Trios_markers[st], color='gray')
    
    # Sacamos los puntos de IMG del gráfico:
    #for i in range(len(Algoritmos)):
        #    plt.scatter(IMGstation[i],T_IMG[i], color='darkslategray', label=r'%s'%Algoritmos[i], marker=IMG_shapes[i])
    
    
    plt.legend(loc='best', fontsize=LegendSize)
    plt.title(r'%s'%Campaign, fontsize=TitleSize)
    plt.xlabel(r'Estación (STxx)', fontsize=AxisLabelSize)
    plt.ylabel(r'Turbidez (FNU)', fontsize=AxisLabelSize)
    plt.grid(axis='both', color='k', linestyle='dashed', linewidth=2, alpha=0.2)
    plt.show()
    
    if Linux:
        plt.savefig(path + '/Algoritmo-Trios/' + '[%s] Trios_MA.png'%Campaign)

    ############################################################
        
    # Gráfico (turbidez - estaciones) [VIIRS]:
    
    plt.figure()
    
    #IMG_colours = {645: 'black', 860: 'darkgray'}
    '''
    IMG_shapes = {'GW94-SWIR12': 'o',
                  'GW94-SWIR13': 's',
                  'GW94-SWIR23': '^',
                  'PCA-SWIR12': '*',
                  'PCA-SWIR13': '+',
                  'PCA-SWIR23': 'x',
                  'PCA-SWIR123': '2'}
    '''
    IMG_shapes = ['o', 's', '^', '*', '+', 'x', '2']
    Algoritmos = ['GW94-SWIR12', 'GW94-SWIR13', 'GW94-SWIR23', 'PCA-SWIR12', 'PCA-SWIR13', 'PCA-SWIR23', 'PCA-SWIR123']
    
    estaciones = range(1,len(stations)+1) # Para los gráficos.
    
    plt.plot(estaciones,ntu_ECO, '-o', color='orange', label=r'ECO FLNTU')
    plt.plot(estaciones,ntu_OBS, '-o', color='blue', label=r'OBS501 (2016) [SS]')
    plt.plot(estaciones,ntu_HACH, '-o', color='red', label=r'HACH')
    
    plt.errorbar(estaciones, T_Trios_VIIRS_viejo[645], yerr=T_Trios_VIIRS_err, color='springgreen', label=r'TriOS+D2015 ($\lambda = 645$)')
    plt.errorbar(estaciones, T_Trios_VIIRS_viejo[860], yerr=T_Trios_VIIRS_err, color='forestgreen', label=r'TriOS+D2015 ($\lambda = 860$)')
    
    plt.errorbar(estaciones, T_Trios_VIIRS, yerr=T_Trios_VIIRS_err, color='gray', label=r'TriOS+D2015')

    for st in stations:
        plt.plot(estaciones[st], T_Trios_VIIRS[st], marker=Trios_markers[st], color='gray')
    
    # Sacamos los puntos de IMG del gráfico:
    #for i in range(len(Algoritmos)):
        #    plt.scatter(IMGstation[i],T_IMG[i], color='darkslategray', label=r'%s'%Algoritmos[i], marker=IMG_shapes[i])
    
    
    plt.legend(loc='best', fontsize=LegendSize)
    plt.title(r'%s'%Campaign, fontsize=TitleSize)
    plt.xlabel(r'Estación (STxx)', fontsize=AxisLabelSize)
    plt.ylabel(r'Turbidez (FNU)', fontsize=AxisLabelSize)
    plt.grid(axis='both', color='k', linestyle='dashed', linewidth=2, alpha=0.2)
    plt.show()
    
    if Linux:
        plt.savefig(path + '/Algoritmo-Trios/' + '[%s] Trios_VIIRS.png'%Campaign)

    ############################################################
    
    #HACH vs Trios [Rhow]
    
    def lineal(x, a, b):
        return a*x+ b
    
    parametros_iniciales = [1,-10]
    
    def Ajustar(x,y):

        # Eliminamos los nans:
        x = x[np.logical_not(np.isnan(y))]
        y = y[np.logical_not(np.isnan(y))]

                
        
        popt, pcov = curve_fit(lineal, x, y, p0=parametros_iniciales, check_finite=True)    
        
        pstd = np.sqrt(np.diag(pcov))
        nombres_de_param = ['a', 'b']
        
        print('Resultado del ajuste:\n')
        for c, v in enumerate(popt):
            print('%s = %5.4f ± %5.4f' % (nombres_de_param[c], v, pstd[c]/2))
        
        return popt


    # Gráfico:
    fig = plt.figure()
    ax = fig.add_subplot()

    ax.set_aspect('equal')
    ax.set_ylim(0,70)
    x = np.linspace(0, 65, 10)
    
    plt.plot(x, x, '--k', label=r'$y=x$')
    
    [a, b] = Ajustar(ntu_HACH,T_Trios)
    
    # Gráfico de los ajustes:
    plt.scatter(ntu_HACH,T_Trios, color='gray', label=r'TriOS+D2015')    
    plt.scatter(ntu_HACH, T_Trios_viejo[645], color='springgreen', label=r'TriOS+D2015 ($\lambda = 645$ nm)')
    plt.scatter(ntu_HACH, T_Trios_viejo[860], color='forestgreen', label=r'TriOS+D2015 ($\lambda = 860$ nm)')

    # Gráfico de los ajustes:
    [a, b] = Ajustar(ntu_HACH,T_Trios)
    plt.plot(x,lineal(x, a, b), '-', color='gray', label=r'$%.2f x %.2f$'%(a,b))
    
    [a, b] = Ajustar(ntu_HACH,T_Trios_viejo[645])
    plt.plot(x,lineal(x, a, b), '-', color='springgreen', label=r'$%.2f x + %.2f$'%(a,b))
    
    [a, b] = Ajustar(ntu_HACH,T_Trios_viejo[860])
    plt.plot(x,lineal(x, a, b), '-', color='forestgreen', label=r'$%.2f x %.2f$'%(a,b))
    
    #H = list(ntu_HACH[IMGstation])
    #for i in range(len(Algoritmos)):
    #    plt.scatter(H[i],T_IMG[i], color='black', label=r'%s'%Algoritmos[i], marker=IMG_shapes[i])
    
    
    #plt.plot(ntu_HACH[IMGstation], T_IMG, 'o', label=r'IMG')
      
    plt.legend(loc='best', fontsize=LegendSize)
    plt.title(r'%s'%Campaign, fontsize=TitleSize)
    plt.xlabel(r'HACH (FNU)', fontsize=AxisLabelSize)
    plt.ylabel(r'TriOS (FNU)', fontsize=AxisLabelSize)
    plt.grid(axis='both', color='k', linestyle='dashed', linewidth=2, alpha=0.2)
    plt.show()
    
    if Linux:
        plt.savefig(path + '/Algoritmo-IMG/' + '[%s] HACH_vs_Trios_Rhow.png'%Campaign)

    ############################################################
    
    #HACH vs Trios [MA]
    
    # Gráfico:
    fig = plt.figure()
    ax = fig.add_subplot()

    ax.set_aspect('equal')
    ax.set_ylim(0,70)
    x = np.linspace(0, 65, 10)
    
    plt.plot(x, x, '--k', label=r'$y=x$')
    
    [a, b] = Ajustar(ntu_HACH,T_Trios_MA)
    
    # Gráfico de los ajustes:
    plt.scatter(ntu_HACH, T_Trios_MA, color='gray', label=r'TriOS+D2015')    
    plt.scatter(ntu_HACH, T_Trios_MA_viejo[645], color='springgreen', label=r'TriOS+D2015 ($\lambda = 645$ nm)')
    plt.scatter(ntu_HACH, T_Trios_MA_viejo[860], color='forestgreen', label=r'TriOS+D2015 ($\lambda = 860$ nm)')

    # Gráfico de los ajustes:
    [a, b] = Ajustar(ntu_HACH, T_Trios_MA)
    plt.plot(x,lineal(x, a, b), '-', color='gray', label=r'$%.2f x %.2f$'%(a,b))
    
    [a, b] = Ajustar(ntu_HACH, T_Trios_MA_viejo[645])
    plt.plot(x,lineal(x, a, b), '-', color='springgreen', label=r'$%.2f x + %.2f$'%(a,b))
    
    [a, b] = Ajustar(ntu_HACH, T_Trios_MA_viejo[860])
    plt.plot(x,lineal(x, a, b), '-', color='forestgreen', label=r'$%.2f x %.2f$'%(a,b))
    
    #H = list(ntu_HACH[IMGstation])
    #for i in range(len(Algoritmos)):
    #    plt.scatter(H[i],T_IMG[i], color='black', label=r'%s'%Algoritmos[i], marker=IMG_shapes[i])
    
    
    #plt.plot(ntu_HACH[IMGstation], T_IMG, 'o', label=r'IMG')
      
    plt.legend(loc='best', fontsize=LegendSize)
    plt.title(r'%s'%Campaign, fontsize=TitleSize)
    plt.xlabel(r'HACH (FNU)', fontsize=AxisLabelSize)
    plt.ylabel(r'TriOS (FNU)', fontsize=AxisLabelSize)
    plt.grid(axis='both', color='k', linestyle='dashed', linewidth=2, alpha=0.2)
    plt.show()
    
    if Linux:
        plt.savefig(path + '/Algoritmo-IMG/' + '[%s] HACH_vs_Trios_MA.png'%Campaign)
    
    ############################################################
    
    #HACH vs Trios [VIIRS]
    
    # Gráfico:
    fig = plt.figure()
    ax = fig.add_subplot()

    ax.set_aspect('equal')
    ax.set_ylim(0,70)
    x = np.linspace(0, 65, 10)
    
    plt.plot(x, x, '--k', label=r'$y=x$')
    
    [a, b] = Ajustar(ntu_HACH,T_Trios_VIIRS)
    
    # Gráfico de los ajustes:
    plt.scatter(ntu_HACH, T_Trios_VIIRS, color='gray', label=r'TriOS+D2015')    
    plt.scatter(ntu_HACH, T_Trios_VIIRS_viejo[645], color='springgreen', label=r'TriOS+D2015 ($\lambda = 645$ nm)')
    plt.scatter(ntu_HACH, T_Trios_VIIRS_viejo[860], color='forestgreen', label=r'TriOS+D2015 ($\lambda = 860$ nm)')

    # Gráfico de los ajustes:
    [a, b] = Ajustar(ntu_HACH, T_Trios_VIIRS)
    plt.plot(x,lineal(x, a, b), '-', color='gray', label=r'$%.2f x %.2f$'%(a,b))
    
    [a, b] = Ajustar(ntu_HACH, T_Trios_VIIRS_viejo[645])
    plt.plot(x,lineal(x, a, b), '-', color='springgreen', label=r'$%.2f x + %.2f$'%(a,b))
    
    [a, b] = Ajustar(ntu_HACH, T_Trios_VIIRS_viejo[860])
    plt.plot(x,lineal(x, a, b), '-', color='forestgreen', label=r'$%.2f x %.2f$'%(a,b))
    
    #H = list(ntu_HACH[IMGstation])
    #for i in range(len(Algoritmos)):
    #    plt.scatter(H[i],T_IMG[i], color='black', label=r'%s'%Algoritmos[i], marker=IMG_shapes[i])
    
    
    #plt.plot(ntu_HACH[IMGstation], T_IMG, 'o', label=r'IMG')
      
    plt.legend(loc='best', fontsize=LegendSize)
    plt.title(r'%s'%Campaign, fontsize=TitleSize)
    plt.xlabel(r'HACH (FNU)', fontsize=AxisLabelSize)
    plt.ylabel(r'TriOS (FNU)', fontsize=AxisLabelSize)
    plt.grid(axis='both', color='k', linestyle='dashed', linewidth=2, alpha=0.2)
    plt.show()
    
    if Linux:
        plt.savefig(path + '/Algoritmo-IMG/' + '[%s] HACH_vs_Trios_VIIRS.png'%Campaign)





