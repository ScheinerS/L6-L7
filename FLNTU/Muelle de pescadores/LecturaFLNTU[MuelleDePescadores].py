# -*- coding: utf-8 -*-
"""
Este programa lee los archivos del FLNTU.

Última actualización: 24/10/2019.
"""

import sys
import os
import pandas as pd
#import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as md
import dateutil
#import glob

# Ver https://matplotlib.org/3.1.1/gallery/text_labels_and_annotations/date.html

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

#files = glob.glob(path + '/*.csv') # Identifica la cantidad de archivos que se quieren leer.

#tabla = pd.DataFrame()  # DataFrame donde vamos a guardar los datos de hach, ntu y fl.



#%%

filename = 'RDP_20191217'

file = path + '/' + filename + '.xlsx'

data = pd.read_excel(file)

#%%
# De la hoja de caracterización del FLNTU:

DC = 50 # counts
SF_NTU = 0.2438 # NTU/counts
SF_FL = 0.0607 # CHL/counts

ntu = SF_NTU * (data['ntu_counts'] - DC)
fl = SF_FL * (data['fl_counts'] - DC)

#%%
###########################################
# Este bloque es para graficar en función del tiempo, pero no funciona bien y lo dejé. Creo que va a ser mejor integrarlo a la base de datos directamente y graficar desde ahí, pero eso quedará para más adelante.
###########################################

timestrings = data['time']

times = [dateutil.parser.parse(s) for s in timestrings]




#%%
# Gráfico:

plt.figure()

plt.xticks( rotation= 00 )
#xfmt = md.DateFormatter('%H:%M:%S')
#ax=plt.gca()
#ax.xaxis.set_major_formatter(xfmt)



plt.plot( ntu, color='orange', label=r'NTU')
plt.plot(fl, color='green', label=r'FL')

plt.legend(loc='best', fontsize=LegendSize)
plt.title(r'ECO FLNTU (17 DIC 2019)', fontsize=TitleSize)
plt.xlabel(r'N\'umero de medici\'on', fontsize=AxisLabelSize)
plt.ylabel(r'ECO-FLNTU (Counts)', fontsize=AxisLabelSize)
plt.grid(axis='both', color='k', linestyle='dashed', linewidth=2, alpha=0.2)
plt.show()

if Linux:
    plt.savefig(path + '/ECO FLNTU.png')

