"""
Use NumPy, SciPy and MDP to do PCA on an advert classification data set
See http://mdp-toolkit.sourceforge.net/index.html#DOWINS

Created on 16/05/2010

@author: peter
"""
import numpy, scipy, mdp, bimdp, csv, random, time
from numpy import *

def covTest():
    x = array([1., 3., 8., 9.])
    variance = cov(x)                       # normalized by N-1
    variance = cov(x, bias=1)               # normalized by N
    T = array([1.3, 4.5, 2.8, 3.9])         # temperature measurements
    P = array([2.7, 8.7, 4.7, 8.2])         # corresponding pressure measurements
    TPcov = cov(T,P)                        # covariance between temperature and pressure
    rho = array([8.5, 5.2, 6.9, 6.5])       # corresponding density measurements
    data = column_stack([T,P,rho])
    print 'T',T
    print 'P',P
    print rho
    print data
    print 'TPcov',TPcov
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
    return [random.random() for i in range(num_vecs)]
 
def applyWeights(vectors, weights):
    "Returns sum(i,v[i]*w[i])"
    assert(len(vectors) == len(weights))
    def getSum(i):
        return sum([vectors[j][i]*weights[j] for j in range(len(weights))])
    return [getSum(i) for i in range(len(vectors[0]))]
 
def makeVectorSamples(num_vecs, size, num_samples):
    vectors = makeBasisVectors(num_vecs, size)
    weights_arr = [makeWeights(num_vecs) for i in range(num_samples)]
    return [applyWeights(vectors, w) for w in weights_arr]
      
def mdpTestRandom(num_vecs, size, num_samples, verbose): 
    """Do PCA on a data set of num_samples random vectors of length size
       based on num_vecs basis vectors"""
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
  
def getPcaCpts(input_data, num_cpts):
    """ Return first num_cpts PCA cpts for data"""
    start_time = time.clock()
    data = array(input_data)
    pcanode = mdp.nodes.PCANode(svd=True, output_dim = num_cpts, dtype='float64')
    pcanode.train(data)
    p = pcanode.get_projmatrix()
    width = len(input_data[0])
    id = scipy.eye(width, width)
    #print 'id', id
    #out = pcanode(id)
    d = pcanode.output_dim
    print 'output dim =', d, ',',
    v = pcanode.explained_variance
    print 'explained variance = %.3f' % v, ',',
    print 'time = %.1f' % (time.clock() - start_time) 
    if False:
        print 'projection matrix'
        print p
        print 'output data'
        print  pcanode(data)
    #return out[:num_cpts]
    return p
       
def pcaAdData(theshold_variance, in_filename, out_filename):   
    """ Run PCA on the Kushmerick ad data
        Stop when there are sufficient PCA components to explain threshold_variance
        Project input data onto these PCA components
        - in_filename : input data read from this CSV file
        - out_filename : output data written to this CSV file
    """
    h2data = csv.readCsvRaw(in_filename)
    csv.validateMatrix(h2data)
    
    # Boolean data are columns 3 to second last
    bool_data = [[float(e) for e in v[3:-1]] for v in h2data[1:]]
    print 'bool_data', len(bool_data), len(bool_data[0])
    x = array(bool_data)
    
    # Find the output dimension (#basis vectors) required to explain
    # threshold_variance
    print 'output_dim, explained_variance, time(sec)' 
    for odim in range(50, len(x[0]), 50):
        start_time = time.clock()
        pcanode = mdp.nodes.PCANode(svd=True, output_dim = odim, dtype='float64')
        pcanode.train(x)
        p = pcanode.get_projmatrix()
        d = pcanode.output_dim
        print '%10d' % d, ',',
        v = pcanode.explained_variance
        print '%15.03f' % v, ',',
        print '%6.1f' % (time.clock() - start_time)
        if v >= theshold_variance:
            break
    #print '-----------------------------1'
    print 'p', len(p), len(p[0]) 
    #print '-----------------------------2'
    # Project out data onto PCA components    
    xfd = dot(x, p)    
    pca = [[x for x in row] for row in xfd]
    print 'pca', len(pca), len(pca[0])    
    pca_header = ['pca_%03d' % i for i in range(len(pca[0]))]
    header = h2data[0][:3] + pca_header + [h2data[0][-1]]
    num_data = [h2data[i+1][:3] + pca[i] + [h2data[i+1][-1]] for i in range(len(h2data)-1)] 
    data = [header] + num_data   
    csv.writeCsv(out_filename, data)
    #print '-----------------------------3'
 
