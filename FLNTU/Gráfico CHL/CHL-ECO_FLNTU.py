#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Gráfico de absorción y emisión de la CHL-a para el ECO FLNTU.

Datos sacados de: https://omlc.org/spectra/PhotochemCAD/html/123.html.
"""


import sys
import os
import matplotlib.pyplot as plt
from matplotlib import rcParams, cycler
#import csv
#import numpy as np
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

#%%

data_abs = pd.read_csv('Absorption.csv', delimiter=',', skiprows=None)
data_fl = pd.read_csv('Fluorescence.csv', delimiter=',', skiprows=None)

plt.figure()

plt.plot(data_abs['wavelength'], data_abs['absorption']/max(data_abs['absorption']), label=r'Absorción')
plt.plot(data_fl['wavelength'], data_fl['fluorescence']/max(data_fl['fluorescence']), label=r'Fluorescencia')

plt.axvline(x=695, label='$\lambda = 695$', linestyle='--', color='black')
plt.axvline(x=470, label='$\lambda = 470$', linestyle='--', color='red')

plt.xlabel(r'$\lambda$', fontsize=AxisLabelSize)
plt.ylabel(r'(u. a.)', fontsize=AxisLabelSize)
plt.title(r'', fontsize=TitleSize)

plt.legend(loc='best', fontsize=LegendSize)
plt.grid(axis='both', color='k', linestyle='dashed', linewidth=2, alpha=0.2)
plt.show()

plt.savefig('CHL_abs_fl.png')
