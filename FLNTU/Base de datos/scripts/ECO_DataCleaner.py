# -*- coding: utf-8 -*-
"""
Este módulo verifica los formatos de las filas del archivo '.raw' que entrega el ECO FLNTU y elimina las que no cumplan con los formatos correspondientes para cada columna. Los datos 'buenos' se guardan en otro archivo '.csv' o .xlsx', ya calibrados y con el timestamp correspondiente.
"""

import sys
import os
import pandas as pd
#import numpy as np
#import matplotlib.pyplot as plt
import datetime
#import glob
#from scipy.optimize import curve_fit
#from scipy.odr import Model,RealData,ODR

path = os.path.dirname(os.path.realpath('__file__'))
sys.path.append(path)

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
            if year>18 and year<datetime.date.today().year+1: # El año en que se está, más uno.
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
    
def check_wavelength_turbidity(l):    
    if l=='700':
        return True
    else:
        return False

#######################
                
def check_wavelength_chl_emission(l):    
    if l=='695':
        return True
    else:
        return False
    
#######################

def check_all(L):
    # esta función verifica todas las columnas para la línea L
   
    a = check_date(L['date'])
    b = check_time(L['time'])
    c = check_counts(L['turbidity_counts'])
    d = check_counts(L['chl_counts'])
    
    e = check_wavelength_chl_emission (L['check_wavelength_chl_emission'])
    f = check_wavelength_turbidity(L['wavelength_turbidity'])
    
    # Chequeamos que la otra columna también tenga enteros acotados entre 0 y 4130, para detectar otros errores:

    g = check_counts(L[6])
    
    
    if a and b and c and d and e and f and g:
        return True
    else:
        return False

def createTimestamp(date, time):
    # función que crea un timestamp en la fila L a partir de la fecha y hora.
    
    # date = '9/15/18'  # ejemplo
    # time = '20:15:45' # ejemplo
    
    date = date.split('/')
    
    # La fecha está inicialmente en el formato mm-dd-aa
    day = int(date[1])
    month = int(date[0])
    year = 2000 + int(date[2])
    
    date = datetime.date(year, month, day)
    
    # Pasamos la fecha a ISO 8601 (aaaa-mm-dd):
    date_ISO = date.isoformat()
    
    timestamp = date_ISO + ' ' + time
    
    return timestamp

def calibrate_ntu(ntu_counts):
    darkcounts = 50 # counts
    scaleFactor_NTU = 0.2438 # NTU/counts
    ntu = scaleFactor_NTU * (ntu_counts - darkcounts)
    return ntu

def calibrate_fl(fl_counts):
    darkcounts = 50 # counts
    scaleFactor_FL = 0.0607 # CHL/counts
    fl = scaleFactor_FL * (fl_counts - darkcounts)
    return fl
    
#%%

def clean(pathCampaign):

#    pathCampaign = '/home/gossn/Dropbox/Documents/L6y7_Scheiner_Santamaria/Datos/regions/RdP/RdP_20191217_Muelle'

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
                2: 'wavelength_chl_emission',
                3: 'chl_counts',
                4: 'wavelength_turbidity',
                5: 'turbidity_counts',
                6: 'cpu_temperature'
                }, inplace=True)    
    
    # Armamos un archivo definitivo a partir del archivo A, y si hay un error, buscamos en el archivo B:
    
    file = pd.DataFrame(columns=data[fileA].columns) # copiamos la estructura del archivo A.
    # Agregamos las columnas para el timestamp, y para las calibraciones de NTU y FL:
    file["timestamp"] = None
    file["turbidity (NTU)"] = None
    file["chl (ug/l)"] = None
    
    for i in range(len(data[fileA])):
        
        L_A = data[fileA].iloc[i]
         
        if check_all(L_A):
            file = file.append(L_A, ignore_index=True)
    
    print('Adding timestamps and calibration...\n')

    # Hacer el loop dos veces no es muy eficiente pero arregla problemas, así que por el momento, lo hacemos así:
    
    for i in range(len(data[fileA])):
        L_A = data[fileA].iloc[i]
        
        if check_all(L_A):
            #print(L_A)
            file.at[i,'timestamp'] = createTimestamp(L_A['date'], L_A['time'])
            file.at[i,'turbidity (NTU)'] = calibrate_ntu(int(L_A['turbidity_counts']))
            file.at[i,'chl (ug/l)'] = calibrate_fl(int(L_A['chl_counts']))
        

    new_filename = filename + '_cleaned' 
    
    if Save_Excel:
        print('Saving as "%s"'%(new_filename + '.xlsx'))
        file.to_excel(pathCampaign + '/ECO_FLNTU/' + new_filename + '.xlsx')

    if Save_CSV:
        print('Saving as "%s"'%(new_filename + '.csv'))
        file.to_csv(pathCampaign + '/ECO_FLNTU/' + new_filename + '.csv')

#clean(pathCampaign)
