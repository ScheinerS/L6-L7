# IMPORTO LIBRERÍAS PARA QUE FUNCIONE TODO. DESPUÉS HAY QUE SACARLAS:



import os
import sys
import pandas as pd
import openpyxl
import numpy as np
from datetime import timedelta


'''
En ppio NO anda la función para determinar el path absoluto del current file en Spyder =(, tal como se comenta en el siguiente thread:
https://github.com/spyder-ide/spyder/issues/3154

Por otro lado, habría que definir dos 'path0': uno que apunte al directorio donde ponen todos sus módulos caseros, y otro que apunte a los datos: los voy a llamar pathModules y path0 - este ultimo igual que antes
'''

# path0 = '/Users/Tele/Desktop/L6-L7/FLNTU/Base de datos'

#path0      = '/home/gossn/Dropbox/Documents/L6y7_Scheiner_Santamaria/Datos'
# pathModules = '/home/gossn/Dropbox/Documents/L6y7_Scheiner_Santamaria/scripts'

# SANTI: Creo que logré automatizar el reconocimiento de los paths (en mi máquina funciona):
path0 = os.path.dirname(os.path.realpath('__file__'))
pathModules = os.path.dirname(path0) + '/Datos'
    
sys.path.append(pathModules)

import ECO_DataCleaner as DC

campaign0 = 'RdP_20191217_Muelle'


#%%
def ECO2Stations(campaign0,path0):

#    campaign0 = 'RdP_20191217_Muelle'
#    path0      = '/home/gossn/Dropbox/Documents/L6y7_Scheiner_Santamaria/Datos'

    pathRegions   = pathModules + '/regions'

    region = campaign0.split('_')[0]
    date   = campaign0.split('_')[1]
    campaign = region + '_' + date
    pathCampaign  = pathRegions + '/' + region + '/' +  campaign0

    
    print('Processing ECO data for campaign: ' + campaign0)
    
    inputs = {}
    try:
        with open(pathCampaign + '/ECO_FLNTU/ECO_FLNTUProcessingInputs') as f0:
            for line in f0:
               (key, val) = line.split()
               inputs[key] = val.split(',')
               if len(inputs[key])==1:
                   inputs[key] = inputs[key][0]
        
        # Limpiamos el archivo del ECO:
        DC.clean(pathCampaign)
    except:
        print('No ECO Input file or no ECO measurements for this campaign!')
#        return
    if not os.path.isdir(pathCampaign + '/ECO_FLNTUProcessed/'):
        os.mkdir(pathCampaign + '/ECO_FLNTUProcessed/')
    
    # ECO Processing
    
    if not os.path.isdir(pathCampaign + '/ECO_FLNTU'):
        print("No ECO data available for this campaign!")
    else:
        filenameCs = campaign + '_cleaned.xlsx'
        
        # Read station IDs and Times
        stationInfo = pd.DataFrame()
        stationInfo = pd.read_excel(pathCampaign + '/' + campaign + '.xlsx',sheet_name='stationInfo',skiprows=1)
    
        ''' J: Creo que ya no es necesario remendar el siguiente bug ... de hecho me tira un DeprecationWarning...'''
        # Remendar bug openpyxl (borra formatos preestablecidos)
#        stationInfo['startTimeUTC'] = pd.to_datetime(stationInfo['startTimeUTC'],format= '%H:%M:%S' )
#        stationInfo['timeStampUTC'] = stationInfo['DateUTC'] + pd.to_timedelta(stationInfo['startTimeUTC']) + timedelta(hours=70*24*365.25-12)
        
        stationIDs   = stationInfo['StationID'   ].astype(object)
        stationTimes = stationInfo['timeStampUTC'].astype(object)
    
    
        pathXlsx = pathCampaign + '/ECO_FLNTUProcessed/' + campaign + '_ECO-FLNTU.xlsx'
        wb = openpyxl.Workbook()
        wb.save(pathXlsx)
        writer = pd.ExcelWriter(pathXlsx, engine = 'openpyxl')
        writer.book = wb
        del wb['Sheet']
    
        # Write to Excel: StationInfo
        sheetname = 'stationInfo'
        if sheetname in wb.sheetnames:
            wb.remove_sheet(wb.get_sheet_by_name(sheetname))
        stationInfo.set_index('StationID')
        stationInfo.to_excel(writer, index = False, sheet_name=sheetname,startrow = 1)

        # Initialize dictionary of dataFrame that will store data per station (all dataloggers)
        csStations = {}
        for stat in ['Mean','Std','CV']:
            csStations[stat] = pd.DataFrame(index=stationIDs)

        csCont = pd.DataFrame()
        '''
        La siguiente funcion no serviría en su caso xq optaron por el formato Excel, deberian usar read_excel:
        '''
