
import sys
import os
import matplotlib.pyplot as plt
from matplotlib import rcParams, cycler
#import csv
import numpy as np
import pandas as pd

path = os.path.dirname(os.path.realpath('__file__'))
sys.path.append(path)

TitleSize = 15
AxisLabelSize = 15
LegendSize = 12
NumberSize = 12

plt.close('all')

if os.name == 'posix':
    Linux = True

plt.rc('text', usetex=Linux)
plt.rc('font', family='serif')

# Para una transición suave de colores entre las curvas:
N_curvas = 3    # cantidad de curvas
cmap = plt.cm.summer #coolwarm, viridis, plasma, inferno, magma, cividis
rcParams['axes.prop_cycle'] = cycler(color=cmap(np.linspace(0, 1, N_curvas)))

path_datos = path + '/Datos/'

CV_threshold = 20

#%%
filenames = {'Trios': 'RdP_20191217_Trios_QC_RhowStd750_SatSensors.xlsx', 'ECO': 'RdP_20191217_ECO-FLNTU.xlsx', 'OBS': 'RdP_20191217_Campbell.xlsx', 'HACH': 'RdP_20191217.xlsx'}

filenames.keys()
# Paths:
path_Trios = path_datos + filenames['Trios']
pathECO = path_datos + filenames['ECO']
pathOBS = path_datos + filenames['OBS']
pathHACH = path_datos + filenames['HACH']

# Data:
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
#%%

rho = {}

#longitudes = [645, 859]

rho[645] = data_Trios_Mean['645.0']
rho[860] = data_Trios_Mean['860.0']



longitudes = [645, 860]
A = {645: 228.1, 860: 3078.9}
C = {645: 0.1641, 860: 0.2112}

T = {}

for l in longitudes:
    T[l] = (A[l]*rho[l])/(1-rho[l]/C[l])

# Filtramos los que tengan CV>30%:
for l in longitudes:
    for i in range(len(T[l])):
        if data_Trios_CV['MaxCV400:900 [%]'][i]>CV_threshold:
            T[l].at[i] = None


#%%
# Gráfico (turbidez - estaciones):

plt.figure()

stations = range(1,13)

for l in longitudes:
    plt.plot(stations,T[l], '-o', label=r'Trios ($\lambda = %d$ nm)'%l)

plt.plot(stations,ntu_ECO, '-o', color='orange', label=r'ECO FLNTU')
plt.plot(stations,ntu_OBS, '-o', color='blue', label=r'OBS501 (2016) [SS]')
plt.plot(stations,ntu_HACH, '-o', color='red', label=r'HACH')

plt.legend(loc='best', fontsize=LegendSize)
plt.title(r'', fontsize=TitleSize)
plt.xlabel(r'Estación (STxx)', fontsize=AxisLabelSize)
plt.ylabel(r'Turbidez (NTU)', fontsize=AxisLabelSize)
plt.grid(axis='both', color='k', linestyle='dashed', linewidth=2, alpha=0.2)
plt.show()

if Linux:
    plt.savefig(path + '/' + 'Trios.png')