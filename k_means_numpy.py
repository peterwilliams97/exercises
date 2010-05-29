'''
http://docs.scipy.org/doc/scipy/reference/cluster.vq.html

'''
import copy
from math import *

def l2(v1, v2):
    "Returns Euclidean distance between vectors v1 and v2"
    return sqrt(sum(map(lambda x: (x[0]-x[1])**2, zip(v1,v2))))

def arrCol(arr2, n):
    "Returns vector of nth column of 2d array arr2"
    for v in arr2:
        assert(len(v) > n)
    return [v[n] for v in arr2]

def transpose(arr2):
    "Returns transpose of 2d array arr2"
    for v in arr2:
        assert(len(v) == len(arr2[0]))
    return [arrCol(arr2, i) for i in range(len(arr2[0]))]

def meanArr(arr2):
    "Returns vector of means of elements of vectors"
    return [sum(v) for v in transpose(arr2)]

def minIndex(v):
    "Returns index of smallest element in vector v"
    mini = 0
    for i,x in enumerate(v):
        if (x < v[mini]):
            mini = i
    assert(0 <= mini and mini < len(v))
    return mini
    
def splitNearest(data, k_means):
    "Splits data (vector of vectors) according to closest means"
    k = len(k_means)
    k_lists = [[] for i in range(k)]
    for v in data:
        k_dists = [l2(v,m) for m in k_means]
        min_k = minIndex(k_dists)
        #print k, len(k_means), len(k_dists), len(k_lists)
        #print k_lists
        assert(0 <= min_k and min_k < len(k_lists))
        k_lists[min_k].append(v)
    assert(sum([len(v) for v in k_lists]))
    return k_lists

def findKMeans(data, k_means_in):
    k_means = copy.deepcopy(k_means_in)
    while True:
        print k_means
        k_lists = splitNearest(data, k_means)
        k_means_2 = meanArr(k_lists)
        if l2(k_means_2, k_means) < epsilon:
            break
        k_means = copy.deepcopy(k_means_2)
    return k_means
    
def readCsv(filename): 
    "Reads a CSV file into a 2d array of float"
    return [[float(n) for n in line.strip().split(',')] for line in file(filename).read().strip().split('\n')]
    

if __name__ == '__main__':
    data = readCsv('k_means_data.csv')
    means_in = readCsv('k_means_means.csv')
    means_out = findKMeans(data, means_in)
    
   