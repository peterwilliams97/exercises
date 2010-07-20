"""
 Make plausible series

Input: 2 time series
    1. Download times
    2. Purchase times

Created on 18/07/2010

@author: peter
"""
from __future__ import division
import  copy as CP, numpy, scipy, csv, random, time, optparse, os

def makePurchaseLags(purchase_max_lag):  
    purchase_lag_fractions = [purchase_max_lag - i for i in range(purchase_max_lag)]
    total = sum(purchase_lag_fractions)
    purchase_lag_fractions = [x/total for x in purchase_lag_fractions]
    roulette_wheel = [{'days':i, 'weight':purchase_lag_fractions[i]} for i in range(purchase_max_lag)]
    roulette_wheel.sort(key = lambda x: -x['weight'])
    return roulette_wheel
                
def spinRouletteWheel():
    """    Find the roulette wheel winner
        roulette is a list of 2-tuples
            1st val is index
            2nd val is probability of the index
        Return an index with probability proportional to one specified
    """
    total = float(sum([x['weight'] for x in roulette_wheel]))
    v = total*random.random()
    base = 0.0
    for x in roulette_wheel:
        top = base + float(x['weight'])
        if v <= top:
            return x['days']
        base = top
        
    # If we get here something is wrong, so dump out state
    print '------------------- spinRouletteWheel -----------------'
    print 'v', v, 'total', total
    print 'roulette', roulette
    print 'ranges', 
    base = 0.0
    for x in roulette:
        print base,
        base = base + float(x['weight'])
    print base
    exit()
 
def randomPositiveIntegerVariate(mean): 
    while True:
        r = int(round(random.normalvariate(mean, mean)))
        if r >= 0:
            return r
            
def makeRandomList(number, mean): 
    sequence = [randomPositiveIntegerVariate(mean) for i in range(number)]
   
    excess = sum(sequence) - number * mean
    print 'number', number
    print 'mean', mean
    print 'excess', excess
    delta = 1 if excess >= 0 else -1
    i = 0
    while excess != 0:
        if sequence[i] - delta > 0:
            sequence[i] = sequence[i] - delta
            excess = excess - delta
        i = (i+1) % number
    assert(sum(sequence) == number * mean)
    return sequence
           
def makeTimeSeries(number_days, purchase_max_lag, mean_downloads_per_day, mean_purchases_per_download, mean_other_purchases):     
    downloads = makeRandomList(number_days, mean_downloads_per_day)
    purchases = makeRandomList(number_days, mean_other_purchases)
    makePurchaseLags()
    for day in range(number_days):
        purchases_per_day = int(round(downloads[day]*mean_purchases_per_download))
        for j in range(purchases_per_day):
            purchase_day = day + spinRouletteWheel()
            if purchase_day < len(purchases):
                purchases[purchase_day] = purchases[purchase_day] + 1
    for day in range(number_days):
        day_of_week = day % 7
        if day_of_week < 2:
            purchase_day = day + 2
            if purchase_day < len(purchases):
                purchases[purchase_day] = purchases[purchase_day] + purchases[day]
                purchases[day] = 0
    return (downloads, purchases)
            
def makeTimeSeriesCsv(filename, number_days, mean_downloads_per_day, mean_purchases_per_download, mean_other_purchases):
    (downloads, purchases) = makeTimeSeries(number_days, mean_downloads_per_day, mean_purchases_per_download, mean_other_purchases) 
    data = zip(downloads, purchases)
    csv.writeCsv(filename, data)           
    
def processCommandLine():
    """Process the command line options using 'optparse'"""
    usage = "usage: %prog [options] arg"
    parser = optparse.OptionParser(usage)
    parser.add_option('--numberDays', type='int', default=365,
                      help='Number of days in time series')
    parser.add_option('--downloadsPerDay', type='int', default=100,
                      help='Average number of downloads per day')
    parser.add_option('--purchasesPerDownload', type='float', default=0.5,
                      help='Average fraction of downloads leading to purchases') 
    parser.add_option('--otherPurchasesPerDay', type='int', default=50,
                      help='Number of purchases per day unrelated to downloads') 
      
    (options, args) = parser.parse_args() 
    
    if len(args) != 1:
        parser.error("incorrect number of arguments")
    filename = args[0]
    
    print '            filename:', filename
    print '          numberDays:', options.numberDays
    print '     downloadsPerDay:', options.downloadsPerDay
    print 'purchasesPerDownload:', options.purchasesPerDownload
    print 'otherPurchasesPerDay:', options.otherPurchasesPerDay
        
    makeTimeSeriesCsv(filename, 40, options.numberDays, options.downloadsPerDay, options.purchasesPerDownload, options.otherPurchasesPerDay)
            
if __name__ == '__main__':
    if False:
        test1()
    if False:
        max_lag = 40
        runWekaOnTimeSeries(r'\dev\exercises\time_series.csv', max_lag, 0.8)
    processCommandLine()