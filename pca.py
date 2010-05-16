'''
Check that NumPy, SciPy and MDP are installed and working
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
    pcanode = mdp.nodes.PCANode(svd=True, output_dim = 0.99, dtype='float64')
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
    
    
if __name__=='__main__':
    describe(numpy)
    describe(scipy)
    describe(mdp)
    describe(bimdp)
    mdpTest()
   
    