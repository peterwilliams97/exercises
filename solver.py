'''
Created on 24/04/2010

@author: peter
'''
 
from math import *
    
def prod(v1, v2):
    "Returns dot product of vectors v1 and v2"
    return  sum(map(lambda x: x[0]*x[1], zip(v1,v2)))

def l2(v1, v2):
    "Returns Euclidean distance between vectors v1 and v2"
    return sqrt(sum(map(lambda x: (x[0]-x[1])**2, zip(v1,v2))))

def eta(t):
    "User defined eta function"
    if t < 4: return 0.6
    if t < 8: return 0.3
    return 0.15

def updateWeight(w, i, t):
    "User defined function for updating weights"
    return map(lambda x: x[1] + eta(t)*(x[0]-x[1]), zip(i,w))

def iterate(w, i, t):
    "One iteration of the self-organizing map algorithm"
    o = map(lambda x: prod(i,x), w)
    d = map(lambda x: l2(i,x), w)
    j = 0 if d[0] > d[1] else 1
    w[j] = updateWeight(w[j],i,t)
    return (w, o, d)

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
    
    assert(len(i_in[0])==len(w_in[0]))
    w = w_in
    print ',' + aa2csv(map(lambda x: title(x[0],x[1]), column_names))
    for t in range(num_iterations):
        i = i_in[t%len(i_in)]
        w,o,d = iterate(w, i, t)
        print 'i' + str(t%len(i_in)+1) + ',' + aa2csv([i,w[0], w[1],o,d])
    # Add the test case    
    print 'i_test,' + aa2csv([i_test,w[0], w[1],o,d])