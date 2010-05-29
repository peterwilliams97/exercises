'''
Use NumPy, SciPy and MDP to do PCA on an advert classification data set
See http://mdp-toolkit.sourceforge.net/index.html#DOWINS

Created on 16/05/2010

@author: peter
'''
import numpy
from numpy import *
import scipy
import mdp
import bimdp
import csv
import random
import time


def covTest():
    x = array([1., 3., 8., 9.])
    variance = cov(x)                       # normalized by N-1
    variance = cov(x, bias=1)               # normalized by N
    T = array([1.3, 4.5, 2.8, 3.9])         # temperature measurements
    P = array([2.7, 8.7, 4.7, 8.2])         # corresponding pressure measurements
    cov(T,P)                                # covariance between temperature and pressure
    rho = array([8.5, 5.2, 6.9, 6.5])       # corresponding density measurements
    data = column_stack([T,P,rho])
    print T
    print P
    print rho
    print data
    print cov(data)                         # covariance matrix of T,P and rho

def describe(module):
    "Print some information about a module"
    print module.__name__, module.__file__
    
    
def mdpTest(): 
    "Do PCA on a data set"  
    x1_in = [
         [1.,1,1, 1],
         [2,2,2, 2],
         [3,3,3, 3]
         ] 
    x2_in = [
         [1.,1,1, 1],
         [2,2,2, 2],
         [1,1,2, 2],
         [3,3,6, 6],
         ] 
    x = array(x2_in)
    x2 = array([[1,1,1,1], [2,2,4,4], [3,3,3,3]])
    print x
    pcanode = mdp.nodes.PCANode(svd=True,  dtype='float64')
    print pcanode
    pcanode.train(x)
    p = pcanode.get_projmatrix()
    print p
    d = pcanode.output_dim
    print d
    v = pcanode.explained_variance
    print v
    z=pcanode(x2)
    print x2
    print z
    x2a = dot(z, transpose(p))
    print x2a
    z2 = dot(x2, p)
    print z2
    # pcanode.inverse(z) gives back the input vectors
    pi = pcanode.inverse(z)
    print pi
    pib = pcanode.inverse(array([[1, 0],[0, 1]]))
    print pib
    
def makeUniqueVector(vec_num, num_vecs, size):
    "Return a vector of length size that is unique for vec_num in num_vecs"
    assert(0 <= vec_num and vec_num < num_vecs)
    assert(num_vecs < size)    
    def numGen(i, v, n):
        if i < n:      x = 1 if i == v else 0
        elif i < 2*n:  x = 0 if i == v else 1
        else:          x = random.choice([0,1])
        return x
    v = [numGen(i, vec_num, num_vecs) for i in range(size)] 
    #print 'makeUniqueVector', v
    return v

def makeBasisVectors(num_vecs, size):
    return [makeUniqueVector(v, num_vecs, size) for v in range(num_vecs)]

def makeWeights(num_vecs):
    "Make a set of num_vecs random weights"
    w = [random.random() for i in range(num_vecs)]
    #print 'makeWeights', w 
    return w

def applyWeights(vectors, weights):
    "Returns sum(i,v[i]*w[i])"
    assert(len(vectors) == len(weights))
    #print 'applyWeights', weights
    def getSum(i):
        v,w = vectors,weights
        #print 'w', w
        #print 'v', v
        return sum([v[j][i]*w[j] for j in range(len(w))])
    return [getSum(i) for i in range(len(vectors[0]))]
 
def makeVectorSamples(num_vecs, size, num_samples):
    vectors = makeBasisVectors(num_vecs, size)
    #print 'vectors', vectors
    weights_arr = [makeWeights(num_vecs) for i in range(num_samples)]
    #print 'weights_arr', weights_arr
    vectors = [applyWeights(vectors, w) for w in weights_arr]
    return vectors
    
def mdpTestRandom(num_vecs, size, num_samples, verbose): 
    '''Do PCA on a data set of num_samples random vectors of length size
       based on num_vecs basis vectors'''
    print '--------------------------------------------------------'
    print 'mdpTestRandom: num_vecs =', num_vecs, 'size =', size, 'num_samples =', num_samples
    start_time = time.clock()
       
    x_in = makeVectorSamples(num_vecs, size, num_samples)
    x = array(x_in)
    if verbose: print x
    pcanode = mdp.nodes.PCANode(svd=True, dtype='float64')
    print pcanode
    pcanode.train(x)
    p = pcanode.get_projmatrix()
    if verbose: print p
    d = pcanode.output_dim
    print 'output_dim', d
    v = pcanode.explained_variance
    print 'explained_variance', v, '****' if d < num_vecs else ''
    print 'time =', round((time.clock() - start_time)*1000.0)/1000.0, 'seconds'
    #assert(d == num_vecs) 
     
