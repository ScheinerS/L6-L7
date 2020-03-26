# -*- coding: utf-8 -*-
"""
Este módulo verifica los formatos de las filas del archivo '.raw' que entrega el ECO FLNTU y elimina las que no cumplan con los formatos correspondientes para cada columna. Los datos 'buenos' se guardan en otro archivo '.csv' o .xlsx'.
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

def clean(pathCampaign):

#    pathCampaign = '/home/gossn/Dropbox/Documents/L6y7_Scheiner_Santamaria/Datos/regions/RdP/RdP_20191217_Muelle'

    '''
        J: filename: Qué les parece así?:
    '''

    filename =      pathCampaign.split('/')[-1 ]
    filename = '_'.join(filename.split('_')[:-1])

    print('Cleaning ECO file...')
    


    Save_Excel = True # Para guardar en formato '.xlsx'
    Save_CSV = False # Para guardar en formato '.csv'
    
    data = {}   # Diccionario con los DataFrames de cada archivo. 
    
    # Lectura de los archivos del FLNTU:
    fileA = pathCampaign + '/ECO_FLNTU/' + filename + '.raw'
    #fileB = pathCampaign + '/ECO_FLNTU/' + filename + '(1).raw'
    
    try:
        data[fileA] = pd.read_csv(fileA, delimiter="\t", skiprows=1, header=None,usecols=range(0,7))    # lee el formato '.raw' como '.csv' sin problemas.
        
        #data[fileB] = pd.read_csv(fileB, delimiter="\t", skiprows=1, header=None,usecols=range(0,7))
    except:
        print('\nError de lectura\n')
 
    data[fileA] = data[fileA].dropna()
    #data[fileB] = data[fileB].dropna()
    
    # Nombramos las columnas relevantes de los archivos:
    
    for f in [fileA]:#, fileB]:
        
        data[f].rename(columns={
                0: 'date',
                1: 'time',
                2: '2',
                3: 'ntu_counts',
                4: '4',
                5: 'fl_counts',
                6: '6'
                }, inplace=True)

    # Creo que 3 y 5 podrían tener los nombres invertidos. Revisar.
        
    # No nos queda del todo claro qué son las columnas 2, 4 y 6. Darkcounts, pero no sabemos para qué sirven.

    # Armamos un archivo definitivo a partir del archivo A, y si hay un error, buscamos en el archivo B:
    
    file = pd.DataFrame(columns=data[fileA].columns) # copiamos la estructura del archivo A.
    

    for i in range(len(data[fileA])):
        # Almacenamos temporalmente la fecha y hora asociada al índice 'i' en el archivo A:
        #DATE = data[fileA].iloc[i]['date']
        #TIME = data[fileA].iloc[i]['time']
        
        L_A = data[fileA].iloc[i]
        
        if check_all(L_A):
            file = file.append(L_A, ignore_index=True)
            #print(L)

    new_filename = filename + '_cleaned' 
    
    if Save_Excel:
        print('Saving as "%s"'%(new_filename + '.xlsx'))
        file.to_excel(pathCampaign + '/ECO_FLNTU/' + new_filename + '.xlsx')

    if Save_CSV:
        print('Saving as "%s"'%(new_filename + '.csv'))
        file.to_csv(pathCampaign + '/ECO_FLNTU/' + new_filename + '.csv')

#clean(pathCampaign)
#%%