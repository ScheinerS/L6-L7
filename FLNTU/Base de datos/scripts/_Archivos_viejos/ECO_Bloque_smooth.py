#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Apr 22 16:20:41 2020

@author: gossn
"""

'''
El bloque va debajo del de datos crudos, que ya lo tienen.
Chequeen si entienden la logica del bloque (no está adaptado al ECO)
'''
##### DATOS SUAVIZADOS A 'smoothWinMin' MIN
if file[0:6] != 'CR200X': # ESTE IF ELIMINENLO! ES el q les eliminé sin querer.
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
        del wb[sheetname]
    csSmooth.to_excel(writer, index = True, sheet_name=sheetname)
    adjustColWidth(wb[sheetname])
    writer.save()
    writer.close()