def mdpTestRandomRange(max_num_vecs, verbose):    
    for num_vecs in range(1, max_num_vecs):
        size = num_vecs*3
        num_samples = size*4
        mdpTestRandom(num_vecs, size, num_samples, verbose)
   
def doTests():    
    #mdpTest()
    if True:
        mdpTestRandom(2, 4, 5, False)
        mdpTestRandomRange(5, False)
    mdpTestRandom(100, 1559, 3279, False)    # 416 sec, output_dim 96, explained_variance 0.991
    mdpTestRandom(2, 1000,  150, False) #   8 sec    
    mdpTestRandom(10, 1000,  150, False) # 8 sec
    mdpTestRandom(20, 1000,  150, False) # 9 sec
    mdpTestRandom(50, 1000,  150, False) # 11 sec
    mdpTestRandom(100,1000,  150, False) # 15 sec
    mdpTestRandom(2, 1000, 1500, False) #  50 sec
    mdpTestRandom(2, 1559, 3279, False) # 170 sec
    
def normalizeData(in_fn, out_fn):
    "Normalize ad data to equal std dev"
    in_cells = csv.readCsvRaw(in_fn)
    csv.validateMatrix(in_cells)
    #last column is ad categorie. normalize other columns
    in_data = [[float(e) for e in row[:-1]] for row in in_cells[1:]]
    print 'data', len(in_data), len(in_data[0])
    values = array(in_data)
    
    def normalizeAxis(column):
        stdev = column.std() 
        print stdev,
        return [e/stdev for e in column]
    
    # http://www.scipy.org/Numpy_Example_List#head-528347f2f13004fc0081dce432e81b87b3726a33
    norm_values = apply_along_axis(normalizeAxis,0,values)
    print
    norm2_values = apply_along_axis(normalizeAxis,0,norm_values)
    print
    
    out_data = [[x for x in row] for row in norm_values]
    print 'out_data', len(out_data), len(out_data[0])  
    out_cells = [in_cells[0]] + out_data  
   
    csv.writeCsv(out_fn, out_cells)
    
def pcaAdData(theshold_variance):   
    "Run PCA on the boolean column of the ad data set"
    h2data = csv.readCsvRaw(csv.headered_name_pp)
    csv.validateMatrix(h2data)
    
    # Boolean data are columns 3 to second last
    bool_data = [[float(e) for e in v[3:-1]] for v in h2data[1:]]
    print 'bool_data', len(bool_data), len(bool_data[0])
    x = array(bool_data)
    
    # Find the output dimension (#basis vectors) required to explain
    # threshold_variance
    for odim in range(200, 1000, 50):
        start_time = time.clock()
        pcanode = mdp.nodes.PCANode(svd=True, output_dim = odim, dtype='float64')
        pcanode.train(x)
        p = pcanode.get_projmatrix()
        d = pcanode.output_dim
        print 'output_dim', d
        v = pcanode.explained_variance
        print 'explained_variance', v
        print 'time =', round((time.clock() - start_time)*1000.0)/1000.0, 'seconds'
        if v >= theshold_variance:
            break
    print 'p', len(p), len(p[0]) 
    
    # Project out data onto PCA components    
    xfd = dot(x, p)    
    pca = [[x for x in row] for row in xfd]
    print 'pca', len(pca), len(pca[0])    
    pca_header = ['pca_%03d' % i for i in range(len(pca[0]))]
    header = h2data[0][:3] + pca_header
    num_data = [h2data[i+1][:3] + pca[i] for i in range(len(h2data)-1)] 
    data = [header] + num_data   
    csv.writeCsv(csv.headered_name_pca, data)
    
if __name__=='__main__':
    describe(numpy)
    describe(scipy)
    describe(mdp)
    describe(bimdp)
    
    #doTests()
    if False:
        pcaAdData(0.90)
        
    if True:
        normalizeData(csv.headered_name_pca, csv.headered_name_pca_norm)    
    
    
    