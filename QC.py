#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri May 22 18:31:58 2020

@author: gossn
"""

import numpy as np

#%% outofRangeDetection
def outofRangeDetection(array,rmin=np.nan,rmax=np.nan):
    '''
    Parameters
    ----------
    array : NumPy array or masked array. Dim (N,) or (N,1).
        Input array.
    rmin : float, optional
        Minimum acceptable value. Values below will be flagged as 'out of range'. The default is np.nan (no threshold applied).
    rmax : TYPE, optional
        Maximum acceptable value. Values above will be flagged as 'out of range'. The default is np.nan (no threshold applied).

    Returns
    -------
    rangeFlag. NumPy array of booleans. Flag indicating values out of range.
    '''
    # Example
    array = np.array([np.nan,1000,2.4,1.5,2,300,4,5,6000])
    mask0 = np.array([0     ,0   ,0  ,0  ,0,0  ,0,0,1   ])
    array = np.ma.array(array,mask=mask0)
    rmin=0;rmax=30
    rangeFlag = outofRangeDetection(array,rmin=0,rmax=10)

    arrayVal   = np.ma.getdata(array)
    rangeFlag = np.zeros(arrayVal.shape,dtype=bool)
    if not np.isnan(rmin):
        rangeFlag = (rangeFlag)|(arrayVal<rmin)
    if not np.isnan(rmax):
        rangeFlag = (rangeFlag)|(arrayVal>rmax)
    return rangeFlag
#%% statsArray
def statsArray(array):
    '''
    Parameters
    ----------
    array : NumPy array or masked array. Dim (N,) or (N,1)
        Computes main statistics of unmasked elements of array.
    Returns
    -------
    stats, dictionary with statistics.

    '''
    # Example:
    # array = np.array([np.nan,1000,2.4,1.5,2,300,4,5,2,7,6000])
    # mask0 = np.array([0     ,0   ,0  ,0  ,0,0  ,0,0,0,0,1   ])
    # array = np.ma.array(array,mask=mask0)
    # stats = statsArray(array)
    
    arrayVal   = np.ma.getdata(array)
    mask = np.ma.getmask(array)
 
    valid = (~mask)&(~np.isnan(arrayVal)) 
    arrayValid = np.ma.getdata(array[valid])

    stats = {}

    stats['N']      = len(array)
    stats['Nvalid'] = len(arrayValid)

    stats['Mean']   = np.mean(arrayValid)
    stats['Std']    = np.std( arrayValid)
    stats['CV']     = stats['Std']/stats['Mean']

    # Compute quartiles 1,2,3: 
    for q,qfrac in zip([1,2,3],[0.25,0.50,0.75]):
        if len(arrayValid)>0:
            stats['Q' + str(q)] = np.quantile(arrayValid,qfrac)
        else:
            stats['Q' + str(q)] = np.nan

    stats['IQR']    = stats['Q3'] - stats['Q1']
    stats['sIQR']   = stats['IQR']/2
    stats['CV_R']   = (20/27)*(stats['IQR']/stats['Q2'])

    return stats
#%% outlierDetection
def outlierDetection(array,mode='iqr'):
    '''
    Parameters
    ----------
    array : NumPy array or masked array. Dim (N,) or (N,1)
    mode  : string, optional. Indicates the method to compute the presence of outliers. The default is 'iqr'.

    Returns
    -------
    outFlag. NumPy array of booleans. Flag indicating outliers. Does not include previously masked values.
    stats. Dictionary with statistics, computed over the non-masked and non-outlier values of the array.
    '''
    # Example
    # array = np.array([np.nan,100000,2.4,1.5,2,300,4,5,6000])
    # mask0 = np.array([0     ,0     ,0  ,0  ,0,0  ,0,0,1   ])
    # array = np.ma.array(array,mask=mask0)
    # outFlag,stats = outlierDetection(array,mode='s3vt')

    stats = statsArray(array)

    arrayVal   = np.ma.getdata(array)
    mask = np.ma.getmask(array)
    
    if mode == 'iqr':
        outFlag = (arrayVal<(stats['Q1']-1.5*stats['IQR']))|(arrayVal>(stats['Q3']+1.5*stats['IQR']))
    elif mode == 's3vt':
        outFlag = np.abs(arrayVal-stats['Mean']) > 1.5*stats['Std']
    elif mode == 's3vt-r':
        outFlag = np.abs(arrayVal-stats['Q2'  ]) > 10/9*stats['IQR']
    else:
        TypeError

    outFlag = (outFlag)&(~mask)
    stats = statsArray(np.ma.array(array,mask=(mask)|(outFlag)))

    return outFlag,stats
#%% qcArray
def qcArray(array,mode='default'):
    '''
    Parameters
    ----------
    array : NumPy array or masked array. Dim (N,) or (N,1)
    mode : string, optional. Decides which mode to apply. The default is 'default'.
        if mode == 'default':
            Reject negative values. No maximum threshold applied
            Uses S3VT-R mode to detect outliers

    Returns
    -------
    rangeFlag. NumPy array of booleans. Flag indicating values out of range.
    outFlag. NumPy array of booleans. Flag indicating outliers. Does not include previously masked values.
    stats. Dictionary with statistics, computed over the non-masked and non-outlier values of the array.
    '''
    # Example
    # array = np.array([np.nan,1000,2.4,1.5,2,300,4,5,6000,-10])
    # mask0 = np.array([0     ,0   ,0  ,0  ,0,0  ,0,0,1   ,0  ])
    # array = np.ma.array(array,mask=mask0)
    # rangeFlag,outFlag,stats = qcArray(array)

    if mode == 'default':
        '''
        Reject negative values. No maximum threshold applied
        Uses S3VT-R mode to detect outliers
        '''
        rmin=0; rmax=np.nan; mode='s3vt-r'

        rangeFlag = outofRangeDetection(array,rmin=rmin,rmax=rmax)
        array = np.ma.array(array,mask=np.ma.getmask(array)|rangeFlag)
    
        outFlag,stats = outlierDetection(array,mode=mode)
    
    return rangeFlag,outFlag,stats