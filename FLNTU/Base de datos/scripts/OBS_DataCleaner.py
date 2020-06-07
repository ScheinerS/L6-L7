# -*- coding: utf-8 -*-
"""
Este módulo elimina los datos correspondientes a los momentos
en que el OBS estuvo fuera del agua, que deben especificarse
de antemano en el archivo IN_OUT.
"""

import sys
import os
import pandas as pd
import numpy as np
#import matplotlib.pyplot as plt
import datetime
#import glob
#from scipy.optimize import curve_fit
#from scipy.odr import Model,RealData,ODR

path = os.path.dirname(os.path.realpath('__file__'))
sys.path.append(path)

#%%

def clean(pathCampaign):

#    pathCampaign = '/home/gossn/Dropbox/Documents/L6y7_Scheiner_Santamaria/Datos/regions/RdP/RdP_20191217_Muelle'

    filename =      pathCampaign.split('/')[-1 ]
    filename = '_'.join(filename.split('_')[:-1])

    print('Cleaning OBS501 file...')
    

    Save_Excel = True # Para guardar en formato '.xlsx'
    Save_CSV = False # Para guardar en formato '.csv'
    
    #data = {}   # Diccionario con los DataFrames de cada archivo. 
    
    # Lectura de los archivos del FLNTU:
    file = pathCampaign + '/campbellContinuous/' + 'CR800_I2016.dat'
    
    data = pd.DataFrame()
    data = pd.read_csv(file, delimiter=",", skiprows=[0]) 
    data = data.drop([0, 1])
    
    #%%
    date = pathCampaign.split('_')[1]
    date_year = date[0:4]
    date_month = date[4:6]
    date_day = date[6:8]
    date = date_year + '-' + date_month + '-' + date_day
    
    path_IN_OUT = '/home/santiago/Documents/L6-L7/FLNTU/Base de datos/Datos/regions/RdP/RdP_20191217_Muelle/ECO_FLNTU/ECO_FLNTU_IN_OUT'
    IN_OUT = pd.read_csv(path_IN_OUT, sep='\t')
    #date = IN_OUT[]
    
    for i in range(len(IN_OUT)):
        # Bloques que hay que eliminar:
        start_remove = pd.to_datetime(date + ' ' + IN_OUT['OUT'].at[i])
        end_remove = pd.to_datetime(date + ' ' + IN_OUT['IN'].at[i])
        
        print('Removing data:\n', start_remove,'\t-->\t',end_remove)
        
        count = 0
        for t in range(2,len(data)):
            timestamp = pd.to_datetime(data.at[t,'TIMESTAMP'])
            if (timestamp>start_remove and timestamp<end_remove):
                data.at[t] = np.nan   # Elimina toda la línea.
                count += 1
        print('Removed lines:',count)
    #%%
    # Guardamos los datos:

    new_filename = filename + '_cleaned' 
    
    if Save_Excel:
        print('Saving as "%s"'%(new_filename + '.xlsx'))
        data.to_excel(pathCampaign + '/campbellContinuous/' + new_filename + '.xlsx')
         
    if Save_CSV:
        print('Saving as "%s"'%(new_filename + '.csv'))
        data.to_csv(pathCampaign + '//' + new_filename + '.csv')
    
    print('Done.')
#%%

if __name__ == "__main__":
    pathCampaign = '/home/santiago/Documents/L6-L7/FLNTU/Base de datos/Datos/regions/RdP/RdP_20191217_Muelle'
    clean(pathCampaign)
