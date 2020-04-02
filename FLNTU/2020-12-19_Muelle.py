#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Comparamos las curvas de turbidez con los de otros instrumentos.

"""

import sys
import os
import pandas as pd
#import numpy as np
import matplotlib.pyplot as plt

path = os.path.dirname(os.path.realpath('__file__'))
sys.path.append(path)