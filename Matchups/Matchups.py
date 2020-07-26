
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
    dataECO_Mean = pd.read_excel(pathECO ,sheet_name='Stations_Mean',skiprows=1)
    dataOBS_Mean = pd.read_excel(pathOBS ,sheet_name='Stations_Mean',skiprows=1)
    dataHACH_Mean = pd.read_excel(pathHACH ,sheet_name='turbidityHACH',skiprows=1)
    
    data_Trios_CV = pd.read_excel(path_Trios, sheet_name='TriosStats', skiprows=1)
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
    rho_IMG = {}    
    #longitudes = [645, 859]
    
    rho_Trios[645] = data_Trios_Mean['645.0']
    rho_Trios[860] = data_Trios_Mean['860.0']
    
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
        T.fill(np.nan)
        # Recorremos cada valor de rho[645]:
        for st in range(len(stations)):
            
            r_645 = rho[645][st]
            
            if r_645<0.05:
                r = rho[645][st]
                T[st] = (A[645]*r)/(1-r/C[645])
                
            elif r_645>0.07:
                r = rho[860][st]
                T[st] = (A[860]*r)/(1-r/C[860])
                
            elif 0.05<r_645<0.07:
                # (Caso intermedio)
                
                T_645 = (A[645]*rho[645][st])/(1-rho[645][st]/C[645])
                T_860 = (A[860]*rho[860][st])/(1-rho[860][st]/C[860])
                
                # Peso:
                w = 50*r_645 - 2.5
                T[st] = (1-w)*T_645 + w*T_860
    
            else:
                T[st] = None
                continue
        
        return T
    
    # Turbidez usando el algoritmo:
    T_Trios = Algoritmo(stations,rho_Trios)
    T_IMG = Algoritmo(IMGstation,rho_IMG)


    # Antigua forma de calcular la turbidez (MAL):

    #T_Trios_viejo = {}
    #T_IMG_viejo = {}
    
    #for l in longitudes:
    #    T_Trios_viejo[l] = (A[l]*rho_Trios[l])/(1-rho_Trios[l]/C[l])
    #    T_IMG_viejo[l] = (A[l]*rho_IMG[l])/(1-rho_IMG[l]/C[l])
    
    ############################################################
    
    # Filtramos los que tengan CV>CV_threshold:
    
    def Filtrar(stations, T, CV_threshold):
        for st in stations:
            if data_Trios_CV['MaxCV400:900 [%]'][st]>CV_threshold:
                T[st] = None
        return T

    Filtrar(stations, T_Trios, CV_threshold)
    Filtrar(IMGstation, T_IMG, CV_threshold)
    
    ############################################################
                
    # Para una transición suave de colores entre las curvas:
    N_curvas = 3    # cantidad de curvas
    cmap = plt.cm.summer #coolwarm, viridis, plasma, inferno, magma, cividis
    rcParams['axes.prop_cycle'] = cycler(color=cmap(np.linspace(0, 1, N_curvas)))

    # Gráfico (turbidez - estaciones):
    
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
    #IMG_shapes = ['o', 's', '^', '*', '+', 'x', '2']
    Algoritmos = ['GW94-SWIR12', 'GW94-SWIR13', 'GW94-SWIR23', 'PCA-SWIR12', 'PCA-SWIR13', 'PCA-SWIR23', 'PCA-SWIR123']
    
    plt.plot(stations,T_Trios, '-o', label=r'Trios')
    plt.plot(IMGstation,T_IMG, 'o', label=r'IMG')
    
    plt.plot(stations,ntu_ECO, '-o', color='orange', label=r'ECO FLNTU')
    plt.plot(stations,ntu_OBS, '-o', color='blue', label=r'OBS501 (2016) [SS]')
    plt.plot(stations,ntu_HACH, '-o', color='red', label=r'HACH')
    
    plt.legend(loc='best', fontsize=LegendSize)
#    plt.legend(loc=(1.04,0), fontsize=LegendSize)
    plt.title(r'%s'%Campaign, fontsize=TitleSize)
    plt.xlabel(r'Estación (STxx)', fontsize=AxisLabelSize)
    plt.ylabel(r'Turbidez (NTU)', fontsize=AxisLabelSize)
    plt.grid(axis='both', color='k', linestyle='dashed', linewidth=2, alpha=0.2)
    plt.show()
    
    if Linux:
        plt.savefig(path + '/' + '[%s] Trios.png'%Campaign)

#%% HACH vs Trios
    
    N_curvas = 3    # cantidad de curvas
    cmap = plt.cm.summer #coolwarm, viridis, plasma, inferno, magma, cividis
    rcParams['axes.prop_cycle'] = cycler(color=cmap(np.linspace(0, 1, N_curvas)))
    
    def lineal(x, a, b):
        return a*x+ b
    
    parametros_iniciales = [1,0]
    
    def Ajustar(x,y):    
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
    
    x = np.linspace(0, 65, 10)
    
    plt.plot(x, x, '--k', label=r'$y=x$')
    
    #[a, b] = Ajustar(ntu_HACH,T[l])
        
    plt.plot(ntu_HACH, T_Trios, 'o', label=r'Trios')
    plt.plot(ntu_HACH[IMGstation], T_IMG, 'o', label=r'IMG')
      
    #plt.legend(loc=(1.04,0), fontsize=LegendSize)
    plt.title(r'%s'%Campaign, fontsize=TitleSize)
    plt.xlabel(r'HACH (NTU)', fontsize=AxisLabelSize)
    plt.ylabel(r'Trios (NTU)', fontsize=AxisLabelSize)
    plt.grid(axis='both', color='k', linestyle='dashed', linewidth=2, alpha=0.2)
    plt.show()
    
    if Linux:
        plt.savefig(path + '/' + '[%s] HACH_vs_Trios.png'%Campaign)
