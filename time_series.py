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
    
    http://techguyinmidtown.com/2009/02/16/pythonic-data-analysis-with-maskedarray-and-timeseries/

Created on 16/07/2010

@author: peter
"""
import numpy, scipy, csv, random, time, optparse, run_weka
from numpy import *

def processOptions():
    """Process the command line options using 'optparse'"""
    parser = optparse.OptionParser()
    parser.add_option('--daysPerSample', type='int', default=7,
                      help='Number of days to include in each sample')
    parser.add_option('--sampleUniqueDays', type='int', default=2,
                      help='Number of non-overlapping days in sample') 
    return options

def timeSeriesToMatrix(x_series, y_series, max_lag):
    """ Generate Weka format csv file for two time series.
        x_series and y_series which is believed to depend on x_series
        max_lag is number of lags in dependence
    """
    assert(len(x_series) == len(y_series))
    num_rows = len(x_series) - 1 - max_lag
    regression_matrix = list(num_rows)
    for i in range(num_rows):
        regression_matrix[i] = y_series[i+1:i+max_lag] + x_series[i+1:i+max_lag] + [y_series[i]]
    return regression_matrix

def timeSeriesToMatrixArray(time_series, max_lag):
    """ Generate Weka format csv file for two time series.
        x_series and y_series which is believed to depend on x_series
        max_lag is number of lags in dependence
    """
    num_rows = time_series.shape[1] - max_lag 
    regression_matrix = zeros((num_rows, 2*max_lag + 1))
    for i in range(num_rows):
        regression_matrix[i,0:max_lag] = time_series[0,i:i+max_lag] 
        regression_matrix[i,max_lag:2*max_lag+1] = time_series[1,i:i+max_lag+1] 
    return regression_matrix

def timeSeriesToMatrixCsv(time_series_csv, regression_matrix_csv, max_lag):
    """ Convert a 2 column time series into regression matrix """
    time_series = transpose(array(csv.readCsvFloat(time_series_csv)))
    regression_matrix = timeSeriesToMatrixArray(time_series, max_lag)
    header_x = ['x[%0d]' % i for i in range(-max_lag,0)]
    header_y = ['y[%0d]' % i for i in range(-max_lag,1)]
    header = header_x + header_y
    csv.writeCsv(regression_matrix_csv, list(regression_matrix), header)
  
def test0():
    x = zeros((1))
    print x
    x = zeros((3,4))
    showArray(x)
    x = arange(12)
    showArray(x)
    x.shape = (2,6)
    showArray(x)
    x.shape = (3,4)
    showArray(x)
    x.shape = (4,3)
    x[2] = zeros((1,3))
    showArray(x)
        
def test1():
    timeSeriesToMatrixCsv(r'\dev\exercises\time_series.csv', r'\dev\exercises\regression_matrix.csv', 40)

def showArray(a):
    print 'shape', a.shape
    print a
    print '--------------------'
        
if __name__ == '__main__':
    test1()
    