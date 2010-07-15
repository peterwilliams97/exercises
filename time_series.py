"""
NARX (http://en.wikipedia.org/wiki/Nonlinear_autoregressive_exogenous_model)
using an MLP with GA unit selection

Input: 2 time series
    1. Download times
    2. Purchase times
    
Map inputs to  
    1. D[t] Downloads/period 
    2. P[t] Purchase/period    
    period can 1 day or 1 week, possibly a moving average

Mode
    P[n] = F(P[n-1],...,P[n-k],D[n-1],...,D[n-k]) 

Created on 16/07/2010

@author: peter
"""
import numpy, csv, random, time
from numpy import *

def timeSeriesToMatrix(x_series, y_series, max_lag):
    """ Generate Weka format csv file for two time series.
        x_series and y_series which is believed to depend on x_series
        max_lag is number of lags in depenedence
    """
    assert(len(x_series) == len(y_series))
    num_rows = len(x_series) - 1 - max_lag
    matrix = list(num_rows)
    for i in range(num_rows):
        matrix[i] = y_series[i+1:i+max_lag] + x_series[i+1:i+max_lag] + [y_series[i]]
    return matrix