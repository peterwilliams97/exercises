"""
Create many time series, run several fitting algorithms on them and take best algorithm

Created on 20/07/2010

@author: peter
"""
from __future__ import division
import time_series, make_time_series

def makeTestFiles():
    nummber_days = 2 * 365
    downloads_per_day = 1000
    test_filenames = {}
    for purchases_per_download_pc in range(20, 81, 20):
        for other_purchase_ratio_pc in range(20, 201, 30):
            for purchase_max_lag in range(5, 41, 5):
                filename = 'time_series_purchases=%03d_other=%03d_lag=%03d.csv' \
                    % (purchases_per_download_pc, other_purchase_ratio_pc, purchase_max_lag)
                purchases_per_download = purchases_per_download_pc/100.0
                other_purchase_ratio = other_purchase_ratio_pc/100.0
                make_time_series.makeTimeSeriesCsv(filename, purchases_per_download, number_days, downloads_per_day, \
                                  purchases_per_download, oother_purchase_ratio)
                test_filenames.append(filename)
                
if __name__ == '__main__':
    makeTestFiles()