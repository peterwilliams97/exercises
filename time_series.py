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
    
References
    http://techguyinmidtown.com/2009/02/16/pythonic-data-analysis-with-maskedarray-and-timeseries/
    http://www.dtreg.com/TimeSeries.htm?gclid=CPrboZmH9qICFYgvpAodFxCZjA
    http://faculty.ksu.edu.sa/hisham/Documents/Students/a_PHCL/NLREG.pdf *

Created on 16/07/2010

@author: peter
"""
from __future__ import division
import  copy as CP, numpy as NP, scipy as SP, pylab as PL, random, time, optparse, os, csv, run_weka


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
        
        !@#$ This is hard with numpy arrays. Use python lists
    """
    trimming_missing_values = True
    if trimming_missing_values:
        def trimMissingValues(vector):
            out_vector = NP.zeros(vector.shape[0])
            num_missing = sum([1 if vector[i] < 0 else 0 for i in range(vector.shape[0])])
            i = num_missing
            for j in range(vector.shape[0]):
                if vector[j] >= 0:
                    out_vector[i] = vector[j]
                    i = i + 1
            print out_vector
            return out_vector
        
        print 'time_series.shape', time_series.shape
        num_rows = time_series.shape[1] - max_lag 
        trimmed_num_rows = sum([1 if time_series[1,i+max_lag] >= 0 else 0 for i in range(num_rows)])
        assert(trimmed_num_rows >= 1)
        regression_matrix = NP.zeros((trimmed_num_rows, 2*max_lag + 1))
        i = 0
        for j in range(trimmed_num_rows):
            if time_series[1,j+max_lag] >= 0:
                regression_matrix[i,0:max_lag] = trimMissingValues(time_series[0,j:j+max_lag]) 
                regression_matrix[i,max_lag:2*max_lag] = trimMissingValues(time_series[1,j:j+max_lag])
                regression_matrix[i,2*max_lag] = time_series[1,j+max_lag]
                i = i + 1
    else:    
        print 'time_series.shape', time_series.shape
        num_rows = time_series.shape[1] - max_lag 
        assert(num_rows >= 1)
        regression_matrix = NP.zeros((num_rows, 2*max_lag + 1))
        for i in range(num_rows):
            regression_matrix[i,0:max_lag] = time_series[0,i:i+max_lag] 
            regression_matrix[i,max_lag:2*max_lag+1] = time_series[1,i:i+max_lag+1] 
    return regression_matrix

def timeSeriesToMatrixCsv(regression_matrix_csv, time_series, max_lag):
    """ Convert a 2 row time series into a 
    regression matrix """
    regression_matrix = timeSeriesToMatrixArray(time_series, max_lag)
    header_x = ['x[%0d]' % i for i in range(-max_lag,0)]
    header_y = ['y[%0d]' % i for i in range(-max_lag,1)]
    header = header_x + header_y
    csv.writeCsv(regression_matrix_csv, list(regression_matrix), header)
    
def removeOutiers(vector, fraction_to_keep):
    N, bins = NP.histogram(vector, 10)
    print 'len(N)', len(N)
    print 'len(bins)', len(bins)
    for i in range(len(N)):
        print N[i], 'in', (bins[i],bins[i+1]), bins[i+1]-bins[i]
    exit()
        
def getMean(sequence):
    n = len(sequence)
    return sum(sequence)/n if n > 0 else 0

