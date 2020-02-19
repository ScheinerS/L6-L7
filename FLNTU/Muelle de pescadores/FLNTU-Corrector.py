# -*- coding: utf-8 -*-
"""
Corrector de errores de transferencia del ECO FLNTU.

    Este programa lee dos archivos del FLNTU correspondientes a la misma campaña (i.e. idénticos, pero transferidos por separado) y los compara, en búsqueda de errores. Cuando una fila no tiene el formato que se espera (siete columnas, cada una con el formato esperado), la elimina y toma el dato del otro archivo.

Para hacer más adelante:
    
    Hasta ahora, asumimos que no se repiten los datos con error en dos transferencias separadas, pero podría ocurrir. El próximo paso sería hacerlo con tres o más transferencias diferentes.
"""

import sys
import os
import pandas as pd
#import numpy as np
import matplotlib.pyplot as plt
#import glob
#from scipy.optimize import curve_fit
#from scipy.odr import Model,RealData,ODR

path = os.path.dirname(os.path.realpath('__file__'))
sys.path.append(path)



#%%

filename = 'RDP_20191217'

Save_Excel = True # Para guardar en formato '.xlsx'
Save_CSV = False # Para guardar en formato '.csv'

#%%

data = {}   # Diccionario con los DataFrames de cada archivo. 

# Lectura de los archivos del FLNTU:
fileA = path + '/' + filename + '(transferenciaA).xlsx'
fileB = path + '/' + filename + '(transferenciaB).xlsx'

try:
    data[fileA] = pd.read_excel(fileA, delimiter="\t", skiprows=1, header=None,usecols=range(0,7))
    data[fileB] = pd.read_excel(fileB, delimiter="\t", skiprows=1, header=None,usecols=range(0,7))
except:
    print('\nError de lectura\n')
    
data[fileA] = data[fileA].dropna()
data[fileB] = data[fileB].dropna()

# Nombramos las columnas relevantes de los archivos:

for f in [fileA, fileB]:
    
    data[f].rename(columns={0: 'date', 1: 'time', 3: 'ntu_counts', 5: 'fl_counts'}, inplace=True)

# Creo que 3 y 5 podrían tener los nombres invertidos. Revisar.


# No nos queda del todo claro qué son las columnas 2, 4 y 6. Darkcounts, pero no sabemos para qué sirven.

#%%

def check_date(date):
    try:
        date = date.split('/')
        if not len(date)==3:
            return False
        
        # La fecha está en el formato mm-dd-aaaa
        day = int(date[1])
        month = int(date[0])
        year = int(date[2])
        
    except:
        return False
            
    if day>0 and day<32:
        if month>0 and month<13:
            if year>18 and year<22: # Va a haber que cambiarlo en 2022.
                return True
            else:
                return False
        else:
            return False
    else:
        return False
    
#######################

def check_time(time):
    try:
        time = time.split(':')
        if not len(time)==3:
            return False
        
        hour = int(time[0])
        min = int(time[1])
        sec = int(time[2])
    except:
        return False
            
    if hour>=0 and hour<24:
        if min>=0 and min<60:
            if sec>=0 and sec<60:
                return True
            else:
                return False
        else:
            return False
    else:
        return False
   
#######################

def check_counts(counts):
    try:
        counts = int(counts)
    except:
        return False
    
    if counts>0 and counts<4131:
        return True
    else:
        return False

#######################

def check_all(L):
    # esta función verifica todas las columnas para la línea L
   
    a = check_date(L['date'])
    b = check_time(L['time'])
    c = check_counts(L['ntu_counts'])
    d = check_counts(L['fl_counts'])
    
    # Chequeamos que las otras columnas también sean enteros acotados entre 0 y 4130, para detectar otros errores:
    
    e = check_counts(L[2])
    f = check_counts(L[4])
    g = check_counts(L[6])
    
    if a and b and c and d and e and f and g:
        return True
    else:
        return False

#%%

# Armamos un archivo definitivo a partir del archivo A, y si hay un error, buscamos en el archivo B:

file = pd.DataFrame(columns=data[fileA].columns) # copiamos la estructura del archivo A.

replaced = 0
errors_A_and_B = 0

for i in range(len(data[fileA])):
    # Almacenamos temporalmente la fecha y hora asociada al índice 'i' en el archivo A:
    DATE = data[fileA].iloc[i]['date']
    TIME = data[fileA].iloc[i]['time']
    
    L_A = data[fileA].iloc[i]
    
    if check_all(L_A):
        file = file.append(L_A, ignore_index=True)
        #print(L)
    else:
        # buscamos la fila equivalente en el archivo B (el índice en A y B podría no coincidir, porque eliminamos las líneas dañadas de cada archivo):
        #L = data[fileB].loc[(data[fileB]['date'] == DATE) & (data[fileB]['time'] == TIME)]
        '''
        % Esto es una prueba que muestra que la línea (errónea en fileA y buena en fileB) da 'False' cuando se le aplica check_all, y debería reemplazarla. Todas las funciones que componen check_all dan False, así que hay algo mal en el formato. L_A y L_B son diferentes y deberían ser iguales. Series y DataFrame. ¿?¿?¿?¿?
        
        TIME = '12:42:06'
        L_a = data[fileA].loc[(data[fileA]['time'] == TIME)]
        L_b = data[fileB].loc[(data[fileB]['time'] == TIME)]
        '''
        L_B = data[fileB].loc[(data[fileB]['time'] == TIME)]
        
        if check_all(L_B):  # ESTO NO ESTÁ ANDANDO. Da falso para renglones que están sanos.
            file = file.append(L_B, ignore_index=True)
            replaced = replaced + 1
        else:
            errors_A_and_B = errors_A_and_B + 1
            print('L_A:\t', L_A)
            print('L_B:\t', L_B)

#print(file)

print('Líneas dañadas reemplazadas:', replaced)
print('No pudieron reemplazarse:', errors_A_and_B)

#%%

if Save_Excel:
    file.to_excel(filename + '.xlsx')

if Save_CSV:
    file.to_csv(filename + '.csv')
