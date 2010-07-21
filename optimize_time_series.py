"""
Create many time series, run several fitting algorithms on them and take best algorithm

Created on 20/07/2010

@author: peter
"""
from __future__ import division
import os, time_series, make_time_series

def makeTestFiles():
    """ Make a set of test files for evaluating time series prediction
        algorithms """
    number_days = 2 * 365
    downloads_per_day = 1000
    test_file_names = []
    file_number = 0
    params_list = []
    for purchases_per_download_pc in range(20, 81, 20):
        for other_purchase_ratio_pc in range(20, 201, 50):
            for purchase_max_lag in range(5, 46, 10):
                params_list.append((purchases_per_download_pc,other_purchase_ratio_pc,purchase_max_lag))
     
    print len(params_list), 'test files'    
        
    for params in params_list:
        (purchases_per_download_pc,other_purchase_ratio_pc,purchase_max_lag) = params
        file_number = file_number + 1
        print 'file', file_number
        filename = 'time_series_purchases_%02d_other_%03d_lag_%02d.csv' \
            % (purchases_per_download_pc, other_purchase_ratio_pc, purchase_max_lag)
        purchases_per_download = purchases_per_download_pc/100.0
        other_purchase_ratio = other_purchase_ratio_pc/100.0
        path = os.path.join(r'C:\dev\exercises', filename)
        make_time_series.makeTimeSeriesCsv(path, purchase_max_lag, number_days, downloads_per_day, \
                          purchases_per_download, other_purchase_ratio)
        test_file_names.append(filename)
        print 'done', file_number
    return test_file_names
                
if __name__ == '__main__':
    test_file_names = makeTestFiles()
    print len(test_file_names), 'test files'