def filterDaysOfWeek(vector, days_to_keep):
    return NP.transpose(NP.array([vector[i] if i % 7 in days_to_keep else -1 for i in range((len(vector)//7)*7)]))
  
def getDaysOfWeekToKeep(vector):
    """ Returns days in week to keep """
    average_for_day = []  
    for day in range(7):
        day_vector = [vector[i] for i in range(day, (len(vector)//7)*7, 7)]
        average_for_day.append(getMean(day_vector))
    median_day = sorted(average_for_day)[3]
    return [day for day in range(7) if average_for_day[day] >= median_day *0.2]
                   
def removeOutlierDaysOfWeek(vector):
    days_to_keep = getDaysOfWeekToKeep(vector)
    return filterDaysOfWeek(vector, days_to_keep)
           
def getAutoCorrelation(vector, max_lag):
    """ Returns auto-correlation of vector for range 0..max_lag-1 """
    comp_len = vector.shape[0] - max_lag
    return NP.array([NP.correlate(vector[0:comp_len], vector[i:comp_len+i]) for i in range(max_lag)])    
    
def findAutoCorrelations(time_series_csv, max_lag, fraction_training):
    """ Run auto-correlations independently 2 column time series 
        by converting into a regression with max_lag x and y lags
        per instance 
        fraction_training is the fraction of sample used for training
    """  
    base_name = os.path.splitext(time_series_csv)[0]
    auto_correlation_matrix_csv = base_name + '.autocorrelation.csv'
    time_series_data,header = csv.readCsvFloat2(time_series_csv, True)
    number_training = int(float(len(time_series_data))*fraction_training)
    print 'number_training', number_training, 'fraction_training', fraction_training,'len(time_series_data)',len(time_series_data)
    assert(number_training > max_lag)
    time_series = NP.transpose(NP.array(time_series_data))
    days_downloads = getDaysOfWeekToKeep(time_series[0,:number_training])
    days_purchases = getDaysOfWeekToKeep(time_series[1,:number_training])
    print days_downloads
    print days_purchases
    exit()
    removeOutlierDaysOfWeek(time_series[1,:number_training])
    removeOutiers(time_series[1,:number_training], 0.8)
    downloads = time_series[0,:number_training]
    purchases = time_series[1,:number_training]
    #auto_correlations = [getAutoCorrelation(time_series[i,:number_training], max_lag) for i in range(time_series.shape[2])]
    #return (getAutoCorrelation(downloads, max_lag),getAutoCorrelation(purchases, max_lag))
    auto_correlation_data = NP.hstack([getAutoCorrelation(downloads, max_lag),getAutoCorrelation(purchases, max_lag)])
    csv.writeCsv(auto_correlation_matrix_csv, list(auto_correlation_data), header)
    
def runWekaOnTimeSeries(time_series_csv, max_lag, fraction_training):
    """ Run Weka training a 2 column time series 
        by converting into a regression with max_lag x and y lags
        per instance 
        fraction_training is the fraction of sample used for training
    """  
    base_name = os.path.splitext(time_series_csv)[0]
    regression_matrix_csv = base_name + '.regression.csv'
    results_filename = base_name + '.results' 
    model_filename = base_name + '.model' 
    predictions_filename =  base_name + '.predict'
    test_filename = base_name + '.test.csv'
    evaluation_filename = base_name + '.evaluation.csv'
    
    time_series_data,_ = csv.readCsvFloat2(time_series_csv, True)
    number_training = (int(float(len(time_series_data))*fraction_training)//7)*7

    print 'number_training', number_training, 'fraction_training', fraction_training,'len(time_series_data)',len(time_series_data)
    assert(number_training > max_lag)
    
    training_time_series = NP.transpose(NP.array(time_series_data[:number_training]))
    print '1: training_time_series.shape', training_time_series.shape
    
    if True:
        days_downloads = getDaysOfWeekToKeep(training_time_series[0,:])
        days_purchases = getDaysOfWeekToKeep(training_time_series[1,:])
        training_time_series = NP.vstack([filterDaysOfWeek(training_time_series[0,:], days_downloads),
         filterDaysOfWeek(training_time_series[1,:], days_purchases)])
        print '2: training_time_series.shape', training_time_series.shape
    
    if True:
    
        timeSeriesToMatrixCsv(regression_matrix_csv, training_time_series, max_lag)
        run_weka.runMLPTrain(regression_matrix_csv, results_filename, model_filename, True)
    
    print 'number_training, training_time_series.shape[1]', number_training, training_time_series.shape[1]
    number_training_x = number_training #- 5
    
    prediction_data = CP.deepcopy(time_series_data)
    prediction_data_downloads = [[row[0],0] for row in prediction_data]

    for i in range(number_training_x, len(prediction_data)):
        if i%7 in days_purchases:
            prediction_array = NP.transpose(NP.array(prediction_data[i-max_lag:i+1]))
            timeSeriesToMatrixCsv(test_filename, prediction_array, max_lag)
            run_weka.runMLPPredict(test_filename, model_filename, predictions_filename)
            prediction_list = run_weka.getPredictionsRegression(predictions_filename)
            print 'predictions', prediction_list
            prediction = prediction_list[0]['predicted']
            if False:
                prediction_array_downloads = NP.transpose(NP.array(prediction_data_downloads[i-max_lag:i+1]))
                timeSeriesToMatrixCsv(test_filename, prediction_array_downloads, max_lag)
                run_weka.runMLPPredict(test_filename, model_filename, predictions_filename)
                prediction_list_downloads = run_weka.getPredictionsRegression(predictions_filename)
                print 'predictions_downloads', prediction_list_downloads
                prediction_downloads = prediction_list[0]['predicted']
        else:
            prediction = -1
            prediction_downloads = -1
        prediction_data[i][1] = prediction
        #prediction_data[i] = [prediction_data[i][0], prediction, prediction_downloads]
       
          
    evaluation_data = []
    for i in range(len(prediction_data)-number_training_x):
        if i%7 in days_purchases:
            row = [0]*5
            for j in [0,1]:
                row[j] = time_series_data[number_training_x+i][j]
            row[2] = prediction_data[number_training_x+i][1] 
            row[3] = abs(row[2]-row[1])
            row[4] = row[3]/abs(row[2]+row[1]) if abs(row[2]+row[1]) else row[3]
            evaluation_data.append([number_training_x+i]+row)
     
    evaluation_header = ['i', 'x', 'y_actual', 'y_predicted', 'abs_error', 'normalized_error']
    
    csv.writeCsv(evaluation_filename, evaluation_data, evaluation_header)
   
def showArray(a):
    """ Display a numpy array """
    print 'shape', a.shape
    print a
    print '--------------------'
         
def test0():
    x = NP.zeros((1))
    print x
    x = NP.zeros((3,4))
    showArray(x)
    x = NP.arange(12)
    showArray(x)
    x.shape = (2,6)
    showArray(x)
    x.shape = (3,4)
    showArray(x)
    x.shape = (4,3)
    x[2] = NP.zeros((1,3))
    showArray(x)
        
def test1():
    timeSeriesToMatrixCsv(r'\dev\exercises\time_series.csv', r'\dev\exercises\regression_matrix.csv', 40)


def processCommandLine():
    """Process the command line options using 'optparse'"""
    usage = "usage: %prog [options] arg"
    parser = optparse.OptionParser(usage)
    parser.add_option('--daysPerSample', type='int', default=7,
                      help='Number of days to include in each sample')
    parser.add_option('--sampleUniqueDays', type='int', default=2,
                      help='Number of non-overlapping days in sample') 
    parser.add_option('--maxLag', type='int', default=28,
                      help='Number of lags to use for each training instance') 
    parser.add_option('--trainingFraction', type='float', default=0.8,
                      help='Fraction of data to use for training') 
    
    (options, args) = parser.parse_args() 
    
    if len(args) != 1:
        parser.error("incorrect number of arguments")
    filename = args[0]
    
    print '         filename:', filename
    print '          max lag:', options.maxLag
    print 'training fraction:', options.trainingFraction
        
    runWekaOnTimeSeries(filename, options.maxLag, options.trainingFraction)
            
if __name__ == '__main__':
    if True:
        test0()
    if False:
        test1()
    if False:
        max_lag = 40
        runWekaOnTimeSeries(r'\dev\exercises\time_series.csv', max_lag, 0.8)
    if False:
        processCommandLine()