def normalizeMatrix(in_data):    
    """ Normalize data to mean=0.0, stdev=1.0
        in_data : input 2D array 
        return : normalized matrix
    """
    def normalizeAxis(column):
        mean = column.mean()
        stdev = column.std() 
        return [(e-mean)/stdev for e in column]
    
    # http://www.scipy.org/Numpy_Example_List#head-528347f2f13004fc0081dce432e81b87b3726a33
    norm_values = apply_along_axis(normalizeAxis, 0, array(in_data))
    return [[x for x in row] for row in norm_values]
    
def normalizeData(in_fn, out_fn):
    """ Normalize ad data to equal std dev
        in_fn : read input data from this csv file
        out_fn : write output data to this csv fuile
    """
    print 'normalizeData:', in_fn, '=>', out_fn
    in_cells = csv.readCsvRaw(in_fn)
    csv.validateMatrix2(in_cells)
  
    # Remove header row on top and category row on right
    in_data = [[float(e.strip()) for e in row[:-1]] for row in in_cells[1:3280]]
    print 'data', len(in_data), len(in_data[0])
        
    out_data = normalizeMatrix(in_data)
    print 'out_data', len(out_data), len(out_data[0])  
    
    out_cells = [in_cells[0]] + [out_data[i-1] + [in_cells[i][-1]] for i in range(1,len(in_cells))]  
    csv.writeCsv(out_fn, out_cells)
    
def correlation(v1, v2):
    "Returns correlation between vectors v1 and v2"
    c = cov(v1, v2)
    assert(c[0][1]==c[1][0])
    return c[1][0]/sqrt(c[0][0]*c[1][1])    
    
def sortBy(vector, order):
    "Sort vector by order"
    assert(len(vector)==len(order))
    return [vector[i] for i in order]    
    
def rankByCorrelationWithOutcomes(in_fn):
    "Rank each attribute by its correlation with the outcome"
    print 'rankByCorrelationWithOutcomes:', in_fn
    in_cells = csv.readCsvRaw(in_fn)
    csv.validateMatrix(in_cells)
    
    name_map = {'nonad.':0.0, 'ad.':1.0}
    def strToFloat(s):
        return name_map[s.strip()]
    
    #last column is ad categories. normalize other columns
    in_data = [[float(e) for e in row[:-1]] for row in in_cells[1:]]
    print 'in_data', len(in_data), len(in_data[0])
    raw_outcomes = [strToFloat(row[-1]) for row in in_cells[1:]]
  
    print 'outcomes', len(raw_outcomes) #,len(raw_outcomes[0])
    values = array(in_data)
    outcomes = array(raw_outcomes)
    
    def correlationWithOutcome(column):
        return correlation(column, outcomes)
   
    # http://www.scipy.org/Numpy_Example_List#head-528347f2f13004fc0081dce432e81b87b3726a33
    corr_with_outcomes = apply_along_axis(correlationWithOutcome,0,values)
    # print 'corr_with_outcomes', corr_with_outcomes
    corr_index = [(i,c) for i,c in enumerate(corr_with_outcomes)]
    # print corr_index
    corr_index.sort(key = lambda x: -abs(x[1])) 
    # print corr_index
    sort_order = [x[0] for x in corr_index]
    #print sort_order
    return (sort_order, corr_index)
    
def reorderMatrix(in_cells, order):
    "Reorder the len(order) left columns in a 2d matrix"
    w = len(order)
    return [sortBy(row[:w],order) + row[w:] for row in in_cells]
        
     
if __name__=='__main__':
    describe(numpy)
    describe(scipy)
    describe(mdp)
    describe(bimdp)
    
    if False:
        covTest()
    #doTests()
    
    explained_variance = 0.99
    ev = str(int(explained_variance*100.0))
    # pca_filename = csv.headered_name_pca
    pca_filename = csv.makeCsvPath('pca' + ev)
    #pca_norm_filename = csv.headered_name_pca_norm
    pca_norm_filename = csv.makeCsvPath('pca' + ev + '.norm')
    #pca_norm_corr_filename = csv.headered_name_pca_corr
    pca_norm_corr_filename = csv.makeCsvPath('pca' + ev + '.norm.corr')
    
    if True:
        pcaAdData(explained_variance, csv.headered_name_pp, pca_filename)
        
    if True:
        normalizeData(pca_filename, pca_norm_filename)    
    
    if True:
        sort_order = rankByCorrelationWithOutcomes(pca_norm_filename)
        def reorder(in_cells):
            return reorderMatrix(in_cells, sort_order)
        csv.modifyCsvRaw(pca_norm_filename, pca_norm_corr_filename, reorder)
        
    