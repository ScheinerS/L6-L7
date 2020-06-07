
import sys
import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
#from scipy.odr import Model,RealData,ODR
#import datetime as dt
import matplotlib.dates as md

path = os.path.dirname(os.path.realpath('__file__'))
sys.path.append(path)

TitleSize = 15
AxisLabelSize = 12
LegendSize = 12
NumberSize = 12

plt.close('all')

if os.name == 'posix':
    Linux = True

plt.rc('text', usetex=False)
plt.rc('font', family='serif')

campaign = 'RdP_20191217_Muelle'

pathECO_Continuous= '/home/santiago/Documents/L6-L7/FLNTU/Base de datos/Datos/regions/RdP/RdP_20191217_Muelle/ECO_FLNTU/RdP_20191217_cleaned.xlsx'

#%%

# Módulo para remover los outliers del ECO. La idea es mandar esto al ECO Cleaner, después.
# Leemos el archivo YA LIMPIADO del ECO:

# Hay que convertir todo, tal como hicimos en el otro archivo...
dataECO_Continuous = pd.read_excel(pathECO_Continuous)

time_ECO_Continuous = dataECO_Continuous['timestamp']
time_ECO_Continuous = pd.to_datetime(time_ECO_Continuous)

ntu_ECO_Continuous_SIN_LIMPIAR = dataECO_Continuous['turbidity (NTU)']
ntu_ECO_Continuous = ntu_ECO_Continuous_SIN_LIMPIAR.copy()

Q1 = ntu_ECO_Continuous.quantile(0.25)
Q3 = ntu_ECO_Continuous.quantile(0.75)
IQR = Q3 - Q1
outliers = (ntu_ECO_Continuous < (Q1 - 1.5 * IQR)) | (ntu_ECO_Continuous > (Q3 + 1.5 * IQR))
ntu_ECO_Continuous[outliers] = np.nan

#%%
# Borrar este bloque cuando todo funcione:
plt.figure()

plt.plot(time_ECO_Continuous, ntu_ECO_Continuous_SIN_LIMPIAR, label=r'Original', color='orange')
plt.plot(time_ECO_Continuous, ntu_ECO_Continuous, label=r'Sin outliers', color='green')

plt.legend(loc='best', fontsize=LegendSize)
plt.title(r'ECO (2019-12-17 - Muelle)', fontsize=TitleSize)
plt.xlabel(r'UTC Time', fontsize=AxisLabelSize)
plt.ylabel(r'ECO (NTU), OBS (FNU)', fontsize=AxisLabelSize)
plt.ylim(0,200)
plt.xticks(rotation=25)
ax=plt.gca()
xfmt = md.DateFormatter('%H:%M')
#xfmt = md.DateFormatter('%Y-%m-%d %H:%M:%S')
ax.xaxis.set_major_formatter(xfmt)

# Anotaciones en el gráfico:
#plt.arrow(20, 0, 10, 10)
#plt.annotate(s, (x,y))     # s: anotación, (x,y): coordenadas

plt.locator_params(axis='y', nbins=8)
plt.grid(axis='both', color='k', linestyle='dashed', linewidth=2, alpha=0.2)
plt.show()

if Linux:
    plt.savefig(path + '/' + campaign + '_Continuous[sin_outliers].png')