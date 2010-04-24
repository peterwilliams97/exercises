'''

Runs a self-organizing map algorithm over some given input data and initial weights
for a user specified eta and weight updating functions 
    
Created on 24/04/2010

@author: peter
'''
import copy 
from math import *
    
def prod(v1, v2):
    "Returns dot product of vectors v1 and v2"
    return  sum(map(lambda x: x[0]*x[1], zip(v1,v2)))

def l2(v1, v2):
    "Returns Euclidean distance between vectors v1 and v2"
    return sqrt(sum(map(lambda x: (x[0]-x[1])**2, zip(v1,v2))))

def calcOutputs(w,i):
    "Calculates outputs o and distances d for inputs i and weights w"
    o = map(lambda x: prod(i,x), w)
    d = map(lambda x: l2(i,x), w)
    return (o, d)

def eta(t):
    "User defined eta function"
    return 0.6 / 2**int(t/4)

def updateFunc(wv, i, t):
    ''' User defined function for updating weights vector wv
        wv = old weights vector
        i = input vector
        t = iteration number 
        returns weights vector for iteration t+1
        Algorithm: w(t+1) = w(t) + eta(t)*(i-w(t))
    '''
    return map(lambda x: x[1] + eta(t)*(x[0]-x[1]), zip(i,wv))

def updateWeights(w, i, t, d):
    ''' Updates  weights in one iteration of the self-organizing map algorithm
        w = old weights, 2 vectors
        i = input vector
        t = iteration number
        d = distances between w's and i
        Algorithm: update the w that is closest to i
    '''
    w_new = copy.deepcopy(w)
    j = 0 if d[0] < d[1] else 1
    w_new[j] = updateFunc(w[j],i,t)
    return w_new

def a2csv(array):
    "Convert array of objects to a comma separated string"
    return ','.join(map(str, array))
    
def aa2csv(array2):
    "Convert array of array of objects to a comma separated string"
    return  ','.join(map(a2csv, array2))

def title(name, number):
    "Returns array of strings 'name[1]'...'name[<number>]'"
    return [name + '[' + str(i+1) + ']' for i in range(number)]
             
if __name__ == '__main__':
    # input data
    # Based on this data, we expect clusters of (speaking in 1-offset indexes) 
    #        inputs 1 and 3 with high weights on elements 1 and 2
    #        inputs 2 and 4 with high weights on elements 3 and 4
    i_in = [
        [1, 1, 0, 0],
        [0, 0, 0, 1],
        [1, 0, 0, 0],
        [0, 0, 1, 1] ]
    w_in = [
        [0.2, 0.6, 0.5, 0.9],
        [0.8, 0.4, 0.7, 0.3]]
    num_iterations = 12
    column_names = (('i',4), ('w1',4), ('w2',4), ('o',2), ('d',2))    
    i_test = [1, 1, 1, 0]
    
    # Some checks for startup and set initial weights
    assert(len(i_in[0])==len(w_in[0]))
    w = w_in
    
    # Step through <num_iterations> iterations of the algorithm
    print ',' + aa2csv(map(lambda x: title(x[0],x[1]), column_names))
    for t in range(num_iterations):
        i = i_in[t%len(i_in)]
        o,d = calcOutputs(w,i)
        w_new = updateWeights(w, i, t, d)
        print 'i' + str(t%len(i_in)+1) + ',' + aa2csv([i,w[0],w[1],o,d])
        w = w_new
    
    # Run the validation case 
    i = i_test
    o,d = calcOutputs(w,i)
    print 'i_test,' + aa2csv([i,w[0],w[1],o,d])
    