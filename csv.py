'''
manipulate csv files
Clean advertisement detection trainging set file

Peter
16/05/2010
'''
import copy
from math import *
from operator import itemgetter

def validateMatrix(matrix):
    "Check that all rows in matrix and same length"
    assert(len(matrix) > 0)
    assert(len(matrix[0]) > 0)
    for i in range(1, len(matrix)):
        assert(len(matrix[i]) == len(matrix[0]))
  
def readCsvRaw(filename): 
    "Reads a CSV file into a 2d array"
    lines = file(filename).read().strip().split('\n')
    entries = [[e for e in l.strip().split(',')] for l in lines]
    print 'readCsvRaw', filename, len(entries), len(entries[0])
    validateMatrix(entries)
    return entries

def readCsvFloat(filename): 
    "Reads a CSV file into a 2d array of float"
    entries = readCsvRaw(filename)
    matrix = [[float(e) for e in row] for row in entries]
    return matrix    

def writeCsv(filename,matrix):
    "Writes a 2d array to a CSV file"
    file(filename, 'w').write('\n'.join(map(lambda row: ','.join(map(str,row)), matrix)) + '\n')  
    
def swapMatrixColumn(matrix, i, j):
    n = len(matrix[0])
    if i < 0: i = n + i
    if j < 0: j = n + j
    if i > j: i,j = j,i
    for v in matrix:
        x = v[i]
        for k in range(i+1, j+1):
            v[k-1] = v[k]
        v[j] = x
'''
 height: continuous. | possibly missing
   width: continuous.  | possibly missing
   aratio: continuous. | possibly missing
   local: 0,1.
   | 457 features from url terms, each of the form "url*term1+term2...";
   | for example:
   url*images+buttons: 0,1.
     ...
   | 495 features from origurl terms, in same form; for example:
   origurl*labyrinth: 0,1.
     ...
   | 472 features from ancurl terms, in same form; for example:
   ancurl*search+direct: 0,1.
     ...
   | 111 features from alt terms, in same form; for example:
   alt*your: 0,1.
     ...
   | 19 features from caption terms
   caption*and: 0,1.
     ...

'''        

def makeHeader():
    "Make a header row based on the above comments"
    h = ['' for i in range(1559)]
    h[0] = 'height'
    h[1] = 'width'
    h[2] = 'aratio'
    h[3] = 'local'
    n = 4
    def addRange(n, span, prefix):
        for i in range(span):
            h[n+i] = prefix + '%03d' % (i+1)
        print n, span, prefix, n+span    
        return n + span 
    n = addRange(n, 457, 'url')
    n = addRange(n, 495, 'org')
    n = addRange(n, 472, 'anc')
    n = addRange(n, 111, 'alt')
    n = addRange(n, 19,  'cap')
    assert(n == 1558)
    h[1558] = 'Advert'
    return h

def isMissingValue(e):
    "User defined function for detecting missing value"
    return e.strip() == '?'

def replaceMissingValues(matrix):
    "Replace missing values in a 2d matrix with average or mode"
    width = len(matrix[0])
    height = len(matrix)
    h = matrix[0]
    for i in range(width):
        num_missing = 0
        for v in matrix[1:]:
            if isMissingValue(v[i]):
                num_missing = num_missing +1
        if num_missing > 0:
            frac_missing = float(num_missing)/float(height)
            head = '"' + h[i] + '"'
            print 'column', '%3d'%i, '%3d'%num_missing, '%.2f'%frac_missing, '%8s'%head, 
            uniques = []
            for v in matrix[1:]:
                if not v[i] in uniques:
                    uniques.append(v[i])
            number_each = [0 for j in range(len(uniques))] 
            for j in range(len(uniques)):
                number_each[j] = 0        
                for v in matrix[1:]:
                    if uniques[j] == v[i]:
                        number_each[j] = number_each[j] + 1
            if len(uniques) <= 3:  # if there a few values then replace wih mode
                j = max(enumerate(number_each), key=itemgetter(1))[0]
                replacement = uniques[j]
                assert(not isMissingValue(v[i]))
            else:  # if there are many values then replace with average
                remaining = [float(v[i]) for v in matrix[1:] if not isMissingValue(v[i])]
                replacement = sum(remaining)/float(len(remaining))
            print 'replacement', replacement  
            for v in matrix[1:]: 
                if isMissingValue(v[i]):
                    v[i] = replacement          
                         
     
if __name__ == '__main__':
    raw_name = 'C:\\dev\\5047assigment1\\ad1.csv'
    headered_name = 'C:\\dev\\5047assigment1\\ad1_header.csv'
    headered_name_pp = 'C:\\dev\\5047assigment1\\ad1_header_pp.csv'
    header = makeHeader()
    data = readCsvRaw(raw_name)
    
    hdata = [header] + data
    assert(len(hdata)==len(data)+1)
    validateMatrix(hdata)

    #swapMatrixColumn(data, 3, -1)
    writeCsv(headered_name, hdata)
    h2data = readCsvRaw(headered_name)
    
    replaceMissingValues(hdata)
    writeCsv(headered_name_pp, hdata)
    
   