#        csCont = pd.read_csv(pathCampaign + '/ECO_FLNTU/' + filenameCs, header = [1,2])

        csCont = pd.read_excel(pathCampaign + '/ECO_FLNTU/' + filenameCs, header = 0,index_col = 0)
        '''HASTA ACÁ REVISADO!!!! FIJENSE SI logran hacer andar el resto de la funcion. Va a haber partes que tengan sentido y otras que no. La esencia está, falta ver - de acá en adelante - que modificaciones son necesarias para obtener los valores por estación y suavizados a 1 minuto...'''

        # Change column names
        colNamesOld = list(csCont.columns)
        colNamesNew = []
        for cname in colNamesOld:
            if cname[1][:len('Unnamed')] == 'Unnamed':
                colNamesNew.append(cname[0])
            else:
                colNamesNew.append(cname[0] + '[' + cname[1].replace(' ','') + ']')
        csCont.columns = colNamesNew

        # campbell Times
        csCont = csCont.drop(csCont.index[[0]])    # Drop extra-headers
        csCont['TIMESTAMP[TS]'] = pd.to_datetime(csCont['TIMESTAMP[TS]'])-timedelta(hours=float(inputs['deltaUTC']))
        csContTime = csCont['TIMESTAMP[TS]']

        
        ##### DATOS POR ESTACION
        print('Data per station')
        
        # campbell collected data
        csContData = pd.DataFrame()
        others = [c for c in csCont.columns if (c.lower()[:2] == 'wd' or c.lower()[:12] == 'stationnames' or c.lower()[:7] == 'temp_cr')]
        csContData = csCont.drop(['TIMESTAMP[TS]','RECORD[RN]','BattV[Volts]'] + others, axis=1)
        csContData = csContData.apply(pd.to_numeric, errors='coerce')
        csMeasures = list(csContData.columns.values)
    
        csStStats  = {}
        for st in stationIDs:
            print('Processing station ' + str(st))
            timeSt = stationTimes[stationIDs==st][0]
            timeDeltaSt = abs(csContTime-timeSt)<pd.Timedelta(float(inputs['timeDeltaStationMin']), unit='m')
            if any(timeDeltaSt):
                csContSt = csContData.loc[timeDeltaSt,:]
                Q1 = csContSt.quantile(0.25)
                Q3 = csContSt.quantile(0.75)
                IQR = Q3 - Q1
                outliers = (csContSt < (Q1 - 1.5 * IQR)) |(csContSt > (Q3 + 1.5 * IQR))
                csContSt[outliers] = np.nan
                csStMed = csContSt.mean()
                csStStd = csContSt.std()
                csStCV  = csStStd/csStMed*100
                
                csStStats[st] = {'Mean': csStMed, 'Std': csStStd,'CV': csStCV}
                
        for stat in ['Mean','Std','CV']:
            csStationsFile = pd.DataFrame(columns=csMeasures)
            for st in stationIDs:
                try:
                    csStationsFile.loc[st]   = csStStats[st][stat]
                except:
                    csStationsFile.loc[st]   = pd.Series(index=csMeasures)
            csStationsFile.fillna('')
            csStationsFile.index.name = 'StationID'
            csStations[stat] = pd.concat([csStations[stat], csStationsFile], axis=1)
                                

            ##### DATOS CRUDOS
            sheetname = file[:-4]
            if sheetname in wb.sheetnames:
                wb.remove_sheet(wb.get_sheet_by_name(sheetname))
            csCont.to_excel(writer, index = False, sheet_name=sheetname)
            #adjustColWidth(wb.get_sheet_by_name(sheetname))
            writer.save()
            writer.close()
            
            ##### DATOS SUAVIZADOS A 'smoothWinMin' MIN
        '''
        J: Este if ya no tiene sentido...
        '''
            if file[0:6] != 'CR200X':
                csSmooth = pd.DataFrame()
                step = 0
                flag = True
                while flag:
                    timeWin = csCont['TIMESTAMP[TS]'].min() + timedelta(minutes=step*float(inputs['smoothWinMin']))
                    step+=1
                    flag = timeWin < csCont['TIMESTAMP[TS]'].max()
                    timeDeltaWin = abs(csContTime-timeWin)<pd.Timedelta(float(inputs['smoothWinMin'])/2, unit='m')
                    if any(timeDeltaWin):
                        csContWin = csContData.loc[timeDeltaWin,:]
                        Q1 = csContWin.quantile(0.25)
                        Q3 = csContWin.quantile(0.75)
                        IQR = Q3 - Q1
                        outliers = (csContWin < (Q1 - 1.5 * IQR)) |(csContWin > (Q3 + 1.5 * IQR))
                        csContWin[outliers] = np.nan
                        csWinMedia = csContWin.mean()
                        csWinStd = csContWin.std()
                        csWinCV = csWinStd/csWinMedia*100
                        
#                        csWinStats = [csWinMedia,csWinStd,csWinMedia]
                        
                        csMeasures = list(csContWin.columns.values)
                        for m in csMeasures:
                            csSmooth.loc[timeWin,m + 'Mean'  ] = csWinMedia[m]
                            csSmooth.loc[timeWin,m + 'Std'  ] = csWinStd[m]
                            csSmooth.loc[timeWin,m + 'CV'] = csWinCV[m]
                sheetname = file[:-4] + 'ContSmooth' + inputs['smoothWinMin'] + 'min'
                if sheetname in wb.sheetnames:
                    wb.remove_sheet(wb.get_sheet_by_name(sheetname))
                csSmooth.to_excel(writer, index = True, sheet_name=sheetname)
                #adjustColWidth(wb.get_sheet_by_name(sheetname))
                writer.save()
                writer.close()


        for stat in ['Mean','Std','CV']:
            csStations[stat] = csStations[stat].reindex(columns=sorted(csStations[stat].columns))
            sheetname = 'Stations' + '_' + stat
            if sheetname in wb.sheetnames:
                wb.remove_sheet(wb.get_sheet_by_name(sheetname))
            csStations[stat].to_excel(writer, index = True, sheet_name=sheetname, startrow=1)
            #adjustColWidth(wb.get_sheet_by_name(sheetname))
            writer.save()
            writer.close()

#%%

# CORRO LA FUNCIÓN. BORRAR ESTE BLOQUE CUANDO ESTÉ TERMINADO.

ECO2Stations(campaign0,path0)
