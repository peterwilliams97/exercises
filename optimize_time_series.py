"""
Create many time series, run several fitting algorithms on them and take best algorithm

Created on 20/07/2010

@author: peter
"""
from __future__ import division
import os, time_series, make_time_series

def makeTestPath(filename):
    return os.path.join(r'C:\dev\exercises', filename)

def makeTestFiles(create_files):
    """ Make a set of test files for evaluating time series prediction
        algorithms """
    number_days = 2 * 365
    downloads_per_day = 1000
    test_file_names = []
    file_number = 0
    params_list = []
    for purchases_per_download_pc in range(20, 81, 20):
        for other_purchase_ratio_pc in range(20, 201, 50):
            for purchase_max_lag in range(5, 26, 5):
                params_list.append((purchases_per_download_pc,other_purchase_ratio_pc,purchase_max_lag))
     
    print len(params_list), 'test files'    
        
    for purchases_per_download_pc,other_purchase_ratio_pc,purchase_max_lag in params_list:
        filename = 'time_series_purchases_%02d_other_%03d_lag_%02d.csv' \
            % (purchases_per_download_pc, other_purchase_ratio_pc, purchase_max_lag)
        purchases_per_download = purchases_per_download_pc/100.0
        other_purchase_ratio = other_purchase_ratio_pc/100.0
        if create_files:
            make_time_series.makeTimeSeriesCsv(makeTestPath(filename), purchase_max_lag, number_days, downloads_per_day, \
                          purchases_per_download, other_purchase_ratio * downloads_per_day)
        test_file_names.append(filename)
    return test_file_names
                
if __name__ == '__main__':
    create_files = True
    test_file_names = makeTestFiles(create_files)
    print len(test_file_names), 'test files'
    max_lag = 30
    fraction_training = 0.8
    for filename in test_file_names:
        time_series.runWekaOnTimeSeries(makeTestPath(filename), max_lag, fraction_training)